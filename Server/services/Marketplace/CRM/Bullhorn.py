import base64
import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, db, CRM as CRM_Model, StoredFileInfo
from services import databases_services, stored_file_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from services.Marketplace.marketplace_helpers import convertSkillsToString

from utilities import helpers
from utilities.enums import DataType as DT, Period, CRM

"""
Bullhorn Notes:
 access_token (used to generate rest_token) lasts 10 minutes, needs to be requested by using the auth from the client
 refresh_token (can be used to generate access_token) - generated with access_token on auth, ...
 ... expires after 1 use (new one comes in), no time limit
 BhRestToken (rest_token) (used to verify users when making queries), expires in 10 minutes
 submitting a new candidate has no required* fields
 auth needs to contain auth data + rest_token, rest_url, access_token, refresh_token (retrieved upon connecting)
 
Auth = 
 {
    "access_token": "91:184cd487-b4b0-4114-be56-67f70f50d358",
    "refresh_token": "91:260a1587-41fd-4c2b-9769-0356049554f3"
 }
"""

CLIENT_ID = os.environ['BULLHORN_CLIENT_ID']
CLIENT_SECRET = os.environ['BULLHORN_CLIENT_SECRET']


def testConnection(auth, companyID):
    try:
        if auth.get("refresh_token"):
            callback: Callback = retrieveRestToken(auth, companyID)
        else:
            callback: Callback = login(auth)

        if not callback.Success:
            raise Exception("Testing failed")

        return Callback(True, 'Logged in successfully', callback.Data)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


def login(auth):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/json'}
        helpers.logError(str(authCopy))
        test_request = requests.get("https://www.thesearchbase.com/api/marketplace/simple_callback?test=yes")
        helpers.logError(str(test_request.text))
        test_request = requests.post("https://www.thesearchbase.com/api/marketplace/simple_callback?test=yes")
        helpers.logError(str(test_request.text))
        test_request = requests.put("https://www.thesearchbase.com/api/marketplace/simple_callback?test=yes")
        helpers.logError(str(test_request.text))
        code_url = "https://auth-emea.bullhornstaffing.com/oauth/authorize?" + \
                           "&response_type=code" + \
                           "&redirect_uri=https://www.thesearchbase.com/api/marketplace/simple_callback" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&action=Login" + \
                           "&username=" + authCopy.get("username") + \
                           "&password=" + authCopy.get("password")

        helpers.logError("SENDING REQUEST " + code_url)
        code_request = requests.post(code_url, timeout=15)
        helpers.logError("text 1: " + str(code_request.text))

        if not code_request.ok:
            raise Exception(code_request.text)

        access_token_url = "https://auth-emea.bullhornstaffing.com/oauth/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=https://www.thesearchbase.com/api/marketplace/simple_callback" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + code_request.text.split("'code', '")[1].split("'), ('client_id'")[0]

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)
        helpers.logError("text 2: " + str(access_token_request.text))

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        authCopy["refresh_token"] = result_body.get("refresh_token")
        helpers.logError(str(authCopy))

        # Logged in successfully
        return Callback(True, 'Logged in successfully', authCopy)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(auth, companyID):
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(auth, "logout", "get", {}, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)
    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.logout() ERROR: " + str(exc))
        return Callback(False, str(exc))


# acquired by using access_token, which can be generated by auth or by refresh_token
def retrieveRestToken(auth, companyID):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/json'}

        # use refresh_token to generate access_token and refresh_token
        url = "https://auth-emea.bullhornstaffing.com/oauth/token?grant_type=refresh_token&client_id=" + CLIENT_ID + \
              "&client_secret=" + CLIENT_SECRET + "&refresh_token=" + authCopy.get("refresh_token")

        if os.environ['FLASK_ENV'] != "production":
            url = url.replace("auth-emea.", "auth9.")

        get_access_token = requests.post(url, headers=headers)
        helpers.logError("BULLHORN TESTING BUG CompID" + str(companyID) + ", CODE: " + str(get_access_token.status_code) +
                         ", TEXT: " + get_access_token.text)

        if get_access_token.status_code == 400:
            login_callback: Callback = login(authCopy)
            if not login_callback.Success:
                raise Exception(login_callback.Message)

            url = url.split("&refresh_token=")[0] + "&refresh_token=" + login_callback.Data["refresh_token"]
            get_access_token = requests.post(url, headers=headers)

        if get_access_token.ok:
            result_body = json.loads(get_access_token.text)
            access_token = result_body["access_token"]
            authCopy["refresh_token"] = result_body["refresh_token"]
        else:
            raise Exception(get_access_token.text)

        url = "https://rest.bullhornstaffing.com/rest-services/login?version=*&" + \
              "access_token=" + access_token

        get_rest_token = requests.put(url, headers=headers)
        if not get_rest_token.ok:
            raise Exception(get_rest_token.text)
        result_body = json.loads(get_rest_token.text)

        authCopy["rest_token"] = result_body.get("BhRestToken")
        authCopy["rest_url"] = result_body.get("restUrl")

        saveAuth_callback: Callback = crm_services.updateByType(CRM.Bullhorn, authCopy, companyID)
        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, 'Rest Token Retrieved', {
            "rest_token": authCopy["rest_token"],
            "rest_url": authCopy.get("rest_url"),
            "refresh_token": authCopy["refresh_token"]
        })

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.CRM.Bullhorn.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, "Failed to retrieve CRM tokens. Please check login information")


# create query url and also tests the BhRestToken to see if it still valid, if not it generates a new one and new url
def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = buildUrl(auth, query, optionalParams)

        if os.environ['FLASK_ENV'] != "production":
            url = url.replace("rest.", "rest9.")

        # set headers
        headers = {'Content-Type': 'application/json'}

        # test the BhRestToken (rest_token)
        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))

        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveRestToken(auth, companyID)
            if not callback.Success:
                raise Exception("Rest token could not be retrieved")

            url = buildUrl(callback.Data, query, optionalParams)

            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            if not r.ok:
                raise Exception(r.text + ". Query could not be sent")

        elif not r.ok:
            raise Exception("Query failed with error code " + str(r.status_code))

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(rest_data, query, optionalParams=None):
    # set up initial url
    url = rest_data.get("rest_url", "https://rest.bullhornstaffing.com/rest-services/5i3n9d/") + query + \
          "?BhRestToken=" + rest_data.get("rest_token", "none")
    # add additional params
    if optionalParams:
        for param in optionalParams:
            url += "&" + param
    # return the url
    return url


def insertCandidate(auth, data, companyID) -> Callback:
    try:
        # availability, yearsExperience
        body = {
            "name": data.get("name"),
            "firstName": data.get("firstName"),
            "lastName": data.get("lastName"),
            "mobile": data.get("mobile"),
            "address": {
                "city": data.get("city"),
            },
            "email": data.get("email"),

            # "primarySkills": data.get("skills"),
            "experience": data.get("yearsExperience"),

            "secondaryAddress": {
                "city": data.get("preferredWorkCity"),
            },

            "educationDegree": data.get("educations"),
            "dateAvailable": data.get("availability"),  # TODO CHECK

            "salary": data.get("annualSalary"),
            "dayRate": data.get("dayRate"),

            "comments": crm_services.additionalCandidateNotesBuilder(
                {
                    "preferredJobTitle": data.get("preferredJobTitle"),
                    "preferredJobType": data.get("preferredJobType"),
                    "yearsExperience": data.get("yearsExperience"),
                    "skills": data.get("skills")
                }, data.get("selectedSolutions")
            )
        }

        # Add additional emails to email2 and email3
        emails = data.get("emails")
        for email in emails:
            index = emails.index(email)
            if index != 0:
                body["email" + str(index + 1)] = email

        if body.get("dayRate") == 0:
            body["dayRate"] = None

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/Candidate", "put", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def uploadFile(auth, storedFileInfo: StoredFileInfo):
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

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "file/" + entity + "/" + entityID,
                                                 "put", body, conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClient(auth, data, companyID) -> Callback:
    try:
        # get query url
        insertCompany_callback: Callback = insertCompany(auth, data, companyID)
        if not insertCompany_callback.Success:
            raise Exception(insertCompany_callback.Message)

        insertClient_callback: Callback = insertClientContact(auth, data, companyID,
                                                              insertCompany_callback.Data.get("changedEntityId"))
        if not insertClient_callback.Success:
            raise Exception(insertClient_callback.Message)

        return Callback(True, insertClient_callback.Message)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(auth, data, companyID, bhCompanyID) -> Callback:
    try:

        body = {
            "name": data.get("name"),
            "mobile": data.get("mobile"),
            "address": {
                "city": data.get("city"),
            },
            # check number of emails and submit them
            "email": data.get("email"),
            "clientCorporation": {"id": bhCompanyID}
        }

        # add additional emails to email2 and email3
        emails = data.get("name")
        for email in emails:
            index = emails.index(email)
            if index != 0:
                body["email" + str(index + 1)] = email

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/ClientContact", "put", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCompany(auth, data, companyID) -> Callback:
    try:
        # New candidate details
        body = {
            "name": data.get("companyName"),
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/ClientCorporation", "put", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


def updateCandidate(auth, data, companyID) -> Callback:
    try:
        # availability, yearsExperience
        body = {
            "id": data.get("id"),
            "name": data.get("name"),
            "firstName": data.get("firstName"),
            "lastName": data.get("lastName"),
            "mobile": data.get("mobile"),
            "address": {
                "city": data.get("city"),
            },
            "email": data.get("email"),

            # "primarySkills": data.get("skills"),
            "experience": data.get("yearsExperience"),

            "secondaryAddress": {
                "city": data.get("preferredWorkCity"),
            },

            "educationDegree": data.get("educations"),
            "dateAvailable": data.get("availability"),  # TODO CHECK

            "salary": data.get("annualSalary"),
            "dayRate": data.get("dayRate"),

            "comments": crm_services.additionalCandidateNotesBuilder(
                {
                    "preferredJobTitle": data.get("preferredJobTitle"),
                    "preferredJobType": data.get("preferredJobType"),
                    "yearsExperience": data.get("yearsExperience"),
                    "skills": data.get("skills")
                }, data.get("selectedSolutions")
            )
        }

        # Add additional emails to email2 and email3
        emails = data.get("emails")
        for email in emails:
            index = emails.index(email)
            if index != 0:
                body["email" + str(index + 1)] = email

        if body.get("dayRate") == 0:
            body["dayRate"] = None

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "entity/Candidate/" + str(data["id"]), "post", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, data, fields=None) -> Callback:
    try:
        query = "query="
        if not fields:
            fields = "fields=id,name,email,mobile,address,primarySkills,status,educations,dayRate,salary"

        # populate filter
        query += populateFilter(data.get("location"), "address.city")

        # if keywords[DT.CandidateSkills.value["name"]]:
        #     query += "primarySkills.data:" + keywords[DT.CandidateSkills.name] + " or"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=status:Available"
        else:
            query += "&status:Available"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                 [fields, query, "count=500"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)
        result = []
        # TODO educations uses ids - need to retrieve them
        for record in return_body["data"]:
            if record.get("dayRate"):
                payPeriod = Period("Daily")
            else:
                payPeriod = Period("Annually")
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("name"),
                                                                  email=record.get("email"),
                                                                  mobile=record.get("mobile"),
                                                                  location=record.get("address", {}).get("city") or "",
                                                                  skills=record.get("primarySkills", {}).get("data"),
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,  #
                                                                  education=None,
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get("salary") or
                                                                                record.get("dayRate", 0),
                                                                  currency=Currency("GBP"),
                                                                  source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchPerfectCandidates(auth, companyID, data, fields=None) -> Callback:
    try:
        query = "query="
        if not fields:
            fields = "fields=id,name,email,mobile,address,primarySkills,status,educations,dayRate,salary"

        # populate filter
        query += populateFilter(data.get("preferredJotTitle"), "occupation")
        query += populateFilter(data.get("location"), "address.city")
        query += populateFilter(data.get("jobCategory"), "employmentPreference")
        # query += populateFilter(data.get("skills"), "primarySkills")
        query += populateFilter(data.get("yearsExperience"), "experience")
        # query += populateFilter(data.get("education"), "educationDegree")

        # if keywords[DT.CandidateSkills.value["name"]]:
        #     query += "primarySkills.data:" + keywords[DT.CandidateSkills.name] + " or"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=status:Available"

            # send query
            sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                     [fields, query, "count=500"])
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            return_body = json.loads(sendQuery_callback.Data.text)

            records = return_body["data"]

        else:
            records = []

            while len(records) < 2000:
                # send query
                sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                         [fields, query, "count=500"])
                if not sendQuery_callback.Success:
                    raise Exception(sendQuery_callback.Message)

                # get query result
                return_body = json.loads(sendQuery_callback.Data.text)

                if return_body["data"]:
                    # add the candidates to the records
                    records = records + list(return_body["data"])

                    # remove duplicate records
                    seen = set()
                    new_l = []
                    for d in records:
                        t = tuple(d.items())
                        if str(t) not in seen:
                            seen.add(str(t))
                            new_l.append(d)

                    records = []
                    for l in new_l:
                        records.append(dict(l))

                # remove the last (least important filter)
                query = "and".join(query.split("and")[:-1])

                # if no filters left - stop
                if not query:
                    break

        result = []
        # TODO educations uses ids - need to retrieve them
        for record in records:
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("name"),
                                                                  email=record.get("email"),
                                                                  mobile=record.get("mobile"),
                                                                  location=record.get("address", {}).get("city") or "",
                                                                  skills=record.get("primarySkills", {}).get("data"),
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education=None,
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get("salary") or
                                                                                record.get("dayRate", 0),
                                                                  currency=Currency("GBP"),
                                                                  source="Bullhorn"))

        return Callback(True, "Search has been successful", result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, data, fields=None) -> Callback:
    try:
        query = "query="
        if not fields:
            fields = "fields=id,title,publicDescription,address,employmentType,salary,skills,yearsRequired,startDate,dateEnd"

        # populate filter TODO
        # query += populateFilter(data.get("jobTitle"), "title")

        query += populateFilter(data.get("city"), "address.city")

        query += populateFilter(data.get("employmentType"), "employmentType")

        # query += populateFilter(data.get("skills"), "skills")

        # query += populateFilter(data.get("startDate"), "startDate")

        # query += populateFilter(data.get("endDate"), "dateEnd")

        # query += populateFilter(data.get("yearsRequired"), "yearsRequired")

        query = query[:-4]

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
                                                            yearsRequired=record.get("yearsRequired", 0),
                                                            startDate=record.get("startDate"),
                                                            endDate=record.get("dateEnd"),
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def populateFilter(value, string):
    if value:
        return string + ":" + value + " and "
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
