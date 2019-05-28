import base64
import json
import logging

import requests
from sqlalchemy import and_

from enums import DataType as DT
from models import Callback, Conversation, db, CRM, StoredFile


# Vincere Notes:
# access_token (used to generate rest_token) lasts 10 minutes, needs to be requested by using the auth from the client
# refresh_token (can be used to generate access_token) - generated with access_token on auth, ...
#       ... expires after 1 use (new one comes in), no time limit
# id_token (used to verify users when making queries), expires in 10 minutes(unconfirmed)
# auth needs to contain client_id, redirect_uri, response_type=code (get request)
# token needs client_id, code=auth_code, grant_type=authorization_code (post request)

# To Do: login and token refresh
# To Test: inserting


# login requires: client_id
from services import stored_file_services, databases_services


def login(auth):
    try:
        authCopy = dict(auth)  # we took copy to delete domain later only from the copy

        headers = {'Content-Type': 'application/json'}

        code_url = "https://" + authCopy.get("domain", "") + ".vincere.io/api/v2/oauth2/authorize?" + \
                   "response_type=code" + \
                   "&redirect_uri=https://www.thesearchbase.com/api/bullhorn_callback" + \
                   "&CLIENT_ID=" + authCopy.get("client_id", "")
        # "&action=Login" + \
        # "&username=" + authCopy.get("username", "") + \
        # "&password=" + urllib.parse.quote(authCopy.get("password", ""))

        # get the authorization code
        code_request = requests.get(code_url, headers=headers)

        if not code_request.ok:
            raise Exception(code_request.text)
        print("HEADERS: ", code_request.headers)
        print("TEXT: ", code_request.text)

        # if length isnt 2 it means the "invalid credentials" log in page has been returned
        if len(code_request.text.split("?code=")) != 2:  # TODO
            raise Exception("Invalid credentials")

        # retrieve the auth code from the url string
        authorization_code = code_request.text.split("?code=")[1].split("&client_id=")[0]  # TODO

        access_token_url = "https://" + authCopy.get("domain", "") + ".vincere.io/api/v2/oauth2/authorize?" + \
                           "&grant_type=authorization_code" + \
                           "&client_id=" + authCopy.get("client_id", "") + \
                           "&code=" + authorization_code

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        authCopy["access_token"] = result_body.get("ACCESS_TOKEN")
        authCopy["refresh_token"] = result_body.get("REFRESH_TOKEN")
        authCopy["rest_token"] = result_body.get("ID_TOKEN")

        # Logged in successfully
        return Callback(True, 'Logged in successfully', authCopy)

    except Exception as exc:
        logging.error("CRM.Vincere.login() ERROR: " + str(exc))
        print(exc)
        return Callback(False, str(exc))


# get auth code, use it to get access token, refresh token and id token
def retrieveRestToken(auth, companyID):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # check if refresh_token exists
        # if it does use it to generate access_token and refresh_token
        if authCopy.get("refresh_token"):
            url = "https://" + authCopy.get("domain", "") + ".vincere.io/api/v2/oauth2/authorize?"
            body = {
                "grant_type": "refresh_token",
                "refresh_token": authCopy.get("refresh_token"),
                "CLIENT_ID=": authCopy.get("client_id")
            }

            get_tokens = requests.put(url, headers=headers, data=json.dumps(body))
            if get_tokens.ok:
                result_body = json.loads(get_tokens.text)
                authCopy["access_token"] = result_body.get("ACCESS_TOKEN")
                authCopy["refresh_token"] = result_body.get("REFRESH_TOKEN")
                authCopy["id_token"] = result_body.get("ID_TOKEN")
            else:
                raise Exception("CRM not set up properly")
        # else if not go through login again with the saved auth
        else:
            login_callback: Callback = login(authCopy)
            if not login_callback.Success:
                raise Exception(login_callback.Message)
            authCopy = dict(login_callback.Data)

        # done here as cannot import crm_services while it is importing Vincere.py
        crm = db.session.query(CRM).filter(and_(CRM.CompanyID == companyID, CRM.Type == "Vincere")).first()
        crm.Auth = dict(authCopy)
        db.session.commit()

        return Callback(True, 'Id Token Retrieved', {
            "id_token": authCopy.get("rest_token")
        })

    except Exception as exc:
        db.session.rollback()
        logging.error("CRM.Vincere.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))


# create query url and also tests the BhRestToken to see if it still valid, if not it generates a new one and new url
def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = build_url(auth, query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json'}

        # test the BhRestToken (rest_token)
        r = send_request(url, method, headers, json.dumps(body))

        if r.status_code == 401:  # wrong rest token
            callback: Callback = retrieveRestToken(auth, companyID)
            if callback.Success:
                url = build_url(callback.Data, query, optionalParams)

                r = send_request(url, method, headers, json.dumps(body))
                if not r.ok:
                    raise Exception(r.text + ". Query could not be sent")
            else:
                raise Exception("Rest token could not be retrieved")
        elif str(r.status_code)[:1] != "2":  # check if error code is in the 200s
            raise Exception("Rest url for query is incorrect")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        logging.error("CRM.Vincere.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def build_url(rest_data, query, optionalParams=None):
    # set up initial url
    url = "https://" + rest_data.get("domain", "") + ".vincere.io/api/v2" + query + \
          "?id_token=" + rest_data.get("rest_token", "none")
    # add additional params
    if optionalParams:
        for param in optionalParams:
            url += "&" + param
    # return the url
    return url


def send_request(url, method, headers, data=None):
    request = None
    if method is "put":
        request = requests.put(url, headers=headers, data=data)
    elif method is "post":
        request = requests.post(url, headers=headers, data=data)
    elif method is "get":
        request = requests.get(url, headers=headers, data=data)
    return request


def insertCandidate(auth, conversation: Conversation) -> Callback:
    try:
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [""])

        # availability, yearsExperience
        body = {
            "first_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[0],
            "last_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[-1],
            "mobile":
                conversation.Data.get('keywordsByDataType').get(DT.CandidateMobile.value['name'], [""])[0],
            "address": {
                "city": "".join(
                    conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [""])),
            },
            "email": emails[0],
            "skills": "".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], [""])),
            "education_summary": "".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'], [])),
            "desired_salary":
                conversation.Data.get('keywordsByDataType').get(DT.CandidateDesiredSalary.value['name'], [0])[0]
        }

        if body.get("desired_salary") == 0:
            body["desired_salary"] = None

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate", "post", body,
                                                 conversation.Assistant.CompanyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        logging.error("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


# vincere only takes in candidate documents
def uploadFile(auth, storedFile: StoredFile):
    try:
        conversation = storedFile.Conversation

        if not conversation.CRMResponse:
            raise Exception("Can't upload file for record with no CRM Response")

        file_callback = stored_file_services.downloadFile(storedFile.FilePath)
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
        # elif conversation.UserType.value is "Client":  # Vincere does not have api call for client files
        #     entity = "ClientContact"
        else:
            raise Exception("Entity type to submit could not be retrieved")

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "file/" + entity + "/" + entityID,
                                                 "put", body, conversation.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        logging.error("CRM.Vincere.insertCandidate() ERROR: " + str(exc))
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
        logging.error("CRM.Vincere.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(auth, conversation: Conversation, bhCompanyID) -> Callback:
    try:
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [""])

        body = {
            "name": " ".join(
                conversation.Data.get('keywordsByDataType').get(DT.ClientName.value['name'], [])),
            "mobile":
                conversation.Data.get('keywordsByDataType').get(DT.ClientTelephone.value['name'], [""])[0],
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
        logging.error("CRM.Vincere.insertClientContact() ERROR: " + str(exc))
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
        logging.error("CRM.Vincere.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, conversation) -> Callback:
    try:
        query = "query="
        keywords = conversation['keywordsByDataType']

        # populate filter
        if keywords.get(DT.CandidateLocation.value["name"]):
            query += "address.city:" + "".join(keywords[DT.CandidateLocation.value["name"]]) + " or"

        # if keywords[DT.CandidateSkills.value["name"]]:
        #     query += "primarySkills.data:" + keywords[DT.CandidateSkills.name] + "&"

        if keywords.get(DT.CandidateDesiredSalary.value["name"]):
            query += " dayRate:" + str((float(keywords[DT.CandidateDesiredSalary.value["name"]]) / 365)) + " or"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/Candidate", "get", {}, companyID,
                                                 ["fields=*", query, "count=99999999"])
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
                                                                  currency=None,
                                                                  source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        logging.error("CRM.Vincere.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, conversation) -> Callback:
    try:
        query = "query=*:*"
        keywords = conversation['keywordsByDataType']

        # populate filter
        if keywords.get(DT.JobTitle.value["name"]):
            query += "title:" + "".join(keywords[DT.JobTitle.value["name"]]) + " or"

        if keywords.get(DT.JobLocation.value["name"]):
            query += "address.city:" + "".join(keywords[DT.JobLocation.value["name"]]) + " or"

        if keywords.get(DT.JobType.value["name"]):
            query += "employmentType:" + "".join(keywords[DT.JobType.value["name"]]) + " or"

        if keywords.get(DT.JobSalary.value["name"]):
            query += "salary:" + "".join(keywords[DT.JobSalary.value["name"]]) + " or"

        if keywords.get(DT.JobDesiredSkills.value["name"]):
            query += "skills:" + "".join(keywords[DT.JobDesiredSkills.value["name"]]) + " or"

        if keywords.get(DT.JobStartDate.value["name"]):
            query += "startDate:" + "".join(keywords[DT.JobStartDate.value["name"]]) + " or"

        if keywords.get(DT.JobEndDate.value["name"]):
            query += "dateEnd:" + "".join(keywords[DT.JobEndDate.value["name"]]) + " or"

        if keywords.get(DT.JobYearsRequired.value["name"]):
            query += "yearsRequired:" + "".join(keywords[DT.JobYearsRequired.value["name"]]) + " or"

        query = query[:-3]

        # check if no conditions submitted
        if len(query) < 6:
            query = "query=*:*"

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "search/JobOrder", "get", {}, companyID,
                                                 ["fields=*", query, "count=99999999"])
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
                                                            desiredSkills=None,
                                                            yearsRequired=record.get("yearsRequired", 0),
                                                            startDate=record.get("startDate"),
                                                            endDate=record.get("dateEnd"),
                                                            linkURL=None,
                                                            currency=None,
                                                            source="Bullhorn"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        logging.error("CRM.Vincere.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllCandidates(auth, companyID) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(auth, "departmentCandidates", "get", {}, companyID, ["fields=*"])
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        logging.error("CRM.Vincere.getAllCandidates() ERROR: " + str(exc))
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
        logging.error("CRM.Vincere.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))
