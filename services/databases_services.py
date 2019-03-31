from models import db, Callback, Database, Candidate, Assistant, Job
from services import assistant_services
from typing import List
import pandas
import re
import enums
from datetime import datetime
from sqlalchemy_utils import Currency
from utilities import helpers
from sqlalchemy import and_
from enums import DatabaseType, DataType as DT
import json
import random
import logging


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
        candidate = db.session.query(Job) \
            .filter(Job.ID == jobID).first()
        if not candidate: raise Exception

        return Callback(True, "Job retrieved successfully.", candidate)

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

        databaseType: DatabaseType = DatabaseType[session['databaseType'].replace(" ", "")]
        databases: List[Database] = db.session.query(Database.ID) \
            .filter(and_(Database.CompanyID == assistant.CompanyID,
                         Database.Type == databaseType)).all()

        # Scan database for solutions based on database type
        if databaseType == enums.DatabaseType.Candidates:
            return scanCandidates(session, [d[0] for d in databases], databaseType)
        elif databaseType == enums.DatabaseType.Jobs:
            return scanJobs(session, [d[0] for d in databases], databaseType)
        else:
            return Callback(False, "Database type is not recognised", None)



    except Exception as exc:
        print("databases_service.scan() ERROR: ", exc)
        logging.error("databases_service.scan(): " + str(exc))
        return Callback(False, 'Error while scanning the database')


# Data analysis using Pandas library
def scanCandidates(session, dbIDs, databaseType: DatabaseType):
    try:

        df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)


        keywords = session['keywordsByDataType']
        df['count'] = 0 # add column for tracking score

        # Numbers
        # Received DataType: CandidateDesiredSalary <> Column: CandidateDesiredSalary | points=3
        if keywords.get(DT.CandidateDesiredSalary.value['name']):
            df.loc[df[Candidate.CandidateDesiredSalary.name] <= float(keywords[DT.CandidateDesiredSalary.value['name']][-1]), 'count'] += 3

        # Received DataType: JobSalary <> Column: DesiredSalary | points=3
        if keywords.get(DT.JobSalary.value['name']):
            df.loc[df[Candidate.CandidateDesiredSalary.name] <= float(keywords[DT.JobSalary.value['name']][-1]), 'count'] += 3


        # Received DataType: CandidateYearsExperience <> Column: CandidateYearsExperience | points=5
        if keywords.get(DT.CandidateYearsExperience.value['name']):
            df.loc[df[Candidate.CandidateYearsExperience.name] >= float(keywords[DT.CandidateYearsExperience.value['name']][-1]), 'count'] += 5


        #  ================================================================================


        # Received DataType: CandidateEducation <> Column: CandidateEducation | points= 1
        if keywords.get(DT.CandidateEducation.value['name']):
            df['count'] += df[Candidate.CandidateEducation.name].str.count('|'.join(keywords[DT.CandidateEducation.value['name']]),
                                                                 flags=re.IGNORECASE) | 0


        # ======================= Candidate Location ===================================
        # Received DataType: CandidateLocation <> Column: CandidateLocation | points= 1
        if keywords.get(DT.CandidateLocation.value['name']):
            df['count'] += df[Candidate.CandidateLocation.name].str.count('|'.join(keywords[DT.CandidateLocation.value['name']]),
                                                                 flags=re.IGNORECASE) | 0

        # Received DataType: JobLocation <> Column: CandidateLocation | points= 1
        if keywords.get(DT.JobLocation.value['name']):
            df['count'] += df[Candidate.CandidateLocation.name].str.count('|'.join(keywords[DT.JobLocation.value['name']]),
                                                                          flags=re.IGNORECASE) | 0


        # Received DataType: CandidateJobTitle <> Column: CandidateJobTitle | points= 1
        if keywords.get(DT.CandidateJobTitle.value['name']):
            df['count'] += df[Candidate.CandidateJobTitle.name].str.count('|'.join(keywords[DT.CandidateJobTitle.value['name']]),
                                                                        flags=re.IGNORECASE) | 0


        # ======================= Candidate Skills ===================================
        # Received DataType: CandidateSkills <> Column: CandidateSkills | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Candidate.CandidateSkills.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                                flags=re.IGNORECASE) | 0

        # Received DataType: JobDesiredSkills <> Column: CandidateSkills | points= 1
        if keywords.get(DT.JobDesiredSkills.value['name']):
            df['count'] += df[Candidate.CandidateSkills.name].str.count('|'.join(keywords[DT.JobDesiredSkills.value['name']]),
                                                                        flags=re.IGNORECASE) | 0

        # Received DataType: JobEssentialSkills <> Column: CandidateSkills | points= 1
        if keywords.get(DT.JobEssentialSkills.value['name']):
            df['count'] += df[Candidate.CandidateSkills.name].str.count('|'.join(keywords[DT.JobEssentialSkills.value['name']]),
                                                                        flags=re.IGNORECASE) | 0
        #  =============================================================================


        # ======================= Candidate Availability ===================================
        # Received DataType: CandidateAvailability <> Column: CandidateAvailability | points= 1
        if keywords.get(DT.CandidateAvailability.value['name']):
            df['count'] += df[Candidate.CandidateAvailability.name].str.count('|'.join(keywords[DT.CandidateAvailability.value['name']]),
                                                                                flags=re.IGNORECASE) | 0

        topResults = json.loads(df[df['count']>0].nlargest(session.get('showTop', 2), 'count')
                                .to_json(orient='records'))

        data = []


        location = ["Their preferred location for work would be [location].",
                    "They prefer to work in [location]."]

        yearsExp = ["This candidate has [yearsExp] years of experience in  [skills].",
                    "They have experience with [skills] for [yearsExp] years."]

        desiredSalary = ["This candidate desired salary is £[desiredSalary]",
                         "Their desired salary is £[desiredSalary]"]



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

            if record[Candidate.CandidateDesiredSalary.name]:
                desc.append(random.choice(desiredSalary).replace("[desiredSalary]",
                                                            str(record[Candidate.CandidateDesiredSalary.name])))
            random.shuffle(desc)
            data.append({
                "id": record["ID"],
                "databaseType": databaseType.value,
                "title": "Candidate " + indexes[i],
                # "subTitle": "Location: " + (record[Candidate.CandidateLocation.name] or "Unavailable"),
                "description": " ".join(desc),
                "buttonText": "Enquire"
            })

        return Callback(True, '', data)

    except Exception as exc:
        print("scanCandidates() ERROR: ", exc)
        logging.error("databases_service.scanCandidates(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')


def scanJobs(session, dbIDs, databaseType: DatabaseType):
    try:

        df = pandas.read_sql(db.session.query(Job).filter(Job.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)

        keywords = session['keywordsByDataType']
        df['count'] = 0 # add column for tracking score

        # ======================= Numbers Comparision ===================================
        # Received DataType: JobSalary <> Column: JobSalary | points=3
        if keywords.get(DT.JobSalary.value['name']):
            df.loc[df[Job.JobSalary.name] >= float(keywords[DT.JobSalary.value['name']][-1]), 'count'] += 3
        #  ================================================================================

        # ======================= Job Title ===================================
        # Received DataType: JobTitle <> Column: JobTitle | points= 1
        if keywords.get(DT.JobTitle.value['name']):
            df['count'] += df[Job.JobTitle.name].str.count('|'.join(keywords[DT.JobTitle.value['name']]),
                                                                        flags=re.IGNORECASE) | 0

        # Received DataType: JobTitle <> Column: JobDescription | points= 1
        if keywords.get(DT.JobTitle.value['name']):
            df['count'] += df[Job.JobDescription.name].str.count('|'.join(keywords[DT.JobTitle.value['name']]),
                                                           flags=re.IGNORECASE) | 0

        # Received DataType: JobType <> Column: JobType | points= 1
        if keywords.get(DT.JobType.value['name']):
            df['count'] += df[Job.JobType.name].str.count('|'.join(keywords[DT.JobType.value['name']]),
                                                              flags=re.IGNORECASE) | 0
        #  =======================================================================


        # ======================= Job Location ===================================
        # Received DataType: JobLocation <> Column: JobLocation | points= 1
        if keywords.get(DT.JobLocation.value['name']):
            df['count'] += df[Job.JobLocation.name].str.count('|'.join(keywords[DT.JobLocation.value['name']]),
                                                           flags=re.IGNORECASE) | 0


        # Received DataType: CandidateLocation <> Column: JobLocation | points= 1
        if keywords.get(DT.CandidateLocation.value['name']):
            df['count'] += df[Job.JobLocation.name].str.count('|'.join(keywords[DT.CandidateLocation.value['name']]),
                                                              flags=re.IGNORECASE) | 0
        # =========================================================================


        # ======================= Job Skills ===================================
        # Received DataType: JobEssentialSkills <> Column: JobEssentialSkills | points= 1
        if keywords.get(DT.JobEssentialSkills.value['name']):
            df['count'] += df[Job.JobEssentialSkills.name].str.count('|'.join(keywords[DT.JobEssentialSkills.value['name']]),
                                                                        flags=re.IGNORECASE) | 0

        # Received DataType: JobDesiredSkills <> Column: JobDesiredSkills | points= 1
        if keywords.get(DT.JobDesiredSkills.value['name']):
            df['count'] += df[Job.JobDesiredSkills.name].str.count('|'.join(keywords[DT.JobDesiredSkills.value['name']]),
                                                                  flags=re.IGNORECASE) | 0


        # Received DataType: CandidateSkills <> Column: JobEssentialSkills | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Job.JobEssentialSkills.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                     flags=re.IGNORECASE) | 0

        # Received DataType: CandidateSkills <> Column: JobDesiredSkills | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Job.JobDesiredSkills.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                   flags=re.IGNORECASE) | 0
        # =========================================================================

        topResults = json.loads(df[df['count']>0].nlargest(session.get('showTop', 0), 'count')
                                .to_json(orient='records'))
        data = []
        for record in topResults:
            data.append({
                "id": record["ID"],
                "databaseType": databaseType.value,
                "title": record[Job.JobTitle.name],
                "subTitle": "Location: " + (record[Job.JobLocation.name] or "Unavailable"),
                "description": "Skills: " + (record[Job.JobEssentialSkills.name] or "Unavailable"),
                "buttonText": "Apply"
            })

        return Callback(True, '', data)

    except Exception as exc:
        print("scanJobs() ERROR: ", exc)
        logging.error("databases_service.scanJobs(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')


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
