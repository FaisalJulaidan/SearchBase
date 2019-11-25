from sqlalchemy.sql import exists
from sqlalchemy.orm import joinedload
from models import db, Callback, User, Company, Role
from services import mail_services, company_services, newsletter_services
from utilities import helpers
from sqlalchemy import and_

def getTimezone(id) -> Callback:
    try:
        user: User = db.session.query(User).filter(User.ID == id).first()

        return Callback(True, "Gathered timezone information", user.TimeZone)
    except Exception as exc:
        return Callback(False, "Failed to gather timezone information")


def create(firstname, surname, email, password, phone, companyID: int, roleID: int, timeZone: str, verified=False, ) -> Callback:
    try:

        # Create a new user with its associated company and role
        newUser: User = User(Firstname=firstname, Surname=surname, Email=email.lower(), Verified=verified,
                             Password=password, PhoneNumber=phone, CompanyID=companyID, RoleID=roleID,
                             ChatbotNotifications=True, TimeZone=timeZone)
        db.session.add(newUser)
        db.session.commit()
        return Callback(True, 'User has been created successfully!', newUser)

    except Exception as exc:
        helpers.logError("user_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')


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
        helpers.logError("user_services.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False,
                        'User with ID ' + str(id) + ' does not exist')



def getByEmail(email) -> User or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.Email == email.lower()).first()
        if not result: raise Exception
        return Callback(True,'User with email ' + email + ' was successfully retrieved.', result)

    except Exception as exc:
        return Callback(False, 'User with email ' + email + ' does not exist.')


# this used to make sure the edited user is under this company
def getByIDAndCompanyID(userID, companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(and_(User.ID == userID,User.CompanyID == companyID)).first()
        if not result: raise Exception("User does not exist")

        return Callback(True,'Users  retrieved successfully.', result)
    except Exception as exc:
        helpers.logError("user_services.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Users could not be retrieved.')

def getAllByCompanyID(companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(User.CompanyID == companyID).all()

        return Callback(True,'Users  retrieved successfully.', result)
    except Exception as exc:
        helpers.logError("user_services.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Users could not be retrieved.')


def getAllByCompanyIDWithEnabledNotifications(companyID, eager: bool = False) -> Callback:
    try:
        # Get result and check if None then raise exception
        query = db.session.query(User) \
            .filter(and_(User.CompanyID == companyID, User.ChatbotNotifications, User.Verified))
        if eager:
            query.options(joinedload("Company").joinedload("StoredFile").joinedload("StoredFileInfo"))


        result = query.all()

        return Callback(True, 'Users were successfully retrieved.', result)
    except Exception as exc:
        helpers.logError("user_services.getAllByCompanyIDWithEnabledNotifications(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Users could not be retrieved.')


# takes in attribute name for Users ex. Users.
def getAllUsersWithEnabled(USProperty):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(User).filter(getattr(User, USProperty)).all()

        return Callback(True,
                        'Records successfully retrieved',
                        result)
    except Exception as exc:
        helpers.logError("user_services.getAllUsersWithEnabled(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in getting records')


def getProfile(userID):
    try:
        result: User = db.session.query(User).filter(User.ID == userID).options(joinedload('Company').joinedload('StoredFile').joinedload('StoredFileInfo')).first()
        if not result:
            raise Exception
        profile = {
            'user': helpers.getDictFromSQLAlchemyObj(result),
            'company': helpers.getDictFromSQLAlchemyObj(result.Company, True),
            'newsletters': newsletter_services.check(result.Email).Success
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
        helpers.logError("user_services.getProfile(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'User settings for this user does not exist.')


def getOwnersOfAssistants(assistants) -> Callback:
    try:
        if not assistants:
            raise Exception

        for assistant in assistants:
            result = db.session.query(User)\
                .filter(User.ID == assistant["OwnerID"]).first()

            assistant.pop("OwnerID", None)
            if not result:
                assistant["Owners"] = []
                continue

            assistant["Owners"] = [{"id": result.ID, "name": result.Firstname + " " + result.Surname}]

        return Callback(True, "Got all assistants  successfully.", assistants)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get the owners.')


# ----- Updaters ----- #
def updateUserSettings(userID, trackingData, techSupport, accountSpecialist, notifications):
    try:

        result = db.session.query(User).filter(User.ID == userID) \
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
        helpers.logError("user_services.updateUserSettings(): " + str(exc))
        db.session.rollback()
        return Callback(False,
                        'User settings could not be updated.')


def updateSubID(email, subID: str):
    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"SubID": subID})

        db.session.commit()
        return Callback(True, 'SubID is updated successfully')

    except Exception as exc:
        helpers.logError("user_services.updateSubID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)


def updateStripeID(email, cusID: str):
    try:
        db.session.query(User).filter(User.Email == email.lower()).update({"StripeID": (cusID)})

        db.session.commit()
        return Callback(True, 'StripeID is updated successfully')

    except Exception as exc:
        helpers.logError("user_services.updateStripeID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not update subID for ' + email)


def updateUser(firstname, surname, phoneNumber, chatbotNotifications: bool,  newsletters: bool, timeZone: str, userID):
    try:

        if not (firstname
                and surname
                and isinstance(chatbotNotifications, bool)
                and isinstance(newsletters, bool)):
            raise Exception("Did not provide all required fields")

        callback: Callback = getByID(userID)
        if not callback: return Callback(False, "Could not find user")
        user: User = callback.Data

        user.Firstname = firstname
        user.Surname = surname
        user.PhoneNumber = phoneNumber
        user.ChatbotNotifications = chatbotNotifications
        user.TimeZone = timeZone


        if newsletters:
            newsletters_callback: Callback = newsletter_services.add(user.Email)
        else:
            newsletters_callback: Callback = newsletter_services.remove(user.Email)

        if not newsletters_callback.Success:
            raise Exception(newsletters_callback.Message)

        # Save
        db.session.commit()

        return Callback(True, "User has been updated", user)
    except Exception as exc:
        helpers.logError("user_services.updateUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, "User could not be updated")


def updatePasswordByID(userID, newPassword, oldPassword=None):
    try:
        result: User = db.session.query(User).filter(User.ID == userID).first()
        if not result:
            return Callback(False, "Could not find user's records")

        if oldPassword is not None:
            if not oldPassword == result.Password:
                return Callback(False, "Old Password is incorrect")

        result.Password = newPassword
        db.session.commit()
        return Callback(True, "Password updated successfully.")

    except Exception as exc:
        helpers.logError("user_services.changePasswordByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Error in updating password")


def updatePasswordByEmail(userEmail, newPassword, currentPassword=None):
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
        helpers.logError("user_services.updatePasswordByEmail(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Error in changing password")


def verifyByEmail(email: str):
    try:
        user: User = db.session.query(User).filter(User.Email == email.lower()).first()
        if not user: raise Exception

        user.Verified = True
        db.session.commit()

        return Callback(True, 'Account has been verified successfully')

    except Exception as exc:
        helpers.logError("user_services.verifyByEmail(): " + str(exc))
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
        helpers.logError("user_services.removeByEmail(): " + str(exc))
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
        helpers.logError("user_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'User with id ' + str(id) + " could not be removed.")
