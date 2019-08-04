from sqlalchemy.sql import and_

from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services.Marketplace.CRM import Greenhouse, Bullhorn
# Process chatbot session
from utilities import helpers
from utilities.enums import CRM, UserType, DataType, Period


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
    crm_type = assistant.CRM.Type.value
    if CRM.has_value(crm_type):
        if assistant.CRM.Type is CRM.Greenhouse:
            return Callback(True, "Greenhouse does not accept candidates at this stage")

        return eval(crm_type + ".insertCandidate(assistant.CRM.Auth, conversation)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def insertClient(assistant: Assistant, conversation: Conversation):
    crm_type = assistant.CRM.Type.value
    if CRM.has_value(crm_type):
        if assistant.CRM.Type is CRM.Greenhouse:
            return Callback(True, "Greenhouse does not accept clients")

        return eval(crm_type + ".insertClient(assistant.CRM.Auth, conversation)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def uploadFile(assistant: Assistant, storedFile: StoredFile):
    crm_type = assistant.CRM.Type.value
    if CRM.has_value(crm_type):
        if assistant.CRM.Type is CRM.Jobscience or assistant.CRM.Type is CRM.Mercury:
            return Callback(True, "CRM does not support file upload at this time")

        return eval(crm_type + ".uploadFile(assistant.CRM.Auth, storedFile)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidates(assistant: Assistant, session):
    crm_type = assistant.CRM.Type.value
    if CRM.has_value(crm_type):
        if assistant.CRM.Type is CRM.Adapt:
            return Callback(True, "CRM does not support candidate search at this time")
        if assistant.CRM.Type is CRM.Greenhouse:
            return Greenhouse.searchCandidates(assistant.CRM.Auth)

        return eval(crm_type + ".searchCandidates(assistant.CRM.Auth, assistant.CompanyID, session)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchJobs(assistant: Assistant, session):
    crm_type = assistant.CRM.Type.value
    if CRM.has_value(crm_type):
        if assistant.CRM.Type is CRM.Adapt:
            return Callback(True, "CRM does not support job search at this time")
        if assistant.CRM.Type is CRM.Greenhouse:
            return Greenhouse.searchJobs(assistant.CRM.Auth, session)

        return eval(crm_type + ".searchJobs(assistant.CRM.Auth, assistant.CompanyID, session)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def produceRecruiterValueReport(companyID, crmName):
    try:
        crm_callback: Callback = getCRMByType(crmName, companyID)
        if not crm_callback.Success:
            return Callback(False, "CRM not found")
        # Check CRM type
        if crmName == CRM.Bullhorn.name:
            return Bullhorn.produceRecruiterValueReport(crm_callback.Data, companyID)

        return Callback(True, crmName + " doesn't support this functionality")
    except Exception as exc:
        helpers.logError("crm_services.produceRecruiterValueReport(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Producing recruiter value report failed")


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
        helpers.logError("crm_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM connection failed")


# Test connection to a CRM
def testConnection(crm_type, auth, companyID) -> Callback:
    try:
        crm_type: CRM = CRM[type]

        # test connection
        if CRM.has_value(crm_type):
            if crm_type == CRM.Adapt or crm_type == CRM.Greenhouse:
                return eval(crm_type + ".testConnection(auth)")

            return eval(crm_type + ".testConnection(auth, companyID)")
        else:
            return Callback(False, "CRM type did not match with those on the system")

    except Exception as exc:
        helpers.logError("crm_services.connect(): " + str(exc))
        return Callback(False, "CRM testing failed.")


def disconnectByType(type, companyID) -> Callback:
    try:
        crm_callback: Callback = getCRMByType(type, companyID)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        # no matter if it fails or not remove it from the system
        logoutOfCRM(crm_callback.Data.Auth, type, companyID)

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully')

    except Exception as exc:
        helpers.logError("crm_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")


def disconnectByID(crmID, companyID) -> Callback:
    try:
        crm_callback: Callback = getCRMByID(crmID, companyID)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        # no matter if it fails or not remove it from the system
        logoutOfCRM(crm_callback.Data.Auth, crm_callback.Data.Type, companyID)

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully', crmID)

    except Exception as exc:
        helpers.logError("crm_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")


def logoutOfCRM(auth, crm_type, companyID) -> Callback:
    try:
        if crm_type == CRM.Bullhorn:
            return Bullhorn.logout(auth, companyID)

        return Callback(False, 'Logout failed')

    except Exception as exc:
        helpers.logError("crm_services.logoutOfCRM(): " + str(exc))
        return Callback(False, "CRM logout failed.")


def getCRMByID(crmID, companyID):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == companyID, CRM_Model.ID == crmID)).first()
        if not crm:
            raise Exception("CRM not found")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        helpers.logError("crm_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getCRMByType(crmType, companyID):
    try:
        crm = db.session.query(CRM_Model) \
            .filter(and_(CRM_Model.CompanyID == companyID, CRM_Model.Type == crmType)).first()
        if not crm:
            return Callback(False, "CRM doesn't exist")

        return Callback(True, "CRM retrieved successfully.", crm)

    except Exception as exc:
        helpers.logError("crm_services.getCRMByCompanyID(): " + str(exc))
        return Callback(False, 'Could not retrieve CRM.')


def getAll(companyID) -> Callback:
    try:
        result = db.session.query(CRM_Model).filter(CRM_Model.CompanyID == companyID).all()
        return Callback(True, "fetched all CRMs  successfully.", result)

    except Exception as exc:
        helpers.logError("crm_services.getAll(): " + str(exc))
        return Callback(False, 'Could not fetch all CRMs.')


def updateByType(type, newAuth, companyID):
    try:
        crm = db.session.query(CRM_Model).filter(and_(CRM_Model.CompanyID == companyID, CRM_Model.Type == type)).first()
        crm.Auth = dict(newAuth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.saveNewCRMAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getSalary(conversation: Conversation, dataType: DataType, salaryType, toPeriod=None):  # type Period
    # ex. Less Than 5000 GBP Monthly
    salary = conversation.Data.get('keywordsByDataType').get(dataType.value['name'], 0)
    if salary:
        salarySplitted = salary[0].split(" ")
        salaryAmmount = salarySplitted[0].split("-")
        if toPeriod:
            if salaryType == "Average":
                salary = helpers.convertSalaryPeriod(str(float(salaryAmmount[1]) - float(salaryAmmount[0])),
                                                     Period[salarySplitted[2]], toPeriod)
            elif salaryType == "Min":
                salary = helpers.convertSalaryPeriod(salaryAmmount[0], Period[salarySplitted[2]], toPeriod)
            elif salaryType == "Max":
                salary = helpers.convertSalaryPeriod(salaryAmmount[1], Period[salarySplitted[2]], toPeriod)
        else:
            if salaryType == "Average":
                salary = str(float(salaryAmmount[1]) - float(salaryAmmount[0]))
            elif salaryType == "Min":
                salary = salaryAmmount[0]
            elif salaryType == "Max":
                salary = salaryAmmount[1]
    return salary
