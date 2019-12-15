import base64
import json
import os

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, StoredFileInfo
from services import stored_file_services, databases_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from utilities import helpers
from utilities.enums import DataType as DT, Period

CLIENT_ID = os.environ['MERCURY_CLIENT_ID']
CLIENT_SECRET = os.environ['MERCURY_CLIENT_SECRET']
DYNAMICS_VERSION = "v9.1"

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
    from utilities import helpers
    try:

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": helpers.getDomain(3000) + "/dashboard/marketplace/Mercury",
            "code": auth.get("code"),
            "resource": "https://" + auth.get("state") + ".dynamics.com"
        }

        url = "https://login.microsoftonline.com/common/oauth2/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)

        return Callback(True, "Success",
                        {
                            "access_token": result_body.get("access_token"),
                            "refresh_token": result_body.get("refresh_token"),
                            "id_token": result_body.get("id_token"),
                            "domain": auth.get("state")
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
            "redirect_uri": helpers.getDomain(3000) + "/dashboard/marketplace/Mercury",
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
        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveAccessToken(auth, companyID)
            if not callback.Success:
                raise Exception(callback.Message)

            headers["Authorization"] = "Bearer " + callback.Data.get("access_token")

            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
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
            url += param + "&"
        url = url[:-1]
    # return the url
    return url


def insertCandidate(auth, data, companyID) -> Callback:
    try:
        body = {
            "crimson_firstname": data.get("firstName"),
            "crimson_surname": data.get("lastName"),
            "crimson_mobile": data.get("mobile"),
            "crimson_HomeAddressLine1": data.get("street"),
            "crimson_town": data.get("city"),
            "crimson_Country": data.get("country"),
            "crimson_PostCode": data.get("postCode"),
            "crimson_email": data.get("email"),

            "crimson_workarea": data.get("preferredWorkCity"),
            "crimson_jobtitle": data.get("preferredJobTitle"),

            "crimson_availability": data.get("availability"),

            "crimson_expsalaryp": float(data.get("annualSalary")),
            "crimson_expratec": float(data.get("dayRate")),

            "crimson_candidateselfsummary": crm_services.additionalCandidateNotesBuilder(
                {
                    "yearsExperience": data.get("yearsExperience"),
                    "preferredJobType": data.get("preferredJobType"),
                    "skills": data.get("skills"),
                    "educations": data.get("educations")
                }, data.get("selectedSolutions")
            )
        }

        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "crimson_candidates", "post", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def uploadFile(auth, storedFileInfo: StoredFileInfo):  # TODO
    try:
        conversation = storedFileInfo.Conversation

        if not conversation.CRMResponse:
            raise Exception("Can't upload file for record with no CRM Response")

        file_callback = stored_file_services.downloadFile(storedFileInfo.AbsFilePath)
        if not file_callback.Success:
            raise Exception(file_callback.Message)
        file = file_callback.Data
        file_content = file.get()["Body"].read()
        file_content = base64.b64encode(file_content).decode('ascii')

        body = {
            "externalID": storedFileInfo.ID,
            "fileType": "SAMPLE",
            "name": "TSB_" + storedFileInfo.FilePath,
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


def insertClient(auth, data, companyID) -> Callback:
    try:
        body = {
            "firstname": data.get("firstName"),
            "lastname": data.get("lastName"),
            "address1_city": data.get("city"),
            # check number of emails and submit them
            "emailaddress1": data.get("emails")[0],
            "telephone1": data.get("mobile"),
            "company": data.get("companyName")
        }
        # send filter
        sendQuery_callback: Callback = sendQuery(auth, "contacts", "post", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Mercury.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, data, fields=None) -> Callback:
    try:
        filter = "$filter="
        if not fields:
            fields = "$select=crimson_availability,crimson_currentjobtitle,crimson_email,crimson_expratec,crimson_" + \
                     "expsalaryp,crimson_jobtitle,crimson_mobile,crimson_name,crimson_town," + \
                     "crimson_workpref_permanent,crimson_workpref_temp,mercury_cvurl,_transactioncurrencyid_value"

        # populate filter
        filter += populateFilter(data.get("location"), "crimson_town")

        filter = filter[:-4]

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
                                                                  preferredJobTitle=record.get("crimson_jobtitle"),
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


def searchJobs(auth, companyID, data, fields=None) -> Callback:
    try:
        filter = "$filter="
        if not fields:
            fields = "$select=crimson_addresscity,crimson_jobsummary,crimson_jobtitle,crimson_startdate," + \
                     "crimson_typeofposition,crimson_vacancyid,mercury_permanentsalary_mc," + \
                     "mercury_tempcandidatepay_mc,_mercury_vacancytype_value,_transactioncurrencyid_value"

        # populate filter TODO
        filter += populateFilter(data.get("preferredJobTitle"), "crimson_jobtitle")

        filter += populateFilter(data.get("city"), "crimson_addresscity")

        # filter += populateFilter(keywords, DT.JobType, "employmentType")

        # salary = crm_services.getSalary(conversation, DT.JobSalary, Period.Annually)
        # if salary > 0:
        #     filter += "salary:" + str(salary) + " or"

        # filter += populateFilter(keywords, DT.JobStartDate, "crimson_startdate")

        filter = filter[:-4]

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
        for record in return_body["value"]:
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


def populateFilter(keywords, dataType: DT, string):
    if keywords.get(dataType.value["name"]):
        return "contains(" + string + ", '" + "".join(keywords[dataType.value["name"]]) + "') and "
    return ""


def populateFilter(value, string):
    if value:
        return "contains(" + string + ", '" + value + "') and "
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
