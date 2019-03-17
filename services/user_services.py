from sqlalchemy.sql import exists

from models import db, Callback, User, Company, Role, UserSettings
from services import mail_services, company_services, newsletter_services
from utilities import helpers
from sqlalchemy import and_


def create(firstname, surname, email, password, phone, company: Company, role: Role, verified=False) -> Callback:
    try:
        # Create a new user with its associated company and role
        newUser: User = User(Firstname=firstname, Surname=surname, Email=email.lower(), Verified=verified,
                             Password=password, PhoneNumber=phone, Company=company,
                             Role=role)
        db.session.add(newUser)
        db.session.flush()

        # Create user settings with its default values
        newUserSettings = UserSettings(ID=newUser.ID)
        db.session.add(newUserSettings)

        db.session.commit()
        return Callback(True, 'User has been created successfully!', newUser)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')
    # finally:
    # db.session.close()


# ----- Getters ----- #

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


def getAllByCompanyIDWithEnabledNotifications(companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User)\
            .filter(and_(User.CompanyID == companyID, User.Settings.UserInputNotifications)).all()
        if not result: raise Exception

        return Callback(True,
                        'Users with company ID ' + str(companyID) + ' were successfully retrieved.',
                        result)
    except Exception as exc:
        db.session.rollback()
        return Callback(False,
                        'Users with company ID ' + str(companyID) + ' could not be retrieved.')


def getProfile(userID):
    try:
        result: UserSettings = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()
        if not result: raise Exception

        profile = {
            'user': helpers.getDictFromSQLAlchemyObj(result.User),
            'company': helpers.getDictFromSQLAlchemyObj(result.User.Company),
            'userSettings': helpers.getDictFromSQLAlchemyObj(result),
            'newsletters': newsletter_services.checkForNewsletter(result.User.Email).Success
        }

        # For security purposes IMPORTANT!
        del profile['user']['ID']
        del profile['user']['CompanyID']
        del profile['user']['RoleID']
        del profile['company']['ID']
        del profile['company']['StripeID']
        del profile['company']['SubID']

        return Callback(True, 'User settings were successfully retrieved.', profile)
    except Exception as exc:
        print("user_services.getProfile() ERROR: ", exc)
        return Callback(False, 'User settings for this user does not exist.')


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


def getAllUserSettingsWithEnabled(USProperty):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(UserSettings).filter(getattr(UserSettings, USProperty)).all()

        return Callback(True,
                        'Records successfully retrieved',
                        result)
    except Exception as exc:
        db.session.rollback()
        print("user_services.getAllUserSettingsWithEnabled() ERROR: ", str(exc))
        return Callback(False, 'Error in getting records')


def getUserSettings(userID):
    try:
        result = db.session.query(UserSettings).filter(UserSettings.ID == userID).first()
        if not result: raise Exception
        return Callback(True,
                        'User settings were successfully retrieved.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        db.session.rollback()
        return Callback(False,
                        'User settings for this user does not exist.')

# ----- Updaters ----- #
def updateAsOwner(userID, firstname, surname, email, role: Role) -> Callback:
    try:
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


def updateUserSettings(userID, trackingData, techSupport, accountSpecialist, notifications):
    try:

        result = db.session.query(UserSettings).filter(UserSettings.ID == userID)\
            .update({
              'TrackingData': trackingData,
              'TechnicalSupport': techSupport,
              'AccountSpecialist': accountSpecialist,
              "UserInputNotifications": notifications})

        db.session.commit()
        return Callback(True,
                        'User settings were successfully updated.',
                        result)
    except Exception as exc:
        print("user_services.getUserSettings() ERROR: ", exc)
        db.session.rollback()
        return Callback(False,
                        'User settings could not be updated.')


def updateSubID(email, subID: str):
    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"SubID": subID})

        db.session.commit()
        return Callback(True, 'SubID is updated successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)


def updateStripeID(email, cusID: str):
    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"StripeID": (cusID)})

        db.session.commit()
        return Callback(True, 'StripeID is updated successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)


def updateUser(firstname, surname, newEmail, userID):
    try:
        callback: Callback = getByID(userID)
        if not callback: return Callback(False, "Could not find user")

        callback.Data.Firstname = firstname
        callback.Data.Surname = surname
        callback.Data.Email = newEmail

        db.session.commit()

        return Callback(True, "User has been updated")
    except Exception as exc:
        print("profile_services.updateUser() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "User could not be updated")



def changePasswordByID(userID, newPassword, oldPassword=None):
    try:
        result = db.session.query(User).filter(User.ID == userID).first()
        if not result:
            return Callback(False, "Could not find user's records")

        if oldPassword is not None:
            if not oldPassword == result:
                return Callback(False, "Old Password is incorrect")

        result.Password = newPassword
        db.session.commit()
        return Callback(True, "Password has been changed.")

    except Exception as exc:
        print("user_services.changePasswordByID() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Error in updating password")


def changePasswordByEmail(userEmail, newPassword, currentPassword=None):
    try:
        user_callback: Callback = getByEmail(userEmail.lower())
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


def verifyByEmail(email: str):
    try:
        user = db.session.query(User).filter(User.Email == email.lower()).update({"Verified": True})
        if not user: raise Exception

        # send us mail
        user = db.session.query(User).filter(User.Email == email.lower()).first()
        company_callback = company_services.getByID(user.CompanyID)
        companyName = "Error"
        if company_callback: companyName = company_callback.Data.Name
        mail_callback: Callback = mail_services.sendNewUserHasRegistered(user.Firstname + user.Surname, user.Email,
                                                                         companyName, user.PhoneNumber)
        if not mail_callback.Success: print("Could not send signed up user email")

        db.session.commit()
        return Callback(True, 'Account has been verified successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not verify account with email  ' + email)


# ----- Removers ----- #

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
