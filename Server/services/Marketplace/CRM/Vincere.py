import base64
import copy
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
            raise Exception("Connection test failed")

        return Callback(True, 'Logged in successfully', callback.Data)

    except Exception as exc:
        helpers.logError("CRM.Vincere.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


# get auth code, use it to get access token, refresh token and id token
def retrieveRestToken(auth, companyID):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

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
        # auth = {'access_token': 'eyJraWQiOiJlUkZlZVM4WmtUMStVRk9FMkVHT0h2U1prWU82aFE5cEltTHZJUlZPWk4wPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhMWQxZTM2NC1iYzc5LTQ2YzgtOThjYS1jMWNmYTVhY2IzZTkiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6InBob25lIG9wZW5pZCBlbWFpbCIsImF1dGhfdGltZSI6MTU3Mjk1NDE5NCwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfREZzUXA3bTdEIiwiZXhwIjoxNTc2NjAyMzYxLCJpYXQiOjE1NzY1OTg3NjEsInZlcnNpb24iOjIsImp0aSI6ImYxNjM2N2FmLTc4ZjMtNGQ0MC05NDY1LWE0NGQzZTRkNTEyZiIsImNsaWVudF9pZCI6IjdiczgwMGNnZ2JlbGM2ODF1dTUxNzVva2JvIiwidXNlcm5hbWUiOiJhMWQxZTM2NC1iYzc5LTQ2YzgtOThjYS1jMWNmYTVhY2IzZTkifQ.pNtqfokYoakLtxagfOB-uDpZ6Im-ap7Hm4FAm5PEwBRL3nmKetiWH6DsrsjjyVLnFlUiVG9gSb-CJpiq2fA4jPhbG2udSzIBXF81tMK2IQZv6X_hlyz9jgXGK815cb_4ok1S-_F5J8VdC4FeFj5CFT62HWn-2OHzqsmPNc4faC3BsZi2s6dDLHXZnH1FFI4o7FCVLBxFHV1Zk35-OZ3arlu7AugUJF4h-GHsJo8HE_8OAnxEn52ISGsqFvCTza6ZuDWO-CPU2KHbUQqpXVTHHMG5CSJoYzGrBtqlkTL9u9sr9ztsrXQIAU4TLkm6I6yE7b3iwpkaK6T8dWJS-xVWVQ', 'refresh_token': 'eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.S6ZK69WUUzgC2fpcmn1ldetg2J6lOibPLd4p-7_2eb86J2mTnHq10m-Q08IpTdMtogHFHMd7ud8otQfHtmhPwPWJ6i2-zcxOz6cXnP_uxzWiBeFg-2waefoQrs-liwzlvyRjfwcXMd6prwNwKbhudTasusvnOZqWEIG5TK0_Rxe0TJ2j6HyS_DLs-fba0s3XDr9O5M1pEqWy3kp5CgrLYIQtE0E6gTTOTXlKrRAsg3XLGBQ6bo6FPh5nfFIu-_IMYQA_fASoMdLN9lkCGZOsXeTyR84Rm-IU7rlE4bVsBfEuDVEN4SDIp6xRGXpeKYMABLGm47rdqeic6O02R5NVjQ.3LQ5lQJkSjDdNitC.2Hu2huJ4sIS82C3C_a8WlHfRT57GqbQyCiBDjOwzij2HS9hMLxYvwukuRzj5q9oMAYqrg44K5dMLl4eGbTqQBwKEUZjCEcdE5P_IOh_5GqKVvzueXbZo1gISFpDSGLy8Wx9KH0E5w_O8I0pZiF3XAd08IH1015yp8f8VrOLPgKz03NCo00YNgjd0u-j76yogUKc7aZFFBWNxNMVTOCKui3vqG-LL1ebz5iwKIJaqyL1lvNCX_FtDnNJYKFv5qWqc7slQ0p4oRZZKl1bYSt0UitqHmgSCDc9CRvdpohIO6L8SNloS7SdX0_ws3NeL7mslrvJj2i58ucOpV7nzcALvZrQ3SIT8Zt4nyPyRg-4oiX94yEZsjK-zvtRAHIAcqS-Dc2GdN2_YHj602PhFp6gP-K3CZCFsa-Wl7I1CLzXKCvT-LFYhclYJqTBiG0UZR5Fdji8x9tyuOQCyWcbMr_fpwsxzs0FzzHRSk9p49DZzOoOQQg9Wnrh6Ph7ck0w8-YWmTWcdD7_ggog-9-opKW_HHRNehKdmFGmKJOAjaryT90CUYpN2laFA_-828fqBWn2VGVdX145zf7guaCs-THB87gSVzhQaHZZW-TiUkvYfj81oJohxPbfrDcWg_H544A76TEw-44_kbhhImUPIERU0l0LhcTwjHzj4dk8V7dxhFj0gU8Oe6ZzSb4tsim4JMKz9ozwApbOHALlMWW-jkqiAm6-mzrsHJ0-nB8Z3Mtje6hMkRQMk_pqlpiZUbYaR2gNHDGWt3gD7VMq8CEPz-llZXrfc4ZqkcEqlwbYSws5OvvslJumCxIdHMb9o0tWigyUfn-yBHclyCjwMM427RCJcIYh1ciPlpovlfi8rvKanVGUG6Cg8p_ZoVJsLj160_wdXFaXeuU1XEqlwcHmCrWJ6IVADOPcb8zCHmw426xg-Zfsd1WnP5V-i55f-8hsLSaiif4D1cgeb5p8k6J0rdy5gZ7BwSgbsWtS6Vke8HUFO1SCoRjKAdfYr7O3MHJfSjzhK7RyC3j_MgCmXEO7WCWflGKIROB5xHxEItgBzyxz28Cb3wSgeHN5dJjycMl9q-sfZe4ed1jLQENfNGmEbgJfg52OJH9LYrJfdEJQMgt86QSW_Vm9XBvLtFALR3NEkKqcvvIq78Uz_MvAQEwqjPyJSuafbDj4CFO1Y4PrL8ok59__hW76hgMyh7MmjI9cbhV61DC_wLshtxWVz7V4_8DAD1B5eMUmBm5OCVd8cqto.QugFxgUBpPf-duX7Ngd8eg', 'id_token': 'eyJraWQiOiI5bHNyUXBsU1lXWDNXXC9CR0o1UjZWUzFKVmp3TjNMYUtyWjg5NTdMXC9UZlU9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoieE5Wdmh2ZmxBWnlzT2htSWY0ODRKQSIsInN1YiI6ImExZDFlMzY0LWJjNzktNDZjOC05OGNhLWMxY2ZhNWFjYjNlOSIsImF1ZCI6IjdiczgwMGNnZ2JlbGM2ODF1dTUxNzVva2JvIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTcyOTU0MTk0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9ERnNRcDdtN0QiLCJjb2duaXRvOnVzZXJuYW1lIjoiYTFkMWUzNjQtYmM3OS00NmM4LTk4Y2EtYzFjZmE1YWNiM2U5IiwiZXhwIjoxNTc2NjAyMzYxLCJpYXQiOjE1NzY1OTg3NjEsImVtYWlsIjoibS5lc3RlQHRoZXNlYXJjaGJhc2UuY29tIn0.DQ5QzCJ7_BMjSaty3xRWo7_aqFqbDezi9CPXuI9i-flYB1sweGA9jIvFMSHe1-c-LyQMYKr6f0m45uG2_tiyb1-8flwTI7SBJ2ruSgxjdQM1UcLv8tUJDTOumxxSAc4GAA86Ky9v6Ql0TB9i-WtW5wsDl7A7CKP9-njoCFaM1hnBsg-cyiY_B5lEeCVd8O6zEN8rgSiEllHLJuEdUrOqTDlQ0DCjlQq8Zizm9yX-HvUTDrJgPedWOfOx44YFeFY5dKBBZk72LzKYD2ZzxerS2v-Dtmn4E1lFrRSjnVrlpBy4wwi4lGzcThGZFVNfN4V9q_fjJFHTctOHfPeL3Iavww', 'domain': 'thesearchbase'}
        # test = {'Content-Type': 'application/json', 'x-api-key': '0720376f4c8f2853ffff713bb8017627', 'id-token': 'eyJraWQiOiI5bHNyUXBsU1lXWDNXXC9CR0o1UjZWUzFKVmp3TjNMYUtyWjg5NTdMXC9UZlU9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoieE5Wdmh2ZmxBWnlzT2htSWY0ODRKQSIsInN1YiI6ImExZDFlMzY0LWJjNzktNDZjOC05OGNhLWMxY2ZhNWFjYjNlOSIsImF1ZCI6IjdiczgwMGNnZ2JlbGM2ODF1dTUxNzVva2JvIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTcyOTU0MTk0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9ERnNRcDdtN0QiLCJjb2duaXRvOnVzZXJuYW1lIjoiYTFkMWUzNjQtYmM3OS00NmM4LTk4Y2EtYzFjZmE1YWNiM2U5IiwiZXhwIjoxNTc2NjAyMzYxLCJpYXQiOjE1NzY1OTg3NjEsImVtYWlsIjoibS5lc3RlQHRoZXNlYXJjaGJhc2UuY29tIn0.DQ5QzCJ7_BMjSaty3xRWo7_aqFqbDezi9CPXuI9i-flYB1sweGA9jIvFMSHe1-c-LyQMYKr6f0m45uG2_tiyb1-8flwTI7SBJ2ruSgxjdQM1UcLv8tUJDTOumxxSAc4GAA86Ky9v6Ql0TB9i-WtW5wsDl7A7CKP9-njoCFaM1hnBsg-cyiY_B5lEeCVd8O6zEN8rgSiEllHLJuEdUrOqTDlQ0DCjlQq8Zizm9yX-HvUTDrJgPedWOfOx44YFeFY5dKBBZk72LzKYD2ZzxerS2v-Dtmn4E1lFrRSjnVrlpBy4wwi4lGzcThGZFVNfN4V9q_fjJFHTctOHfPeL3Iavww'}
        # api_key = test["x-api-key"]
        # auth["id_token"] = test["id-token"]
        # auth["domain"] = "thesearchbase.vincere.io"

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
        return_body = json.loads(sendQuery_callback.Data.text)  # {"id":0}

        # send additional data
        sendAdditionalQuery_callback: Callback = __updateCandidateAdditionalData(auth, str(return_body["id"]), body,
                                                                                 companyID)
        if not sendAdditionalQuery_callback.Success:
            raise Exception(sendAdditionalQuery_callback.Message)

        return Callback(True, sendAdditionalQuery_callback.Data.text)

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
                                                              insertCompany_callback.Data.get("id"))
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
        # retrieve old record
        sendQuery_callback: Callback = sendQuery(auth, "candidate/" + str(data["id"]), "get", {}, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        oldData = json.loads(sendQuery_callback.Data.text)
        data["oldNote"] = oldData.get("note")  # to add the old note to the new one

        body = dict(oldData, **__extractCandidateInsertBody(data))  # update old data

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate/" + str(data["id"]), "put", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        # send additional data
        sendAdditionalQuery_callback: Callback = __updateCandidateAdditionalData(auth, str(data["id"]), body, companyID)
        if not sendAdditionalQuery_callback.Success:
            raise Exception(sendAdditionalQuery_callback.Message)

        return Callback(True, sendAdditionalQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("CRM.Vincere.updateCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def __updateCandidateAdditionalData(auth, candidateID, body, companyID):
    try:
        helpers.logError(str(body))
        # send location
        if body.get("address") or body.get("city"):
            sendQuery_callback: Callback = sendQuery(auth, "candidate/"+str(candidateID)+"/currentlocation", "put",
                                                     body, companyID)
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

        # send current job
        if body.get("job_title"):
            tempBody = copy.deepcopy(body)
            tempBody["address"] = None
            sendQuery_callback: Callback = sendQuery(auth, "candidate/"+str(candidateID)+"/workexperiences", "post",
                                                     tempBody, companyID)
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

        return Callback(True, "Update Success")

    except Exception as exc:
        helpers.logError("CRM.Vincere.__updateCandidateAdditionalData() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchCandidates(auth, companyID, data) -> Callback:
    try:
        query = "q="

        fields = "fl=id,name,primary_email,mobile,phone,nearest_train_station,skill,desired_salary,currency,deleted,last_update,met_status"

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
            sendQuery_callback: Callback = sendQuery(auth, "candidate/search/" + fields, "get", {}, companyID, [query, "limit=100"])
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            return_body = json.loads(sendQuery_callback.Data.text)
            if return_body.get("result", {}).get("total", 0) > 0 or "," not in query:
                break

            query = ",".join(query.split(",")[:-1]) + "%23"

        result = []
        helpers.logError("RESULTS: " + str(return_body["result"]["items"]))
        for record in return_body["result"]["items"]:
            result.append(__extractCandidateReturnData(record))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("CRM.Vincere.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchPerfectCandidates(auth, companyID, data, perfect=False, shortlist=None) -> Callback:
    try:
        query = "q="

        fields = "fl=id,name,primary_email,mobile,phone,nearest_train_station,skill,skills,desired_salary,currency,deleted,last_update,met_status"

        # populate filter
        query += populateFilter(data.get("location"), "current_city")

        for skill in data.get("skills", []):
            query += populateFilter(skill, "skill")

        query = query.replace("#", ".08")

        query = query[:-1]
        records = []
        start = 0

        while len(records) < 10000:
            query += "%23"
            # send query
            sendQuery_callback: Callback = sendQuery(auth, "candidate/search/" + fields, "get", {}, companyID,
                                                     [query, "limit=100", "start="+str(start)])
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
            start += 100
            if start >= return_body["result"]["total"]:
                query = ",".join(query.split(",")[:-1])
                # if no filters left - stop
                if not query or perfect:
                    break

        result = []
        # TODO educations uses ids - need to retrieve them
        helpers.logError("RESULTS: " + str(records))
        for record in records:
            result.append(__extractCandidateReturnData(record))

        return Callback(True, "Search has been successful", result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Vincere.searchPerfectCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(auth, companyID, data) -> Callback:
    try:
        query = "q="

        fields = "fl=id,job_title,public_description,owners,open_date,salary_to,employment_type,location,currency"

        # populate filter
        # query += populateFilter(data.get("preferredJobTitle"), "job_title")
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
            sendQuery_callback: Callback = sendQuery(auth, "job/search/" + fields, "get", {}, companyID, [query, "limit=100"])
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
            result.append(__extractJobReturnData(record))

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
    helpers.logError("DATA: " + str(data))
    return {
        "first_name": data.get("firstName"),
        "last_name": data.get("lastName"),
        "candidate_source_id": "29093",
        "phone": data.get("mobile"),
        "address": data.get("street"),
        "city": data.get("city"),
        "location_name": data.get("city"),
        "post_code": data.get("postCode"),
        "country": data.get("country"),

        "registration_date": datetime.datetime.now().isoformat()[:23] + "Z",

        "email": data.get("email"),
        "skills": data.get("skills"),
        "education_summary": data.get("educations"),

        "job_title": data.get("currentJobTitle"),
        "current_employer": True,
        "desired_salary": data.get("annualSalary"),
        "desired_contract_rate": data.get("dayRate"),
        "summary": "SUMMARY TEST",

        "experience": str(data.get("yearsExperience")) + " years of experience",
        "availability_start": datetime.datetime.strptime((data.get("availability") or "").split(" ")[0],
                                                         '%d/%m/%Y').isoformat()[:23] + ".000Z",
        "note": crm_services.additionalCandidateNotesBuilder(
            {
                "Preferred Job Title": data.get("preferredJobTitle"),
                "Preferred Job Type": data.get("preferredJobType"),
                "Preferred Work City": data.get("preferredWorkCity"),
                "Skills": data.get("skills"),
                "Submitted Education": data.get("educations"),
                "LinkedIn": data.get("linkedIn")
            },
            data.get("selectedSolutions"),
            data.get("oldNote")
        )
    }


def __extractCandidateReturnData(record):
    return databases_services.createPandaCandidate(id=record.get("id", ""),
                                                   name=record.get("name"),
                                                   email=record.get("primary_email"),
                                                   mobile=record.get("phone") or record.get("mobile"),
                                                   location=
                                                   record.get("nearest_train_station", "").replace(
                                                       "station", ""),
                                                   skills=record.get("skill", "").split(","),  # str list
                                                   linkdinURL=None,
                                                   availability=record.get("status"),
                                                   currentJobTitle=None,
                                                   education=None,
                                                   yearsExperience=0,
                                                   desiredSalary=float(record.get("desired_salary", 0)),
                                                   currency=Currency(
                                                       marketplace_helpers.convertToPandaCurrency(
                                                           record.get("currency", "gbp"))),
                                                   source="Vincere")


def __extractJobReturnData(record):
    return databases_services.createPandaJob(id=record.get("id"),
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
                                                            currency=Currency(
                                                                marketplace_helpers.convertToPandaCurrency(
                                                                    record.get("currency", "gbp"))),
                                                            source="Vincere")
