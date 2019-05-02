from models import db, Assistant, Callback
from sqlalchemy import and_
from utilities import helpers, json_schemas
from os.path import join
import json
from config import BaseConfig
from services import flow_services
import logging
from jsonschema import validate


def getAssistantByHashID(hashID):
    try:
        assistantID = helpers.decrypt_id(hashID)
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


def getByID(id, companyID) -> Callback:
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
    # finally:
       # db.session.close()


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
    # finally:
       # db.session.close()


def getAll(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
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

        assistant = Assistant(Name=name, Flow=flow, Route=None, Message=message, TopBarText=topBarText,
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



def update(id, name, message, topBarText, secondsUntilPopup, mailEnabled, mailPeriod, config)-> Callback:
    try:
        # Validate the json config
        validate(config, json_schemas.assistant_config)

        db.session.query(Assistant).filter(Assistant.ID == id).update({'Name': name,
                                                                       'Message': message,
                                                                       'TopBarText': topBarText,
                                                                       'SecondsUntilPopup': secondsUntilPopup,
                                                                       "MailEnabled": mailEnabled,
                                                                       "MailPeriod": mailPeriod,
                                                                       "Config": config
                                                                       })
        db.session.commit()
        return Callback(True, name + ' Updated Successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        logging.error("assistant_services.update(): " + str(exc))
        return Callback(False,
                        "Couldn't update assistant "+name)


def changeStatus(assistant: Assistant, status):
    try:
        isActive = False
        if status:
           isActive = True

        assistant.Active = isActive
        db.session.commit()
        return Callback(True, 'Assistant status has been changed.')

    except Exception as exc:
        print("Error in assistant_services.changeStatus(): ", exc)
        logging.error("assistant_services.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the assistant's status.")


def removeByID(id) -> Callback:
    try:
        db.session.query(Assistant).filter(Assistant.ID == id).delete()
        db.session.commit()
        return Callback(True, 'Assistant has been deleted.')

    except Exception as exc:
        print("Error in assistant_services.removeByID(): ", exc)
        logging.error("assistant_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting assistant.')




# def getNotificationsRegisterByID(id):
#     try:
#         # Get result and check if None then raise exception
#         result = db.session.query(NotificationsRegister).filter(NotificationsRegister.AssistantID == id).all()
#         if not result: raise Exception
#
#         return Callback(True,
#                         "Got NotificationsRegister by assistant ID successfully.",
#                         result)
#     except Exception as exc:
#         print(exc)
#         db.session.rollback()
#         return Callback(False, 'Could not get the NotificationsRegister by assistant ID.')
#
#
# def getAllNotificationsRegisters():
#     try:
#         # Get result and check if None then raise exception
#         result = db.session.query(NotificationsRegister).all()
#         if not result: raise Exception
#
#         return Callback(True,
#                         "Got NotificationsRegisters successfully.",
#                         result)
#     except Exception as exc:
#         print(exc)
#         db.session.rollback()
#         return Callback(False, 'Could not get the NotificationsRegisters.')
