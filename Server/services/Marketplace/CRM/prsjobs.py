import base64
import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, db, CRM as CRM_Model, StoredFile
from services import databases_services, stored_file_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services

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
CLIENT_ID = os.environ['PRSJOBSCLIENT_ID']
CLIENT_SECRET = os.environ['PRSJOBS_CLIENT_SECRET']


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
        helpers.logError("Marketplace.CRM.prsjobs.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


def login(auth):
    try:
        authCopy = dict(auth)
        print("LOGGING IN HERE")
        headers = {'Content-Type': 'application/json'}

        access_token_url = "https://test.salesforce.com/services/oauth2/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=" + helpers.getDomain() + "/dashboard/marketplace/PRSJobs" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + authCopy.get("code")

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        # Logged in successfully
        return Callback(True, 'Logged in successfully', {"refresh_token": result_body.get("refresh_token")})

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def retrieveRestToken(auth, companyID):
    try:
        authCopy = dict(auth)
        headers = {'Content-Type': 'application/json'}

        # use refresh_token to generate access_token and refresh_token
        url = "https://auth.bullhornstaffing.com/oauth/token?grant_type=refresh_token&refresh_token=" + \
              authCopy.get("refresh_token") + \
              "&client_id=" + CLIENT_ID + \
              "&client_secret=" + CLIENT_SECRET
        get_access_token = requests.post(url, headers=headers)

        if get_access_token.ok:
            result_body = json.loads(get_access_token.text)
            access_token = result_body.get("access_token")
            authCopy["refresh_token"] = result_body.get("refresh_token")
        else:
            raise Exception("CRM not set up properly")

        url = "https://rest.bullhornstaffing.com/rest-services/login?version=*&" + \
              "access_token=" + access_token

        get_rest_token = requests.put(url, headers=headers)
        if not get_rest_token.ok:
            raise Exception("Failure in generating rest_token")
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
        return Callback(False, str(exc))

