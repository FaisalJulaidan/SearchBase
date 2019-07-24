import base64
import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, StoredFile, CRM as CRM_Model
from services import stored_file_services, databases_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from utilities import helpers
from utilities.enums import DataType as DT, Period

CLIENT_ID = os.environ['MERCURY_CLIENT_ID']
CLIENT_SECRET = os.environ['MERCURY_CLIENT_SECRET']

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
            "redirect_uri": helpers.getDomain() + "/dashboard/marketplace/Mercury",
            "code": auth.get("code")
        }

        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)
        print(result_body)
        return Callback(True, "Success",
                        {
                            "access_token": result_body.get("access_token"),
                            "refresh_token": result_body.get("refresh_token"),
                            "id_token": result_body.get("id_token"),
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
        url = buildUrl(query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer " + auth.get("access_token")}

        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))

        if r.status_code == 401:  # wrong access token
            callback: Callback = retrieveAccessToken(auth, companyID)
            if not callback.Success:
                raise Exception(callback.Message)

            headers["Authorization"] = "Bearer " + callback.Data.get("access_token")
            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            if not r.ok and not r.status_code == 409:
                raise Exception(r.text + ". Query could not be sent")

        elif not r.ok and not r.status_code == 409:
            raise Exception(r.text + ". Unexpected error occurred when calling the API")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("Marketplace.Crm.Bullhorn.sendQuery() ERROR: " + str(exc))
        return Callback(False, "Query could not be sent")


def buildUrl(query, optionalParams=None):
    # set up initial url
    url = "https://graph.microsoft.com/v1.0/me/" + query
    # add additional params
    if optionalParams:
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

            "name": conversation.Name or " ",
            "firstName": helpers.getListValue(name, 0, " "),
            "lastName": helpers.getListValue(name, 1, " "),
            "mobile": conversation.PhoneNumber or " ",
            "address": {
                "city": "".join(
                    conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [" "])),
            },
            "email": conversation.Email or " ",
            "primarySkills": "".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], [" "])),
            "educations": {
                "data": conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'], [])
            },
            "salary": str(crm_services.getSalary(conversation, DT.CandidateDesiredSalary, Period.Annually))
        }

        # Add additional emails to email2 and email3
        for email in emails:
            index = emails.index(email)
            if index != 0:
                body["email" + str(index + 1)] = email

        if body.get("dayRate") == 0:
            body["dayRate"] = None

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/Candidate", "put", body,
                                                 conversation.Assistant.CompanyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
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

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "file/" + entity + "/" + entityID,
                                                 "put", body, conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClient(auth, conversation: Conversation) -> Callback:
    try:
        # get query url
        insertCompany_callback: Callback = insertCompany(auth, conversation)
        if not insertCompany_callback.Success:
            raise Exception(insertCompany_callback.Message)

        insertClient_callback: Callback = insertClientContact(auth, conversation,
                                                              insertCompany_callback.Data.get("changedEntityId"))
        if not insertClient_callback.Success:
            raise Exception(insertClient_callback.Message)

        return Callback(True, insertClient_callback.Message)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(auth, conversation: Conversation, bhCompanyID) -> Callback:
    try:
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])

        body = {
            "name": conversation.Name or " ",
            "mobile": conversation.PhoneNumber or " ",
            "address": {
                "city": " ".join(
                    conversation.Data.get('keywordsByDataType').get(DT.ClientLocation.value['name'], [])),
            },
            # check number of emails and submit them
            "email": emails[0],
            "clientCorporation": {"id": bhCompanyID}
        }

        # add additional emails to email2 and email3
        for email in emails:
            index = emails.index(email)
            if index != 0:
                body["email" + str(index + 1)] = email

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/ClientContact", "put", body,
                                                 conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCompany(auth, conversation: Conversation) -> Callback:
    try:
        # New candidate details
        body = {
            "name": " ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CompanyName.value['name'],
                                                                ["Undefined Company - TSB"])),
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/ClientCorporation", "put", body,
                                                 conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, conversation, fields=None) -> Callback:
    try:
        query = "query="
        if not fields:
            fields = "fields=id,name,email,mobile,address,primarySkills,status,educations,dayRate,salary"
        keywords = conversation['keywordsByDataType']

        # populate filter
        query += checkFilter(keywords, DT.CandidateLocation, "address.city")

        # if keywords[DT.CandidateSkills.value["name"]]:
        #     query += "primarySkills.data:" + keywords[DT.CandidateSkills.name] + " or"

        salary = crm_services.getSalary(conversation, DT.CandidateDesiredSalary, Period.Annually)
        if salary:
            query += " salary:" + str(salary) + " or"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                 [fields, query, "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        result = []
        for record in return_body["data"]:
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("name"),
                                                                  email=record.get("email"),
                                                                  mobile=record.get("mobile"),
                                                                  location=record.get("address", {}).get("city") or "",
                                                                  skills="".join(
                                                                      record.get("primarySkills", {}).get("data")),
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education="".join(
                                                                      record.get("educations", {}).get("data")),
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get("salary") or
                                                                                record.get("dayRate", 0) * 261,
                                                                  currency=Currency("GBP"),
                                                                  payPeriod=Period("Annually"),
                                                                  source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, conversation, fields=None) -> Callback:
    try:
        query = "query="
        if not fields:
            fields = "fields=id,title,publicDescription,address,employmentType,salary,skills,yearsRequired,startDate,dateEnd"
        keywords = conversation['keywordsByDataType']

        # populate filter TODO
        query += checkFilter(keywords, DT.JobTitle, "title")

        query += checkFilter(keywords, DT.JobLocation, "address.city")

        query += checkFilter(keywords, DT.JobType, "employmentType")

        salary = crm_services.getSalary(conversation, DT.JobSalary, Period.Annually)
        if salary > 0:
            query += "salary:" + str(salary) + " or"

        query += checkFilter(keywords, DT.JobDesiredSkills, "skills")

        query += checkFilter(keywords, DT.JobStartDate, "startDate")

        query += checkFilter(keywords, DT.JobEndDate, "dateEnd")

        query += checkFilter(keywords, DT.JobYearsRequired, "yearsRequired")

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 4:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 [fields, query, "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)
        result = []
        # not found match for JobLinkURL
        for record in return_body["data"]:
            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("title"),
                                                            desc=record.get("publicDescription", ""),
                                                            location=record.get("address", {}).get("city"),
                                                            type=record.get("employmentType"),
                                                            salary=record.get("salary"),
                                                            essentialSkills=record.get("skills", {}).get("data"),
                                                            desiredSkills=None,
                                                            yearsRequired=record.get("yearsRequired", 0),
                                                            startDate=record.get("startDate"),
                                                            endDate=record.get("dateEnd"),
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            payPeriod=Period("Annually"),
                                                            source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def checkFilter(keywords, dataType: DT, string):
    if keywords.get(dataType.value["name"]):
        return string + ":" + "".join(keywords[dataType.value["name"]]) + " or"
    return ""


def searchJobsCustomQuery(auth, companyID, query, fields=None) -> Callback:
    try:

        if not fields:
            fields = "fields=id,title,publicDescription,address,employmentType,salary,skills,yearsRequired,startDate,dateEnd"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 [fields, query, "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllCandidates(auth, companyID, fields=None) -> Callback:
    try:
        # custom fields?
        if not fields:
            fields = "fields=id,name,email,mobile,address,primarySkills,status,educations,dayRate"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "departmentCandidates", "get", {}, companyID, [fields])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllJobs(auth, companyID, fields=None) -> Callback:
    try:
        # custom fields?
        if not fields:
            fields = "fields=*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 [fields, "query=*:*", "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def produceRecruiterValueReport(crm: CRM_Model, companyID) -> Callback:
    try:

        getJobs_callback: Callback = searchJobsCustomQuery(
            crm.Auth, companyID,
            "query=employmentType:\"permanent\" AND status:\"accepting candidates\"",
            "fields=dateAdded,title,clientCorporation,salary,feeArrangement,owner")
        if not getJobs_callback.Success:
            raise Exception("Jobs could not be retrieved")

        def extractName(json):
            return int(json["owner"]["id"])

        return_body = getJobs_callback.Data["data"]
        return_body.sort(key=extractName, reverse=True)

        def getTotalPipeline(result, previousUser):
            if len(result.keys()) > 0:
                totalPipeline = 0
                for pRecord in result[previousUser]:
                    totalPipeline += float(pRecord[-1])
                result[previousUser].append(["", "", "", "", "", previousUser + " Total Pipeline Value",
                                             totalPipeline])
            return result

        titles = ["User Assigned", "Date Added", "Title", "Client Corporation", "Salary", "Fee Arrangement",
                  "Pipeline Value"]

        data = {}
        previousUser = None
        for record in return_body:
            tempRecord = data.get(record["owner"]["firstName"] + " " + record["owner"]["lastName"])
            if not tempRecord:
                tempRecord = []
                data = getTotalPipeline(data, previousUser)

            tempRecord.append([
                record["owner"]["firstName"] + " " + record["owner"]["lastName"],
                datetime.fromtimestamp(int(str(record["dateAdded"])[:-3])),
                record["title"],
                record["clientCorporation"].get("name"),
                record["salary"],
                str(float(record["feeArrangement"]) * 100) + "%",
                float(record["salary"]) * float(record["feeArrangement"])
            ])
            previousUser = record["owner"]["firstName"] + " " + record["owner"]["lastName"]

            data[previousUser] = tempRecord
        data = getTotalPipeline(data, previousUser)

        nestedList = [titles]

        totalPipelineValue = 0
        for key, value in data.items():
            for csvLine in value:
                nestedList.append(csvLine)
            totalPipelineValue += float(value[-1][-1])

        nestedList = [["", "", "", "", "", "Overall Total Pipeline Value", totalPipelineValue]] + nestedList

        return Callback(True, "Report information has been retrieved", nestedList)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.produceRecruiterValueReport() ERROR: " + str(exc))
        return Callback(False, "Error in creating report")
