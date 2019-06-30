import json
import random
import re
from datetime import datetime
from typing import List

import pandas
from utilities.enums import DatabaseType, DataType as DT, Period
from models import db, Callback, Database, Candidate, Assistant, Job
from services import assistant_services
from services.Marketplace.CRM import crm_services
from sqlalchemy import and_
from sqlalchemy_utils import Currency
from utilities import helpers


def fetchDatabase(id, companyID: int, pageNumber: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        database: Database = db.session.query(Database) \
            .filter(and_(Database.CompanyID == companyID, Database.ID == id)).first()

        if not database:
            raise Exception

        databaseContent = None

        if database.Type == DatabaseType.Candidates:
            databaseContent = getAllCandidates(id, pageNumber)

        elif database.Type == DatabaseType.Jobs:
            databaseContent = getAllJobs(id, pageNumber)

        if not databaseContent:
            raise Exception()

        return Callback(True, "", {'databaseInfo': helpers.getDictFromSQLAlchemyObj(database),
                                   'databaseContent': databaseContent})

    except Exception as exc:
        helpers.logError("databases_service.fetchDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not fetch the database.')


def updateDatabase(id, newName, companyID) -> Callback:
    try:
        if not newName: raise Exception
        db.session.query(Database).filter(and_(Database.ID == id, Database.CompanyID == companyID)) \
            .update({'Name': newName})
        db.session.commit()
        return Callback(True, newName + ' database updated successfully')

    except Exception as exc:
        helpers.logError("databases_service.updateDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False,"Couldn't update database ")


# ----- Uploader ----- #
def uploadDatabase(data: dict, companyID: int) -> Callback:
    try:

        def parseRecord(record):
            parsed = {}
            for key, content in record.items():  # loop through record's columns
                data = content.get('data', None)
                if data:
                    if key in [Candidate.Currency.name, Job.Currency.name]:
                        parsed[key] = Currency(data)
                    elif key in [Candidate.PayPeriod.name, Job.PayPeriod.name]:
                        parsed[key] = enums.Period[data]
                    elif key in [Job.JobStartDate.name, Job.JobEndDate.name]:
                        parsed[key] = datetime(year=data['year'],
                                               month=data['month'],
                                               day=data['day'])
                    else:
                        parsed[key] = data
                else:
                    parsed[key] = None
            return parsed

        # Inner/nested functions
        def createDatabase(name, type: DatabaseType):
            return Database(Name=name, Type=type, CompanyID=companyID)

        def uploadCandidates(databaseData, newDatabase: Database):
            candidates = []
            for record in databaseData["records"]:
                candidates.append(Candidate(Database=newDatabase, **parseRecord(record)))
            db.session.add_all(candidates)

        def uploadJobs(databaseData, newDatabase: Database):
            jobs = []
            for record in databaseData["records"]:
                jobs.append(Job(Database=newDatabase, **parseRecord(record)))
            db.session.add_all(jobs)

        # ===========================

        databaseData = data.get('newDatabase')
        databaseName = databaseData["databaseName"]

        # Upload Candidates database
        if databaseData['databaseType'] == enums.DatabaseType.Candidates.name:
            newDatabase = createDatabase(databaseName, DatabaseType.Candidates)
            uploadCandidates(databaseData, newDatabase)

        # Upload Jobs database
        elif databaseData['databaseType'] == enums.DatabaseType.Jobs.name:
            newDatabase = createDatabase(databaseName, DatabaseType.Jobs)
            uploadJobs(databaseData, newDatabase)
        else:
            return Callback(False, "Database type is not recognised")

        # After finishing from uploading database without errors, save changes
        db.session.commit()
        return Callback(True, "Databases was successfully uploaded!", newDatabase)

    except Exception as exc:
        helpers.logError("databases_service.uploadDatabase(): " + str(exc))
        return Callback(False, 'Could not upload the databases.')


# ----- Getters ----- #
def getDatabasesList(companyID: int) -> Callback:
    try:
        databases: List[Database] = db.session.query(Database) \
            .filter(and_(Database.CompanyID == companyID)).all()
        return Callback(True, "Databases list is here", databases)

    except Exception as exc:
        helpers.logError("databases_service.getDatabasesList(): " + str(exc))
        return Callback(False, 'Could not fetch the databases list.')


def getRecord(recordID, databaseType: DatabaseType) -> Callback:
    if databaseType == DatabaseType.Candidates:
        return getCandidate(recordID)

    elif databaseType == DatabaseType.Jobs:
        return getJob(recordID)

    return Callback(False, "Database type is not recognised")


def getCandidate(candidateID):
    try:
        candidate = db.session.query(Candidate) \
            .filter(Candidate.ID == candidateID).first()
        if not candidate: raise Exception

        return Callback(True, "Candidate retrieved successfully.", candidate)

    except Exception as exc:
        helpers.logError("databases_service.getCandidate(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the candidate.')


def getJob(jobID):
    try:
        job = db.session.query(Job) \
            .filter(Job.ID == jobID).first()
        if not job: raise Exception

        return Callback(True, "Job retrieved successfully.", job)

    except Exception as exc:
        helpers.logError("databases_service.getJob(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the job.')


# Get All
def getAllCandidates(dbID, page) -> dict:
    try:
        result = db.session.query(Candidate) \
            .filter(Candidate.DatabaseID == dbID) \
            .paginate(page=page, error_out=False, per_page=20)

        data = {
            'records': helpers.getListFromSQLAlchemyList(result.items),
            'currentPage': result.page,
            'totalItems': result.total,
            'totalPages': result.pages,
            'totalPerPage': result.per_page
        }
        return data

    except Exception as exc:
        helpers.logError("databases_service.getAllCandidates(): " + str(exc))
        raise Exception


def getAllJobs(dbID, page) -> dict:
    try:
        result = db.session.query(Job) \
            .filter(Job.DatabaseID == dbID) \
            .paginate(page=page, error_out=False, per_page=20)

        data = {
            'records': helpers.getListFromSQLAlchemyList(result.items),
            'currentPage': result.page,
            'totalItems': result.total,
            'totalPages': result.pages,
            'totalPerPage': result.per_page
        }
        return data

    except Exception as exc:
        helpers.logError("databases_service.getAllJobs(): " + str(exc))
        raise Exception('Error: getAllJobs()')


# ----- Deletion ----- #
def deleteDatabase(databaseID, companyID) -> Callback:
    try:
        db.session.query(Database).filter(and_(Database.CompanyID == companyID, Database.ID == databaseID)) \
            .delete()
        db.session.commit()
        return Callback(True, 'Database has been deleted.')

    except Exception as exc:
        helpers.logError("databases_service.deleteDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not remove the database.')


# ----- Scanners (Pandas) ----- #
def scan(session, assistantHashID):
    try:

        callback: Callback = assistant_services.getByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = callback.Data

        databaseType: DatabaseType = DatabaseType[session['databaseType']]
        databases: List[Database] = db.session.query(Database.ID) \
            .filter(and_(Database.CompanyID == assistant.CompanyID,
                         Database.Type == databaseType)).all()

        # get CRM Data
        extraRecords = getCRMData(assistant, databaseType.name, session)

        # Scan database for solutions based on database type
        if databaseType == enums.DatabaseType.Candidates:
            return scanCandidates(session, [d[0] for d in databases], extraRecords)
        elif databaseType == enums.DatabaseType.Jobs:
            return scanJobs(session, [d[0] for d in databases], extraRecords)
        else:
            return Callback(False, "Database type is not recognised", None)

    except Exception as exc:
        helpers.logError("databases_service.scan(): " + str(exc))
        return Callback(False, 'Error while scanning the database')


def getCRMData(assistant, scanEntity, session):
    # check CRM
    if assistant.CRM:
        if scanEntity is "Jobs":
            return crm_services.searchJobs(assistant, session).Data
        elif scanEntity is "Candidates":
            return crm_services.searchCandidates(assistant, session).Data

    return None


# Data analysis using Pandas library
def scanCandidates(session, dbIDs, extraCandidates=None):
    try:

        df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)

        df = df.drop('DatabaseID', axis=1)  # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0  # Add column for tracking score
        df['Source'] = "Internal Database"  # Source of solution e.g. Bullhorn, Adapt...
        if extraCandidates:
            df = df.append(extraCandidates, ignore_index=True)  # TODO
            # print("df: ", df["CandidateLocation"])

        # Fill None values with 0 for numeric columns and with empty string for string columns
        df = df.fillna({Candidate.CandidateDesiredSalary.name: 0, Candidate.CandidateYearsExperience: 0}).fillna('')

        # Salary comparision for JobSalary (LessThan is forced)
        salaryInputs: list = keywords.get(DT.JobSalary.value['name'])
        if salaryInputs and len(salaryInputs):
            df[['Score', Candidate.CandidateDesiredSalary.name, Candidate.Currency.name, Job.PayPeriod.name]] = \
                df.apply(lambda row: __salary(row, Candidate.CandidateDesiredSalary,
                                              Candidate.Currency, Candidate.PayPeriod,
                                              salaryInputs[-1], plus=8, forceLessThan=True), axis=1, result_type='expand')

        # Salary comparision for CandidateDesiredSalary
        salaryInputs: list = keywords.get(DT.CandidateDesiredSalary.value['name'])
        if salaryInputs and len(salaryInputs):
            df[['Score', Candidate.CandidateDesiredSalary.name, Candidate.Currency.name, Job.PayPeriod.name]] = \
                df.apply(lambda row: __salary(row, Candidate.CandidateDesiredSalary,
                                              Candidate.Currency, Candidate.PayPeriod,
                                              salaryInputs[-1], plus=8, forceLessThan=False), axis=1, result_type='expand')

        # Years of EXP
        __numCounter(Candidate.CandidateYearsExperience, '>', DT.CandidateYearsExperience, keywords, df, plus=5, addInputToScore=True)

        # Education
        __wordsCounter(DT.CandidateEducation, Candidate.CandidateEducation, keywords, df, 1)

        # Location
        __wordsCounter(DT.JobLocation, Candidate.CandidateLocation, keywords, df, 6)
        __wordsCounter(DT.CandidateLocation, Candidate.CandidateLocation, keywords, df, 6)

        # JobTitle
        __wordsCounter(DT.CandidateJobTitle, Candidate.CandidateJobTitle, keywords, df, 1)
        __wordsCounter(DT.JobTitle, Candidate.CandidateJobTitle, keywords, df, 1)

        # Skills
        __wordsCounter(DT.CandidateSkills, Candidate.CandidateSkills, keywords, df, 2)
        __wordsCounter(DT.JobDesiredSkills, Candidate.CandidateSkills, keywords, df, 2)
        __wordsCounter(DT.JobEssentialSkills, Candidate.CandidateSkills, keywords, df, 2)

        # Availability
        __wordsCounter(DT.CandidateAvailability, Candidate.CandidateAvailability, keywords, df, 1)

        topResults = json.loads(df[df['Score'] > 0].nlargest(session.get('showTop', 2), 'Score')
                                .to_json(orient='records'))

        data = []  # List of candidates
        location = ["Their preferred location for work would be [location].",
                    "They prefer to work in [location]."]
        yearsExp = ["This candidate has [yearsExp] years of experience in  [skills].",
                    "They have experience with [skills] for [yearsExp] years."]

        indexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
        for i, record in enumerate(topResults):
            desc = []
            # Build random dynamic candidate description
            if record[Candidate.CandidateLocation.name]:
                desc.append(random.choice(location).replace("[location]",
                                                            record[Candidate.CandidateLocation.name]))

            if record[Candidate.CandidateYearsExperience.name] and record[Candidate.CandidateSkills.name]:
                desc.append(random.choice(yearsExp)
                            .replace("[yearsExp]", str(int(record[Candidate.CandidateYearsExperience.name])))
                            .replace("[skills]", record[Candidate.CandidateSkills.name]))

            random.shuffle(desc)
            data.append({
                "id": record["ID"],
                "databaseType": enums.DatabaseType.Candidates.value,
                "title": "Candidate " + indexes[i],
                "subTitles": [],
                "description": " ".join(desc),
                "buttonText": "Enquire",
                "output": helpers.encrypt(record, True)
            })

        return Callback(True, '', data)

    except Exception as exc:
        helpers.logError("databases_service.scanCandidates(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')


def scanJobs(session, dbIDs, extraJobs=None):
    try:

        df = pandas.read_sql(db.session.query(Job).filter(Job.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)\
            .fillna({Job.JobSalary.name: 0, Job.JobYearsRequired.name: 0})\
            .fillna('')


        df = df.drop('DatabaseID', axis=1)  # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0  # Add column for tracking score
        df['Source'] = "Internal Database"  # Source of solution e.g. Bullhorn, Adapt...

        if extraJobs:
            df = df.append(extraJobs, ignore_index=True)

        # Fill None values with 0 for numeric columns and with empty string for string columns
        df = df.fillna({Job.JobSalary.name: 0, Job.JobYearsRequired.name: 0}).fillna('')

        # Salary comparision
        salaryInputs: list = keywords.get(DT.JobSalary.value['name'], keywords.get(DT.CandidateDesiredSalary.value['name']))
        if salaryInputs and len(salaryInputs):
            df[['Score', Job.JobSalary.name, Job.Currency.name, Job.PayPeriod.name]] = \
                df.apply(lambda row: __salary(row, Job.JobSalary, Job.Currency, Job.PayPeriod, salaryInputs[-1], 8),
                                                                            axis=1, result_type='expand')

        # Job Year Required
        __numCounter(Job.JobYearsRequired, '<', DT.JobYearsRequired, keywords, df, plus=5, addInputToScore=True)

        # Job Year Required
        __numCounter(Job.JobYearsRequired, '<', DT.CandidateYearsExperience, keywords, df, plus=5, addInputToScore=True)

        # Job Title
        __wordsCounter(DT.JobTitle, Job.JobTitle, keywords, df, 2)
        __wordsCounter(DT.JobTitle, Job.JobDescription, keywords, df, 2)
        __wordsCounter(DT.CandidateSkills, Job.JobTitle, keywords, df, 2)
        __wordsCounter(DT.CandidateSkills, Job.JobDescription, keywords, df, 2)

        # Type
        __wordsCounter(DT.JobType, Job.JobType, keywords, df, 2)

        # Location
        __wordsCounter(DT.JobLocation, Job.JobLocation, keywords, df, 3)
        __wordsCounter(DT.CandidateLocation, Job.JobLocation, keywords, df, 3)

        # Skills
        __wordsCounter(DT.JobEssentialSkills, Job.JobEssentialSkills, keywords, df, 3)
        __wordsCounter(DT.JobDesiredSkills, Job.JobDesiredSkills, keywords, df, 3)
        __wordsCounter(DT.CandidateSkills, Job.JobEssentialSkills, keywords, df, 3)
        __wordsCounter(DT.CandidateSkills, Job.JobDesiredSkills, keywords, df, 3)


        # Results
        topResults = json.loads(df[df['Score'] > 0].nlargest(session.get('showTop', 0), 'Score')
                                .to_json(orient='records'))


        jobType = ["This role is a [jobType]", "This job is a [jobType]"]
        location = [" located in [location]. "]
        requiredYearsSkills = ["It requires [yearsRequired] year(s) with [essentialSkills]. ",
                               "This role requires [yearsRequired] year(s) with [essentialSkills]. "]
        desiredSkills = ["Candidates who also have experience with [desirableSkills] are highly desired.",
                         "Desirable skills include [desirableSkills]."]

        data = []
        for record in topResults:
            desc = []
            # Build random dynamic job description
            if record[Job.JobType.name]:
                desc.append(random.choice(jobType).replace("[jobType]",
                                                           record[Job.JobType.name]))
                if record[Job.JobLocation.name]:
                    desc[0] += random.choice(location).replace("[location]",
                                                               record[Job.JobLocation.name])
                else:
                    desc[0] += ". "

            if record[Job.JobYearsRequired.name] and record[Job.JobEssentialSkills.name]:
                desc.append(random.choice(requiredYearsSkills)
                            .replace("[yearsRequired]", str(int(record[Job.JobYearsRequired.name])))
                            .replace("[essentialSkills]", record[Job.JobEssentialSkills.name]))

            if record[Job.JobDesiredSkills.name]:
                desc.append(random.choice(desiredSkills).replace("[desirableSkills]",
                                                                 record[Job.JobDesiredSkills.name]))

            # Build job subtitles
            subTitles = []
            if record[Job.JobLocation.name]:
                subTitles.append("Location: " + record[Job.JobLocation.name])

            if record[Job.JobSalary.name]:
                currency = record[Job.Currency.name] or '' # it could be a Currency object e.g. {code: 'USD'...}
                payPeriod = record[Job.PayPeriod.name] or '' # it could be a Period object e.g. {name: 'Annual'...}

                if isinstance(currency, dict): currency = currency['code']
                if isinstance(payPeriod, dict): payPeriod = payPeriod['name']

                subTitles.append("Salary: "
                                 + str(int(record[Job.JobSalary.name]))
                                 + ' ' + currency
                                 + ' ' + payPeriod)

            if record[Job.JobEssentialSkills.name]:
                subTitles.append("Essential Skills: " + record[Job.JobEssentialSkills.name])


            data.append({
                "id": record["ID"],
                "databaseType": enums.DatabaseType.Jobs.value,
                "title": record[Job.JobTitle.name],
                "subTitles": subTitles,
                "description": " ".join(desc),
                "buttonText": "Apply",
                "output": helpers.encrypt(record, True)
            })

        # time.sleep(5)
        return Callback(True, '', data)

    except Exception as exc:
        helpers.logError("databases_service.scanJobs(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')



def __wordsCounter(dataType: DT, dbColumn, keywords, df, x=1):
    if keywords.get(dataType.value['name']):
        df['Score'] += x * df[dbColumn.name].str.count('|'.join(keywords[dataType.value['name']]),
                                                       flags=re.IGNORECASE) | 0


def __numCounter(dbColumn, compareSign, dataType: DT, keywords, df, plus=1, addInputToScore=False):
    if keywords.get(dataType.value['name']):
        numberInput = int(keywords.get(dataType.value['name'])[-1])

        # it is good for years of exp to be added to the score
        if addInputToScore:
            plus += 7 if numberInput > 7 else numberInput

        # Compare
        if compareSign == '>':
            df.loc[df[dbColumn.name] >=
                   int(numberInput), 'Score'] += plus
        else: # '<'
            df.loc[df[dbColumn.name] <=
                   int(numberInput), 'Score'] += plus


def __salary(row, dbSalaryColumn, dbCurrencyColumn, dbPayPeriodColumn, salaryInput: str, plus=4, forceLessThan=False):

    userSalary = salaryInput.split(' ') # e.g. Less Than 5000 GBP Annually

    # Convert salary currency if did not match with user's entered currency
    dbSalary = row[dbSalaryColumn.name] or 0
    if (not row[dbCurrencyColumn.name] == userSalary[3]) and dbSalary > 0:
        dbSalary = helpers.currencyConverter.convert(row[dbCurrencyColumn.name], userSalary[3], dbSalary)
        row[dbSalaryColumn.name] = dbSalary

    # Convert salary rate if did not match with user's entered pay period e.g. Annually to Monthly...
    if (not row[dbPayPeriodColumn.name] == userSalary[4]) and dbSalary > 0:
        dbSalary = helpers.convertSalaryPeriod(dbSalary, row[dbPayPeriodColumn.name], Period[userSalary[4]])

    # Add old score to new score if success
    plus += row['Score']

    # Compare salaries, if true then return 'plus' to be added to the score otherwise old score
    if userSalary[0] == 'Greater' and not (forceLessThan):
        return (plus if dbSalary >= float(userSalary[2]) else row['Score']), dbSalary, userSalary[3], userSalary[4]
    else: # Less
        return (plus if dbSalary <= float(userSalary[2]) else row['Score']), dbSalary, userSalary[3], userSalary[4]



def createPandaCandidate(id, name, email, mobile, location, skills,
                         linkdinURL, availability, jobTitle, education,
                         yearsExperience: int, desiredSalary: float, currency: Currency, payPeriod: Period, source):
    return {"ID": id,
            "CandidateName": name or '',
            "CandidateEmail": email or '',
            "CandidateMobile": mobile or '',
            "CandidateLocation": location or '',
            "CandidateSkills": skills or '',
            "CandidateLinkdinURL": linkdinURL or '',
            "CandidateAvailability": availability or '',
            "CandidateJobTitle": jobTitle or '',
            "CandidateEducation": education or '',
            "CandidateYearsExperience": yearsExperience or 0,
            "CandidateDesiredSalary": desiredSalary or 0,
            "Currency": currency,
            "PayPeriod": payPeriod,
            "Score": 0,
            "Source": source or '',
            }


def createPandaJob(id, title, desc, location, type, salary: float, essentialSkills, desiredSkills, yearsRequired,
                   startDate, endDate, linkURL, currency: Currency, payPeriod: Period, source):
    return {"ID": id,
            "JobTitle": title or '',
            "JobDescription": desc or '',
            "JobLocation": location or '',
            "JobType": type or '',
            "JobSalary": salary or 0,
            "JobEssentialSkills": essentialSkills or '',
            "JobDesiredSkills": desiredSkills or '',
            "JobYearsRequired": yearsRequired or 0,
            "JobStartDate": startDate or '',
            "JobEndDate": endDate,
            "JobLinkURL": linkURL,
            "Currency": currency,
            "PayPeriod": payPeriod,
            "Score": 0,
            "Source": source or '',
            }