import json
from datetime import datetime
from os.path import join

from jsonschema import validate
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from config import BaseConfig
from models import db, Assistant, Callback, AutoPilot, AppointmentAllocationTime, StoredFileInfo, StoredFile
from services import auto_pilot_services, flow_services, stored_file_services, user_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import calendar_services
from services.Marketplace.Messenger import messenger_servicess
from utilities import helpers, json_schemas, enums


def create(name, desc, welcomeMessage, topBarText, flow, template, companyID) -> Assistant or None:
    try:
        # if there is already a flow then ignore creating from template
        if not flow and template and template != 'none':
            # Get json template
            relative_path = join('static/assistant_templates', template + '.json')
            absolute_path = join(BaseConfig.APP_ROOT, relative_path)
            flow = json.load(open(absolute_path))


        # Validate flow
        callback: Callback = flow_services.isValidFlow(flow)
        if not callback.Success:
            raise Exception(callback.Message)

        # default assistant config values
        config = {
            "restrictedCountries": [],
            "chatbotPosition": "Right"
        }
        validate(config, json_schemas.assistant_config)

        assistant = Assistant(Name=name,
                              Description=desc,
                              Flow=flow,
                              Message=welcomeMessage,
                              TopBarText=topBarText,
                              SecondsUntilPopup=0,
                              Active=True,
                              Config=config,
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


def getByID(id: int, companyID: int, eager= False) -> Callback:
    try:
        # Get result and check if None then raise exception
        query = db.session.query(Assistant)

        if eager:
            query = query.options(joinedload('StoredFile').joinedload("StoredFileInfo"))

        result = query.filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).first()

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
                                  Assistant.Active,
                                  Assistant.UserID)\
            .filter(Assistant.CompanyID == companyID).all()
        if len(result) == 0:
            return Callback(True, "No assistants  to be retrieved.", [])

        return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        db.session.rollback()
        # helpers.logError("assistant_services.getAll(): " + str(exc))
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
            return Callback(True, "There are no available time slots")

        appointmentAllocationTime: AppointmentAllocationTime = connectedAutoPilot.AppointmentAllocationTime
        # Check if the auto pilot is not linked with an AppointmentAllocationTime table
        if not (appointmentAllocationTime and connectedAutoPilot.SendCandidatesAppointments):
            return Callback(True, "There are no available time slots")

        # OpenTimes is an array of all open slots per day
        return Callback(True, "Got open time slots successfully.", appointmentAllocationTime)

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


def updateConfigs(id, name, desc, message, topBarText, secondsUntilPopup, notifyEvery, config, ownerID, companyID) -> Callback:
    try:

        # Check if owner/user belongs to the company
        if ownerID and not user_services.getByIDAndCompanyID(ownerID, companyID).Success:
            raise Exception("User does not exist")

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
        assistant.UserID = ownerID

        if not assistant.LastNotificationDate and notifyEvery != "null":
            assistant.LastNotificationDate = datetime.now()

        db.session.commit()
        return Callback(True, name + ' Updated Successfully', assistant)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("assistant_services.update(): " + str(exc))
        return Callback(False, "Couldn't update assistant ")


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


def updateContacts(contacts, assistantID, companyID):
    try:
        if not contacts:
            db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
                .update({"User": None})

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"User": contacts[0]})

        db.session.commit()
        return Callback(True, 'Assistant contacts have been changed.')

    except Exception as exc:
        helpers.logError("assistant_services.updateContacts(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the assistant's contacts.")


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

    # ----- Logo Operations ----- #
def uploadLogo(file, assistantID, companyID):
    try:

        assistant: Assistant = getByID(assistantID, companyID, True).Data
        if not assistant: raise Exception

        # Delete old logo ref from DB. DigitalOcean will override the old logo since they have the same name
        oldLogo: StoredFileInfo = helpers.keyFromStoredFile(assistant.StoredFile, enums.FileAssetType.Logo)
        if oldLogo.AbsFilePath:
            db.session.delete(oldLogo.StoredFile)
            db.session.delete(oldLogo) # comment this if u want to use a unique filename for every new logo instead of company id encoded

        # Generate unique name using assistant name encoded
        filename = helpers.encodeID(assistantID) + "_AssistantLogo" + '.' + \
                   secure_filename(file.filename).rsplit('.', 1)[1].lower()

        sf = StoredFile()
        db.session.add(sf)
        db.session.flush()

        upload_callback: Callback = stored_file_services.uploadFile(file, filename, True, model=Assistant,
                                                                    identifier="ID",
                                                                    identifier_value=assistant.ID,
                                                                    stored_file_id=sf.ID,
                                                                    key=enums.FileAssetType.Logo)

        return Callback(True, 'Logo uploaded successfully.', upload_callback.Data)

    except Exception as exc:
        helpers.logError("assistant_service.uploadLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in uploading assistant logo.')


def deleteLogo(assistantID, companyID):
    try:

        assistant: Assistant = getByID(assistantID, companyID, True).Data
        if not assistant: raise Exception


        logo: StoredFile = assistant.StoredFile
        if not logo: return Callback(False, 'No logo to delete')

        # Delete file from cloud Space and reference from database
        path = helpers.keyFromStoredFile(logo, enums.FileAssetType.Logo).FilePath

        delete_callback : Callback = stored_file_services.deleteFile(path, logo)
        if not delete_callback.Success:
            raise Exception(delete_callback.Message)

        db.session.commit()
        return Callback(True, 'Logo deleted successfully.')

    except Exception as exc:
        helpers.logError("company_service.deleteLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting logo.')
