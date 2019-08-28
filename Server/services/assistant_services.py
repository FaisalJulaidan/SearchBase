from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from models import db, Assistant, Callback, AutoPilot
from services import auto_pilot_services, flow_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import calendar_services
from services.Marketplace.Messenger import messenger_servicess
from utilities import helpers, json_schemas
from os.path import join
from config import BaseConfig
from jsonschema import validate
import json


def create(name, desc, welcomeMessage, topBarText, template, companyID) -> Assistant or None:
    try:

        flow = None
        if template and template != 'none':
            # Get json template
            relative_path = join('static/assistant_templates', template + '.json')
            absolute_path = join(BaseConfig.APP_ROOT, relative_path)
            flow = json.load(open(absolute_path))
            # Validate template
            callback: Callback = flow_services.isValidFlow(flow)
            if not callback.Success:
                raise Exception(callback.Message)

        assistant = Assistant(Name=name,
                              Description=desc,
                              Flow=flow,
                              Message=welcomeMessage,
                              TopBarText=topBarText,
                              SecondsUntilPopup=0,
                              Active=True,
                              CompanyID=companyID)

        db.session.add(assistant)
        db.session.commit()
        return Callback(True, 'Assistant created successfully', assistant)

    except Exception as exc:
        helpers.logError("assistant_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Failed to create the assistant', None)


# ----- Getters ----- #
def getByHashID(hashID):
    try:
        assistantID = helpers.decodeID(hashID)
        if len(assistantID) == 0:
            return Callback(False, "Assistant not found!", None)

        # Get result and check if None then raise exception
        assistant: Assistant = db.session.query(Assistant).get(assistantID[0])
        if not assistant: raise Exception
        return Callback(True, "", assistant)


    except Exception as exc:
        helpers.logError("assistant_services.getAssistantByHashID(): " + str(exc))
        return Callback(False, "Assistant not found!")


def getByID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result: Assistant = db.session.query(Assistant)\
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).options(joinedload('StoredFile').joinedload('StoredFileInfo')).first()
        if not result: raise Exception
        return Callback(True, "Got assistant successfully.", result)

    except Exception as exc:
        helpers.logError("assistant_services.getByID(): " + str(exc))
        return Callback(False, 'Could not get the assistant.')


def getByName(name) -> Callback:
    try:
        # Get result and check if None then raise exception
        assistant: Assistant = db.session.query(Assistant).filter(Assistant.Name == name).first()
        if not assistant: raise Exception

        return Callback(True, "Got assistant by nickname successfully.", assistant)

    except Exception as exc:
        helpers.logError("assistant_services.getByName(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')


def getAll(companyID) -> Callback:
    try:
        if not companyID: raise Exception
        # Get result and check if None then raise exception
        result = db.session.query(Assistant.ID,
                                  Assistant.Name,
                                  Assistant.Description,
                                  Assistant.Message,
                                  Assistant.TopBarText,
                                  Assistant.Active)\
            .filter(Assistant.CompanyID == companyID).all()

        if len(result) == 0:
            return Callback(True, "No assistants  to be retrieved.", [])

        return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get all assistants.')


def getAllFull(companyID) -> Callback:
    try:
        if not companyID: raise Exception
        # Get result and check if None then raise exception
        result = db.session.query(Assistant)\
            .filter(Assistant.CompanyID == companyID).all()

        if len(result) == 0:
            return Callback(True, "No assistants  to be retrieved.", [])

        return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get all assistants.')


def getAllWithEnabledNotifications(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(
                and_(Assistant.CompanyID == companyID, Assistant.MailEnabled)).all()
            if len(result) == 0:
                return Callback(True, "No assistants  to be retrieved.", [])

            return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        helpers.logError("assistant_services.getAllWithEnabledNotifications(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get all assistants.')


# Return the openTimes from the autoPilot connected to this assistant
def getAppointmentAllocationTime(assistantID) -> Callback:
    try:
        # Get assistant and check if None then raise exception
        assistant: Assistant = db.session.query(Assistant).filter(Assistant.ID == assistantID).first()
        if not assistant: raise Exception

        connectedAutoPilot: AutoPilot = assistant.AutoPilot

        # If the assistant is not connected to an autoPilot then return an empty array which means no open times
        if not connectedAutoPilot:
            return Callback(True,"There are no open time slots")

        # OpenTimes is an array of all open slots per day
        return Callback(True, "Got open time slots successfully.", connectedAutoPilot.AppointmentAllocationTime)

    except Exception as exc:
        helpers.logError("assistant_services.getOpenTimes(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the open times for this assistant.')


# ----- Updaters ----- #
def update(id, name, desc, message, topBarText, companyID) -> Callback:
    try:
        assistant: Assistant = db.session.query(Assistant) \
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)) \
            .first()

        assistant.Name = name
        assistant.Description = desc
        assistant.Message = message
        assistant.TopBarText = topBarText

        db.session.commit()
        return Callback(True, 'Assistant updated successfully', assistant)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.update(): " + str(exc))
        return Callback(False,
                        "Couldn't update assistant " + str(id))


def updateConfigs(id, name, desc, message, topBarText, secondsUntilPopup, notifyEvery, config, companyID) -> Callback:
    try:
        # Validate the json config
        validate(config, json_schemas.assistant_config)

        assistant: Assistant = db.session.query(Assistant)\
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)) \
            .first()

        assistant.Name = name
        assistant.Description = desc
        assistant.Message = message
        assistant.TopBarText = topBarText
        assistant.SecondsUntilPopup = secondsUntilPopup
        assistant.NotifyEvery = None if notifyEvery == "null" else int(notifyEvery)
        assistant.Config = config

        db.session.commit()
        return Callback(True, name + ' Updated Successfully', assistant)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.update(): " + str(exc))
        return Callback(False,
                        "Couldn't update assistant " + str(id))


def updateStatus(assistantID, newStatus, companyID):
    try:

        if newStatus is None: raise Exception("Please provide the new status")
        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"Active": newStatus})

        db.session.commit()
        return Callback(True, 'Assistant status has been changed.')

    except Exception as exc:
        helpers.logError("assistant_services.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the assistant's status.")


# ----- Deletion ----- #
def removeByID(id, companyID) -> Callback:
    try:
        db.session.query(Assistant).filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'Assistant has been deleted.')

    except Exception as exc:
        helpers.logError("assistant_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting assistant.')


# ----- CRM Connection ----- #
def connectToCRM(assistantID, CRMID, companyID):
    try:

        crm_callback: Callback = crm_services.getByID(CRMID, companyID)
        if not crm_callback.Success:
            raise Exception(crm_callback.Message)

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CRMID": CRMID})

        db.session.commit()

        return Callback(True, 'Assistant has been connected to CRM.')

    except Exception as exc:
        helpers.logError("assistant_services.connectToCRM(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to CRM.')


def disconnectFromCRM(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CRMID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from CRM.')

    except Exception as exc:
        helpers.logError("assistant_services.disconnectFromCRM(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from CRM.')


# ----- Calendar Connection ----- #
def connectToCalendar(assistantID, CalendarID, companyID):
    try:

        calendar_callback: Callback = calendar_services.getCalendarByID(CalendarID, companyID)
        if not calendar_callback.Success:
            raise Exception(calendar_callback.Message)

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CalendarID": CalendarID})

        db.session.commit()

        return Callback(True, 'Assistant has been connected to the Calendar.')

    except Exception as exc:
        helpers.logError("assistant_services.connectToCalendar(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to Calendar.')


def disconnectFromCalendar(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CalendarID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from Calendar.')

    except Exception as exc:
        helpers.logError("assistant_services.disconnectFromCalendar(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from Calendar.')


# ----- Messenger Connection ----- #
def connectToMessenger(assistantID, messengerID, companyID):
    try:

        messenger_callback: Callback = messenger_servicess.getByID(messengerID, companyID)
        if not messenger_callback.Success:
            raise Exception(messenger_callback.Message)

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"MessengerID": messengerID})

        db.session.commit()
        return Callback(True, 'Assistant has been connected to Messenger.')

    except Exception as exc:
        helpers.logError("assistant_services.connectToAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to Messenger.')


def disconnectFromMessenger(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"MessengerID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from Messenger.')

    except Exception as exc:
        helpers.logError("assistant_services.disconnectFromAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from AutoPilot.')


# ----- AutoPilot Connection ----- #
def connectToAutoPilot(assistantID, autoPilotID, companyID):
    try:

        ap_callback: Callback = auto_pilot_services.getByID(autoPilotID, companyID)
        if not ap_callback.Success:
            raise Exception(ap_callback.Message)

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"AutoPilotID": autoPilotID})

        db.session.commit()
        return Callback(True, 'Assistant has been connected to AutoPilot.')

    except Exception as exc:
        helpers.logError("assistant_services.connectToAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to AutoPilot.')


def disconnectFromAutoPilot(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"AutoPilotID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from AutoPilot.')

    except Exception as exc:
        helpers.logError("assistant_services.disconnectFromAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from AutoPilot.')