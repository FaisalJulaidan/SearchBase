import sqlalchemy.exc

from services import mail_services, company_services
from models import db, Callback, User, Company, Role, UserSettings
from utilties import helpers
from sqlalchemy.sql import exists, func





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


def getAllByCompanyID_safe(companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User.ID,
                                  User.Firstname,
                                  User.Surname,
                                  User.Email,
                                  User.LastAccess)\
            .filter(User.CompanyID == companyID).all()
        if not result: raise Exception

        return Callback(True,
                        'Users with company ID ' + str(companyID) + ' were successfully retrieved.',
                        result)
    except Exception as exc:
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')


def create(firstname, surname, email, password, phone, company: Company, role: Role, verified=False) -> Callback:
    try:
        # Create a new user with its associated company and role
        newUser = User(Firstname=firstname, Surname=surname, Email=email, Verified=verified,
                    Password=helpers.hashPass(password), PhoneNumber=phone, Company=company,
                    Role=role)
        db.session.add(newUser)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')
    # Save
    db.session.commit()
    return Callback(True, 'User has been created successfully!', newUser)


def updateAsOwner(userID, firstname, surname, email, role: Role) -> Callback:
    try:
        # Create a new user with its associated company and role
        user_callback: Callback = getByID(userID)
        if not user_callback.Success:
            return Callback(False, "Could not find user's records")
        user: User = user_callback.Data

        # Update user
        user.Firstname = firstname
        user.Surname = surname
        user.Email = email
        user.Role = role

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')

    # Save
    db.session.commit()
    return Callback(True, 'User has been edited successfully!')


def changePasswordByID(userID, newPassword, currentPassword=None):
    user_callback : Callback = getByID(userID)
    if not user_callback.Success:
        return Callback(False, "Could not find user's records")

    if currentPassword is not None:
        if not helpers.hashPass(currentPassword, user_callback.Data.Password) == user_callback.Data.Password:
            return Callback(False, "Incorrect Password.")

    user_callback.Data.Password = helpers.hashPass(newPassword)
    db.session.commit()

    return Callback(True, "Password has been changed.")


def changePasswordByEmail(userEmail, newPassword, currentPassword=None):
    user_callback : Callback = getByEmail(userEmail)
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
        if not db.session.query(exists().where(User.Email == email)).scalar():
            return Callback(False, "The user with email '" + str(email) + "' doesn't exist")
        db.session.query(User).filter(User.Email == email).delete()
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'User with email ' + email + " could not be removed.")
    # Save
    db.session.commit()
    return Callback(True, 'User with email ' + email + " has been removed successfully.")


def removeByID(id) -> Callback:

    try:
        if not db.session.query(exists().where(User.ID == id)).scalar():
            return Callback(False, "the user with id '" + str(id) + "' doesn't exist")
        db.session.query(User).filter(User.ID == id).delete()

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'User with id ' + str(id) + " could not be removed.")
    # Save
    db.session.commit()
    return Callback(True, 'User with id ' + str(id) + " has been removed successfully.")


def verifyByEmail(email: str):

    try:
        user = db.session.query(User).filter(User.Email == email).update({"Verified": True})
        if not user: raise Exception
        
        #send us mail
        result = db.session.query(User).filter(User.Email == email).first()
        company_callback = company_services.getByID(result.CompanyID)
        companyName = "Error"
        if company_callback : companyName = company_callback.Data.Name
        mail_callback : Callback = mail_services.sendNewUserHasRegistered(result.Firstname + result.Surname, result.Email, companyName, result.PhoneNumber)
        if not mail_callback.Success: print("Could not send signed up user email")

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

def createUpdateUserSettings(userID, trackingData, techSupport, accountSpecialist):
    try:
        result = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()
        if not result: 
            newUser = UserSettings(ID=userID, TrackingData=trackingData, TechnicalSupport=techSupport, AccountSpecialist=accountSpecialist)
            db.session.add(newUser)
        else:
            result.TrackingData = trackingData
            result.TechnicalSupport = techSupport
            result.AccountSpecialist = accountSpecialist

        db.session.commit()
        return Callback(True,
                        'User settings were successfully updated.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        return Callback(False,
                        'User settings could not be updated.')

def getUserSettings(userID):
    try:
        result = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()

        return Callback(True,
                        'User settings were successfully retrieved.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        return Callback(False,
                        'User settings for this user does not exist.')