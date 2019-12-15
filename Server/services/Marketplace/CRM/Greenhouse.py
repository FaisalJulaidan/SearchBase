import base64
import json

import requests
from sqlalchemy_utils import Currency

from models import Callback, StoredFileInfo
from services import databases_services, stored_file_services
from utilities import helpers


# Greenhouse Notes:
# auth is done by submitting a header "Authorization" with value "Basic " + base64encoded(api token + ":")


def testConnection(auth):
    return login(auth)


# login requires: API key
def login(auth):
    try:
        # encode to base64
        if "Basic" in auth.get("rest_token", ""):
            authorization = auth.get("rest_token")
        else:
            authorization = "Basic " + base64.b64encode((auth.get("api_key") + ":").encode('utf-8')).decode('ascii')

        headers = {"Authorization": authorization, "Content-Type": "application/json"}

        body = {"per_page": 1}

        # get the authorization code
        code_request = requests.get("https://harvest.greenhouse.io/v1/candidates/", headers=headers,
                                    data=json.dumps(body))
        if not code_request.ok:
            raise Exception(code_request.text)

        authCopy = {"rest_token": authorization, "user_id": str(auth.get("user_id"))}

        # Logged in successfully
        return Callback(True, 'Logged in successfully', authCopy)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def sendQuery(auth, query, method, body, optionalParams=None):
    try:
        # get url
        url = buildUrl(query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "Authorization": auth.get("rest_token")}

        if query is not "get":
            headers["On-Behalf-Of"] = auth.get("user_id")

        r = sendRequest(url, method, headers, json.dumps(body))

        if str(r.status_code)[:1] != "2":  # check if error code is in the 200s
            raise Exception("Request to API servers failed with error " + str(r.status_code))

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(query, optionalParams=None):
    # set up initial url
    url = "https://harvest.greenhouse.io/v1/" + query
    # add additional params
    if optionalParams:
        for param in optionalParams:
            url += "&" + param
    # return the url
    return url


def sendRequest(url, method, headers, data=None):
    request = None
    if method is "put":
        request = requests.put(url, headers=headers, data=data)
    elif method is "post":
        request = requests.post(url, headers=headers, data=data)
    elif method is "get":
        request = requests.get(url, headers=headers, data=data)
    return request


# To create a candidate you need to create an application, to create an application: job, to create a job: job template
# def insertCandidate(auth, conversation: Conversation) -> Callback:
#     try:
#         # New candidate details
#         body = {
#             "first_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [" "])[0],
#             "last_name": conversation.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [" "])[-1],
#             "phone_numbers": [],
#             "email_addresses": [],
#             "applications": [{}]  # TODO NEEDS SOMETHING IN HERE...
#         }
#
#         emails = conversation.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [])
#         mobiles = conversation.Data.get('keywordsByDataType').get(DT.CandidateMobile.value['name'], [])
#
#         # does not like value to be ""
#         if conversation.Data.get('keywordsByDataType').get(DT.CandidateCity.value['name'], None):
#             body["addresses"] = [{
#                 "value": "".join(
#                     conversation.Data.get('keywordsByDataType').get(DT.CandidateCity.value['name'], [" "])),
#                 "type": "home"
#             }]
#
#         # add emails
#         for email in emails:
#             body["email_addresses"].append({"value": email, "type": "personal"})
#
#         # add mobile numbers
#         for mobile in mobiles:
#             body["phone_numbers"].append({"value": mobile, "type": "mobile"})
#
#         # send query
#         sendQuery_callback: Callback = sendQuery(auth, "candidates", "post", body)
#
#         if not sendQuery_callback.Success:
#             raise Exception(sendQuery_callback.Message)
#
#         return Callback(True, sendQuery_callback.Data.text)
#
#     except Exception as exc:
#         helpers.logError("CRM.Greenhouse.insertCandidate() ERROR: " + str(exc))
#         return Callback(False, str(exc))


def uploadFile(auth, storedFileInfo: StoredFileInfo):
    try:
        conversation = storedFileInfo.Conversation

        if not conversation.CRMResponse:
            raise Exception("Can't upload file for record with no CRM Response")
        # storedFile.
        file_callback = stored_file_services.downloadFile(storedFileInfo.AbsFilePath)
        if not file_callback.Success:
            raise Exception(file_callback.Message)
        file = file_callback.Data
        file_content = file.get()["Body"].read()
        file_content = base64.b64encode(file_content).decode('ascii')

        body = {
            "filename": storedFileInfo.FilePath,
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
        helpers.logError("CRM.Greenhouse.insertCandidate() ERROR: " + str(exc))
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
        for record in return_body:
            result.append(databases_services.createPandaCandidate(id=record.get("id"),
                                                                  name=record.get("first_name", "") +
                                                                       record.get("last_name", ""),
                                                                  email=
                                                                  getValue(record.get("email_addresses"), "value"),
                                                                  mobile=
                                                                  getValue(record.get("phone_numbers"), "value"),
                                                                  location=
                                                                  getValue(record.get("addresses"), "value") or "",
                                                                  skills=None,
                                                                  linkdinURL=None,
                                                                  availability=None,
                                                                  preferredJobTitle=None,
                                                                  education=
                                                                  getValue(record.get("educations"), "degree"),
                                                                  yearsExperience=0,
                                                                  desiredSalary=0,
                                                                  currency=Currency("GBP"),
                                                                  source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getValue(variable, objectName):
    if variable:
        return variable[0].get(objectName)
    else:
        return None


def searchJobs(auth) -> Callback:
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
        result = []
        for record in return_body:
            if record.get("confidential", True):
                continue

            min_salary = record.get("custom_fields", {}).get("salary_range", {}).get("min_value", 0)
            max_salary = record.get("custom_fields", {}).get("salary_range", {}).get("max_value", 0)
            mid_salary = min_salary + ((max_salary - min_salary) / 2)

            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("name"),
                                                            desc=record.get("notes", ""),  # are these public?
                                                            location="london",  # use office location name?
                                                            type=record.get("custom_fields", {}).get("employment_type"),
                                                            salary=mid_salary,
                                                            essentialSkills=None,
                                                            yearsRequired=0,
                                                            startDate=None,
                                                            endDate=None,
                                                            linkURL=None,
                                                            currency=
                                                            record.get("custom_fields", {}).get("salary_range", {}).get(
                                                                "unit"),
                                                            source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllCandidates(auth) -> Callback:
    try:
        body = {
            "per_page": 500,
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidates", "get", body)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        result = []
        for record in return_body:
            result.append(databases_services.createPandaCandidate(id=record.get("id"),
                                                                  name=record.get("first_name", "") +
                                                                       record.get("last_name", ""),
                                                                  email=
                                                                  getValue(record.get("email_addresses"), "value"),
                                                                  mobile=
                                                                  getValue(record.get("phone_numbers"), "value"),
                                                                  location=
                                                                  getValue(record.get("addresses"), "value") or "",
                                                                  skills=None,
                                                                  linkdinURL=None,
                                                                  availability=None,
                                                                  preferredJobTitle=None,
                                                                  education= getValue(record.get("educations"), "degree"),
                                                                  yearsExperience=0,
                                                                  desiredSalary=0,
                                                                  currency=Currency("GBP"),
                                                                  source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.getAllCandidates() ERROR: " + str(exc))
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
        result = []
        for record in return_body:
            if record.get("confidential", True):
                continue

            min_salary = record.get("custom_fields", {}).get("salary_range", {}).get("min_value", 0)
            max_salary = record.get("custom_fields", {}).get("salary_range", {}).get("max_value", 0)
            mid_salary = min_salary + ((max_salary - min_salary) / 2)

            result.append(databases_services.createPandaJob(id=record.get("id"),
                                                            title=record.get("name"),
                                                            desc=record.get("notes", ""),  # are these public?
                                                            location="london",  # use office location name?
                                                            type=record.get("custom_fields", {}).get("employment_type"),
                                                            salary=mid_salary,
                                                            essentialSkills=None,
                                                            yearsRequired=0,
                                                            startDate=None,
                                                            endDate=None,
                                                            linkURL=None,
                                                            currency=
                                                            record.get("custom_fields", {}).get("salary_range", {}).get(
                                                                "unit"),
                                                            source="Greenhouse"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Greenhouse.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))
