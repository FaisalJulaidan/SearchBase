from .db_services import _safeCommit
from models import db, Company, User, Role


# class CompanyServices:

def getByID(id):
    return db.session.query(Company).get(id)

def getAll():
    return db.session.query(Company)


def addCompany(company: Company):

    # company = Company(Name=name, Size=size, PhoneNumber=phoneNumber, URL=url)
    db.session.add(company)

    return _safeCommit()


def deleteByName(name):

    db.session.query(Company).filter(Company.Name == name).delete()

    return _safeCommit()