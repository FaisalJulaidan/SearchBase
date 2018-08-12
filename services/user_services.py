import sqlalchemy.exc

from models import User
from .db_services import _safeCommit
from models import db, Callback, User, Company, Role
from utilties import helpers


def getByID(id) -> User or None:
    return db.session.query(User).get(id)


def getByEmail(email) -> User or None:
    return db.session.query(User).filter(User.Email == email).first()


def getAll() -> list:
    return db.session.query(User)


def create(firstname, surname, email, password, company: Company, role: Role, verified=False) -> User or None:

    try:
        # Create a new user with its associated company and role
        user = User(Firstname=firstname, Surname=surname, Email=email, Verified=verified,
                    Password=helpers.hashPass(password), Company=company,
                    Role=role)
        db.session.add(user)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return None

    db.session.commit()
    return user


def updateSubID(email, subID: str):

    try:
        db.session.query(User).filter(User.Email == email).update({"SubID": subID})
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)

    db.session.commit()
    return Callback(True, 'SubID is updated successfully')


def updateStripeID(email, cusID: str):

    try:
        db.session.query(User).filter(User.Email == email).update({"StripeID": (cusID)})
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)

    db.session.commit()
    return Callback(True, 'StripeID is updated successfully')



def removeByEmail(email) -> Callback:

    try:
     db.session.query(User).filter(User.Email == email).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return Callback(False, 'User with email ' + email + " could not be removed.")

    db.session.commit()
    return Callback(True, 'User with email ' + email + " has been removed successfully.")
