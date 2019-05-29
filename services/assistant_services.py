from models import db, Assistant, Callback
from sqlalchemy import and_
from utilities import helpers, json_schemas
from services.CRM import crm_services
from os.path import join
from config import BaseConfig
from services import flow_services, stored_file_services, auto_pilot_services
from jsonschema import validate
from werkzeug.utils import secure_filename
import logging, json


def create(name, message, topBarText, secondsUntilPopup, mailEnabled, mailPeriod, template, config, companyID) -> Assistant or None:
    try:

        # Validate the json config
        validate(config, json_schemas.assistant_config)

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

        assistant = Assistant(Name=name, Flow=flow, Message=message, TopBarText=topBarText,
                              SecondsUntilPopup=secondsUntilPopup, MailEnabled=mailEnabled, MailPeriod=mailPeriod,
                              Config=config, CompanyID=companyID)
        db.session.add(assistant)

        # Save
        db.session.commit()
        return Callback(True, 'Assistant has ben created successfully!', assistant)
    except Exception as exc:
        print(exc)
        logging.error("assistant_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Failed to create the assistant', None)


# ----- Getters ----- #
def getByHashID(hashID):
    try:
        assistantID = helpers.decode_id(hashID)
        if len(assistantID) == 0:
            return Callback(False, "Assistant not found!", None)

        # Get result and check if None then raise exception
        assistant: Assistant = db.session.query(Assistant).get(assistantID[0])
        if not assistant: raise Exception
        return Callback(True, "", assistant)


    except Exception as exc:
        print("getAssistantByHashID() ERROR:" + str(exc))
        logging.error("assistant_services.getAssistantByHashID(): " + str(exc))
        return Callback(False, "Assistant not found!")


def getByID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant)\
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got assistant successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("assistant_services.getByID(): " + str(exc))
        return Callback(False, 'Could not get the assistant.')


def getByName(name) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant).filter(Assistant.Name == name).first()
        if not result: raise Exception

        return Callback(True,
                        "Got assistant by nickname successfully.",
                        result)
    except Exception as exc:
        print(exc)
        logging.error("assistant_services.getByName(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')


def getAll(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
            print(result)
            if len(result) == 0:
                return Callback(True,"No assistants  to be retrieved.", [])

            return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        logging.error("assistant_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get all assistants.')


def getAllWithEnabledNotifications(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(and_(Assistant.CompanyID == companyID, Assistant.MailEnabled)).all()
            if len(result) == 0:
                return Callback(True, "No assistants  to be retrieved.", [])

            return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("assistant_services.getAllWithEnabledNotifications(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get all assistants.')


# ----- Updaters ----- #
def update(id, name, message, topBarText, secondsUntilPopup, mailEnabled, mailPeriod, config, companyID)-> Callback:
    try:
        # Validate the json config
        validate(config, json_schemas.assistant_config)

        assistant: Assistant = db.session.query(Assistant)\
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID))\
            .first()

        assistant.Name = name
        assistant.Message = message
        assistant.TopBarText = topBarText
        assistant.SecondsUntilPopup = secondsUntilPopup
        assistant.MailEnabled = mailEnabled
        assistant.MailPeriod = mailPeriod
        assistant.Config = config

        db.session.commit()
        return Callback(True, name + ' Updated Successfully', assistant)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        logging.error("assistant_services.update(): " + str(exc))
        return Callback(False,
                        "Couldn't update assistant " + str(id))


def changeStatus(assistantID, newStatus, companyID):
    try:

        if not newStatus: raise Exception("Please provide the new status")
        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"Active": newStatus})

        db.session.commit()
        return Callback(True, 'Assistant status has been changed.')

    except Exception as exc:
        print("Error in assistant_services.changeStatus(): ", exc)
        logging.error("assistant_services.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the assistant's status.")

# ----- Deletion ----- #
def removeByID(id, companyID) -> Callback:
    try:
        db.session.query(Assistant).filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'Assistant has been deleted.')

    except Exception as exc:
        print("Error in assistant_services.removeByID(): ", exc)
        logging.error("assistant_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting assistant.')


# ----- CRM Connection ----- #
def connectToCRM(assistantID, CRMID, companyID):
    try:

        crm_callback: Callback = crm_services.getCRMByID(CRMID, companyID)
        if not crm_callback.Success:
            raise Exception(crm_callback.Message)

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CRMID": CRMID})

        db.session.commit()
        return Callback(True, 'Assistant has been connected to CRM.')

    except Exception as exc:
        print("assistant_services.connectToCRM(): ", exc)
        logging.error("assistant_services.connectToCRM(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to CRM.')


def disconnectFromCRM(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"CRMID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from CRM.')

    except Exception as exc:
        print("assistant_services.disconnectFromCRM(): ", exc)
        logging.error("assistant_services.disconnectFromCRM(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from CRM.')


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
        print("assistant_services.connectToAutoPilot(): ", exc)
        logging.error("assistant_services.connectToAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in connecting assistant to AutoPilot.')


def disconnectFromAutoPilot(assistantID, companyID):
    try:

        db.session.query(Assistant).filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)) \
            .update({"AutoPilotID": None})

        db.session.commit()
        return Callback(True, 'Assistant has been disconnected from AutoPilot.')

    except Exception as exc:
        print("assistant_services.disconnectFromAutoPilot(): ", exc)
        logging.error("assistant_services.disconnectFromAutoPilot(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in disconnecting assistant from AutoPilot.')


# ----- Logo Operations ----- #
def uploadLogo(assistantID, file, companyID):
    try:

        assistant: Assistant = db.session.query(Assistant) \
            .filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)).first()
        if not assistant: raise Exception

        # Generate unique name: hash_sessionIDEncrypted.extension
        filename = helpers.encode_id(assistant.ID) + '.' + \
                   secure_filename(file.filename).rsplit('.', 1)[1].lower()
        assistant.LogoName = filename

        # Upload file to cloud Space
        upload_callback : Callback = stored_file_services.uploadFile(file, filename, '/chatbot_logos', public=True)
        if not upload_callback.Success:
            raise Exception(upload_callback.Message)

        db.session.commit()

        return Callback(True, 'Logo uploaded successfully.')

    except Exception as exc:
        print("assistant_services.uploadLogo(): ", exc)
        logging.error("assistant_services.uploadLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in uploading logo.')


def deleteLogo(assistantID, companyID):
    try:

        assistant: Assistant = db.session.query(Assistant) \
            .filter(and_(Assistant.ID == assistantID, Assistant.CompanyID == companyID)).first()
        if not assistant: raise Exception

        logoName = assistant.LogoName
        if not logoName: return Callback(False, 'No logo to delete')

        # Delete file from cloud Space and reference from database
        assistant.LogoName = None
        delete_callback : Callback = stored_file_services.deleteFile(logoName, '/chatbot_logos')
        if not delete_callback.Success:
            raise Exception(delete_callback.Message)

        db.session.commit()
        return Callback(True, 'Logo deleted successfully.')

    except Exception as exc:
        logging.error("assistant_services.deleteLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting logo.')
