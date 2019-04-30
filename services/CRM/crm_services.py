import logging

from sqlalchemy.sql import and_

from enums import CRM, UserType
from models import db, Callback, ChatbotSession, Assistant, CRM as modelsCRM
from services import company_services
from services.CRM import Adapt


# Process chatbot session
def processSession(assistant: Assistant, session: ChatbotSession) -> Callback:
    # Insert base on userType
    if session.UserType is UserType.Candidate:
        return insertCandidate(assistant, session)
    elif session.UserType is UserType.Client:
        return insertClient(assistant, session)
    else:
        return Callback(False, "The data couldn't be synced with the CRM due to lack of information" +
                        " whether user is a Candidate or Client ")


def insertCandidate(assistant: Assistant, session: ChatbotSession):
    # Check CRM type
    if assistant.CRM is CRM.Adapt:
        return Adapt.insertCandidate(assistant.CRMAuth, session)


def insertClient(assistant: Assistant, session: ChatbotSession):
    # Check CRM type
    if assistant.CRM is CRM.Adapt:
        return Adapt.insertClient(assistant.CRMAuth, session)


# Connect to a new CRM
# details is a dict that has {auth, type}
def connect(company_id, details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        test_callback: Callback = testConnection(details)
        if not test_callback.Success:
            return test_callback

        save_callback = save_connection(company_id, crm_type, crm_auth)
        if not save_callback.Success:
            raise Exception(save_callback.Message)

        return Callback(True, 'CRM has been connected successfully')

    except Exception as exc:
        print(exc)
        logging.error("CRM_services.connect(): " + test_callback.Message)
        db.session.rollback()
        return Callback(False, test_callback.Message)


# Update CRM Details
# details is a dict that has {auth, type}
def update(crm_id, company_id, details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        test_callback: Callback = testConnection(details)
        if not test_callback.Success:
            return test_callback

        update_callback = update_connection(crm_id, company_id, crm_type, crm_auth)
        if not update_callback.Success:
            raise Exception(update_callback.Message)

        return Callback(True, 'CRM has been updated successfully')

    except Exception as exc:
        print(exc)
        logging.error("CRM_services.update(): " + test_callback.Message)
        db.session.rollback()
        return Callback(False, test_callback.Message)


# Test connection to a CRM
def testConnection(details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        login_callback: Callback = Callback(False, 'Connection failure. Please check entered details')
        if crm_type == CRM.Adapt:
            login_callback = Adapt.login(crm_auth)

        # When connection failed
        if not login_callback.Success:
            return login_callback

        return Callback(True, 'Successful connection')

    except Exception as exc:
        logging.error("CRM_services.connect(): " + login_callback.Message)
        return Callback(False, login_callback.Message)


def disconnect(crm_id, company_id) -> Callback:
    try:

        crm_callback: Callback = get_crm_by_company_id(crm_id, company_id)
        if not crm_callback:
            raise Exception(crm_callback.Message)

        crm_callback.Data.delete()
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully')

    except Exception as exc:
        logging.error("CRM_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, str(exc))


# get crm with id and company_id
# also checking if the crm is under that company
def get_crm_by_company_id(crm_id, company_id):
    try:
        crm = db.session.query(modelsCRM) \
            .filter(and_(modelsCRM.CompanyID == company_id, modelsCRM.ID == crm_id)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        print("CRM_services.get_crm_by_company_id() Error: ", exc)
        logging.error("CRM_services.get_crm_by_company_id(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve CRM.')


# save the connection to the CRM in the DB
def save_connection(company_id, type, auth):
    try:

        company_callback = company_services.getByID(company_id)
        if not company_callback.Success:
            raise Exception(company_callback.Message)

        connection = modelsCRM(Type=type, Auth=auth, Company=company_callback.Data)

        # Save
        db.session.add(connection)
        db.session.commit()
        return Callback(True, 'CRM has been saved successfully')

    except Exception as exc:
        logging.error("CRM_services.save_connection(): " + str(exc))
        db.session.rollback()
        return Callback(False, str(exc))


# update the connection to the CRM in the db
def update_connection(crm_id, company_id, crm_type, crm_auth):
    try:

        company_callback = company_services.getByID(company_id)
        if not company_callback.Success:
            raise Exception(company_callback.Message)

        connection_callback: Callback = get_crm_by_company_id(crm_id, company_id)
        if not connection_callback.Success:
            raise Exception(connection_callback.Message)

        crm = connection_callback.Data

        crm.Type = crm_type
        crm.Auth = crm_auth

        # Save
        db.session.commit()
        return Callback(True, 'CRM has been updated successfully')

    except Exception as exc:
        logging.error("CRM_services.update_connection(): " + str(exc))
        db.session.rollback()
        return Callback(False, str(exc))
