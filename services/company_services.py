import sqlalchemy.exc

from .db_services import _safeCommit
from models import db, Callback, Company, User, Role
from flask import session


def getByID(id) -> Company or None:
    return db.session.query(Company).get(id)

def getAll() -> list:
    return db.session.query(Company)


def create(name, size, phoneNumber, url) -> Company or None:

    try:
        company = Company(Name=name, Size=size, PhoneNumber=phoneNumber, URL=url)
        db.session.add(company)
    except Exception as exc:
        print(exc)
        return None

    return company


def removeByName(name) -> bool:

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
    except Exception as exc:
        print(exc)
        return False

    return True

def getByEmail(email) -> Callback:

    result = db.session.query(User).filter(User.Email == email).first()
    if not result: return Callback(False, 'Could not retrieve user\'s data')

    result = db.session.query(Company).filter(Company.ID == result.ID).first()
    if not result: return Callback(False, 'Could not retrieve company\'s data.')
    
    return Callback(True, 'Company was successfully retrieved.', result)

def getByCompanyID(id) -> Callback:

    result = db.session.query(Company).filter(Company.ID == id).first()
    if not result: return Callback(False, 'Could not retrieve company\'s data.')
    
    return Callback(True, 'Company was successfully retrieved.', result)