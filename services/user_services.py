import sqlalchemy.exc

from models import db, Callback, User, Company, Role
from utilties import helpers
from flask import session


def getByID(id) -> Callback:
    try:
        return Callback(True,
                        'User with ID ' + str(id) + ' was successfully retrieved',
                        db.session.query(User).get(id))
    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        return Callback(False,
                        'User with ID ' + str(id) + ' does not exist')


def getByEmail(email) -> User or None:
    try:
        return Callback(True,
                        'User with email ' + email + ' was successfully retrieved.',
                        db.session.query(User).filter(User.Email == email).first())
    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        return Callback(False,
                        'User with email ' + email + ' does not exist.')


def getAllByCompanyID(companyID) -> Callback:
    try:
        return Callback(True,
                        'Users with company ID ' + str(companyID) + ' were successfully retrieved.',
                        db.session.query(User).filter(User.CompanyID == companyID).all())
    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')


def create(firstname, surname, email, password, company: Company, role: Role, verified=False) -> User or None:
    try:
        # Create a new user with its associated company and role
        user = User(Firstname=firstname, Surname=surname, Email=email, Verified=verified,
                    Password=helpers.hashPass(password), Company=company,
                    Role=role)
        db.session.add(user)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return Callback(False, 'Sorry, Could not create the user.')
    return Callback(True, 'User has been created successfully!')


def removeByEmail(email) -> Callback:

    try:
     db.session.query(User).filter(User.Email == email).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return Callback(False, 'User with email ' + email + " could not be removed.")

    db.session.commit()
    return Callback(True, 'User with email ' + email + " has been removed successfully.")


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



