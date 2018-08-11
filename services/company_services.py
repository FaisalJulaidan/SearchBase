import sqlalchemy.exc

from .db_services import _safeCommit
from models import db, Company, User, Role


def getByID(id) -> Company or None:
    return db.session.query(Company).get(id)

def getAll() -> list:
    return db.session.query(Company)


def createCompany(name, size, phoneNumber, url) -> Company or None:

    try:
        company = Company(Name=name, Size=size, PhoneNumber=phoneNumber, URL=url)
        db.session.add(company)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return None

    return company


def removeByName(name) -> bool:

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return False

    return True