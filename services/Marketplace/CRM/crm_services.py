import logging

from sqlalchemy.sql import and_

from enums import CRM, UserType
from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services.Marketplace.CRM import Greenhouse, Adapt, Bullhorn


# Process chatbot session
def processConversation(assistant: Assistant, conversation: Conversation) -> Callback:
    # Insert base on userType
    if conversation.UserType is UserType.Candidate:
        return insertCandidate(assistant, conversation)
    elif conversation.UserType is UserType.Client:
        return insertClient(assistant, conversation)
    else:
        return Callback(False, "The data couldn't be synced with the CRM due to lack of information" +
                        " whether user is a Candidate or Client ")


def insertCandidate(assistant: Assistant, conversation: Conversation):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.insertCandidate(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertCandidate(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept candidates at this stage")


def insertClient(assistant: Assistant, conversation: Conversation):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.insertClient(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertClient(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept clients")


def uploadFile(assistant: Assistant, storedFile: StoredFile):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.uploadFile(assistant.CRM.Auth, storedFile)


def searchCandidates(assistant: Assistant, session):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.searchCandidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchCandidates(assistant.CRM.Auth)


def searchJobs(assistant: Assistant, session):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchJobs(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchJobs(assistant.CRM.Auth, session)


def getAllCandidates(assistant: Assistant):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.getAllCandidates(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.getAllCandidates(assistant.CRM.Auth)


def getAllJobs(assistant: Assistant):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.getAllJobs(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.getAllJobs(assistant.CRM.Auth)


def produceRecruiterValueReport(companyID, crmName):
    crm_callback: Callback = getCRMByType(crmName, companyID)
    if not crm_callback.Success:
        return Callback(False, "CRM not found")
    # Check CRM type
    if crmName == CRM.Bullhorn.name:
        return Bullhorn.produceRecruiterValueReport(crm_callback.Data, companyID)

    return Callback(True, crmName + " doesn't support this functionality")


# Connect to a new CRM
# details is a dict that has {auth, type}
def connect(company_id, details) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        # test connection
        test_callback: Callback = testConnection(details, company_id)
        if not test_callback.Success:
            return test_callback

        connection = CRM_Model(Type=crm_type, Auth=test_callback.Data, CompanyID=company_id)

        # Save
        db.session.add(connection)
        db.session.commit()

        return Callback(True, 'CRM has been connected successfully', connection)

    except Exception as exc:
        logging.error("CRM_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM connection failed")


# Update CRM Details
# details is a dict that has {auth, type}
def update(crm_id, company_id, details) -> Callback:
    try:
        crm_auth = details['auth']

        # test connection
        test_callback: Callback = testConnection(details, company_id)
        if not test_callback.Success:
            return test_callback

        connection_callback: Callback = getCRMByID(crm_id, company_id)
        if not connection_callback.Success:
            raise Exception(connection_callback.Message)

        crm = connection_callback.Data

        crm.Auth = crm_auth

        # Save
        db.session.commit()

        return Callback(True, 'CRM has been updated successfully')

    except Exception as exc:
        logging.error("CRM_services.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Update CRM details failed.")


def updateByCompanyAndType(crm_type, company_id, auth):
    try:
        crm_type: CRM = CRM[crm_type]
        crm_auth = auth

        # test connection
        test_callback: Callback = testConnection({"auth": auth}, company_id)
        if not test_callback.Success:
            return test_callback

        connection_callback: Callback = getCRMByType(crm_type, company_id)
        if not connection_callback.Success:
            raise Exception(connection_callback.Message)

        crm = connection_callback.Data

        crm.Auth = crm_auth

        # Save
        db.session.commit()

        return Callback(True, 'CRM has been updated successfully')

    except Exception as exc:
        logging.error("CRM_services.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Update CRM details failed.")


# Test connection to a CRM
def testConnection(details, companyID) -> Callback:
    try:
        crm_type: CRM = CRM[details['type']]
        crm_auth = details['auth']

        # test connection
        test_callback: Callback = Callback(False, 'Connection failure. Please check entered details')
        if crm_type == CRM.Adapt:
            test_callback = Adapt.login(crm_auth)
        elif crm_type == CRM.Bullhorn:
            test_callback = Bullhorn.testConnection(crm_auth, companyID)
        elif crm_type == CRM.Greenhouse:
            test_callback = Greenhouse.login(crm_auth)

        # When connection failed
        if not test_callback.Success:
            return test_callback

        return Callback(True, 'Successful connection', test_callback.Data)

    except Exception as exc:
        logging.error("CRM_services.connect(): " + str(exc))
        return Callback(False, "CRM connection failed.")


def disconnect(crm_id, company_id) -> Callback:
    try:

        crm_callback: Callback = getCRMByID(crm_id, company_id)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully', crm_id)

    except Exception as exc:
        logging.error("CRM_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")


# get crm with id and company_id
# also checking if the crm is under that company
def getCRMByID(crm_id, company_id):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == company_id, CRM_Model.ID == crm_id)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        logging.error("CRM_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getCRMByType(crm_type, company_id):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == company_id, CRM_Model.Type == crm_type)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        logging.error("CRM_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getAll(companyID) -> Callback:
    try:
        result = db.session.query(CRM_Model).filter(CRM_Model.CompanyID == companyID).all()
        return Callback(True, "fetched all CRMs  successfully.", result)

    except Exception as exc:
        logging.error("crm_services.getAll(): " + str(exc))
        return Callback(False, 'Could not fetch all CRMs.')
