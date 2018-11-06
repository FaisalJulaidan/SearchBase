import sqlalchemy.exc

from services import mail_services, company_services, role_services
from models import db, Callback, User, Company, Role, UserSettings
from utilities import helpers
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
        db.session.rollback()
        return Callback(False,
                        'User with ID ' + str(id) + ' does not exist')

    # finally:
       # db.session.close()

def getByEmail(email) -> User or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.Email == email.lower()).first()
        if not result: raise Exception

        return Callback(True,
                        'User with email ' + email + ' was successfully retrieved.',
                        result)
    except Exception as exc:
        db.session.rollback()
        return Callback(False,
                        'User with email ' + email + ' does not exist.')

    # finally:
       # db.session.close()

def getAllByCompanyID(companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.CompanyID == companyID).all()
        if not result: raise Exception

        return Callback(True,
                        'Users with company ID ' + str(companyID) + ' were successfully retrieved.',
                        result)
    except Exception as exc:
        db.session.rollback()
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')

    # finally:
       # db.session.close()

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
        db.session.rollback()
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')

    # finally:
       # db.session.close()

def create(firstname, surname, email, password, phone, company: Company, role: Role, verified=False) -> Callback:
    try:
        # Create a new user with its associated company and role
        newUser = User(Firstname=firstname, Surname=surname, Email=email.lower(), Verified=verified,
                    Password=password, PhoneNumber=phone, Company=company,
                    Role=role)
        db.session.add(newUser)

        db.session.commit()
        return Callback(True, 'User has been created successfully!', newUser)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')
    # finally:
       # db.session.close()


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
        user.Email = email.lower()
        user.Role = role

        db.session.commit()
        return Callback(True, 'User has been edited successfully!')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')

    # finally:
       # db.session.close()
    # Save


def changePasswordByID(userID, newPassword, currentPassword=None):
    try:
        user_callback : Callback = getByID(userID)
        if not user_callback.Success:
            return Callback(False, "Could not find user's records")

        if currentPassword is not None:
            if not currentPassword == user_callback.Data.Password:
                return Callback(False, "Incorrect Password.")

        user_callback.Data.Password = newPassword
        db.session.commit()

        return Callback(True, "Password has been changed.")

    except Exception as exc:
        print("user_services.changePasswordByID() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Error in updating password")

    # finally:
       # db.session.close()

def changePasswordByEmail(userEmail, newPassword, currentPassword=None):
    try:
        user_callback : Callback = getByEmail(userEmail.lower())
        if not user_callback.Success:
            return Callback(False, "Could not find user's records")

        if currentPassword is not None:
            if not currentPassword == user_callback.Data.Password:
                return Callback(False, "Incorrect Password.")

        user_callback.Data.Password = newPassword
        db.session.commit()

        return Callback(True, "Password has been changed.")

    except Exception as exc:
        print("user_services.changePasswordByEmail() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Error in changing password")

    # finally:
       # db.session.close()

def removeByEmail(email) -> Callback:

    try:
        if not db.session.query(exists().where(User.Email == email.lower())).scalar():
            return Callback(False, "The user with email '" + str(email) + "' doesn't exist")
        db.session.query(User).filter(User.Email == email).delete()

        db.session.commit()
        return Callback(True, 'User with email ' + email + " has been removed successfully.")

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'User with email ' + email + " could not be removed.")

    # finally:
       # db.session.close()


def removeByID(id) -> Callback:

    try:
        if not db.session.query(exists().where(User.ID == id)).scalar():
            return Callback(False, "the user with id '" + str(id) + "' doesn't exist")
        db.session.query(User).filter(User.ID == id).delete()

        db.session.commit()
        return Callback(True, 'User with id ' + str(id) + " has been removed successfully.")

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'User with id ' + str(id) + " could not be removed.")

    # finally:
       # db.session.close()


def verifyByEmail(email: str):

    try:
        user = db.session.query(User).filter(User.Email == email.lower()).update({"Verified": True})
        if not user: raise Exception

        #send us mail
        user = db.session.query(User).filter(User.Email == email.lower()).first()
        company_callback = company_services.getByID(user.CompanyID)
        companyName = "Error"
        if company_callback : companyName = company_callback.Data.Name
        mail_callback : Callback = mail_services.sendNewUserHasRegistered(user.Firstname + user.Surname, user.Email, companyName, user.PhoneNumber)
        if not mail_callback.Success: print("Could not send signed up user email")

        db.session.commit()
        return Callback(True, 'Account has been verified successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not verify account with email  ' + email)

    # finally:
       # db.session.close()


def updateSubID(email, subID: str):

    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"SubID": subID})

        db.session.commit()
        return Callback(True, 'SubID is updated successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)

    # finally:
       # db.session.close()


def updateStripeID(email, cusID: str):

    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"StripeID": (cusID)})

        db.session.commit()
        return Callback(True, 'StripeID is updated successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)

    # finally:
       # db.session.close()

def createUpdateUserSettings(userID, trackingData, techSupport, accountSpecialist, notifications):
    try:
        result = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()
        if not result:
            newUser = UserSettings(ID=userID, TrackingData=trackingData, TechnicalSupport=techSupport, AccountSpecialist=accountSpecialist, UserInputNotifications=notifications)
            db.session.add(newUser)
        else:
            result.TrackingData = trackingData
            result.TechnicalSupport = techSupport
            result.AccountSpecialist = accountSpecialist
            result.UserInputNotifications = notifications

        db.session.commit()
        return Callback(True,
                        'User settings were successfully updated.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        db.session.rollback()
        return Callback(False,
                        'User settings could not be updated.')

    # finally:
       # db.session.close()

def getAllUserSettings():
    try:
        # Get result and check if None then raise exception
        result = db.session.query(UserSettings).all()

        return Callback(True,
                        'Records successfully retrieved',
                        result)
    except Exception as exc:
        db.session.rollback()
        return Callback(False, 'Error in getting records')

    # finally:
       # db.session.close()

def getUserSettings(userID):
    try:
        result = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()

        return Callback(True,
                        'User settings were successfully retrieved.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        db.session.rollback()
        return Callback(False,
                        'User settings for this user does not exist.')

    # finally:
       # db.session.close()

def getRolePermissions(userID):
    try:
        user_callback : Callback = getByID(userID)
        if not user_callback.Success: raise Exception("User not found")

        role_callback : Callback = role_services.getByID(user_callback.Data.RoleID)
        if not user_callback.Success: raise Exception("Role not found")

        return Callback(True, 'User Permissions have been retrieved', role_callback.Data)
    except Exception as exc:
        print("user_services.getRolePermissions() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Coult not retrieve user\'s permissions.')

    # finally:
       # db.session.close()
