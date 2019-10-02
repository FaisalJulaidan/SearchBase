import base64
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
# access_token (used to generate rest_token) lasts 10 minutes, needs to be requested by using the auth from the client
# refresh_token (can be used to generate access_token) - generated with access_token on auth, ...
#       ... expires after 1 use (new one comes in), no time limit
# id_token (used to verify users when making queries), expires in 10 minutes(unconfirmed)
# auth needs to contain client_id, redirect_uri, response_type=code (get request)
# token needs client_id, code=auth_code, grant_type=authorization_code (post request)
from utilities import helpers

client_id = os.environ['VINCERE_CLIENT_ID']


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
                            "rest_token": result_body.get("id_token"),
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
        helpers.logError("CRM.Bullhorn.testConnection() ERROR: " + str(exc))
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
            "id_token": authCopy.get("rest_token")
        })

    except Exception as exc:
        db.session.rollback()
        helpers.logError("CRM.Vincere.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))


# create query url and also tests the BhRestToken to see if it still valid, if not it generates a new one and new url
def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = buildUrl(auth, query, optionalParams)
        helpers.logError(url)
        # set headers
        headers = {'Content-Type': 'application/json',
                   "id-token": auth.get("rest_token", "none")}

        # test the BhRestToken (rest_token)
        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
        helpers.logError(str(r.status_code))
        helpers.logError(r.text)
        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveRestToken(auth, companyID)
            if not callback.Success:
                raise Exception("Rest token could not be retrieved")

            url = buildUrl(callback.Data, query, optionalParams)

            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            if not r.ok:
                raise Exception(r.text + ". Query could not be sent")

        elif str(r.status_code)[:1] != "2":  # check if error code is in the 200s
            raise Exception("Rest url for query is incorrect")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("CRM.Vincere.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(rest_data, query, optionalParams=None):
    # set up initial url
    url = "https://" + rest_data.get("domain", "") + ".vincere.io/api/v2" + query
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
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "mobile": data.get("mobile"),
            "address": {
                "city": data.get("city"),
            },
            "email": data.get("email"),
            "skills": data.get("skills"),
            "education_summary": data.get("educations")
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate", "post", body, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


# vincere only takes in candidate documents
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
        helpers.logError("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
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


def searchCandidates(auth, companyID, data) -> Callback:
    try:
        query = "query="

        # populate filter
        query += populateFilter(data.get("location"), "address.city")

        # if keywords[DT.CandidateSkills.value["name"]]:
        #     query += "primarySkills.data:" + keywords[DT.CandidateSkills.name] + "&"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                 ["fields=*", query, "count=9999"])
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
                                                                  desiredSalary=record.get("dayRate", 0) * 365,
                                                                  currency= Currency("GBP"), # TODO
                                                                  source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Vincere.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, data) -> Callback:
    try:
        query = "query="

        # populate filter
        query += populateFilter(data.get("jobTitle"), "title")

        query += populateFilter(data.get("city"), "address.city")

        query += populateFilter(data.get("employmentType"), "employmentType")

        query += populateFilter(data.get("skills"), "skills")

        query += populateFilter(data.get("yearsRequired"), "yearsRequired")

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 4:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 ["fields=*", query, "count=9999"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)
        result = []
        # not found match for JobLinkURL
        for record in return_body["data"]:
            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("title"),
                                                            desc=record.get("publicDescription", "") + " " +
                                                                 record.get("description", ""),
                                                            location=record.get("address", {}).get("city"),
                                                            type=record.get("employmentType"),
                                                            salary=record.get("salary"),
                                                            essentialSkills=record.get("skills", {}).get("data"),
                                                            yearsRequired=record.get("yearsRequired", 0),
                                                            startDate=record.get("startDate"),
                                                            endDate=record.get("dateEnd"),
                                                            linkURL=None,
                                                            currency=Currency('GBP'.upper()),
                                                            source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Vincere.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def populateFilter(value, string):
    if value:
        return string + ":" + value + " or "
    return ""


def getAllCandidates(auth, companyID) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(auth, "departmentCandidates", "get", {}, companyID, ["fields=*"])
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
        sendQuery_callback: Callback = sendQuery(auth, "departmentJobOrders", "get", {}, companyID, ["fields=*"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("CRM.Vincere.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))
