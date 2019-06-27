from sqlalchemy.sql import and_

from enums import CRM, UserType
from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services.Marketplace.CRM import Greenhouse, Adapt, Bullhorn, Vincere
# Process chatbot session
from utilities import helpers


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
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.insertCandidate(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertCandidate(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept candidates at this stage")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def insertClient(assistant: Assistant, conversation: Conversation):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.insertClient(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.insertClient(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertClient(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept clients")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def uploadFile(assistant: Assistant, storedFile: StoredFile):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.uploadFile(assistant.CRM.Auth, storedFile)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidates(assistant: Assistant, session):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.searchCandidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchCandidates(assistant.CRM.Auth)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchJobs(assistant: Assistant, session):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchJobs(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.searchJobs(assistant.CRM.Auth, assistant.CompanyID, session)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchJobs(assistant.CRM.Auth, session)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def getAllCandidates(assistant: Assistant):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.getAllCandidates(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.getAllCandidates(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.getAllCandidates(assistant.CRM.Auth)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def getAllJobs(assistant: Assistant):
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.getAllJobs(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.getAllJobs(assistant.CRM.Auth, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.getAllJobs(assistant.CRM.Auth)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def produceRecruiterValueReport(companyID, crmName):
    crm_callback: Callback = getCRMByType(crmName, companyID)
    if not crm_callback.Success:
        return Callback(False, "CRM not found")
    # Check CRM type
    if crmName == CRM.Bullhorn.name:
        return Bullhorn.produceRecruiterValueReport(crm_callback.Data, companyID)

    return Callback(True, crmName + " doesn't support this functionality")


# Connect to a new CRM
# type e.g. Bullhorn, Adapt etc.
def connect(type, auth, companyID) -> Callback:
    try:
        crm_type: CRM = CRM[type]
        # test connection
        test_callback: Callback = testConnection(type, auth, companyID)
        if not test_callback.Success:
            return test_callback

        connection = CRM_Model(Type=crm_type, Auth=test_callback.Data, CompanyID=companyID)

        # Save
        db.session.add(connection)
        db.session.commit()

        return Callback(True, 'CRM has been connected successfully', connection)

    except Exception as exc:
        helpers.logError("CRM_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM connection failed")


# Test connection to a CRM
def testConnection(type, auth, companyID) -> Callback:
    try:
        crm_type: CRM = CRM[type]
        crm_auth = auth

        # test connection
        test_callback: Callback = Callback(False, 'Connection failure. Please check entered details')
        if crm_type == CRM.Adapt:
            test_callback = Adapt.login(crm_auth)
        elif crm_type == CRM.Bullhorn:
            test_callback = Bullhorn.testConnection(crm_auth, companyID) # oauth2
        elif crm_type == CRM.Greenhouse:
            test_callback = Greenhouse.login(crm_auth)
        elif crm_type == CRM.Vincere:
            test_callback = Vincere.testConnection(crm_auth, companyID) # oauth2

        # When connection failed
        if not test_callback.Success:
            return test_callback

        return Callback(True, 'Successful connection', test_callback.Data)

    except Exception as exc:
        helpers.logError("CRM_services.connect(): " + str(exc))
        return Callback(False, "CRM testing failed.")


def disconnectByType(type, companyID) -> Callback:
    try:

        crm_callback: Callback = getCRMByType(type, companyID)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully')

    except Exception as exc:
        helpers.logError("CRM_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")



def disconnectByID(crmID, companyID) -> Callback:
    try:

        crm_callback: Callback = getCRMByID(crmID, companyID)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully', crmID)

    except Exception as exc:
        helpers.logError("CRM_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")


# get marketplace with id and company_id
# also checking if the marketplace is under that company
def getCRMByID(crmID, companyID):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == companyID, CRM_Model.ID == crmID)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        helpers.logError("CRM_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getCRMByType(crmType, companyID):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == companyID, CRM_Model.Type == crmType)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        helpers.logError("CRM_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getAll(companyID) -> Callback:
    try:
        result = db.session.query(CRM_Model).filter(CRM_Model.CompanyID == companyID).all()
        return Callback(True, "fetched all CRMs  successfully.", result)

    except Exception as exc:
        helpers.logError("crm_services.getAll(): " + str(exc))
        return Callback(False, 'Could not fetch all CRMs.')