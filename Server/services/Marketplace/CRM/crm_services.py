from sqlalchemy.sql import and_

from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services.Marketplace.CRM import Greenhouse, Adapt, Bullhorn, Vincere, Jobscience, Mercury
# Process chatbot session
from utilities import helpers
from utilities.enums import CRM, UserType, DataType, Period
from utilities.enums import DataType as DT


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
    name = (conversation.Name or " ").split(" ")

    data = {
        "name": conversation.Name or " ",
        "firstName": helpers.getListValue(name, 0, " "),
        "lastName": helpers.getListValue(name, 1, " "),
        "mobile": conversation.PhoneNumber or " ",
        "city": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [" "])),
        "email": conversation.Email or " ",
        "emails": conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [" "]),
        "skills": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], [" "])),
        "educations": conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'], []),
        "availability": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateAvailability.value['name'], [])) or None,
        "jobTitle": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobTitle.value['name'], [])),
        "salary": getSalary(conversation, DT.CandidateAnnualDesiredSalary, "Average"),
        "rate": getSalary(conversation, DT.CandidateAnnualDesiredSalary or
                          DT.CandidateDailyDesiredSalary, "Average")
    }

    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.insertCandidate(assistant.CRM.Auth, data, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Mercury:
        return Mercury.insertCandidate(assistant.CRM.Auth, data, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.insertCandidate(assistant.CRM.Auth, data, assistant.CompanyID)
    # elif assistant.CRM.Type is CRM.Mercury:
    #     return Mercury.insertCandidate(assistant.CRM.Auth, conversation)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertCandidate(assistant.CRM.Auth, data)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept candidates at this point in time")
    elif assistant.CRM.Type is CRM.Jobscience:
        return Jobscience.insertCandidate(assistant.CRM.Auth, data)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def insertClient(assistant: Assistant, conversation: Conversation):
    emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])
    name = (conversation.Name or " ").split(" ")

    data = {
        "name": conversation.Name or " ",
        "firstName": name[0],
        "lastName": name[-1],
        "emails": emails,
        "mobile": conversation.PhoneNumber or " ",
        "city": " ".join(
                conversation.Data.get('keywordsByDataType').get(DT.ClientLocation.value['name'], [])),
        # check number of emails and submit them
        "email": emails[0],
        "companyName": " ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CompanyName.value['name'],
                                                                ["Undefined Company - TSB"]))
    }

    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.insertClient(assistant.CRM.Auth, data, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Mercury:
        return Mercury.insertClient(assistant.CRM.Auth, data, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.insertClient(assistant.CRM.Auth, data, assistant.CompanyID)
    elif assistant.CRM.Type is CRM.Adapt:
        return Adapt.insertClient(assistant.CRM.Auth, data)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Callback(True, "Greenhouse does not accept clients")
    elif assistant.CRM.Type is CRM.Jobscience:
        return Jobscience.insertClient(assistant.CRM.Auth, data)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def uploadFile(assistant: Assistant, storedFile: StoredFile):
    # Check CRM type
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.uploadFile(assistant.CRM.Auth, storedFile)
    # elif assistant.CRM.Type is CRM.Mercury: TODO
    #     return Mercury.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.uploadFile(assistant.CRM.Auth, storedFile)
    elif assistant.CRM.Type is CRM.Jobscience:
        return Callback(True, "Jobscience does not support file upload at this time")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidates(assistant: Assistant, session):
    data = {
        "location": checkFilter(session['keywordsByDataType'], DT.CandidateLocation)
    }
    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.searchCandidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Mercury:
        return Mercury.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.searchCandidates(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchCandidates(assistant.CRM.Auth)
    elif assistant.CRM.Type is CRM.Jobscience:
        t = Jobscience.searchCandidates(assistant.CRM.Auth, data)
        return t
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchJobs(assistant: Assistant, session):
    data = {
        "jobTitle": checkFilter(session['keywordsByDataType'], DT.JobTitle),
        "city": checkFilter(session['keywordsByDataType'], DT.JobLocation),
        "employmentType": checkFilter(session['keywordsByDataType'], DT.JobType),
        "skills": checkFilter(session['keywordsByDataType'], DT.JobEssentialSkills),
        "startDate": checkFilter(session['keywordsByDataType'], DT.JobStartDate),
        "endDate": checkFilter(session['keywordsByDataType'], DT.JobEndDate),
        "yearsRequired": checkFilter(session['keywordsByDataType'], DT.JobYearsRequired),
    }

    # Check CRM type
    # if assistant.CRM.Type is CRM.Adapt:
    #     return Adapt.pullAllCadidates(assistant.CRM.Auth)
    if assistant.CRM.Type is CRM.Bullhorn:
        return Bullhorn.searchJobs(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Mercury:
        return Mercury.searchJobs(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Vincere:
        return Vincere.searchJobs(assistant.CRM.Auth, assistant.CompanyID, data)
    elif assistant.CRM.Type is CRM.Greenhouse:
        return Greenhouse.searchJobs(assistant.CRM.Auth)
    elif assistant.CRM.Type is CRM.Jobscience:
        return Jobscience.searchJobs(assistant.CRM.Auth, data)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def checkFilter(keywords, dataType: DT):
    if keywords.get(dataType.value["name"]):
        return " ".join(keywords[dataType.value["name"]])
    return None


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
def testConnection(type, auth, companyID) -> Callback:
    try:
        crm_type: CRM = CRM[type]

        # test connection
        if crm_type == CRM.Bullhorn:
            return Bullhorn.testConnection(auth, companyID)  # oauth2
        elif crm_type == CRM.Mercury:
            return Mercury.testConnection(auth, companyID)  # oauth2
        elif crm_type == CRM.Adapt:
            return Adapt.testConnection(auth)
        elif crm_type == CRM.Greenhouse:
            return Greenhouse.login(auth)
        elif crm_type == CRM.Vincere:
            return Vincere.testConnection(auth, companyID)  # oauth2
        elif crm_type == CRM.Jobscience:
            return Jobscience.testConnection(auth, companyID)  # oauth2

        return Callback(False, 'Connection failure. Please check entered details')

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
        # elif crm_type == CRM.Adapt:
        #     return Adapt.testConnection(auth)
        # elif crm_type == CRM.Greenhouse:
        #     return Greenhouse.login(auth)
        # elif crm_type == CRM.Vincere:
        #     return Vincere.testConnection(auth, companyID)

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


# get min/max/average salary from the string and convert to specified period (daily, annually)
def getSalary(conversation: Conversation, dataType: DataType, salaryType, toPeriod=None):  # type Period
    # Less Than 5000 GBP Monthly
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
