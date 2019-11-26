import json
import random
import re
from datetime import datetime
from typing import List

import pandas
from sqlalchemy import and_
from sqlalchemy_utils import Currency

from services.Marketplace.marketplace_helpers import convertSkillsToString
from utilities.enums import DatabaseType, DataType as DT
from models import db, Callback, Database, Candidate, Assistant, Job
from services import assistant_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.marketplace_helpers import convertSkillsToString
from utilities import helpers
from utilities.enums import DatabaseType, Period, DataType as DT


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
        return Callback(False, "Couldn't update database ")


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

        # Upload Candidates database
        if databaseData['databaseType'] == DatabaseType.Candidates.name:
            newDatabase = createDatabase(databaseName, DatabaseType.Candidates)
            uploadCandidates(databaseData, newDatabase)

        # Upload Jobs database
        elif databaseData['databaseType'] == DatabaseType.Jobs.name:
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


def updateCandidate(candidateID, conversation) -> Callback:
    try:
        candidate = db.session.query(Candidate) \
            .filter(Candidate.ID == candidateID).first()
        if not candidate: raise Exception

        data = {
            "name": conversation.Name or " ",
            "firstName": helpers.getListValue(conversation.Name, 0, " "),
            "lastName": helpers.getListValue(conversation.Name, 1, " "),
            "mobile": conversation.PhoneNumber or " ",
            "city": ", ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateCity.value['name']) or
                conversation.Data.get('keywordsByDataType').get(DT.JobCity.value['name'], [])),
            "email": conversation.Email or " ",

            "skills": ", ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], ) or
                conversation.Data.get('keywordsByDataType').get(DT.JobEssentialSkills.value['name'], [])) or None,
            "yearsExperience": ", ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateYearsExperience.value['name']) or
                conversation.Data.get('keywordsByDataType').get(DT.JobYearsRequired.value['name'], [])) or None,
            "preferredJobTitle": ", ".join(
                conversation.Data.get('keywordsByDataType').get(DT.JobTitle.value['name'], [])) or None,

            "educations": ", ".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'],
                                                                                    [])) or None,
            "availability": ", ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateAvailability.value['name'], [])) or None,

            "annualSalary": crm_services.getSalary(conversation, DT.CandidateDesiredSalary, "Min", Period.Annually) or
                            crm_services.getSalary(conversation, DT.JobSalary, "Min", Period.Annually),
            "dayRate": crm_services.getSalary(conversation, DT.CandidateDesiredSalary, "Min", Period.Daily) or
                       crm_services.getSalary(conversation, DT.JobSalary, "Min", Period.Daily)
        }

        for key, value in data.items():
            if type(value) is str:
                data[key] = value.strip()

        candidate.CandidateName = data.get("name") or candidate.CandidateName
        candidate.CandidateMobile = data.get("mobile") or candidate.CandidateMobile
        candidate.CandidateCity = data.get("city") or candidate.CandidateCity
        candidate.CandidateEmail = data.get("email") or candidate.CandidateEmail
        candidate.CandidateSkills = data.get("skills") or candidate.CandidateSkills
        candidate.CandidateYearsExperience = data.get("yearsExperience") or candidate.CandidateYearsExperience
        candidate.CandidateJobTitle = data.get("preferredJobTitle") or candidate.CandidateJobTitle
        candidate.CandidateEducation = data.get("educations") or candidate.CandidateEducation
        candidate.CandidateAvailability = data.get("availability") or candidate.CandidateAvailability
        candidate.CandidateDesiredSalary = data.get("annualSalary") or data.get("dayRate") \
                                           or candidate.CandidateDesiredSalary

        db.session.commit()

        return Callback(True, "Candidate has been updated")

    except Exception as exc:
        db.session.rollback()
        helpers.logError(exc)
        return Callback(False, "Candidate could not be updated")


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
def scan(session, assistantHashID, campaign=False, campaignDBID=None):
    try:
        callback: Callback = assistant_services.getByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = callback.Data

        databaseType: DatabaseType = DatabaseType[session['databaseType']]
        databases: List[Database] = db.session.query(Database.ID) \
            .filter(and_(Database.CompanyID == assistant.CompanyID,
                         Database.Type == databaseType)).all()

        if not campaign:
            # get CRM Data
            extraRecords = getCRMData(assistant, databaseType.name, session)
        else:
            extraRecords = []
            if campaignDBID:
                for database in databases:
                    if database.ID == campaignDBID:
                        databases = list([database])
                        break

        # Scan database for solutions based on database type
        if databaseType == DatabaseType.Candidates:
            return scanCandidates(session, [d[0] for d in databases], extraRecords, campaign)
        elif databaseType == DatabaseType.Jobs:
            return scanJobs(session, [d[0] for d in databases], extraRecords)
        else:
            return Callback(False, "Database type is not recognised", None)

    except Exception as exc:
        helpers.logError("databases_service.scan(): " + str(exc))
        return Callback(False, 'Error while scanning the database')


def getCRMData(assistant, databaseType, session):
    # check CRM
    if assistant.CRM:
        if databaseType is "Jobs":
            return crm_services.searchJobs(assistant, session).Data
        elif databaseType is "Candidates":
            return crm_services.searchCandidates(assistant, session).Data
    return None


# Data analysis using Pandas library
def scanCandidates(session, dbIDs, extraCandidates=None, campaign=False):
    try:

        df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)

        df = df.drop('DatabaseID', axis=1)  # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0  # Add column for tracking score
        df['Source'] = "Internal Database"  # Source of solution e.g. Bullhorn, Adapt...

        if extraCandidates:
            df = df.append(extraCandidates, ignore_index=True)

        # Check if there are no Candidates.
        if not len(df):
            return Callback(True, '', [])

        # Fill None values with 0 for numeric columns and with empty string for string columns
        df = df.fillna({Candidate.CandidateDesiredSalary.name: 0, Candidate.CandidateYearsExperience.name: 0}).fillna(
            '')

        # Salary comparision for JobSalary (LessThan is forced)
        salaryInputs: list = keywords.get(DT.JobSalary.value['name'])
        if salaryInputs and len(salaryInputs):
            df[['Score', Candidate.CandidateDesiredSalary.name, Candidate.Currency.name]] = \
                df.apply(lambda row: __salary(row, Candidate.CandidateDesiredSalary, Candidate.Currency,
                                              salaryInputs[-1], plus=8, forceLessThan=True), axis=1,
                         result_type='expand')

        # Salary comparision for CandidateDesiredSalary
        salaryInputs: list = keywords.get(DT.CandidateDesiredSalary.value['name'])
        if salaryInputs and len(salaryInputs):
            df[['Score', Candidate.CandidateDesiredSalary.name, Candidate.Currency.name]] = \
                df.apply(lambda row: __salary(row, Candidate.CandidateDesiredSalary, Candidate.Currency,
                                              salaryInputs[-1], plus=8, forceLessThan=False), axis=1,
                         result_type='expand')

        # Years of EXP
        __numCounter(Candidate.CandidateYearsExperience, '>', DT.CandidateYearsExperience, keywords, df, plus=5,
                     addInputToScore=True)

        # Education
        __wordsCounter(DT.CandidateEducation, Candidate.CandidateEducation, keywords, df, 1)

        # Location
        __wordsCounter(DT.JobCity, Candidate.CandidateCity, keywords, df, 6)
        __wordsCounter(DT.CandidateCity, Candidate.CandidateCity, keywords, df, 6)

        # JobTitle
        # __wordsCounter(DT.CandidateJobTitle, Candidate.CandidateJobTitle, keywords, df, 1)
        # __wordsCounter(DT.JobTitle, Candidate.CandidateJobTitle, keywords, df, 1)

        # Skills
        __wordsCounter(DT.CandidateSkills, Candidate.CandidateSkills, keywords, df, 2)
        __wordsCounter(DT.JobEssentialSkills, Candidate.CandidateSkills, keywords, df, 2)

        # Availability
        __wordsCounter(DT.CandidateAvailability, Candidate.CandidateAvailability, keywords, df, 1)

        topResults = json.loads(df[df['Score'] > 0].nlargest(session.get('showTop', 2), 'Score')
                                .to_json(orient='records'))

        if campaign:
            return Callback(True, '', topResults)

        data = []  # List of candidates
        location = ["Candidate's preferred location of work is [location].",
                    "They prefer to work in [location]."]
        skills = ["Their skill set includes [skills].",
                  "They are proficient in [skills].",
                  "The candidate's skills include [skills]."]
        yearsExp = ["The candidate also has [yearsExp] years of experience in their line of work.",
                    "The candidate has also reported [yearsExp] years of experience in their area of work.",
                    "They also have [yearsExp] years of experience."]
        salary = ["Preferred salary for them is [salary] [currency].",
                  "Their preferred salary is [salary] [currency]."]

        indexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
        for i, record in enumerate(topResults):
            desc = []
            # Build random dynamic candidate description
            if record[Candidate.CandidateCity.name]:
                desc.append(random.choice(location).replace("[location]",
                                                            record[Candidate.CandidateCity.name]))

            if record[Candidate.CandidateSkills.name]:
                desc.append(random.choice(skills)
                            .replace("[skills]", record[Candidate.CandidateSkills.name]))

            if record[Candidate.CandidateYearsExperience.name]:
                desc.append(random.choice(yearsExp)
                            .replace("[yearsExp]", str(int(record[Candidate.CandidateYearsExperience.name]))))

            if record[Candidate.CandidateDesiredSalary.name] and record[Candidate.Currency.name]:
                currency = record[Job.Currency.name] or ''  # it could be a Currency object e.g. {code: 'USD'...}
                if isinstance(currency, dict): currency = currency.get('code', '')
                desc.append(random.choice(salary)
                            .replace("[salary]", str(round(record[Candidate.CandidateDesiredSalary.name])))
                            .replace("[currency]", currency))

            # random.shuffle(desc)
            data.append({
                "id": record["ID"],
                "databaseType": DatabaseType.Candidates.value,
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
                             con=db.session.bind).fillna('')

        df = df.drop('DatabaseID', axis=1)  # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0  # Add column for tracking score
        df['Source'] = "Internal Database"  # Source of solution e.g. Bullhorn, Adapt...

        if extraJobs:
            df = df.append(extraJobs, ignore_index=True)

        # Check if there are no Jobs.
        if not len(df):
            return Callback(True, '', [])


        # Fill None values with 0 for numeric columns and with empty string for string columns
        df = df.fillna({Job.JobSalary.name: 0, Job.JobYearsRequired.name: 0}).fillna('')

        # Salary comparision
        salaryInputs: list = \
            keywords.get(DT.JobSalary.value['name'], keywords.get(DT.CandidateDesiredSalary.value['name']))

        if salaryInputs:
            df[['Score', Job.JobSalary.name, Job.Currency.name]] = \
                df.apply(lambda row: __salary(row, Job.JobSalary, Job.Currency, salaryInputs[-1], 8),
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
        __wordsCounter(DT.JobCity, Job.JobCity, keywords, df, 3)
        __wordsCounter(DT.CandidateCity, Job.JobCity, keywords, df, 3)

        # Skills
        __wordsCounter(DT.JobEssentialSkills, Job.JobEssentialSkills, keywords, df, 3)
        __wordsCounter(DT.CandidateSkills, Job.JobEssentialSkills, keywords, df, 3)

        # Results
        topResults = json.loads(df[df['Score'] > 0].nlargest(session.get('showTop', 0), 'Score')
                                .to_json(orient='records'))

        jobType = ["This role is a [jobType]", "This job is a [jobType]"]
        location = [" located in [location]. "]
        requiredYearsSkills = ["It requires [yearsRequired] year(s) with [essentialSkills]. ",
                               "This role requires [yearsRequired] year(s) with [essentialSkills]. "]

        data = []
        for record in topResults:
            desc = []
            # Build random dynamic job description
            if record[Job.JobType.name]:
                desc.append(random.choice(jobType).replace("[jobType]",
                                                           record[Job.JobType.name]))
                if record[Job.JobCity.name]:
                    desc[0] += random.choice(location).replace("[location]",
                                                               record[Job.JobCity.name])
                else:
                    desc[0] += ". "

            essentialSkills = record[Job.JobEssentialSkills.name]

            if record[Job.JobYearsRequired.name] and essentialSkills:
                desc.append(random.choice(requiredYearsSkills)
                            .replace("[yearsRequired]", str(int(record[Job.JobYearsRequired.name])))
                            .replace("[essentialSkills]", essentialSkills))

            # Build job subtitles
            subTitles = []
            if record[Job.JobCity.name]:
                subTitles.append("Location: " + record[Job.JobCity.name])

            if record[Job.JobSalary.name]:
                currency = record[Job.Currency.name] or ''  # it could be a Currency object e.g. {code: 'USD'...}
                if isinstance(currency, dict): currency = currency.get('code', '')
                subTitles.append("Salary: "
                                 + str(float(record[Job.JobSalary.name]))
                                 + ' ' + currency)

            if essentialSkills:
                subTitles.append("Essential Skills: " + essentialSkills)

            data.append({
                "id": record["ID"],
                "databaseType": DatabaseType.Jobs.value,
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


# ----------------------------------------------------------------
def __wordsCounter(dataType: DT, dbColumn, keywords, df, x=1):
    keywords = keywords.get(dataType.value['name'])
    if keywords:
        df['Score'] += x * df[dbColumn.name].str.count('|'.join([re.escape(k) for k in keywords]),
                                                       flags=re.IGNORECASE) | 0


def __numCounter(dbColumn, compareSign, dataType: DT, keywords, df, plus=1, addInputToScore=False):
    if keywords.get(dataType.value['name']):
        numberInput = float(keywords.get(dataType.value['name'])[-1])

        # it is good for years of exp to be added to the score
        if addInputToScore:
            plus += 7 if numberInput > 7 else numberInput

        # Compare
        if compareSign == '>':
            df.loc[df[dbColumn.name] >= numberInput, 'Score'] += plus
        else:  # '<'
            df.loc[df[dbColumn.name] <= numberInput, 'Score'] += plus


# min-max currency period / ex. "10000-45000 GBP Annually" old: "Greater Than 5000 GBP Annually"
def __salary(row, dbSalaryColumn, dbCurrencyColumn, salaryInput: str, plus=4, forceLessThan=False):
    userSalary = salaryInput.split(' ')

    # Get user's min and max salary
    userMin = float(re.sub("[^0-9]", "", userSalary[0].split("-")[0]))
    userMax = float(re.sub("[^0-9]", "", userSalary[0].split("-")[1]))

    # Convert db salary currency if did not match with user's entered currency
    dbSalary = row[dbSalaryColumn.name] or 0
    if (row[dbCurrencyColumn.name] != userSalary[1]) and dbSalary > 0:
        print("Convert")
        dbSalary = helpers.currencyConverter.convert(row[dbCurrencyColumn.name], userSalary[1], dbSalary)
        row[dbSalaryColumn.name] = dbSalary

    # Convert salary rate if did not match with user's entered pay period e.g. Annually to Daily...
    # if (not row[dbPayPeriodColumn.name] == userSalary[2]) and dbSalary > 0:
    #     dbSalary = helpers.convertSalaryPeriod(dbSalary, row[dbPayPeriodColumn.name], Period[userSalary[2]])

    # Add old score to new score
    plus += row['Score']

    # Compare salaries, if true then return 'plus' to be added to the score otherwise old score
    if not forceLessThan:
        return (plus if (userMin <= dbSalary <= userMax) else row['Score']), dbSalary, userSalary[1]
    else:  # Less
        return (plus if dbSalary <= userMax else row['Score']), dbSalary, userSalary[1]


def createPandaCandidate(id, name, email, mobile, location, skills,
                         linkdinURL, availability, jobTitle, education,
                         yearsExperience: int, desiredSalary, currency: Currency, source):
    if isinstance(desiredSalary, str):
        desiredSalary = float(re.sub("[^0-9]", "", desiredSalary))
    return {"ID": id,
            "CandidateName": name or '',
            "CandidateEmail": email or '',
            "CandidateMobile": mobile or '',
            "CandidateCity": location or '',
            "CandidateSkills": convertSkillsToString(skills) or '',
            "CandidateLinkdinURL": linkdinURL or '',
            "CandidateAvailability": availability or '',
            "CandidateJobTitle": jobTitle or '',
            "CandidateEducation": education or '',
            "CandidateYearsExperience": yearsExperience or 0,
            "CandidateDesiredSalary": desiredSalary or 0,
            "Currency": currency,
            "Score": 0,
            "Source": source or '',
            }


def createPandaJob(id, title, desc, location, type, salary, essentialSkills, yearsRequired,
                   startDate, endDate, linkURL, currency: Currency, source):
    if isinstance(salary, str):
        salary = float(re.sub("[^0-9]", "", salary))
    return {"ID": id,
            "JobTitle": title or '',
            "JobDescription": desc or '',
            "JobCity": location or '',
            "JobType": type or '',
            "JobSalary": salary or 0,
            "JobEssentialSkills": convertSkillsToString(essentialSkills) or '',
            "JobYearsRequired": yearsRequired or 0,
            "JobStartDate": startDate or '',
            "JobEndDate": endDate,
            "JobLinkURL": linkURL,
            "Currency": currency,
            "Score": 0,
            "Source": source or '',
            }