import base64
import json
import os

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, StoredFile
from services import stored_file_services, databases_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from utilities import helpers
from utilities.enums import DataType as DT, Period

CLIENT_ID = os.environ['MERCURY_CLIENT_ID']
CLIENT_SECRET = os.environ['MERCURY_CLIENT_SECRET']
DYNAMICS_VERSION = "v9.1"

TEST_DOMAIN = "greenrecruitmentcompanysandbox.crm11"  # NEEDS TO BE TAKEN FROM THE LOGIN

"""
requires domain name ex. greenrecruitmentcompanysandbox.crm11.dynamics.com
"""


def testConnection(auth, companyID):
    try:
        if auth.get("refresh_token"):
            return retrieveAccessToken(auth, companyID)
        elif auth.get("code"):
            return login(auth)
        else:
            return Callback(False, "Parameters for connection were not provided")

    except Exception as exc:
        helpers.logError("Marketplace.Crm.Mercury.testConnection() ERROR: " + str(exc))
        return Callback(False, "Error in testing connection")


def login(auth):
    print("AUTH: ", auth)
    from utilities import helpers
    try:

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": helpers.getDomain() + "/dashboard/marketplace/Mercury",
            "code": auth.get("code")
        }

        url = "https://login.microsoftonline.com/ded6800a-6adb-4fc5-b14e-76747a56d913/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)

        return Callback(True, "Success",
                        {
                            "access_token": result_body.get("access_token"),
                            "refresh_token": result_body.get("refresh_token"),
                            "id_token": result_body.get("id_token"),
                            "domain": auth.get("domain")
                        })

    except Exception as exc:
        helpers.logError("Marketplace.Crm.Mercury.login() ERROR: " + str(exc))
        return Callback(False, "Error in logging you in. Please try again")


def retrieveAccessToken(auth, companyID):
    from utilities import helpers
    try:
        auth = dict(auth)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": helpers.getDomain() + "/dashboard/marketplace/Mercury",
            "refresh_token": auth.get("refresh_token")
        }

        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)

        auth["access_token"] = result_body.get("access_token")
        if result_body.get("refresh_token"):
            auth["refresh_token"] = result_body.get("refresh_token")

        saveAuth_callback: Callback = crm_services.updateByType("Mercury", auth, companyID)
        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, "Access Token retrieved", auth)

    except Exception as exc:
        helpers.logError("Marketplace.Crm.Mercury.retrieveAccessToken() ERROR: " + str(exc))
        return Callback(False, "Could not retrieve access token")


def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = buildUrl(query, auth.get("domain"), optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer " + auth.get("access_token")}

        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
        print("refresh toekn", auth.get("refresh_token"))
        print("CODE: ", r.status_code)
        print("TEXT", r.text)
        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveAccessToken(auth, companyID)
            if not callback.Success:
                raise Exception(callback.Message)

            headers["Authorization"] = "Bearer " + callback.Data.get("access_token")
            print(headers)
            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            print("CODE 2", r.status_code)
            print("TEXT 2", r.text)
            if not r.ok:
                raise Exception(r.text + ". Query could not be sent")

        elif not r.ok:
            raise Exception(r.text + ". Unexpected error occurred when calling the API")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("Marketplace.Crm.Mercury.sendQuery() ERROR: " + str(exc))
        return Callback(False, "Query could not be sent")


def buildUrl(query, domain, optionalParams=None):
    # set up initial url
    url = "https://" + domain + ".dynamics.com/api/data/" + DYNAMICS_VERSION + "/" + query
    # add additional params
    if optionalParams:
        url += "?"
        for param in optionalParams:
            url += "&" + param
    # return the url
    return url


def insertCandidate(auth, conversation: Conversation) -> Callback:
    try:
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [" "])
        name = (conversation.Name or " ").split(" ")

        # availability, yearsExperience
        body = {
            "crimson_firstname": helpers.getListValue(name, 0, " "),
            "crimson_surname": helpers.getListValue(name, 1, " "),
            "crimson_mobile": conversation.PhoneNumber or " ",
            "crimson_town": " ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [" "])),
            "crimson_email": conversation.Email or " ",
            "crimson_availability": DT.CandidateAvailability,
            "crimson_jobtitle": DT.JobTitle,
            "crimson_expsalaryp": str(crm_services.getSalary(conversation, DT.CandidateDesiredSalary, Period.Annually)),
            "crimson_expratec": str(crm_services.getSalary(conversation, DT.CandidateDesiredSalary, Period.Daily))
        }

        # Add additional emails to email2 and email3
        # for email in emails:
        #     index = emails.index(email)
        #     if index != 0:
        #         body["email" + str(index + 1)] = email

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "entity/Candidate", "post", body,
                                                 conversation.Assistant.CompanyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def uploadFile(auth, storedFile: StoredFile):
    try:
        conversation = storedFile.Conversation

        if not conversation.CRMResponse:
            raise Exception("Can't upload file for record with no CRM Response")

        file_callback = stored_file_services.downloadFile(storedFile.FilePath, stored_file_services.USER_FILES_PATH)
        if not file_callback.Success:
            raise Exception(file_callback.Message)
        file = file_callback.Data
        file_content = file.get()["Body"].read()
        file_content = base64.b64encode(file_content).decode('ascii')

        body = {
            "externalID": storedFile.ID,
            "fileType": "SAMPLE",
            "name": "TSB_" + storedFile.FilePath,
            "fileContent": file_content
        }

        conversationResponse = json.loads(conversation.CRMResponse)
        entityID = str(conversationResponse.get("changedEntityId"))

        if conversation.UserType.value is "Candidate":
            entity = "Candidate"
        elif conversation.UserType.value is "Client":
            entity = "ClientContact"
        else:
            raise Exception("Entity type to submit could not be retrieved")

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "file/" + entity + "/" + entityID,
                                                 "put", body, conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClient(auth, conversation: Conversation) -> Callback:
    try:
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])

        body = {
            "firstname": conversation.Name or " ",
            "lastname": conversation.PhoneNumber or " ",
            "address": {
                "city": " ".join(
                    conversation.Data.get('keywordsByDataType').get(DT.ClientLocation.value['name'], [])),
            },
            # check number of emails and submit them
            "email": emails[0],
        }

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "contacts", "post", body,
                                                 conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, conversation, fields=None) -> Callback:
    try:
        filter = "$filter="
        if not fields:
            fields = "$select=crimson_availability,crimson_currentjobtitle,crimson_email,crimson_expratec,crimson_" + \
                     "expsalaryp,crimson_jobtitle,crimson_mobile,crimson_name,crimson_town," + \
                     "crimson_workpref_permanent,crimson_workpref_temp,mercury_cvurl,_transactioncurrencyid_value"

        keywords = conversation['keywordsByDataType']

        # populate filter
        filter += checkFilter(keywords, DT.CandidateLocation, "crimson_town")

        filter = filter[:-3]

        # check if no conditions submitted
        if len(filter) < 6:
            filter = "$filter=*:*"

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "crimson_candidates", "get", {}, companyID,
                                                 [fields, filter])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        result = []
        for record in return_body["value"]:
            if record.get("crimson_workpref_permanent"):
                payPeriod = Period("Annually")
            elif record.get("crimson_workpref_temp"):
                payPeriod = Period("Daily")
            else:
                payPeriod = None
            # mercury_cvurl    - CV
            # _transactioncurrencyid_value   - currency id
            result.append(databases_services.createPandaCandidate(id=record.get("crimson_candidateid", ""),
                                                                  name=record.get("crimson_name"),
                                                                  email=record.get("crimson_email"),
                                                                  mobile=record.get("crimson_mobile"),
                                                                  location=record.get("crimson_town"),
                                                                  skills=None,
                                                                  linkdinURL=None,
                                                                  availability=record.get("crimson_availability"),
                                                                  jobTitle=record.get("crimson_jobtitle"),
                                                                  education=None,
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get("crimson_expsalaryp") or
                                                                                record.get("crimson_expratec", 0),
                                                                  currency=Currency("GBP"),
                                                                  source="Mercury"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, conversation, fields=None) -> Callback:
    try:
        filter = "$filter="
        if not fields:
            fields = "$select=crimson_addresscity,crimson_jobsummary,crimson_jobtitle,crimson_startdate," + \
                     "crimson_typeofposition,crimson_vacancyid,mercury_permanentsalary_mc," + \
                     "mercury_tempcandidatepay_mc,_mercury_vacancytype_value,_transactioncurrencyid_value"
        keywords = conversation['keywordsByDataType']

        # populate filter TODO
        filter += checkFilter(keywords, DT.JobTitle, "crimson_jobtitle")

        filter += checkFilter(keywords, DT.JobLocation, "crimson_addresscity")

        # filter += checkFilter(keywords, DT.JobType, "employmentType")

        # salary = crm_services.getSalary(conversation, DT.JobSalary, Period.Annually)
        # if salary > 0:
        #     filter += "salary:" + str(salary) + " or"

        filter += checkFilter(keywords, DT.JobStartDate, "crimson_startdate")

        filter = filter[:-3]

        # check if no conditions submitted
        if len(filter) < 4:
            filter = "$filter=*:*"

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "crimson_vacancies", "get", {}, companyID,
                                                 [fields, filter])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)
        result = []
        # not found match for JobLinkURL
        for record in return_body["data"]:
            # crimson_typeofposition    - code for job type (143570000 is permanent, 143570001 is contract)
            # TODO make it retrieve the job type from code from their api
            if record.get("crimson_typeofposition") == 143570000:
                payPeriod = Period("Annually")
                employmentType = "Permanent"
            elif record.get("crimson_typeofposition") == 143570001:
                payPeriod = Period("Daily")
                employmentType = "Contract"
            else:
                payPeriod = None
                employmentType = None
            # _transactioncurrencyid_value    - currency code
            result.append(databases_services.createPandaJob(id=record.get("crimson_vacancyid"),
                                                            title=record.get("crimson_jobtitle"),
                                                            desc=record.get("crimson_jobsummary", ""),
                                                            location=record.get("crimson_addresscity"),
                                                            type=employmentType,
                                                            salary=record.get("mercury_permanentsalary_mc") or
                                                                   record.get("mercury_tempcandidatepay_mc"),
                                                            essentialSkills=None,
                                                            desiredSkills=None,
                                                            yearsRequired=0,
                                                            startDate=record.get("crimson_startdate"),
                                                            endDate=None,
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            source="Mercury"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def checkFilter(keywords, dataType: DT, string):
    if keywords.get(dataType.value["name"]):
        return string + " eq '" + "".join(keywords[dataType.value["name"]]) + "' or"
    return ""


def searchJobsCustomQuery(auth, companyID, filter, fields=None) -> Callback:
    try:

        if not fields:
            fields = "fields=id,title,publicDescription,address,employmentType,salary,skills,yearsRequired,startDate,dateEnd"

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 [fields, filter, "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))

# def getAllCandidates(auth, companyID, fields=None) -> Callback:
#     try:
#         # custom fields?
#         if not fields:
#             fields = "fields=id,name,email,mobile,address,primarySkills,status,educations,dayRate"
#
#         # send filter
#         sendQuery_callback: Callback = sendQuery(auth, "departmentCandidates", "get", {}, companyID, [fields])
#         if not sendQuery_callback.Success:
#             raise Exception(sendQuery_callback.Message)
#
#         return_body = json.loads(sendQuery_callback.Data.text)
#
#         return Callback(True, sendQuery_callback.Message, return_body)
#
#     except Exception as exc:
#         helpers.logError("Marketplace.CRM.Mercury.getAllCandidates() ERROR: " + str(exc))
#         return Callback(False, str(exc))
#
#
# def getAllJobs(auth, companyID, fields=None) -> Callback:
#     try:
#         # custom fields?
#         if not fields:
#             fields = "fields=*"
#
#         # send filter
#         sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
#                                                  [fields, "$filter=*:*", "count=500"])
#         if not sendQuery_callback.Success:
#             raise Exception(sendQuery_callback.Message)
#
#         return_body = json.loads(sendQuery_callback.Data.text)
#
#         return Callback(True, sendQuery_callback.Message, return_body)
#
#     except Exception as exc:
#         helpers.logError("Marketplace.CRM.Mercury.getAllJobs() ERROR: " + str(exc))
#         return Callback(False, str(exc))


# def produceRecruiterValueReport(crm: CRM_Model, companyID) -> Callback:
#     try:
#
#         getJobs_callback: Callback = searchJobsCustomQuery(
#             crm.Auth, companyID,
#             "$filter=employmentType:\"permanent\" AND status:\"accepting candidates\"",
#             "fields=dateAdded,title,clientCorporation,salary,feeArrangement,owner")
#         if not getJobs_callback.Success:
#             raise Exception("Jobs could not be retrieved")
#
#         def extractName(json):
#             return int(json["owner"]["id"])
#
#         return_body = getJobs_callback.Data["data"]
#         return_body.sort(key=extractName, reverse=True)
#
#         def getTotalPipeline(result, previousUser):
#             if len(result.keys()) > 0:
#                 totalPipeline = 0
#                 for pRecord in result[previousUser]:
#                     totalPipeline += float(pRecord[-1])
#                 result[previousUser].append(["", "", "", "", "", previousUser + " Total Pipeline Value",
#                                              totalPipeline])
#             return result
#
#         titles = ["User Assigned", "Date Added", "Title", "Client Corporation", "Salary", "Fee Arrangement",
#                   "Pipeline Value"]
#
#         data = {}
#         previousUser = None
#         for record in return_body:
#             tempRecord = data.get(record["owner"]["firstName"] + " " + record["owner"]["lastName"])
#             if not tempRecord:
#                 tempRecord = []
#                 data = getTotalPipeline(data, previousUser)
#
#             tempRecord.append([
#                 record["owner"]["firstName"] + " " + record["owner"]["lastName"],
#                 datetime.fromtimestamp(int(str(record["dateAdded"])[:-3])),
#                 record["title"],
#                 record["clientCorporation"].get("name"),
#                 record["salary"],
#                 str(float(record["feeArrangement"]) * 100) + "%",
#                 float(record["salary"]) * float(record["feeArrangement"])
#             ])
#             previousUser = record["owner"]["firstName"] + " " + record["owner"]["lastName"]
#
#             data[previousUser] = tempRecord
#         data = getTotalPipeline(data, previousUser)
#
#         nestedList = [titles]
#
#         totalPipelineValue = 0
#         for key, value in data.items():
#             for csvLine in value:
#                 nestedList.append(csvLine)
#             totalPipelineValue += float(value[-1][-1])
#
#         nestedList = [["", "", "", "", "", "Overall Total Pipeline Value", totalPipelineValue]] + nestedList
#
#         return Callback(True, "Report information has been retrieved", nestedList)
#
#     except Exception as exc:
#         helpers.logError("Marketplace.CRM.Mercury.produceRecruiterValueReport() ERROR: " + str(exc))
#         return Callback(False, "Error in creating report")
