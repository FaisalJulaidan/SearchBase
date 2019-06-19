import enums
import json
import pandas
import random
import re
from datetime import datetime
from typing import List

from sqlalchemy import and_
from sqlalchemy_utils import Currency

from enums import DatabaseType, DataType as DT
from models import db, Callback, Database, Candidate, Assistant, Job
from services import assistant_services
from services.CRM import crm_services
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
        if databaseData['databaseType'] == enums.DatabaseType.Candidates.name:
            newDatabase = createDatabase(databaseName, DatabaseType.Candidates)
            uploadCandidates(databaseData, newDatabase)
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

        # Convert job salary to the submitted currency from chat (Format: "Greater Than 5000 GBP")
        if keywords.get(DT.JobSalary.value['name']):
            inputSplitted = keywords.get(DT.JobSalary.value['name'])[-1].split(' ')
            df[Job.JobSalary.name] = df.apply(lambda x: helpers.currencyConverter.convert(x[Job.Currency.name], inputSplitted[3], x[Job.JobSalary.name]), axis=1)
            df[Job.Currency.name] = inputSplitted[3]

        elif keywords.get(DT.CandidateDesiredSalary.value['name']):
            inputSplitted = keywords.get(DT.JobSalary.value['name'])[-1].split(' ')
            df[Job.JobSalary.name] = df.apply(lambda x: helpers.currencyConverter.convert(x[Job.Currency.name], inputSplitted[3], x[Job.JobSalary.name]), axis=1)
            df[Job.Currency.name] = inputSplitted[3]

        # Desired Salary
        __salary(DT.CandidateDesiredSalary, Candidate.CandidateDesiredSalary, keywords, df, 3)
        __salary(DT.JobSalary, Candidate.CandidateDesiredSalary, keywords, df, 3)

        # Years of EXP
        __numCounter(DT.CandidateYearsExperience, '<', Candidate.CandidateYearsExperience, keywords, df, 5)

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
                             con=db.session.bind)
        df = df.drop('DatabaseID', axis=1)  # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 8  # Add column for tracking score
        df['Source'] = "Internal Database"  # Source of solution e.g. Bullhorn, Adapt...

        if extraJobs:
            df = df.append(extraJobs, ignore_index=True)


        # Convert job salary to the submitted currency from chat
        if keywords.get(DT.JobSalary.value['name']):
            inputSplitted = keywords.get(DT.JobSalary.value['name'])[-1].split(' ') # (Format: "Greater Than 5000 GBP")
            df[Job.JobSalary.name] = df.apply(lambda x: helpers.currencyConverter.convert(x[Job.Currency.name], inputSplitted[3], x[Job.JobSalary.name]), axis=1)
            df[Job.Currency.name] = inputSplitted[3]

        elif keywords.get(DT.CandidateDesiredSalary.value['name']):
            inputSplitted = keywords.get(DT.JobSalary.value['name'])[-1].split(' ')
            df[Job.JobSalary.name] = df.apply(lambda x: helpers.currencyConverter.convert(x[Job.Currency.name], inputSplitted[3], x[Job.JobSalary.name] or 0), axis=1)
            df[Job.Currency.name] = inputSplitted[3]

        # Salary
        __salary(DT.JobSalary, Job.JobSalary, keywords, df, 8)
        __salary(DT.CandidateDesiredSalary, Job.JobSalary, keywords, df, 8)

        # Year Required
        __numCounter(DT.JobYearsRequired, '>', Job.JobYearsRequired, keywords, df, 5)
        __numCounter(DT.CandidateYearsExperience, '>', Job.JobYearsRequired, keywords, df, 5)

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
                if isinstance(record[Job.Currency.name], dict): currency = currency['code']
                subTitles.append("Salary: " + str(int(record[Job.JobSalary.name])) + ' ' + currency)

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

        return Callback(True, '', data)

    except Exception as exc:
        helpers.logError("databases_service.scanJobs(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')



def __wordsCounter(dataType: DT, dbColumn, keywords, df, x=1):
    if keywords.get(dataType.value['name']):
        df['Score'] += x * df[df[dbColumn.name].notnull()][dbColumn.name].str.count('|'.join(keywords[dataType.value['name']]),
                                                       flags=re.IGNORECASE) | 0


def __numCounter(dataType: DT, compare, dbColumn, keywords, df, plus=1):
    if keywords.get(dataType.value['name']):
        if compare == '>':
            df.loc[df[dbColumn.name] <= float(keywords[dataType.value['name']][-1]), 'Score'] += plus
        else: # '<'
            df.loc[df[dbColumn.name] >= float(keywords[dataType.value['name']][-1]), 'Score'] += plus


def __salary(dataType: DT, dbColumn, keywords, df, plus=1):
    input = keywords.get(dataType.value['name'])
    if input:
        inputSplitted = input[-1].split(' ') # Less Than 5000 GBP
        if inputSplitted[0] == 'Less':
            df.loc[df[dbColumn.name] <= float(inputSplitted[2]), 'Score'] += plus
        else: # Greater
            df.loc[df[dbColumn.name] >= float(inputSplitted[2]), 'Score'] += plus


def createPandaCandidate(id, name, email, mobile, location, skills,
                         linkdinURL, availability, jobTitle, education,
                         yearsExperience: int, desiredSalary: float, currency, source):
    return {"ID": id,
            "CandidateName": name,
            "CandidateEmail": email,
            "CandidateMobile": mobile,
            "CandidateLocation": location,
            "CandidateSkills": skills,
            "CandidateLinkdinURL": linkdinURL,
            "CandidateAvailability": availability,
            "CandidateJobTitle": jobTitle,
            "CandidateEducation": education,
            "CandidateYearsExperience": yearsExperience,
            "CandidateDesiredSalary": desiredSalary,
            "Currency": currency,
            "Score": 0,
            "Source": source,
            }


def createPandaJob(id, title, desc, location, type, salary: float, essentialSkills, desiredSkills, yearsRequired,
                   startDate, endDate, linkURL, currency, source):
    return {"ID": id,
            "JobTitle": title,
            "JobDescription": desc,
            "JobLocation": location,
            "JobType": type,
            "JobSalary": salary,
            "JobEssentialSkills": essentialSkills,
            "JobDesiredSkills": desiredSkills,
            "JobYearsRequired": yearsRequired,
            "JobStartDate": startDate,
            "JobEndDate": endDate,
            "JobLinkURL": linkURL,
            "Currency": currency,
            "Score": 0,
            "Source": source,
            }
