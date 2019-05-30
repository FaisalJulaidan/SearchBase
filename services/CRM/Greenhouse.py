import base64
import json
import logging

import requests

from enums import DataType as DT
from models import Callback, Conversation, StoredFile
from services import databases_services, stored_file_services


# Greenhouse Notes:
# auth is done by submitting a header "Authorization" with value "Basic " + base64encoded(api token + ":")


# login requires: API key
def login(auth):
    try:
        authCopy = dict(auth)  # we took copy to delete domain later only from the copy

        authorization = "Bearer " + base64.b64encode(authCopy.get("authorization")).decode('ascii')  # encode to base64

        headers = {"Authorization": authorization}

        # get the authorization code
        code_request = requests.get("https://harvest.greenhouse.io/v1/candidates/", headers=headers)

        if not code_request.ok:
            raise Exception(code_request.text)

        authCopy = {"rest_token": authorization}

        # Logged in successfully
        return Callback(True, 'Logged in successfully', authCopy)

    except Exception as exc:
        logging.error("CRM.Greenhouse.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def sendQuery(auth, query, method, body, optionalParams=None):
    try:
        # get url
        url = build_url(query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "Authorization": auth.get("rest_token")}

        # test the BhRestToken (rest_token)
        r = send_request(url, method, headers, json.dumps(body))

        if str(r.status_code)[:1] != "2":  # check if error code is in the 200s
            raise Exception("API token provided is no longer correct")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        logging.error("CRM.Greenhouse.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def build_url(query, optionalParams=None):
    # set up initial url
    url = "https://harvest.greenhouse.io/v1/" + query
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
        body = {
            "first_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[0],
            "last_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[-1],
            "phone_numbers": [],
            "addresses": [{
                "value": "".join(
                    conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [""])),
                "type": "home"
            }],
            "email_addresses": [],
            "applications": []  # TODO NEEDS SOMETHING IN HERE...
        }

        emails = conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [""])
        mobiles = conversation.Data.get('keywordsByDataType').get(DT.CandidateMobile.value['name'], [""])

        # add emails
        for email in emails:
            body["email_addresses"].append({"value": email, "type": "personal"})

        # add mobile numbers
        for mobile in mobiles:
            body["phone_numbers"].append({"value": mobile, "type": "mobile"})

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidates", "post", body)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        logging.error("CRM.Greenhouse.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


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
            "filename": storedFile.FilePath,
            "type": "resume",
            "content": file_content
        }

        conversationResponse = json.loads(conversation.CRMResponse)
        entityID = str(conversationResponse.get("changedEntityId"))  # TODO CHECK RETURN TYPE

        if conversation.UserType.value is "Candidate":
            entity = "candidates"
        else:
            raise Exception("Entity type to submit could not be retrieved")

        # send query
        sendQuery_callback: Callback = sendQuery(auth, entity + "/" + entityID + "/attachments", "post", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        logging.error("CRM.Greenhouse.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth) -> Callback:
    try:
        body = {
            "per_page": 500
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidates", "get", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        result = []
        for record in return_body["data"]:
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("first_name", "") +
                                                                  record.get("last_name", ""),
                                                                  email=
                                                                  record.get("email_addresses", [{}])[0].get("value"),
                                                                  mobile=
                                                                  record.get("phone_numbers", [{}])[0].get("value"),
                                                                  location=
                                                                  record.get("addresses", [{}])[0].get("value"),
                                                                  skills=None,
                                                                  linkdinURL=None,
                                                                  availability=None,
                                                                  jobTitle=None,
                                                                  education=
                                                                  record.get("educations", [{}])[0].get("degree"),
                                                                  yearsExperience=0,
                                                                  desiredSalary=0,
                                                                  currency=None,
                                                                  source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        logging.error("CRM.Greenhouse.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, conversation) -> Callback:
    try:
        keywords = conversation['keywordsByDataType']  # maybe filter by office location name for location

        body = {
            "per_page": 500,
            "status": "open"
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "jobs", "get", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)
        result = []
        for record in return_body["data"]:
            if record.get("confidential", True):
                continue
                
            min_salary = record.get("custom_fields", {}).get("salary_range", {}).get("min_value", 0)
            max_salary = record.get("custom_fields", {}).get("salary_range", {}).get("max_value", 0)
            mid_salary = min_salary + ((max_salary-min_salary) / 2)
            
            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("name"),
                                                            desc=record.get("notes", ""),  # are these public?
                                                            location=None,  # use office location name?
                                                            type=record.get("custom_fields", {}).get("employment_type"),
                                                            salary=mid_salary,
                                                            essentialSkills=None,
                                                            desiredSkills=None,
                                                            yearsRequired=0,
                                                            startDate=None,
                                                            endDate=None,
                                                            linkURL=None,
                                                            currency=
                                                            record.get("custom_fields", {}).get("salary_range", {}).get("unit"),
                                                            source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        logging.error("CRM.Greenhouse.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllCandidates(auth) -> Callback:
    try:
        body = {
            "per_page": 500
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidates", "get", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        logging.error("CRM.Greenhouse.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllJobs(auth) -> Callback:
    try:
        body = {
            "per_page": 500,
            "status": "open"
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "jobs", "get", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        logging.error("CRM.Greenhouse.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))
