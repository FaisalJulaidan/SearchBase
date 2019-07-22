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
CLIENT_ID = os.environ['PRSJOBS_CLIENT_ID']
CLIENT_SECRET = os.environ['PRSJOBS_CLIENT_SECRET']


def testConnection(auth, companyID):

    try:
        print("ATTEMPTING LOGIN")
        print("auth: ")
        print(auth)
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
