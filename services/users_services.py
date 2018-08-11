from models import User
from .db_services import _safeCommit
from models import db, User, Company, Role
from utilties import helpers


# class UserServices:

def getByID(id):
    return db.session.query(User).get(id)

def getByEmail(email):
    return db.session.query(User).filter(User.Email == email).first()

def getAll():
    return db.session.query(User)

def addUser(user: User):

    # companyObject = Company.query.get(1)
    # roleObject = Role.query.filter(Role.Name.like("Admin")).first()

    # user = User(Firstname=firstname, Surname=surname, Email=email, Password=helpers.hashPass(password),
    #             Company=company, Role=role)
    db.session.add(user)

    return _safeCommit()

def deleteByEmail(email):

    db.session.query(User).filter(User.Email == email).delete()

    return _safeCommit()