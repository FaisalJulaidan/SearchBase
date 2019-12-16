from sqlalchemy.sql import and_

from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services import assistant_services
from services.Marketplace.CRM import Greenhouse, Bullhorn, Mercury, Jobscience, Vincere, Adapt
# Process chatbot session
from utilities import helpers
from utilities.enums import CRM, UserType, DataType, Period, DataType as DT
from datetime import date


def processConversation(assistant: Assistant, conversation: Conversation) -> Callback:
    # Insert base on userType
    if conversation.UserType is UserType.Candidate:
        return insertCandidate(assistant, conversation)
    elif conversation.UserType is UserType.Client:
        return insertClient(assistant, conversation)
    else:
        return Callback(False, "The data couldn't be synced with the CRM due to lack of information" +
                        " whether user is a Candidate or Client ")


def insertCandidate(assistant: Assistant, conversation: Conversation, update_id=None):
    data = __extractCandidateInsertData(conversation)

    if update_id and assistant.CRM.Type is CRM.Bullhorn:
        func = "update"
    else:
        func = "insert"

        # do not insert Candidates with no contact information
        if not data.get("email") and not data.get("mobile"):
            return Callback(False, "No email and telephone given. Candidate will not be submitted to CRM")

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Greenhouse:
            return Callback(True, "Greenhouse does not accept candidates at this stage")
        if crm_type is CRM.Adapt or crm_type is CRM.Jobscience:
            data["owner"] = assistant.User
            return eval(crm_type.value + "." + func + "Candidate(assistant.CRM.Auth, data)")

        return eval(crm_type.value + "." + func + "Candidate(assistant.CRM.Auth, data, assistant.CompanyID)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def insertClient(assistant: Assistant, conversation: Conversation):
    emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])
    name = (conversation.Name or " ").split(" ")

    data = {
        "name": conversation.Name or " ",
        "firstName": name[0],
        "lastName": name[-1],
        "mobile": conversation.PhoneNumber or " ",
        "city": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.ClientLocation.value['name'], [])),
        # check number of emails and submit them
        "email": emails[0],
        "emails": emails,
        "availability": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.UserAvailabilityDate.value['name'], [])),

        "companyName": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CompanyName.value['name'],
                                                            ["Undefined Company - TSB"]))
    }

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Greenhouse:
            return Callback(True, "Greenhouse does not accept clients")
        if crm_type is CRM.Adapt or crm_type is CRM.Jobscience:
            return eval(crm_type.value + ".insertClient(assistant.CRM.Auth, data)")

        return eval(crm_type.value + ".insertClient(assistant.CRM.Auth, data, assistant.CompanyID)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def updateCandidate(candidateID, conversation, companyID, sourceID):
    crm_callback: Callback = getByID(sourceID, companyID)
    if not crm_callback.Success:
        return crm_callback

    crm_type = crm_callback.Data.Type

    if crm_type not in [CRM.Bullhorn, CRM.Vincere, CRM.Jobscience]:
        return Callback(False, "CRM " + crm_type.value + " is not allowed for updating")

    data = __extractCandidateInsertData(conversation)
    data["id"] = candidateID

    if CRM.has_value(crm_type.value):
        # if crm_type is CRM.Greenhouse:
        #     return Callback(True, "Greenhouse does not accept clients")
        # if crm_type is CRM.Adapt or crm_type is CRM.Jobscience:
        #     return eval(crm_type.value + "." + func + "Candidate(assistant.CRM.Auth, data)")

        return eval(crm_type.value + ".updateCandidate(crm_callback.Data.Auth, data, companyID)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def uploadFile(filePath, fileName, conversation):
    callback: Callback = assistant_services.getByID(conversation.AssistantID, conversation.Assistant.CompanyID)
    if not callback.Success:
        return Callback(False, "Assistant not found!")
    assistant: Assistant = callback.Data

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Jobscience or crm_type is CRM.Mercury:
            return Callback(True, "CRM does not support file upload at this time")

        return eval(crm_type.value + ".uploadFile(assistant.CRM.Auth, filePath, fileName, conversation)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidates(assistant: Assistant, session):
    data = {
        "location": __checkFilter(session['keywordsByDataType'], DT.CandidateCity),
        "preferredJotTitle": __checkFilter(session['keywordsByDataType'], DT.PreferredJobTitle),
        "yearsExperience": __checkFilter(session['keywordsByDataType'], DT.CandidateYearsExperience),
        "skills": __checkFilter(session['keywordsByDataType'], DT.CandidateSkills, True),
        "jobCategory": __checkFilter(session['keywordsByDataType'], DT.JobCategory),
        "education": __checkFilter(session['keywordsByDataType'], DT.CandidateEducation)
    }

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Adapt:
            return Callback(True, "CRM does not support candidate search at this time")
        if crm_type is CRM.Greenhouse:
            return eval(crm_type.value + ".searchCandidates(assistant.CRM.Auth)")
        if crm_type is CRM.Jobscience:
            return eval(crm_type.value + ".searchCandidates(assistant.CRM.Auth, data)")
        return eval(crm_type.value + ".searchCandidates(assistant.CRM.Auth, assistant.CompanyID, data)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidatesCustom(crm, companyID, campaign_data, perfectFunc=False, customData=False, customSearch=None, **kwargs):
    if customData:
        data = campaign_data
    else:
        data = {
            "location": campaign_data.get("location"),
            "preferredJotTitle": campaign_data.get("preferredJobTitle"),
            "skills": campaign_data.get("skills", []),
            "jobType": campaign_data.get("jobType"),
            "shortlist_id": campaign_data.get("shortlist_id")
        }

    crm_type = crm.Type.value
    campaignCRMs = ["Bullhorn", "Vincere"]
    if perfectFunc and crm_type in campaignCRMs:
        searchFunc = "searchPerfectCandidates"
    elif customSearch:
        searchFunc = "searchCandidates{}".format(customSearch)
    elif crm_type == "Jobscience" and campaign_data.get("useShortlist"):
        searchFunc = "searchCandidatesByShortlist"
    else:
        searchFunc = "searchCandidates"

    if CRM.has_value(crm_type):
        if crm.Type is CRM.Adapt:
            return Callback(True, "CRM does not support candidate search at this time")
        if crm.Type is CRM.Greenhouse:
            return eval(crm_type + "." + searchFunc + "(crm.Auth)")
        if crm.Type is CRM.Jobscience:
            return eval(crm_type + "." + searchFunc + "(crm.Auth, data)")
        if crm.Type is CRM.Bullhorn:
            return eval(crm_type + "." + searchFunc + "(crm.Auth, companyID, data, **kwargs)")

        return eval(crm_type + "." + searchFunc + "(crm.Auth, companyID, data)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchPlacements(crm, companyID, params):
    crm_type = crm.Type.value
    if CRM.has_value(crm_type):
        if crm.Type is not CRM.Bullhorn:
            return Callback(True, "CRM does not support placement search at this time")
        return Bullhorn.searchPlacement(crm.Auth, companyID, params)
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchJobs(assistant: Assistant, session):
    data = {
        "preferredJobTitle": __checkFilter(session['keywordsByDataType'], DT.PreferredJobTitle),
        "city": __checkFilter(session['keywordsByDataType'], DT.JobCity) or
                __checkFilter(session['keywordsByDataType'], DT.CandidateCity),
        "employmentType": __checkFilter(session['keywordsByDataType'], DT.JobType),
        "skills": __checkFilter(session['keywordsByDataType'], DT.JobEssentialSkills) or
                  __checkFilter(session['keywordsByDataType'], DT.CandidateSkills),
        # "startDate": checkFilter(session['keywordsByDataType'], DT.JobStartDate),
        # "endDate": checkFilter(session['keywordsByDataType'], DT.JobEndDate),
        "yearsRequired": __checkFilter(session['keywordsByDataType'], DT.JobYearsRequired),
    }

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Adapt:
            return Callback(True, "CRM does not support job search at this time")
        if crm_type is CRM.Greenhouse:
            return eval(crm_type.value + ".searchJobs(assistant.CRM.Auth)")
        if crm_type is CRM.Jobscience:
            return eval(crm_type.value + ".searchJobs(assistant.CRM.Auth, data)")

        return eval(crm_type.value + ".searchJobs(assistant.CRM.Auth, assistant.CompanyID, data)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


# Hotlists, Shortlists, Saved Searches etc... (list of candidates made in the CRM)
def getShortlists(auth, crm_type, companyID, listID=None):
    if crm_type is CRM.Bullhorn:
        return Bullhorn.getSavedSearches(auth, companyID, "Candidate", listID)
    elif crm_type is CRM.Jobscience:
        return Jobscience.getShortLists(auth)

    else:
        return Callback(False, "CRM type did not match with those on the system")


# private helper function
def __checkFilter(keywords, dataType: DT, returnList=False):
    if keywords.get(dataType.value["name"]) and not returnList:
        return " ".join(keywords[dataType.value["name"]])
    elif keywords.get(dataType.value["name"]):
        return keywords.get(dataType.value["name"])
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
def connect(crm_type, auth, companyID) -> Callback:
    try:
        # test connection
        test_callback: Callback = testConnection(crm_type, auth, companyID)
        if not test_callback.Success:
            return test_callback

        connection = CRM_Model(Type=crm_type, Auth=test_callback.Data, CompanyID=companyID)

        # Save
        db.session.add(connection)
        db.session.commit()

        # refresh tokens
        test_callback: Callback = testConnection(crm_type, test_callback.Data, companyID)
        if not test_callback.Success:
            return test_callback

        return Callback(True, 'CRM has been connected successfully', connection)

    except Exception as exc:
        helpers.logError("crm_services.connect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM connection failed")


# Test connection to a CRM
def testConnection(crm_type, auth, companyID) -> Callback:
    try:
        # test connection
        if CRM.has_value(crm_type):
            crm: CRM = CRM[crm_type]
            if crm == CRM.Adapt or crm == CRM.Greenhouse:
                return eval(crm_type + ".testConnection(auth)")

            return eval(crm_type + ".testConnection(auth, companyID)")
        else:
            return Callback(False, "CRM type did not match with those on the system")

    except Exception as exc:
        helpers.logError("crm_services.connect(): " + str(exc))
        return Callback(False, "CRM testing failed.")


def disconnectByType(crm_type, companyID) -> Callback:
    try:
        crm_callback: Callback = getCRMByType(crm_type, companyID)
        if not crm_callback:
            return Callback(False, "Could not find CRM.")

        # no matter if it fails or not remove it from the system
        logoutOfCRM(crm_callback.Data.Auth, crm_type, companyID)

        db.session.delete(crm_callback.Data)
        db.session.commit()
        return Callback(True, 'CRM has been disconnected successfully')

    except Exception as exc:
        helpers.logError("crm_services.disconnect(): " + str(exc))
        db.session.rollback()
        return Callback(False, "CRM disconnection failed.")


def disconnectByID(crmID, companyID) -> Callback:
    try:
        crm_callback: Callback = getByID(crmID, companyID)
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

        if crm_type == CRM.Bullhorn:  # Need to change this?
            return Bullhorn.logout(auth, companyID)

        elif crm_type == "Jobscience":
            return Jobscience.logout(auth, companyID)

        return Callback(False, 'Logout failed')

    except Exception as exc:
        helpers.logError("crm_services.logoutOfCRM(): " + str(exc))
        return Callback(False, "CRM logout failed.")


def getByID(crmID, companyID):
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


def updateByType(crm_type, newAuth, companyID):
    try:
        crm = db.session.query(CRM_Model).filter(
            and_(CRM_Model.CompanyID == companyID, CRM_Model.Type == crm_type)).first()
        crm.Auth = dict(newAuth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.saveNewCRMAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))


def updateAutopilotConnection(crm_type, autoPilotID, companyID):
    try:
        crm = db.session.query(CRM_Model).filter(
            and_(CRM_Model.CompanyID == companyID, CRM_Model.Type == crm_type)).first()
        crm.CRMAutoPilotID = autoPilotID
        db.session.commit()
        return Callback(True, "New CRM Autopilot ID has been saved", crm)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.updateAutopilotConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


# get min/max/average salary from the string and convert to specified period (daily, annually)
def getSalary(conversation: Conversation, dataType: DataType, salaryType, toPeriod: Period = None):  # type Period
    # ex. 5000-20000 GBP Annually
    salary = conversation.Data.get('keywordsByDataType').get(dataType.value['name'], 0)

    if salary:
        salarySplitted = salary[0].split(" ")
        salaryAmmount = salarySplitted[0].split("-")

        if salaryType == "Average":
            salary = str(float(salaryAmmount[1]) - float(salaryAmmount[0]))
        elif salaryType == "Min":
            salary = salaryAmmount[0]
        elif salaryType == "Max":
            salary = salaryAmmount[1]

        if toPeriod:
            salary = helpers.convertSalaryPeriod(salary, Period[salarySplitted[2]], toPeriod)

    return salary


# create a paragraph regarding the candidate with data that the API cannot accept
def additionalCandidateNotesBuilder(data, selectedSolutions=None, oldNote=None):
    data = helpers.cleanDict(data)
    if not data:
        return ""

    paragraph = "At " + str(date.today().strftime("%B %d, %Y")) + \
                " SearchBase has also collected the following information regarding this candidate: \n"
    for key, value in data.items():
        # if not sentences.get(key):
        #     helpers.logError(str(key) + " needs to be added to crm_services.additionalCandidateNotesBuilder.")
        #     continue
        # paragraph += sentences[key].replace("[" + key + "]", value)
        paragraph += "\n  - " + str(key) + ": " + str(value)

    if selectedSolutions:
        paragraph += "\n\n\nThe Candidate has also expressed interest in the following jobs: \n"
        for solution in selectedSolutions:
            for key, value in helpers.cleanDict(solution.get("data")).items():
                paragraph += "\n " + str(key) + " : " + str(value)
            paragraph += "\n"

    if oldNote:
        paragraph = paragraph + "\n\n\n\n" + oldNote

    return paragraph


def __extractCandidateInsertData(conversation):
    name = (conversation.Name or " ").split(" ")
    return {
        "name": conversation.Name or " ",
        "firstName": helpers.getListValue(name, 0, " "),
        "lastName": helpers.getListValue(name, 1, " "),
        "mobile": conversation.PhoneNumber or " ",
        "street": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateStreet.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobStreet.value['name'], [])),
        "city": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateCity.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobCity.value['name'], [])),
        "postCode": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidatePostCode.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobPostCode.value['name'], [])),
        "country": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateCountry.value['name'], [])),
        "email": conversation.Email or " ",
        "emails": conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], []),
        "currentJobTitle": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CurrentJobTitle.value['name'], [])) or None,

        "skills": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], ) or
            conversation.Data.get('keywordsByDataType').get(DT.JobEssentialSkills.value['name'], [])) or None,
        "yearsExperience": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateYearsExperience.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobYearsRequired.value['name'], [])) or None,

        "preferredWorkCity": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobCity.value['name'], [])) or None,
        "preferredJobTitle": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.PreferredJobTitle.value['name'], [])) or None,
        "preferredJobType": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobType.value['name'], [])) or None,

        "educations": " ".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'],
                                                                               [])) or None,
        "linkedIn": " ".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateLinkdinURL.value['name'],
                                                                             [])) or None,

        "availability": " ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateAvailability.value['name'], [])) or None,

        "annualSalary": getSalary(conversation, DT.CandidateDesiredSalary, "Min", Period.Annually) or
                        getSalary(conversation, DT.JobSalary, "Min", Period.Annually),
        "dayRate": getSalary(conversation, DT.CandidateDesiredSalary, "Min", Period.Daily) or
                   getSalary(conversation, DT.JobSalary, "Min", Period.Daily),

        "selectedSolutions": conversation.Data.get("selectedSolutions")
    }


# prevents IDEA from automatically removing dependencies that are used in eval
def IDEA_Calmer():
    print(Jobscience, Mercury, Greenhouse, Vincere, Adapt)
