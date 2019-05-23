import json
import logging

import requests
from sqlalchemy import and_

from enums import DataType as DT
from models import Callback, Conversation, db, CRM


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
def login(auth):
    try:
        authCopy = dict(auth)  # we took copy to delete domain later only from the copy

        headers = {'Content-Type': 'application/json'}

        code_url = "https://auth.bullhornstaffing.com/oauth/authorize?" + \
                   "response_type=code" + \
                   "&redirect_uri=https://www.thesearchbase.com/api/bullhorn_callback" + \
                   "&client_id=" + authCopy.get("client_id", "")
        # "&action=Login" + \
        # "&username=" + authCopy.get("username", "") + \
        # "&password=" + urllib.parse.quote(authCopy.get("password", ""))

        # get the authorization code
        code_request = requests.post(code_url, headers=headers)

        if not code_request.ok:
            raise Exception(code_request.text)
        print("HEADERS: ", code_request.headers)
        print("TEXT: ", code_request.text)

        # if length isnt 2 it means the "invalid credentials" log in page has been returned
        if len(code_request.text.split("?code=")) != 2:
            raise Exception("Invalid credentials")

        # retrieve the auth code from the url string
        authorization_code = code_request.text.split("?code=")[1].split("&client_id=")[0]

        access_token_url = "https://auth9.bullhornstaffing.com/oauth/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=https://www.thesearchbase.com/api/bullhorn_callback" + \
                           "&client_id=" + authCopy.get("client_id", "") + \
                           "&client_secret=" + authCopy.get("client_secret", "") + \
                           "&code=" + authorization_code

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        authCopy["access_token"] = result_body.get("access_token")
        authCopy["refresh_token"] = result_body.get("refresh_token")
        authCopy["rest_token"] = ""
        authCopy["rest_url"] = ""

        # Logged in successfully
        return Callback(True, 'Logged in successfully', authCopy)

    except Exception as exc:
        logging.error("CRM.Bullhorn.login() ERROR: " + str(exc))
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
            url = "https://id.vincere.io/oauth2/authorize?"
            body = {
                "grant_type": "refresh_token",
                "refresh_token": authCopy.get("refresh_token"),
                "client_id=": authCopy.get("client_id")
            }

            get_tokens = requests.put(url, headers=headers, data=json.dumps(body))
            if get_tokens.ok:
                result_body = json.loads(get_tokens.text)
                authCopy["access_token"] = result_body.get("access_token")
                authCopy["refresh_token"] = result_body.get("refresh_token")
                authCopy["id_token"] = result_body.get("id_token")
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
        logging.error("CRM.Bullhorn.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))


# create query url and also tests the BhRestToken to see if it still valid, if not it generates a new one and new url
def sendQuery(auth, query, method, body, companyID):
    try:
        # set up initial url
        url = auth.get("rest_url", "https://rest91.bullhornstaffing.com/rest-services/5i3n9d/") + query
        headers = {
            'Content-Type': 'application/json',
            'id-token': auth.get("id_token", "none"),
            'x-api-key': "407d3305547bdd16eeadfdf1aaa56c91"
        }
        print("url 1: ", url)
        # test the id_token
        test = send_request(url, method, headers, json.dumps(body))
        print("test.status_code: ", test.status_code)
        print("test.text: ", test.text)
        if test.status_code == 401:  # wrong rest token
            callback: Callback = retrieveRestToken(auth, companyID)
            if callback.Success:
                url = callback.Data.get("rest_url", "") + "entity/Candidate" + "?BhRestToken=" + \
                      callback.Data.get("rest_token", "")
                print("url 2: ", url)
                r = send_request(url, method, headers, json.dumps(body))
                if not r.ok:
                    raise Exception(r.text + ". Query could not be sent")
            else:
                raise Exception("Id token could not be retrieved")
        elif test.status_code != 400 and test.status_code != 200:  # token correct but no submitted data
            raise Exception("Rest url for query is incorrect")

        return Callback(True, "Query was successful", url)

    except Exception as exc:
        logging.error("CRM.Bullhorn.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def send_request(url, method, headers, data):
    test = None
    if method is "post":
        test = requests.post(url, headers=headers, data=data)
    elif method is "get":
        test = requests.get(url, headers=headers, data=data)
    return test


def insertCandidate(auth, session: Conversation) -> Callback:
    try:
        # New candidate details
        body = {
            "first_name": session.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[0],
            "last_name": session.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[-1],
            "mobile":
                session.Data.get('keywordsByDataType').get(DT.CandidateMobile.value['name'], [""])[0],
            # "address": {
            #     "city": " ".join(
            #         session.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [])),
            # },
            # check number of emails and submit them
            "email": session.Data.get('keywordsByDataType').get(DT.CandidateEmail.value['name'], [""])[0],
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "candidate", "post", body, session.Assistant.CompanyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Message)

    except Exception as exc:
        logging.error("CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClient(auth, session: Conversation) -> Callback:
    try:
        # get query url
        insertCompany_callback: Callback = insertCompany(auth, session)
        if not insertCompany_callback.Success:
            raise Exception(insertCompany_callback.Message)

        insertClient_callback: Callback = insertClientContact(auth, session,
                                                              insertCompany_callback.Data.get("changedEntityId"))
        if not insertClient_callback.Success:
            raise Exception(insertClient_callback.Message)

        return Callback(True, "Client has been added")

    except Exception as exc:
        logging.error("CRM.Bullhorn.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(auth, session: Conversation, bhCompanyID) -> Callback:
    try:
        # New candidate details
        body = {
            "first_name": session.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[0],
            "last_name": session.Data.get('keywordsByDataType').get(DT.CandidateName.value['name'], [""])[-1],
            "mobile":
                session.Data.get('keywordsByDataType').get(DT.ClientTelephone.value['name'], [""])[0],
            # "address": {
            #     "city": " ".join(
            #         session.Data.get('keywordsByDataType').get(DT.ClientLocation.value['name'], [])),
            # },
            # check number of emails and submit them
            "email": session.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [""])[0],
            "company_id": bhCompanyID
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "contact", body, session.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Message)

    except Exception as exc:
        logging.error("CRM.Bullhorn.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCompany(auth, session: Conversation) -> Callback:
    try:
        # New candidate details
        body = {
            "company_name": " ".join(
                session.Data.get('keywordsByDataType').get(DT.CompanyName.value['name'], ["Undefined Company - TSB"])),
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "company", body, session.Assistant.CompanyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Message)

    except Exception as exc:
        logging.error("CRM.Bullhorn.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))
