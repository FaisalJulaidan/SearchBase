import sqlalchemy.exc

from models import db, Callback, User, Company, Role
from utilties import helpers
from flask import session


def getByID(id) -> Callback:
    try:
        if id:
            # Get result and check if None then raise exception
            result = db.session.query(User).get(id)
            if not result: raise Exception

            return Callback(True,
                            'User with ID ' + str(id) + ' was successfully retrieved',
                            result)
        else:
            raise Exception
    except Exception as exc:
        return Callback(False,
                        'User with ID ' + str(id) + ' does not exist')


def getByEmail(email) -> User or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.Email == email).first()
        if not result: raise Exception

        return Callback(True,
                        'User with email ' + email + ' was successfully retrieved.',
                        result)
    except Exception as exc:
        return Callback(False,
                        'User with email ' + email + ' does not exist.')


def getAllByCompanyID(companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.CompanyID == companyID).all()
        if not result: raise Exception

        return Callback(True,
                        'Users with company ID ' + str(companyID) + ' were successfully retrieved.',
                        result)
    except Exception as exc:
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')


def create(firstname, surname, email, password, company: Company, role: Role, verified=False) -> User or None:
    try:
        # Create a new user with its associated company and role
        user = User(Firstname=firstname, Surname=surname, Email=email, Verified=verified,
                    Password=helpers.hashPass(password), Company=company,
                    Role=role)
        db.session.add(user)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')
    # Save
    db.session.commit()
    return Callback(True, 'User has been created successfully!')

def changePasswordByID(userID, newPassword, currentPassword=None):
    user_callback : Callback = user_services.getByID(userID)
    if not user_callback.Success:
        return Callback(False, "Could not find user's records")

    if currentPassword is not None:
        if not helpers.hashPass(currentPassword, user_callback.Data.Password) == user_callback.Data.Password:
            return Callback(False, "Incorrect Password.")

    user_callback.Data.Password = helpers.hashPass(newPassword)
    db.session.commit()

    return Callback(True, "Password has been changed.")

def changePasswordByEmail(userEmail, newPassword, currentPassword=None):
    user_callback : Callback = user_services.getByEmail(userEmail)
    if not user_callback.Success:
        return Callback(False, "Could not find user's records")

    if currentPassword is not None:
        if not helpers.hashPass(currentPassword, user_callback.Data.Password) == user_callback.Data.Password:
            return Callback(False, "Incorrect Password.")

    user_callback.Data.Password = helpers.hashPass(newPassword)
    db.session.commit()

    return Callback(True, "Password has been changed.")

def removeByEmail(email) -> Callback:

    try:
     db.session.query(User).filter(User.Email == email).delete()

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'User with email ' + email + " could not be removed.")
    # Save
    db.session.commit()
    return Callback(True, 'User with email ' + email + " has been removed successfully.")


def verifyByEmail(email: str):

    try:
        db.session.query(User).filter(User.Email == email).update({"Verified": True})

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not verify account with email  ' + email)
    # Save
    db.session.commit()
    return Callback(True, 'Account has been verified successfully')



def updateSubID(email, subID: str):

    try:
        db.session.query(User).filter(User.Email == email).update({"SubID": subID})

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)
    # Save
    db.session.commit()
    return Callback(True, 'SubID is updated successfully')


def updateStripeID(email, cusID: str):

    try:
        db.session.query(User).filter(User.Email == email).update({"StripeID": (cusID)})

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)
    # Save
    db.session.commit()
    return Callback(True, 'StripeID is updated successfully')



