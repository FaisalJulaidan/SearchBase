from sqlalchemy.sql import and_

from models import db, Callback, Conversation, Assistant, CRM as CRM_Model, StoredFile
from services.Marketplace.CRM import Greenhouse, Bullhorn, Mercury, Jobscience, Vincere
# Process chatbot session
from utilities import helpers
from utilities.enums import CRM, UserType, DataType, Period, DataType as DT


def processConversation(assistant: Assistant, conversation: Conversation) -> Callback:
    print("Should be processing the conversation")
    # Insert base on userType
    if conversation.UserType is UserType.Candidate:
        return insertCandidate(assistant, conversation)
    elif conversation.UserType is UserType.Client:
        return insertClient(assistant, conversation)
    else:
        return Callback(False, "The data couldn't be synced with the CRM due to lack of information" +
                        " whether user is a Candidate or Client ")


def insertCandidate(assistant: Assistant, conversation: Conversation, update_id=None):
    name = (conversation.Name or " ").split(" ")
    data = {
        "name": conversation.Name or " ",
        "firstName": helpers.getListValue(name, 0, " "),
        "lastName": helpers.getListValue(name, 1, " "),
        "mobile": conversation.PhoneNumber or " ",
        "city": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobLocation.value['name'], [])),
        "email": conversation.Email or " ",
        "emails": conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], []),

        "skills": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], ) or
            conversation.Data.get('keywordsByDataType').get(DT.JobEssentialSkills.value['name'], [])) or None,
        "yearsExperience": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateYearsExperience.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobYearsRequired.value['name'], [])) or None,

        "preferredWorkCity": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobLocation.value['name'], [])) or None,
        "preferredJobTitle": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobTitle.value['name'], [])) or None,
        "preferredJobType": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobType.value['name'], [])) or None, # cant be used until predefined values

        "educations": ", ".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'],
                                                                                [])) or None,
        "availability": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateAvailability.value['name'], [])) or None,

        "annualSalary": getSalary(conversation, DT.CandidateAnnualDesiredSalary, "Min") or
                        getSalary(conversation, DT.JobAnnualSalary, "Min"),
        "dayRate": getSalary(conversation, DT.CandidateDailyDesiredSalary, "Min") or
                   getSalary(conversation, DT.JobDayRate, "Min"),

        "selectedSolutions": conversation.Data.get("selectedSolutions")
    }

    if update_id and assistant.CRM.Type is CRM.Bullhorn:
        func = "update"
    else:
        func = "insert"

    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Greenhouse:
            return Callback(True, "Greenhouse does not accept candidates at this stage")
        if crm_type is CRM.Adapt or crm_type is CRM.Jobscience:
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
            conversation.Data.get('keywordsByDataType').get(DT.ClientAvailability.value['name'], [])),

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


def updateCandidate(details, conversation, companyID):
    crm_callback: Callback = getByID(details["source_id"], companyID)

    if not crm_callback.Success:

        return crm_callback

    crm_type = crm_callback.Data.Type

    if crm_type not in [CRM.Bullhorn, CRM.Jobscience]:

        return Callback(False, "CRM " + crm_type.value + " is not allowed for updating")

    name = (conversation.Name or " ").split(" ")
    data = {
        "id": details["id"],
        "name": conversation.Name or " ",
        "firstName": helpers.getListValue(name, 0, " "),
        "lastName": helpers.getListValue(name, 1, " "),
        "mobile": conversation.PhoneNumber or " ",
        "city": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobLocation.value['name'], [])),
        "email": conversation.Email or " ",
        "emails": conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], []),

        "skills": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], ) or
            conversation.Data.get('keywordsByDataType').get(DT.JobEssentialSkills.value['name'], [])) or None,
        "yearsExperience": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateYearsExperience.value['name']) or
            conversation.Data.get('keywordsByDataType').get(DT.JobYearsRequired.value['name'], [])) or None,

        "preferredWorkCity": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobLocation.value['name'], [])) or None,
        "preferredJobTitle": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobTitle.value['name'], [])) or None,
        "preferredJobType": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.JobType.value['name'], [])) or None, # cant be used until predefined values

        "educations": ", ".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'],
                                                                                [])) or None,
        "availability": ", ".join(
            conversation.Data.get('keywordsByDataType').get(DT.CandidateAvailability.value['name'], [])) or None,

        "annualSalary": getSalary(conversation, DT.CandidateAnnualDesiredSalary, "Min") or
                        getSalary(conversation, DT.JobAnnualSalary, "Min"),
        "dayRate": getSalary(conversation, DT.CandidateDailyDesiredSalary, "Min") or
                   getSalary(conversation, DT.JobDayRate, "Min"),

        "selectedSolutions": conversation.Data.get("selectedSolutions")
    }

    if CRM.has_value(crm_type.value):
        # if crm_type is CRM.Greenhouse:
        #     return Callback(True, "Greenhouse does not accept clients")
        # if crm_type is CRM.Adapt or crm_type is CRM.Jobscience:
        #     return eval(crm_type.value + "." + func + "Candidate(assistant.CRM.Auth, data)")

        return eval(crm_type.value + ".updateCandidate(crm_callback.Data.Auth, data, companyID)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def uploadFile(assistant: Assistant, storedFile: StoredFile):
    print("IN CRM_SERVICES...")
    crm_type = assistant.CRM.Type
    if CRM.has_value(crm_type.value):
        if crm_type is CRM.Jobscience or crm_type is CRM.Mercury:
            return Callback(True, "CRM does not support file upload at this time")

        return eval(crm_type.value + ".uploadFile(assistant.CRM.Auth, storedFile)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchCandidates(assistant: Assistant, session):
    data = {
        "location": __checkFilter(session['keywordsByDataType'], DT.CandidateLocation),
        "preferredJotTitle": __checkFilter(session['keywordsByDataType'], DT.CandidateJobTitle),
        "yearsExperience": __checkFilter(session['keywordsByDataType'], DT.CandidateYearsExperience),
        "skills": __checkFilter(session['keywordsByDataType'], DT.CandidateSkills),
        "jobCategory": __checkFilter(session['keywordsByDataType'], DT.CandidateJobCategory),
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


def searchCandidatesCustom(crm, companyID, candidate_data, perfect=False):
    data = {
        "location": candidate_data.get("location"),
        "preferredJotTitle": candidate_data.get("jobTitle"),
        "skills": candidate_data.get("skills"),
        # "yearsExperience": checkFilter(session['keywordsByDataType'], DT.CandidateYearsExperience),
        # "jobCategory": checkFilter(session['keywordsByDataType'], DT.CandidateJobCategory),
        # "education": checkFilter(session['keywordsByDataType'], DT.CandidateEducation)
    }

    crm_type = crm.Type.value

    if perfect and crm == "Bullhorn":
        searchFunc = "searchPerfectCandidates"
    else:
        searchFunc = "searchCandidates"

    if CRM.has_value(crm_type):
        if crm.Type is CRM.Adapt:
            return Callback(True, "CRM does not support candidate search at this time")
        if crm.Type is CRM.Greenhouse:
            return eval(crm_type + "." + searchFunc + "(crm.Auth)")
        if crm.Type is CRM.Jobscience:
            return eval(crm_type + "." + searchFunc + "(crm.Auth, data)")

        return eval(crm_type + "." + searchFunc + "(crm.Auth, companyID, data)")
    else:
        return Callback(False, "CRM type did not match with those on the system")


def searchJobs(assistant: Assistant, session):
    data = {
        "jobTitle": __checkFilter(session['keywordsByDataType'], DT.JobTitle) or
                    __checkFilter(session['keywordsByDataType'], DT.CandidateJobTitle),
        "city": __checkFilter(session['keywordsByDataType'], DT.JobLocation) or
                __checkFilter(session['keywordsByDataType'], DT.CandidateLocation),
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


# private helper function
def __checkFilter(keywords, dataType: DT):
    print("FILTERING...")
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

        if crm_type == CRM.Bullhorn: # Need to change this?
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


# get min/max/average salary from the string and convert to specified period (daily, annually)
def getSalary(conversation: Conversation, dataType: DataType, salaryType, toPeriod=None):  # type Period
    # ex. 5000-20000 GBP Annual
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


# create a paragraph regarding the candidate with data that the API cannot accept
def additionalCandidateNotesBuilder(data, selectedSolutions=None):
    data = helpers.cleanDict(data)
    if not data:
        return ""

    sentences = {
        "yearsExperience": "They have [yearsExperience] years experience with their qualifications. ",
        "preferredJobTitle": "They have stated that their preferred jobs are connected with \"[preferredJobTitle]\". ",
        "preferredJobType": "They also prefer [preferredJobType] roles. ",
        "skills": "They are also well versed in [skills]. ",
        "educations": "For education they have provided \"[educations]\". "
    }

    paragraph = "SearchBase has also collected the following information regarding this candidate: "
    for key, value in data.items():
        paragraph += sentences[key].replace("[" + key + "]", value)

    if selectedSolutions:
        paragraph += "\n\nThe Candidate has also expressed interest in the following jobs: "
        for solution in selectedSolutions:
            for key, value in helpers.cleanDict(solution.get("data")).items():
                paragraph += "\n " + str(key) + " : " + str(value)
            paragraph += "\n"

    return paragraph


# prevents IDEA from automatically removing dependencies that are used in eval
def ideaCalmer():
    print(Jobscience, Mercury, Greenhouse)

