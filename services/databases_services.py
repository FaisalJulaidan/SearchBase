from models import db, Callback, Database, Candidate, Client, Company, Assistant, Job
from typing import List
import pandas
import re
import enums

from sqlalchemy import and_
from enums import  DatabaseType, DataType as DT

def fetchDatabase(id, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        database: Database = db.session.query(Database)\
            .filter(and_(Database.CompanyID == companyID, Database.ID == id)).first()
        if not database: raise Exception

        if database.Type == DatabaseType.Clients:
            print('fetch from client table')
            return getAllClients(database.ID)

        elif database.Type == DatabaseType.Candidates:
            print('fetch from candidate table')
            return getAllCandidates(database.ID)

        # Reaching to this point means the type of the db is not supported
        return Callback(False, "No database found!")

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not fetch the database.')
    # finally:
        # db.session.close()


# ----- Getters ----- #
def getDatabasesList(companyID: int) -> Callback:
    try:
        databases: List[Database] = db.session.query(Database) \
            .filter(and_(Database.CompanyID == companyID))
        return Callback(True, "Databases list is here", databases)

    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not fetch the databases list.')
    # finally:
    # db.session.close()



def getAllCandidates(dbID) -> Callback:
    try:
        candidates: List[Candidate] = db.session.query(Candidate).filter(Database.ID == dbID).all()
        if not candidates: raise Exception
        return Callback(True, 'Candidates was successfully retrieved.', candidates)

    except Exception as exc:
        db.session.rollback()
        print("fetchCandidates() ERROR: ", exc)
        return Callback(False, 'Candidates could not be retrieved.')

    # finally:
    # db.session.close()


def getAllClients(dbID) -> Callback:
    try:
        clients: List[Client] = db.session.query(Client).filter(Database.ID == dbID).all()
        if not clients: raise Exception
        return Callback(True, 'Candidates was successfully retrieved.', clients)

    except Exception as exc:
        db.session.rollback()
        print("fetchCandidates() ERROR: ", exc)
        return Callback(False, 'Clients could not be retrieved.')

    # finally:
    # db.session.close()

# ----- Scanners (Pandas) ----- #
def scanCandidates(company: Company, databaseName, keywords: dict):
    try:
        database: Database = db.session.query(Database) \
            .filter(and_(Database.CompanyID == company.ID, Database.Name == databaseName)).first()
        if not database: raise Exception


        # Data analysis using Pandas library

        df = pandas.read_sql("SELECT * FROM Candidate WHERE DatabaseID=1", con=db.session.bind)

        df['count'] = 0
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




        print(df.nlargest(2, 'count'))
        print(df.nlargest(2, 'count').to_json(orient='records'))

    except Exception as exc:
        print("scanCandidates() ERROR: ", exc)
        return Callback(False, 'Error while search the database for matches!')



def getOptions() -> Callback:
    options =  {
        'types': [a.value for a in enums.DatabaseType ],
        enums.DatabaseType.Candidates.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                             for c in Candidate.__table__.columns],
        enums.DatabaseType.Jobs.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                       for c in Job.__table__.columns],
    }
    return Callback(True, '', options)