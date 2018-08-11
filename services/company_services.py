import sqlalchemy.exc

from .db_services import _safeCommit
from models import db, Company, User, Role


def getByID(id):
    return db.session.query(Company).get(id)

def getAll():
    return db.session.query(Company)


def createCompany(name, size, phoneNumber, url):

    try:
        company = Company(Name=name, Size=size, PhoneNumber=phoneNumber, URL=url)
        db.session.add(company)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return None

    return company


def removeByName(name):

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return False

    return True