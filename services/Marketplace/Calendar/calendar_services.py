import logging

from sqlalchemy.sql import and_

from enums import UserType, Calendar as Calendar_Enum
from models import db, Callback, Conversation, Assistant, Calendar as Calendar_Model, StoredFile
from services import assistant_services
from services.Marketplace.Calendar import Google, Outlook
from utilities import helpers


# Process chatbot session
# def processConversation(assistant: Assistant, conversation: Conversation) -> Callback:
#     # Insert base on userType
#     if conversation.UserType is UserType.Candidate:
#         return insertCandidate(assistant, conversation)
#     elif conversation.UserType is UserType.Client:
#         return insertClient(assistant, conversation)
#     else:
#         return Callback(False, "The data couldn't be synced with the Calendar due to lack of information" +
#                         " whether user is a Candidate or Client ")

def addEvent(eventDetails, assistant=None, assistantID=None):
    if not (assistant or assistantID):
        return Callback(False, "Assistant was not provided")

    if not assistant:
        assistant_callback: Callback = assistant_services.getByHashID(assistantID)
        if not assistant_callback.Success:
            return Callback(False, "Assistant could not be retrieved")
        assistant = assistant_callback.Data

    if assistant.Calendar.Type is Calendar_Enum.Outlook:
        return Outlook.addEvent(assistant.Calendar, eventDetails)
    elif assistant.Calendar.Type is Calendar_Enum.Google:
        return Google.addEvent(assistant.CompanyID, eventDetails.get("name"), eventDetails.get("description"),
                               eventDetails.get("start"), eventDetails.get("end"))
    else:
        return Callback(False, "Could not retrieve the Calendar's Provider")


# Connect to a new Calendar
# details is a dict that has {auth, type}
def connect(company_id, details) -> Callback:
    try:
        calendar_type: Calendar_Enum = Calendar_Enum[details['type']]
        # test connection
        test_callback: Callback = testConnection(details, company_id)
        if not test_callback.Success:
            return test_callback

        connection = Calendar_Model(Type=calendar_type, Auth=test_callback.Data, CompanyID=company_id, MetaData=None)

        # Save
        db.session.add(connection)
        db.session.commit()

        return Callback(True, 'Calendar has been connected successfully', connection)

    except Exception as exc:
        helpers.logError("calendar_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Calendar connection failed")


# Update Calendar Details
# details is a dict that has {auth, type}
def update(calendar_id, company_id, details) -> Callback:
    try:
        calendar_auth = details['auth']

        # test connection
        test_callback: Callback = testConnection(details, company_id)
        if not test_callback.Success:
            return test_callback

        connection_callback: Callback = getCalendarByID(calendar_id, company_id)
        if not connection_callback.Success:
            raise Exception(connection_callback.Message)

        Calendar = connection_callback.Data

        Calendar.Auth = calendar_auth

        # Save
        db.session.commit()

        return Callback(True, 'Calendar has been updated successfully')

    except Exception as exc:
        helpers.logError("calendar_services.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Update Calendar details failed.")


def updateByCompanyAndType(calendar_type, company_id, auth, metaData):
    try:
        # test connection
        test_callback: Callback = testConnection({"auth": auth, "type": calendar_type}, company_id)
        if not test_callback.Success:
            return test_callback

        connection_callback: Callback = getCalendarByType(calendar_type, company_id)
        if not connection_callback.Success:
            raise Exception(connection_callback.Message)

        Calendar: Calendar_Model = connection_callback.Data

        Calendar.Auth = auth
        Calendar.MetaData = metaData

        # Save
        db.session.commit()

        return Callback(True, 'Calendar has been updated successfully', Calendar)

    except Exception as exc:
        helpers.logError("calendar_services.updateByCompanyAndType(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Update Calendar details failed.")


# Test connection to a Calendar (details must include the auth)
def testConnection(details, companyID) -> Callback:
    try:
        calendar_type: Calendar_Enum = Calendar_Enum[details['type']]

        if calendar_type == Calendar_Enum.Outlook:
            return Outlook.testConnection(details["auth"], companyID)
        else:
            return Callback(False, "Could not match Calendar's type")

    except Exception as exc:
        helpers.logError("calendar_services.testConnection(): " + str(exc))
        return Callback(False, "Calendar test failed.")


def disconnect(calendar_id, company_id) -> Callback:
    try:

        calendar_callback: Callback = getCalendarByID(calendar_id, company_id)
        if not calendar_callback:
            return Callback(False, "Could not find Calendar.")

        db.session.delete(calendar_callback.Data)
        db.session.commit()
        return Callback(True, 'Calendar has been disconnected successfully', calendar_id)

    except Exception as exc:
        helpers.logError("calendar_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Calendar disconnection failed.")


# get Calendar with id and company_id
# also checking if the Calendar is under that company
def getCalendarByID(calendar_id, company_id):
    try:
        Calendar = db.session.query(Calendar_Model) \
            .filter(and_(Calendar_Model.CompanyID == company_id, Calendar_Model.ID == calendar_id)).first()
        if not Calendar:
            raise Exception("Calendar not found")

        return Callback(True, "Calendar retrieved successfully.", Calendar)

    except Exception as exc:
        helpers.logError("calendar_services.getCalendarByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve Calendar.')


def getCalendarByType(calendar_type, company_id):
    try:
        Calendar = db.session.query(Calendar_Model) \
            .filter(and_(Calendar_Model.CompanyID == company_id, Calendar_Model.Type == calendar_type)).first()
        if not Calendar:
            raise Exception("Calendar not found")

        return Callback(True, "Calendar retrieved successfully.", Calendar)

    except Exception as exc:
        helpers.logError("calendar_services.getCalendarByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve Calendar.')


def getAll(companyID) -> Callback:
    try:
        result = db.session.query(Calendar_Model).filter(Calendar_Model.CompanyID == companyID).all()
        return Callback(True, "fetched all Calendars  successfully.", result)

    except Exception as exc:
        helpers.logError("calendar_services.getAll(): " + str(exc))
        return Callback(False, 'Could not fetch all Calendars.')
