from sqlalchemy import and_

from models import Callback, db, Messenger as Messenger_Model
from services.Marketplace.Messenger import Twilio
from utilities import helpers
from utilities.enums import Messenger


# Test connection to a Messenger
def sendMessage(type: Messenger, recipient, body, auth, whatsapp=False) -> Callback:
    try:

        # Note: Dont actually send message while testing...

        # test connection
        if type is Messenger.Twilio:
            return Twilio.sendMessage(recipient, body, auth, whatsapp)  # oauth2
            pass

        return Callback(False, 'Connection failure. Please check entered details')

    except Exception as exc:
        helpers.logError("messenger_services.connect(): " + str(exc))
        return Callback(False, "Messenger testing failed.")


def connect(type, auth, companyID) -> Callback:
    try:
        messenger_type: Messenger = Messenger[type]
        # test connection
        test_callback: Callback = testConnection(type, auth)
        if not test_callback.Success:
            return test_callback

        connection = Messenger_Model(Type=messenger_type, Auth=test_callback.Data, CompanyID=companyID)

        # Save
        db.session.add(connection)
        db.session.commit()

        return Callback(True, 'Messenger has been connected successfully', connection)

    except Exception as exc:
        helpers.logError("messenger_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Messenger connection failed")


# Test connection to a Messenger
def testConnection(type, auth) -> Callback:
    try:
        messenger_type: Messenger = Messenger[type]

        # test connection
        if messenger_type == Messenger.Twilio:
            return Twilio.testConnection(auth)  # oauth2

        return Callback(False, 'Connection failure. Please check entered details')

    except Exception as exc:
        helpers.logError("messenger_services.connect(): " + str(exc))
        return Callback(False, "Messenger testing failed.")


def disconnectByType(type, companyID) -> Callback:
    try:
        messenger_callback: Callback = getMessengerByType(type, companyID)
        if not messenger_callback:
            return Callback(False, "Could not find Messenger.")

        db.session.delete(messenger_callback.Data)
        db.session.commit()
        return Callback(True, 'Messenger has been disconnected successfully')

    except Exception as exc:
        helpers.logError("messenger_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Messenger disconnection failed.")


def disconnectByID(messengerID, companyID) -> Callback:
    try:
        messenger_callback: Callback = getByID(messengerID, companyID)
        if not messenger_callback:
            return Callback(False, "Could not find Messenger.")

        db.session.delete(messenger_callback.Data)
        db.session.commit()
        return Callback(True, 'Messenger has been disconnected successfully', messengerID)

    except Exception as exc:
        helpers.logError("messenger_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Messenger disconnection failed.")


def getByID(messengerID, companyID):
    try:
        messenger = db.session.query(Messenger_Model) \
            .filter(and_(Messenger_Model.CompanyID == companyID, Messenger_Model.ID == messengerID)).first()
        if not messenger:
            raise Exception("Messenger not found")

        return Callback(True, "Messenger retrieved successfully.", messenger)

    except Exception as exc:
        helpers.logError("messenger_services.getMessengerByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve Messenger.')


def getMessengerByType(messengerType, companyID):
    try:
        messenger = db.session.query(Messenger_Model) \
            .filter(and_(Messenger_Model.CompanyID == companyID, Messenger_Model.Type == messengerType)).first()
        if not messenger:
            return Callback(False, "Messenger doesn't exist")

        return Callback(True, "Messenger retrieved successfully.", messenger)

    except Exception as exc:
        helpers.logError("messenger_services.getMessengerByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve Messenger.')


def getAll(companyID) -> Callback:
    try:
        result = db.session.query(Messenger_Model).filter(Messenger_Model.CompanyID == companyID).all()
        return Callback(True, "fetched all Messengers  successfully.", result)

    except Exception as exc:
        helpers.logError("messenger_services.getAll(): " + str(exc))
        return Callback(False, 'Could not fetch all Messengers.')


def updateByType(type, newAuth, companyID):
    try:
        messenger = db.session.query(Messenger_Model).filter(
            and_(Messenger_Model.CompanyID == companyID, Messenger_Model.Type == type)).first()
        messenger.Auth = dict(newAuth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.saveNewMessengerAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))
