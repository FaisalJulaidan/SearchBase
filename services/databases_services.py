from models import db, Callback, Database, Candidate, Client, Assistant, Job
from services import assistant_services
from typing import List
import pandas
import re
import enums
from datetime import datetime
from sqlalchemy_utils import Currency
from utilities import helpers
from sqlalchemy import and_
from enums import  DatabaseType, DataType as DT
import json

def fetchDatabase(id, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        database: Database = db.session.query(Database)\
            .filter(and_(Database.CompanyID == companyID, Database.ID == id)).first()
        if not database: raise Exception

        databaseContent = None
        if database.Type == DatabaseType.Candidates:
            print('fetch from candidate table')
            databaseContent = helpers.getListFromSQLAlchemyList(getAllCandidates(id))


        elif database.Type == DatabaseType.Clients:
            print('fetch from client table')
            databaseContent = helpers.getListFromSQLAlchemyList(getAllClients(id))


        elif database.Type == DatabaseType.Jobs:
            print('fetch from candidate table')
            databaseContent = helpers.getListFromSQLAlchemyList(getAllJobs(id))
            for i, _ in enumerate(databaseContent):
                temp = databaseContent[i]['Currency'].code
                del databaseContent[i]['Currency']
                databaseContent[i]['Currency'] = temp

                day = databaseContent[i]['StartDate'].day
                month = databaseContent[i]['StartDate'].month
                year = databaseContent[i]['StartDate'].year
                del databaseContent[i]['StartDate']
                databaseContent[i]['StartDate'] = '/'.join(map(str, [year, month, day]))


        if not databaseContent: raise Exception()
        return Callback(True, "", {'databaseInfo': helpers.getDictFromSQLAlchemyObj(database),
                                   'databaseContent': databaseContent})

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not fetch the database.')
    # finally:
        # db.session.close()


# ----- Uploader ----- #
def uploadDatabase(data: dict, companyID: int) -> Callback:

    try:
        # Inner/nested functions
        def createDatabase(name, type: DatabaseType):
            return Database(Name=name, Type=type, CompanyID=companyID)

        # Create currency for Currency column
        def createCurrency(currency):
            currency = currency.get('data', None)
            if currency:
                return Currency(currency)
            return None

        def uploadCandidates(databaseData, newDatabase):
            candidates = []
            for record in databaseData["records"]:
                print(record)
                new_record = Candidate(
                                       Database=newDatabase,
                                       Name=record.get('Name',{}).get('data'),
                                       Email=record.get('Email',{}).get('data'),
                                       Telephone=record.get('Telephone',{}).get('data'),
                                       LinkdinURL=record.get('LinkdinURL',{}).get('data'),
                                       PostCode=record.get('PostCode',{}).get('data'),
                                       Gender=record.get('Gender',{}).get('data'),
                                       Degree=record.get('Degree',{}).get('data'),
                                       ContactTime=record.get('ContactTime',{}).get('data'),
                                       Availability=record.get('Availability',{}).get('data'),
                                       CurrentSalary=record.get('CurrentSalary',{}).get('data') or None,
                                       Currency=createCurrency(record.get('Currency', {})),
                                       CurrentRole=record.get('CurrentRole',{}).get('data'),
                                       JobTitle=record.get('JobTitle',{}).get('data'),
                                       CurrentEmployer=record.get('CurrentEmployer',{}).get('data'),
                                       CurrentEmploymentType=record.get('CurrentEmploymentType',{}).get('data'),
                                       DesiredSalary=record.get('DesiredSalary',{}).get('data') or None,
                                       DesiredPosition=record.get('DesiredPosition',{}).get('data'),
                                       CandidateSkills=record.get('CandidateSkills',{}).get('data'),
                                       YearsExp=record.get('YearsExp',{}).get('data') or None,
                                       PreferredLocation=record.get('PreferredLocation',{}).get('data'),
                                       PreferredEmploymentType=record.get('PreferredEmploymentType',{}).get('data'),
                                       DesiredHourlyRate=record.get('DesiredHourlyRate',{}).get('data') or None
                )
                candidates.append(new_record)
            db.session.add_all(candidates)

        def uploadClients(databaseData, newDatabase):
            clients = []
            for record in databaseData["records"]:
                new_record = Client(
                    Database=newDatabase,
                    Name=record.get('Name',{}).get('data'),
                    Email=record.get('Email',{}).get('data'),
                    Telephone=record.get('Telephone',{}).get('data'),
                    LinkdinURL=record.get('LinkdinURL',{}).get('data'),
                    PostCode=record.get('PostCode',{}).get('data'),
                    Location=record.get('Location',{}).get('data'),
                    NearbyStation=record.get('NearbyStation',{}).get('data'),
                    JobSalaryOffered=record.get('JobSalaryOffered',{}).get('data') or None,
                    Currency=createCurrency(record.get('Currency', {})),
                    EmploymentTypeOffered=record.get('EmploymentTypeOffered',{}).get('data') or None,
                    CandidatesNeeded=record.get('CandidatesNeeded',{}).get('data') or None,
                    EssentialSkills=record.get('EssentialSkills',{}).get('data'),
                    EssentialYearsExp=record.get('EssentialYearsExp',{}).get('data') or None,
                    ContractRate=record.get('ContractRate',{}).get('data') or None,
                    JobDescription=record.get('JobDescription',{}).get('data'),
                    JobAvailability=record.get('JobAvailability',{}).get('data')
                )
                clients.append(new_record)
            db.session.add_all(clients)

        def uploadJobs(databaseData, newDatabase):
            jobs = []
            for record in databaseData["records"]:
                # create datetime for StartDate
                startDate = record.get('StartDate',{}).get('data', None)
                if startDate:
                    startDate = datetime(year=startDate['year'],
                                         month=startDate['month'],
                                         day=startDate['day'])

                new_record = Job(
                    Database=newDatabase,
                    JobTitle=record.get('JobTitle',{}).get('data'),
                    Location=record.get('Location',{}).get('data'),
                    PositionType=record.get('PositionType',{}).get('data'),
                    EmploymentType=record.get('EmploymentType',{}).get('data'),
                    Salary=record.get('Salary',{}).get('data') or None,
                    Currency=createCurrency(record.get('Currency', {})),
                    StartDate=startDate,
                )
                jobs.append(new_record)
            db.session.add_all(jobs)
        # ===========================

        databaseData = data.get('newDatabase')
        databaseName = databaseData["databaseName"]
        if databaseData['databaseType'] == enums.DatabaseType.Candidates.value:
            newDatabase = createDatabase(databaseName, DatabaseType.Candidates)
            uploadCandidates(databaseData, newDatabase)
        elif databaseData['databaseType'] == enums.DatabaseType.Clients.value:
            newDatabase = createDatabase(databaseName, DatabaseType.Clients)
            uploadClients(databaseData, newDatabase)
        elif databaseData['databaseType'] == enums.DatabaseType.Jobs.value:
            newDatabase = createDatabase(databaseName, DatabaseType.Jobs)
            uploadJobs(databaseData, newDatabase)
        else:
            return Callback(False, "Database type is not recognised")
        # After finishing from uploading database without errors, save changes
        db.session.commit()
        return Callback(True, "Databases was successfully uploaded!", newDatabase)
    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not upload the databases.')


# ----- Getters ----- #
def getDatabasesList(companyID: int) -> Callback:
    try:
        databases: List[Database] = db.session.query(Database) \
            .filter(and_(Database.CompanyID == companyID)).all()
        return Callback(True, "Databases list is here", databases)

    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not fetch the databases list.')

def getAllCandidates(dbID) -> Callback:
    try:
        return db.session.query(Candidate).filter(Candidate.DatabaseID == dbID).all()

    except Exception as exc:
        db.session.rollback()
        print("fetchCandidates() ERROR: ", exc)
        return Callback(False, 'Candidates could not be retrieved.')


def getAllClients(dbID) -> Callback:
    try:
        return db.session.query(Client).filter(Client.DatabaseID == dbID).all()
    except Exception as exc:
        print("fetchCandidates() ERROR: ", exc)
        raise Exception('Error: fetchCandidates()')



def getAllJobs(dbID) -> Callback:
    try:
        return db.session.query(Job).filter(Job.DatabaseID == dbID).all()
    except Exception as exc:
        print("fetchCandidates() ERROR: ", exc)
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
        db.session.rollback()
        return Callback(False, 'Could not remove the database.')
    # finally:
    # db.session.close()


# ----- Scanners (Pandas) ----- #

def scan(session, assistantHashID):
    try:

        callback: Callback = assistant_services.getAssistantByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = callback.Data

        database: Database = db.session.query(Database) \
            .filter(and_(Database.CompanyID == assistant.CompanyID, Database.ID == session['databaseID'])).first()
        if not database: raise Exception

        # Scan database for solutions based on database type
        result = None
        if database.Type == enums.DatabaseType.Candidates:
            return scanCandidates(session)
        elif database.Type == enums.DatabaseType.Clients:
            pass
        elif database.Type == enums.DatabaseType.Jobs:
            pass
        else:
            return Callback(False, "Database type is not recognised")

        return Callback(False, "", result)


    except Exception as exc:
        print("scan() ERROR: ", exc)
        return Callback(False, 'Error while scanning the database')


# Data analysis using Pandas library
def scanCandidates(session):
    try:
        dbID = int(session['databaseID']) # prevent sql injection
        df = pandas.read_sql("SELECT * FROM Candidate WHERE DatabaseID=" + str(dbID),
                             con=db.session.bind)

        keywords = session['keywordsByDataType']
        df['count'] = 0 # add column for tracking score
        # Delete sensitive columns e.g. candidate name
        df.drop(['ID', DT.Name.name, DT.Email.name, DT.Telephone.name], axis=1, inplace=True)

        # Desired Salary <> Job Salary Offered | points=3
        if keywords.get(DT.JobSalaryOffered.value['name']):
            df.loc[df[DT.DesiredSalary.name] >= keywords[DT.JobSalaryOffered.value['name']][-1], 'count'] += 3

        # Desired Hourly Rate <> Contract Rate | points=3
        if keywords.get(DT.ContractRate.value['name']):
            df.loc[df[DT.DesiredHourlyRate.name] >= keywords[DT.ContractRate.value['name']][-1], 'count'] += 3

        # Years Exp <> Essential Years Exp | points=3
        if keywords.get(DT.EssentialYearsExp.value['name']):
            df.loc[df[DT.YearsExp.name] >= keywords[DT.EssentialYearsExp.value['name']][-1], 'count'] += 6



        # Desired Position <> Job Description | points= 1
        if keywords.get(DT.JobDescription.value['name']):
            print('|'.join(keywords[DT.JobDescription.value['name']]))
            df['count'] += df[DT.DesiredPosition.name].str.count('|'.join(keywords[DT.JobDescription.value['name']]),
                                                                 flags=re.IGNORECASE)

        # Candidate Skills <> Essential Skills | points=3 per skill
        if keywords.get(DT.EssentialSkills.value['name']):
            df['count'] += 3 * df[DT.CandidateSkills.name].str.count('|'.join(keywords[DT.EssentialSkills.value['name']]),
                                                                 flags=re.IGNORECASE)


        # Preferred Employment Type <> Employment Type Offered | points=2
        if keywords.get(DT.EmploymentTypeOffered.value['name']):
            df['count'] += 2 * df[DT.PreferredEmploymentType.name].str.count('|'.join(keywords[DT.EmploymentTypeOffered.value['name']]),
                                                                     flags=re.IGNORECASE)



        return Callback(True, '', json.loads(df[df['count']>0].nlargest(session.get('showTop', 0), 'count')
                                          .to_json(orient='records')))

    except Exception as exc:
        print("scanCandidates() ERROR: ", exc)
        return Callback(False, 'Error while search the database for matches!')



def getOptions() -> Callback:
    options =  {
        'types': [a.value for a in enums.DatabaseType ],
        enums.DatabaseType.Candidates.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                             for c in Candidate.__table__.columns
                                             if (c.key != 'ID' and c.key != 'DatabaseID')],
        enums.DatabaseType.Jobs.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                       for c in Job.__table__.columns
                                       if (c.key != 'ID' and c.key != 'DatabaseID')],
        enums.DatabaseType.Clients.name: [{'column': c.key, 'type': str(c.type), 'nullable': c.nullable}
                                          for c in Client.__table__.columns
                                          if (c.key != 'ID' and c.key != 'DatabaseID')],
        'currencyCodes': ['GBP', 'USD', 'EUR', 'AED', 'CAD']
    }
    return Callback(True, '', options)
