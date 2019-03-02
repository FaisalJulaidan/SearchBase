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
from enums import  DatabaseType, DataType as DT
import json

def fetchDatabase(id, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        database: Database = db.session.query(Database)\
            .filter(and_(Database.CompanyID == companyID, Database.ID == id)).first()
        if not database: raise Exception

        databaseContent = None
        # TODO Ensure it works
        if database.Type == DatabaseType.Candidates:
            print('fetch from candidate table')
            # result = helpers.getListFromSQLAlchemyList(getAllCandidates(id))
            # databaseContent = result['records']
            databaseContent = helpers.getListFromSQLAlchemyList(getAllCandidates(id))
            for i, _ in enumerate(databaseContent):
                if databaseContent[i]['Currency']:
                    temp = databaseContent[i]['Currency'].code
                    del databaseContent[i]['Currency']
                    databaseContent[i]['Currency'] = temp

        elif database.Type == DatabaseType.Jobs:
            print('fetch from candidate table')
            databaseContent = helpers.getListFromSQLAlchemyList(getAllJobs(id))
            for i, _ in enumerate(databaseContent):
                if databaseContent[i]['Currency']:
                    temp = databaseContent[i]['Currency'].code
                    del databaseContent[i]['Currency']
                    databaseContent[i]['Currency'] = temp

                if databaseContent[i]['StartDate']:
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

        def uploadJobs(databaseData, newDatabase):
            jobs = []
            for record in databaseData["records"]:
                # create datetime for StartDate
                startDate = record.get('StartDate', {}).get('data', None)
                if startDate:
                    startDate = datetime(year=startDate['year'],
                                         month=startDate['month'],
                                         day=startDate['day'])

                new_record = Job(
                    Database=newDatabase,
                    Title=record.get('Title', {}).get('data'),
                    Description=record.get('Description', {}).get('data'),
                    Location=record.get('Location', {}).get('data'),
                    PositionType=record.get('PositionType', {}).get('data'),
                    EmploymentType=record.get('EmploymentType', {}).get('data'),
                    Salary=record.get('Salary', {}).get('data') or None,
                    Currency=createCurrency(record.get('Currency', {})),
                    StartDate=startDate,
                )
                jobs.append(new_record)
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

def getAllCandidates(dbID) -> dict:
    try:
        return db.session.query(Candidate).filter(Candidate.DatabaseID == dbID).all()
        result = db.session.query(Candidate).filter(Candidate.DatabaseID == dbID).paginate(1, 1, False)
        # data = {
        #     'records': result.items,
        #     'hasNext': result.has_next,
        #     'hasPrev': result.has_prev,
        #     'nextNum': result.next_num,
        #     'prevNum': result.prev_num,
        # }
        # return data

    except Exception as exc:
        print("fetchCandidates() ERROR: ", exc)
        raise Exception

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

        databaseType: DatabaseType = DatabaseType[session['databaseType'].replace(" ", "")]
        databases: List[Database] = db.session.query(Database.ID) \
            .filter(and_(Database.CompanyID == assistant.CompanyID,
                         Database.Type == databaseType)).all()


        # if len(databases) == 0 : raise Exception
        print([d[0] for d in databases])

        # Scan database for solutions based on database type
        if databaseType == enums.DatabaseType.Candidates:
            return scanCandidates(session, [d[0] for d in databases])
        elif databaseType == enums.DatabaseType.Jobs:
            return scanJobs(session, [d[0] for d in databases])
        else:
            return Callback(False, "Database type is not recognised", None)



    except Exception as exc:
        print("scan() ERROR: ", exc)
        return Callback(False, 'Error while scanning the database')


# Data analysis using Pandas library
def scanCandidates(session, dbIDs):
    try:

        df = pandas.read_sql(db.session.query(Candidate).filter(Candidate.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)


        keywords = session['keywordsByDataType']
        df['count'] = 0 # add column for tracking score
        # Delete sensitive columns e.g. candidate name
        # df.drop(['ID', 'Name', 'Email', 'Telephone'], axis=1, inplace=True) # No need

        # Numbers
        # Received DataType: DesiredSalary <> Column: DesiredSalary | points=3
        if keywords.get(DT.DesiredSalary.value['name']):
            df.loc[df[Candidate.DesiredSalary.name] <= float(keywords[DT.DesiredSalary.value['name']][-1]), 'count'] += 3


        # Received DataType: YearsExp <> Column: YearsExp | points=5
        if keywords.get(DT.YearsExp.value['name']):
            df.loc[df[Candidate.YearsExp.name] >= float(keywords[DT.YearsExp.value['name']][-1]), 'count'] += 5


        # Received DataType: YearsExp <> Column: YearsExp | points=5
        if keywords.get(DT.DesiredPayRate.value['name']):
            df.loc[df[Candidate.DesiredPayRate.name] <= float(keywords[DT.DesiredPayRate.value['name']][-1]), 'count'] += 3

        #  =======================================


        # Received DataType: DesiredPosition <> Column: DesiredPosition | points= 1
        if keywords.get(DT.DesiredPosition.value['name']):
            df['count'] += df[Candidate.DesiredPosition.name].str.count('|'.join(keywords[DT.DesiredPosition.value['name']]),
                                                                 flags=re.IGNORECASE)


        # Received DataType: CandidateSkills <> Column: CandidateSkills | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Candidate.CandidateSkills.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                 flags=re.IGNORECASE)


        # Received DataType: PreferredLocation <> Column: PreferredLocation | points= 1
        if keywords.get(DT.PreferredLocation.value['name']):
            df['count'] += df[Candidate.PreferredLocation.name].str.count('|'.join(keywords[DT.PreferredLocation.value['name']]),
                                                                        flags=re.IGNORECASE)


        # Received DataType: PreferredEmploymentType <> Column: PreferredEmploymentType | points= 1
        if keywords.get(DT.PreferredEmploymentType.value['name']):
            df['count'] += df[Candidate.PreferredEmploymentType.name].str.count('|'.join(keywords[DT.PreferredEmploymentType.value['name']]),
                                                                                flags=re.IGNORECASE)


        # Received DataType: OfferedJobTitle <> Column: DesiredPosition | points= 1
        if keywords.get(DT.OfferedJobTitle.value['name']):
            df['count'] += df[Candidate.DesiredPosition.name].str.count('|'.join(keywords[DT.OfferedJobTitle.value['name']]),
                                                                                flags=re.IGNORECASE)


        # Received DataType: JobDescription <> Column: DesiredPosition | points= 1
        if keywords.get(DT.JobDescription.value['name']):
            df['count'] += df[Candidate.DesiredPosition.name].str.count('|'.join(keywords[DT.JobDescription.value['name']]),
                                                                        flags=re.IGNORECASE)

        print(df)

        topResults = json.loads(df[df['count']>0].nlargest(session.get('showTop', 2), 'count')
                                .to_json(orient='records'))
        data = []
        for tr in topResults:
            data.append({
                "title": tr[Candidate.DesiredPosition.name],
                "description": tr[Candidate.CandidateSkills.name],
                "tail": "Salary: " + str(tr[Candidate.DesiredSalary.name])
            })
        print(data)
        return Callback(True, '', data)

    except Exception as exc:
        print("scanCandidates() ERROR: ", exc)
        return Callback(False, 'Error while search the database for matches!')



def scanJobs(session, dbIDs):
    try:

        df = pandas.read_sql(db.session.query(Job).filter(Job.DatabaseID.in_(dbIDs)).statement,
                             con=db.session.bind)


        keywords = session['keywordsByDataType']
        df['count'] = 0 # add column for tracking score
        # Delete sensitive columns e.g. candidate name
        df.drop(['ID'], axis=1, inplace=True)

        # Numbers
        # Received DataType: DesiredSalary <> Column: DesiredSalary | points=3
        if keywords.get(DT.DesiredSalary.value['name']):
            df.loc[df[Job.Salary.name] >= float(keywords[DT.DesiredSalary.value['name']][-1]), 'count'] += 3


        # Received DataType: DesiredPayRate <> Column: PayRate | points=3
        if keywords.get(DT.DesiredPayRate.value['name']):
            df.loc[df[Job.PayRate.name] >= float(keywords[DT.DesiredPayRate.value['name']][-1]), 'count'] += 3

        #  =======================================

        # Received DataType: DesiredPosition <> Column: DesiredPosition | points= 1
        if keywords.get(DT.DesiredPosition.value['name']):
            df['count'] += df[Job.Description.name].str.count('|'.join(keywords[DT.DesiredPosition.value['name']]),
                                                                        flags=re.IGNORECASE)


        # Received DataType: CandidateSkills <> Column: EssentialSkills | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Job.EssentialSkills.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                        flags=re.IGNORECASE)

        # Received DataType: CandidateSkills <> Column: Description | points= 1
        if keywords.get(DT.CandidateSkills.value['name']):
            df['count'] += df[Job.Description.name].str.count('|'.join(keywords[DT.CandidateSkills.value['name']]),
                                                                  flags=re.IGNORECASE)


        # Received DataType: PreferredLocation <> Column: Location | points= 1
        if keywords.get(DT.PreferredLocation.value['name']):
            df['count'] += df[Job.Location.name].str.count('|'.join(keywords[DT.PreferredLocation.value['name']]),
                                                                          flags=re.IGNORECASE)


        # Received DataType: PreferredEmploymentType <> Column: EmploymentType | points= 1
        if keywords.get(DT.PreferredEmploymentType.value['name']):
            df['count'] += df[Job.EmploymentType.name].str.count('|'.join(keywords[DT.PreferredEmploymentType.value['name']]),
                                                                                flags=re.IGNORECASE)


        # Received DataType: OfferedJobTitle <> Column: Title | points= 1
        if keywords.get(DT.OfferedJobTitle.value['name']):
            df['count'] += df[Job.Title.name].str.count('|'.join(keywords[DT.OfferedJobTitle.value['name']]),
                                                                        flags=re.IGNORECASE)

        # Received DataType: OfferedJobTitle <> Column: Description | points= 1
        if keywords.get(DT.OfferedJobTitle.value['name']):
            df['count'] += df[Job.Description.name].str.count('|'.join(keywords[DT.OfferedJobTitle.value['name']]),
                                                              flags=re.IGNORECASE)


        # Received DataType: JobDescription <> Column: Description | points= 1
        if keywords.get(DT.JobDescription.value['name']):
            df['count'] += df[Job.Description.name].str.count('|'.join(keywords[DT.JobDescription.value['name']]),
                                                                        flags=re.IGNORECASE)

        topResults = json.loads(df[df['count']>0].nlargest(session.get('showTop', 0), 'count')
                                .to_json(orient='records'))
        data = []
        for tr in topResults:
            data.append({
                "title": tr[Job.Title.name],
                "description": tr[Job.Description.name],
                "tail": "Salary: " + str(tr[Job.Salary.name])
            })
        print(data)
        return Callback(True, '', data)

    except Exception as exc:
        print("scanJobs() ERROR: ", exc)
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
