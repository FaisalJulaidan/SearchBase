from enums import CRM, UserType
from models import db, Callback, ChatbotSession, Assistant
from services.CRM import Adapt
import logging

# First Step
def processSession (assistant: Assistant, session: ChatbotSession):
    if session.UserType is UserType.Candidate:
        print("process session insert Candidate")
        return insertCandidate(assistant, session)
    elif session.UserType is UserType.Client:
        print("process session insert Client")
        return insertClient(assistant, session)


def insertCandidate(assistant: Assistant, session: ChatbotSession):
   if assistant.CRM is CRM.Adapt:
       return Adapt.insertCandidate(assistant.CRMAuth, session)


def insertClient(assistant: Assistant, session: ChatbotSession):
    if assistant.CRM is CRM.Adapt:
        return Adapt.insertClient(assistant.CRMAuth, session)


# Connect assistant to a new CRM
# details is a dict that has {auth, type}
def connect(assistant: Assistant, details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        test_callback: Callback = testConnection(details)
        if not test_callback.Success:
            return test_callback

        assistant.CRM = crm_type
        assistant.CRMAuth = crm_auth
        assistant.CRMConnected = True

        # Save
        db.session.commit()
        return Callback(True, 'CRM has been connected successfully', assistant)

    except Exception as exc:
        print(exc)
        logging.error("CRM_services.connect(): " + test_callback.Message)
        db.session.rollback()
        return Callback(False, test_callback.Message)



# Test connection to a CRM
def testConnection(details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        login_callback: Callback = Callback(False, 'Connection failure. Please check entered details')
        print(crm_type == CRM.Adapt)
        print(CRM.Adapt)
        if crm_type == CRM.Adapt:
            login_callback = Adapt.login(crm_auth)

        # When connection failed
        if not login_callback.Success:
            print("here I go")
            return login_callback

        return Callback(True, 'Successful connection')

    except Exception as exc:
        logging.error("CRM_services.connect(): " + login_callback.Message)
        db.session.rollback()
        return Callback(False, login_callback.Message)
