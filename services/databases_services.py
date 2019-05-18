from models import db, Callback, Database, Candidate, Assistant, Job
from services import assistant_services
from typing import List
from datetime import datetime
from sqlalchemy_utils import Currency
from utilities import helpers
from sqlalchemy import and_
from enums import DatabaseType, DataType as DT
import json, random, logging, pandas, re, enums



def fetchDatabase(id, companyID: int, pageNumber: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        database: Database = db.session.query(Database)\
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
        print(exc)
        logging.error("databases_service.fetchDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not fetch the database.')


def updateDatabase(id, newName, companyID)-> Callback:
    try:
        if not newName: raise  Exception
        db.session.query(Database).filter(and_(Database.ID == id, Database.CompanyID == companyID))\
            .update({'Name': newName})
        db.session.commit()
        return Callback(True, newName + ' database updated successfully')

    except Exception as exc:
        print(exc)
        logging.error("databases_service.updateDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False,
                        "Couldn't update database ")


# ----- Uploader ----- #
def uploadDatabase(data: dict, companyID: int) -> Callback:

    try:

        def parseRecord(record):
            parsed = {}
            for key, content in record.items(): # loop through record's columns
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

        def uploadCandidates(databaseData, newDatabase):
            candidates = []
            for record in databaseData["records"]:
                candidates.append(Candidate(Database=newDatabase, **parseRecord(record)))
            db.session.add_all(candidates)

        def uploadJobs(databaseData, newDatabase):
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
        print(exc)
        logging.error("databases_service.uploadDatabase(): " + str(exc))
        return Callback(False, 'Could not upload the databases.')


# ----- Getters ----- #
def getDatabasesList(companyID: int) -> Callback:
    try:
        databases: List[Database] = db.session.query(Database) \
            .filter(and_(Database.CompanyID == companyID)).all()
        return Callback(True, "Databases list is here", databases)

    except Exception as exc:
        print(exc)
        logging.error("databases_service.getDatabasesList(): " + str(exc))
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
        print("databases_services.getCandidate() Error: ", exc)
        logging.error("databases_service.getCandidate(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the candidate.')


def getJob(jobID):
    try:
        job = db.session.query(Job) \
            .filter(Job.ID == jobID).first()
        if not job: raise Exception

        return Callback(True, "Job retrieved successfully.", job)

    except Exception as exc:
        print("databases_services.getJob() Error: ", exc)
        logging.error("databases_service.getJob(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the job.')



# Get All
def getAllCandidates(dbID, page) -> dict:
    try:
        result = db.session.query(Candidate)\
            .filter(Candidate.DatabaseID == dbID) \
            .paginate(page=page, error_out=False, per_page=100)

        data = {
            'records': helpers.getListFromSQLAlchemyList(result.items),
            'currentPage': result.page,
            'totalItems': result.total,
            'totalPages': result.pages,
            'totalPerPage': result.per_page
        }
        return data

    except Exception as exc:
        print("fetchCandidates() ERROR: ", exc)
        logging.error("databases_service.getAllCandidates(): " + str(exc))
        raise Exception


def getAllJobs(dbID, page) -> dict:
    try:
        result = db.session.query(Job) \
            .filter(Job.DatabaseID == dbID) \
            .paginate(page=page, error_out=False, per_page=100)

        data = {
            'records': helpers.getListFromSQLAlchemyList(result.items),
            'currentPage': result.page,
            'totalItems': result.total,
            'totalPages': result.pages,
            'totalPerPage': result.per_page
        }
        return data

    except Exception as exc:
        print("fetchCandidates() ERROR: ", exc)
        logging.error("databases_service.getAllJobs(): " + str(exc))
        raise Exception('Error: getAllJobs()')



# ----- Deletion ----- #
def deleteDatabase(databaseID, companyID) -> Callback:
    try:
        db.session.query(Database).filter(and_(Database.CompanyID == companyID, Database.ID == databaseID)) \
            .delete()
        db.session.commit()
        return Callback(True, 'Database has been deleted.')

    except Exception as exc:
        print("Error in deleteDatabase(): ", exc)
        logging.error("databases_service.deleteDatabase(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not remove the database.')


# ----- Scanners (Pandas) ----- #
def scan(session, assistantHashID):
    try:

        callback: Callback = assistant_services.getAssistantByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = callback.Data

        databaseType: DatabaseType = DatabaseType[session['databaseType']]
        databases: List[Database] = db.session.query(Database.ID) \
            .filter(and_(Database.CompanyID == assistant.CompanyID,
                         Database.Type == databaseType)).all()

        # Scan database for solutions based on database type
        if databaseType == enums.DatabaseType.Candidates:
            return scanCandidates(session, [d[0] for d in databases])
        elif databaseType == enums.DatabaseType.Jobs:
            return scanJobs(session, [d[0] for d in databases])
        else:
            return Callback(False, "Database type is not recognised", None)



    except Exception as exc:
        print("databases_service.scan() ERROR: ", exc)
        logging.error("databases_service.scan(): " + str(exc))
        return Callback(False, 'Error while scanning the database')


# Data analysis using Pandas library
def scanCandidates(session, dbIDs, extraCandidates=None):
    try:

        df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)
        df = df.drop('DatabaseID', axis=1) # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0 # Add column for tracking score
        df['Source'] = "Internal Database" # Source of solution e.g. Bullhorn, Adapt...


        if extraCandidates:
            df = df.append(extraCandidates, ignore_index=True)

        def wordsCounter(dataType: DT, dbColumn, x=1):
            if keywords.get(dataType.value['name']):
                df['Score'] += x * df[dbColumn.name].str.count('|'.join(keywords[dataType.value['name']]),
                                                           flags=re.IGNORECASE) | 0

        def greaterCounter(dataType: DT, dbColumn, plus=1):
            if keywords.get(dataType.value['name']):
                df.loc[df[dbColumn.name] <=
                       float(keywords[dataType.value['name']][-1]), 'Score'] += plus

        def lessCounter(dataType: DT, dbColumn, plus=1):
            if keywords.get(dataType.value['name']):
                df.loc[df[dbColumn.name] >=
                       float(keywords[dataType.value['name']][-1]), 'Score'] += plus

        # Desired Salary
        greaterCounter(DT.CandidateDesiredSalary, Candidate.CandidateDesiredSalary, 3)
        greaterCounter(DT.JobSalary, Candidate.CandidateDesiredSalary, 3)

        # Years of EXP
        lessCounter(DT.CandidateYearsExperience, Candidate.CandidateYearsExperience, 5)

        # Education
        wordsCounter(DT.CandidateEducation, Candidate.CandidateEducation)

        # Location
        wordsCounter(DT.JobLocation, Candidate.CandidateLocation, 6)
        wordsCounter(DT.CandidateLocation, Candidate.CandidateLocation, 6)

        # JobTitle
        wordsCounter(DT.CandidateJobTitle, Candidate.CandidateJobTitle)
        wordsCounter(DT.JobTitle, Candidate.CandidateJobTitle)

        # Skills
        wordsCounter(DT.CandidateSkills, Candidate.CandidateSkills, 2)
        wordsCounter(DT.JobDesiredSkills, Candidate.CandidateSkills, 2)
        wordsCounter(DT.JobEssentialSkills, Candidate.CandidateSkills, 2)

        # Availability
        wordsCounter(DT.CandidateAvailability, Candidate.CandidateAvailability)


        topResults = json.loads(df[df['Score']>0].nlargest(session.get('showTop', 2), 'Score')
                                .to_json(orient='records'))

        data = [] # List of candidates
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
        print("scanCandidates() ERROR: ", exc)
        logging.error("databases_service.scanCandidates(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')


def scanJobs(session, dbIDs, extraJobs=None):
    try:

        df = pandas.read_sql(db.session.query(Job).filter(Job.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)
        df = df.drop('DatabaseID', axis=1) # Drop column

        keywords = session['keywordsByDataType']
        df['Score'] = 0 # Add column for tracking score
        df['Source'] = "Internal Database" # Source of solution e.g. Bullhorn, Adapt...

        if extraJobs:
            df = df.append(extraJobs, ignore_index=True)

        def wordsCounter(dataType: DT, dbColumn, x=1):
            if keywords.get(dataType.value['name']):
                df['Score'] += x * df[dbColumn.name].str.count('|'.join(keywords[dataType.value['name']]),
                                                               flags=re.IGNORECASE) | 0

        def greaterCounter(dataType: DT, dbColumn, plus=1):
            if keywords.get(dataType.value['name']):
                df.loc[df[dbColumn.name] <=
                       float(keywords[dataType.value['name']][-1]), 'Score'] += plus

        def lessCounter(dataType: DT, dbColumn, plus=1):
            if keywords.get(dataType.value['name']):
                df.loc[df[dbColumn.name] >=
                       float(keywords[dataType.value['name']][-1]), 'Score'] += plus

        # Salary
        lessCounter(DT.JobSalary, Job.JobSalary, 3)
        lessCounter(DT.CandidateDesiredSalary, Job.JobSalary, 3)
        # Year Required
        greaterCounter(DT.JobYearsRequired, Job.JobYearsRequired, 5)
        greaterCounter(DT.CandidateYearsExperience, Job.JobYearsRequired, 5)
        # Job Title
        wordsCounter(DT.JobTitle, Job.JobTitle, 2)
        wordsCounter(DT.JobTitle, Job.JobDescription, 2)
        wordsCounter(DT.CandidateSkills, Job.JobTitle, 2)
        wordsCounter(DT.CandidateSkills, Job.JobDescription, 2)
        # Type
        wordsCounter(DT.JobType, Job.JobType, 2)
        # Location
        wordsCounter(DT.JobLocation, Job.JobLocation, 3)
        wordsCounter(DT.CandidateLocation, Job.JobLocation, 3)
        # Skills
        wordsCounter(DT.JobEssentialSkills, Job.JobEssentialSkills, 3)
        wordsCounter(DT.JobDesiredSkills, Job.JobDesiredSkills, 3)
        wordsCounter(DT.CandidateSkills, Job.JobEssentialSkills, 3)
        wordsCounter(DT.CandidateSkills, Job.JobDesiredSkills, 3)

        # Results
        topResults = json.loads(df[df['Score']>0].nlargest(session.get('showTop', 0), 'Score')
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
        print("scanJobs() ERROR: ", exc)
        logging.error("databases_service.scanJobs(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')



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


def getOptions() -> Callback:
    options =  {
        'types': [dt.name for dt in enums.DatabaseType ],
        enums.DatabaseType.Candidates.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                             for c in Candidate.__table__.columns
                                             if (c.key != 'ID' and c.key != 'DatabaseID')],
        enums.DatabaseType.Jobs.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                       for c in Job.__table__.columns
                                       if (c.key != 'ID' and c.key != 'DatabaseID')],
        'currencyCodes': ['GBP', 'USD', 'EUR', 'AED', 'CAD']
    }
    return Callback(True, '', options)


def test():
    # df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_([1,2])).statement,
    #                      con=db.session.bind)
    #
    # print(df)
    #
    # d = {"f":"g"}
    # s = json.dumps(d)
    #
    # a = helpers.encryptor.encrypt(bytes((s.encode('utf-8'))))
    # # print(helpers.encryptor.decrypt(json.loads(a['f'])))
    # r = helpers.encryptor.decrypt(bytes('gAAAAABc34DnlnV_xIPtwcMMLH_qZ4JQv36Cdxpg_YgMQ1vw9OjX-yD7QyZ3LAsPTv9XP1EGRB4YoBEUg54s295yy8dOD7BtZw=='.encode('utf-8')))
    # r2 = json.loads(r)
    # print(r2['f'])


    d = {"f":"g"}
    e = helpers.encrypt(d, isDict=True)
    print(e)
    # r = helpers.decrypt(e, isDict=True)
    # print(r['f'])

    print(helpers.decrypt(e,True, True))


