import base64
import datetime
import json
import os

import requests

from utilities.enums import DataType as DT, Period, CRM
from sqlalchemy_utils import Currency
from models import Callback, Conversation, db, StoredFileInfo
from services import stored_file_services, databases_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services

# Vincere Notes:
# access_token (used to generate id_token) lasts 10 minutes, needs to be requested by using the auth from the client
# refresh_token (can be used to generate access_token) - generated with access_token on auth, ...
#       ... expires after 1 use (new one comes in), no time limit
# id_token (used to verify users when making queries), expires in 10 minutes(unconfirmed)
# auth needs to contain client_id, redirect_uri, response_type=code (get request)
# token needs client_id, code=auth_code, grant_type=authorization_code (post request)
from utilities import helpers

client_id = os.environ['VINCERE_CLIENT_ID']
api_key = os.environ['VINCERE_API_KEY']


# login requires: client_id
def login(auth):
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        access_token_url = "https://id.vincere.io/oauth2/token?" + \
                           "&grant_type=authorization_code" + \
                           "&client_id=" + client_id + \
                           "&code=" + auth.get("code")

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        # Logged in successfully
        return Callback(True, 'Logged in successfully',
                        {
                            "access_token": result_body.get("access_token"),
                            "refresh_token": result_body.get("refresh_token"),
                            "id_token": result_body.get("id_token"),
                            "domain": auth.get("state")
                        })

    except Exception as exc:
        helpers.logError("CRM.Vincere.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


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
        helpers.logError("CRM.Vincere.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


# get auth code, use it to get access token, refresh token and id token
def retrieveRestToken(auth, companyID):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # check if refresh_token exists
        # if it does use it to generate access_token and refresh_token
        if authCopy.get("refresh_token"):
            url = "https://id.vincere.io/oauth2/token?"
            body = {
                "grant_type": "refresh_token",
                "refresh_token": authCopy.get("refresh_token"),
                "client_id": client_id
            }

            get_tokens = requests.post(url, headers=headers, data=body)

            if get_tokens.ok:
                result_body = json.loads(get_tokens.text)
                authCopy["access_token"] = result_body["access_token"]
                authCopy["id_token"] = result_body["id_token"]
            else:
                raise Exception("CRM not set up properly")
        # else if not go through login again with the saved auth
        else:
            login_callback: Callback = login(authCopy)
            if not login_callback.Success:
                raise Exception(login_callback.Message)
            authCopy = dict(login_callback.Data)

        saveAuth_callback: Callback = crm_services.updateByType(CRM.Vincere, authCopy, companyID)

        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, 'Id Token Retrieved', {
            "id_token": authCopy.get("id_token")
        })

    except Exception as exc:
        db.session.rollback()
        helpers.logError("CRM.Vincere.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))


def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = buildUrl(auth, query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "x-api-key": api_key, "id-token": auth.get("id_token", "none")}

        # test the Token (id_token)
        helpers.logError("Vincere url: " + url)
        helpers.logError("Vincere headers: " + str(headers))
        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
        helpers.logError("Vincere response text: " + r.text)

        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveRestToken(auth, companyID)
            if not callback.Success:
                raise Exception("Rest token could not be retrieved")

            headers["id-token"] = callback.Data.get("id_token", "none")

            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            if not r.ok:
                raise Exception(r.text + ". Query could not be sent")

        elif not r.ok:
            raise Exception("Query failed with error code " + str(r.status_code))

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("CRM.Vincere.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(rest_data, query, optionalParams=None):
    # set up initial url
    domain = rest_data.get("domain", "")

    domainStart = "https://"
    if "https://" in domain:
        domainStart = ""

    domainEnd = ".vincere.io"
    if ".vincere.io" in domain:
        domainEnd = ""

    url = domainStart + rest_data.get("domain", "") + domainEnd + "/api/v2/" + query

    # add additional params
    if optionalParams:
        url = url + "?"
        for param in optionalParams:
            url += "&" + param.strip()
    # return the url
    return url


def insertCandidate(auth, data, companyID) -> Callback:
    try:
        # availability, yearsExperience
        body = __extractCandidateInsertBody(data)

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate", "post", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


# vincere only takes in candidate documents
def uploadFile(auth, filePath, fileName, conversation):
    try:
        if not conversation.CRMResponse:
            raise Exception("Can't upload file for record with no CRM Response")

        file_callback = stored_file_services.downloadFile(filePath.split("/")[-1])
        if not file_callback.Success:
            raise Exception(file_callback.Message)
        file = file_callback.Data
        file_content = file.get()["Body"].read()
        file_content = base64.b64encode(file_content).decode('ascii')

        conversationResponse = json.loads(conversation.CRMResponse)
        entityID = str(conversationResponse.get("id"))

        body = {
            "original_cv": True,
            "document_type_id": 1,
            "file_name": "TSB_" + fileName,
            "base_64_content": file_content
        }

        if conversation.UserType.value is "Candidate":
            entity = "candidate"
        # elif conversation.UserType.value is "Client":  # Vincere does not have api call for client files
        #     entity = "ClientContact"
        else:
            raise Exception("Entity type to submit could not be retrieved")  # -------------------------------

        # send query
        sendQuery_callback: Callback = sendQuery(auth, entity + "/" + entityID + "/file",
                                                 "post", body, conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.uploadFile() ERROR: " + str(exc))
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
        helpers.logError("CRM.Vincere.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(auth, data, companyID, vincCompanyID) -> Callback:
    try:

        body = {
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "mobile": data.get("mobile"),
            "address": {
                "city": data.get("city"),
            },
            # check number of emails and submit them
            "email": data.get("emails")[0],
            "company_id": vincCompanyID
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "contact", "post", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCompany(auth, data, companyID) -> Callback:
    try:
        # New candidate details
        body = {
            "company_name": data.get("companyName"),
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "company", "post", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("CRM.Vincere.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


def updateCandidate(auth, data, companyID) -> Callback:
    try:
        # availability, yearsExperience
        body = __extractCandidateInsertBody(data)

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate/"+data["id"], "put", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, data) -> Callback:
    try:
        query = "q="

        fields = "fl=id,name,primary_email,mobile,phone,current_location,skill,desired_salary,currency,deleted,last_update,met_status"

        # populate filter
        query += populateFilter(data.get("location"), "current_city")

        for skill in data.get("skills", []):
            query += populateFilter(skill, "skill")

        query = query.replace("#", ".08")

        # check if no conditions submitted
        if len(query) < 3:
            query = ""
        else:
            query = query[:-1]
            query += "%23"

        # send query
        while True:
            sendQuery_callback: Callback = sendQuery(auth, "candidate/search/" + fields, "get", {}, companyID, [query])
            helpers.logError("return_body: " + str(json.loads(sendQuery_callback.Data.text)))
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            return_body = json.loads(sendQuery_callback.Data.text)
            if return_body.get("result", {}).get("total", 0) > 0 or "," not in query:
                break

            query = ",".join(query.split(",")[:-1]) + "%23"

        result = []
        for record in return_body["result"]["items"]:
            currency = record.get("currency", "gbp").lower()
            if currency == "pound":
                currency = "GBP"
            else:
                currency = record.get("currency", "GBP").upper()

            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("name"),
                                                                  email=record.get("primary_email"),
                                                                  mobile=record.get("mobile", record.get("phone")),
                                                                  location=
                                                                  record.get("current_location", {}).get("city", ""),
                                                                  skills=record.get("skill", "").split(","),  # str list
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education=None,
                                                                  yearsExperience=0,
                                                                  desiredSalary=float(record.get("desired_salary", 0)),
                                                                  currency=Currency(currency.upper()),
                                                                  source="Vincere"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Vincere.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchPerfectCandidates(auth, companyID, data) -> Callback:
    try:
        query = "q="

        fields = "fl=id,name,primary_email,mobile,phone,current_location,skill,desired_salary,currency,deleted,last_update,met_status"

        # populate filter
        query += populateFilter(data.get("location"), "current_city")

        for skill in data.get("skills", []):
            query += populateFilter(skill, "skill")

        query = query.replace("#", ".08")

        # check if no conditions submitted
        if len(query) < 3:
            query = ""

            # send query
            sendQuery_callback: Callback = sendQuery(auth, "candidate/search/" + fields, "get", {}, companyID, [query])
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            return_body = json.loads(sendQuery_callback.Data.text)

            records = return_body["result"]["items"]

        else:
            query = query[:-1]
            query += "%23"
            records = []

            while len(records) < 2000:
                # send query
                sendQuery_callback: Callback = sendQuery(auth, "candidate/search/" + fields, "get", {}, companyID,
                                                         [query])
                if not sendQuery_callback.Success:
                    raise Exception(sendQuery_callback.Message)

                # get query result
                return_body = json.loads(sendQuery_callback.Data.text)

                if return_body["result"]["items"]:
                    # add the candidates to the records
                    records = records + list(return_body["result"]["items"])

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
                query = ",".join(query.split(",")[:-1])
                # if no filters left - stop
                if not query:
                    break

        result = []
        # TODO educations uses ids - need to retrieve them
        for record in records:
            currency = record.get("currency", "gbp").lower()
            if currency == "pound":
                currency = "GBP"
            else:
                currency = record.get("currency", "GBP").upper()
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("name"),
                                                                  email=record.get("primary_email"),
                                                                  mobile=record.get("mobile", record.get("phone")),
                                                                  location=record.get("current_location", ""),
                                                                  skills=record.get("skill", ""),  # stringified json
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education=None,
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get("desired_salary", 0),
                                                                  currency=Currency(currency.upper()),
                                                                  source="Vincere"))

        return Callback(True, "Search has been successful", result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Vincere.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, data) -> Callback:
    try:
        query = "q="

        fields = "fl=id,job_title,public_description,owners,open_date,salary_to,employment_type,location,currency"

        # populate filter
        # query += populateFilter(data.get("jobTitle"), "job_title")
        #
        # query += populateFilter(data.get("city"), "address")

        query += populateFilter(data.get("city"), "city")
        helpers.logError("VINCERE SKILLS 1: " + str(data.get("skills")))
        helpers.logError("VINCERE SKILLS 2: " + str((data.get("skills") or [])))
        for skill in (data.get("skills") or []):
            query += populateFilter(skill, "public_description")

        # query += populateFilter(data.get("employmentType"), "employment_type")

        query = query.replace("#", ".08")

        # check if no conditions submitted
        if len(query) < 3:
            query = ""
        else:
            query = query[:-1]
            query += "%23"

        # send query
        while True:
            sendQuery_callback: Callback = sendQuery(auth, "job/search/" + fields, "get", {}, companyID, [query])
            helpers.logError("return_body: " + str(json.loads(sendQuery_callback.Data.text)))
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            return_body = json.loads(sendQuery_callback.Data.text)
            if return_body.get("result", {}).get("total", 0) > 0 or "," not in query:
                break

            query = ",".join(query.split(",")[:-1]) + "%23"

        result = []
        # not found match for JobLinkURL
        for record in return_body["result"]["items"]:
            currency = record.get("currency", "gbp").lower()
            if currency == "pound":
                currency = "GBP"
            else:
                currency = record.get("currency", "GBP").upper()
            helpers.logError("Currency: " + str(currency) + ", is it pound: " + str(currency == "pound"))

            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("job_title"),
                                                            desc=record.get("public_description", ""),
                                                            location=record.get("location", {}).get("city"),
                                                            type=record.get("employment_type"),
                                                            salary=record.get("salary_to"),
                                                            essentialSkills=None,
                                                            yearsRequired=0,
                                                            startDate=record.get("open_date"),
                                                            endDate=record.get("closed_date"),
                                                            linkURL=None,
                                                            currency=Currency(currency.upper()),
                                                            source="Vincere"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Vincere.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def populateFilter(value, string):
    if value:
        return string + ":" + value + ","
    return ""


def getAllCandidates(auth, companyID) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(auth, "departmentCandidates", "get", {}, companyID, [])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("CRM.Vincere.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllJobs(auth, companyID) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(auth, "departmentJobOrders", "get", {}, companyID, [])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("CRM.Vincere.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def __extractCandidateInsertBody(data):
    return {
        "first_name": data.get("firstName"),
        "last_name": data.get("lastName"),
        "candidate_source_id": "29093",
        "mobile": data.get("mobile"),
        "nearest_train_station": data.get("city"),
        "registration_date": datetime.datetime.now().isoformat()[:23] + "Z",
        "email": data.get("email"),
        "skills": data.get("skills"),
        "education_summary": data.get("educations"),
        "desired_salary": data.get("annualSalary"),
        "desired_contract_rate": data.get("dayRate"),
        "experience": str(data.get("yearsExperience")) + " years",
        "note": crm_services.additionalCandidateNotesBuilder(
            {
                "dateAvailable": data.get("availability"),
                "preferredJobTitle": data.get("preferredJobTitle"),
                "preferredJobType": data.get("preferredJobType")
            },
            data.get("selectedSolutions")
        )
    }
