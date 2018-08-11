import sqlalchemy.exc

from models import User
from .db_services import _safeCommit
from models import db, User, Company, Role
from utilties import helpers


def getByID(id):
    return db.session.query(User).get(id)


def getByEmail(email):
    return db.session.query(User).filter(User.Email == email).first()


def getAll():
    return db.session.query(User)


def createUser(firstname, surname, email, password, company: Company, role: Role):

    try:
        # Create a new user with its associated company and role
        user = User(Firstname=firstname, Surname=surname, Email=email,
                    Password=helpers.hashPass(password),Company=company,
                    Role=role)

        db.session.add(user)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return None

    return user


def removeByEmail(email):

    try:
     db.session.query(User).filter(User.Email == email).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return False

    return True
