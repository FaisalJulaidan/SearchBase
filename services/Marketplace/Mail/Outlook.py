import json
import logging
import os

import requests

from models import Callback

from services.Marketplace import marketplace_helpers as helpers

# Client ID and secret
client_id = os.environ['OUTLOOK_CLIENT_ID']
client_secret = os.environ['OUTLOOK_CLIENT_SECRET']


def login(auth):
    try:
        print("auth", auth)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "https://www.thesearchbase.com/api/outlook_callback",
            "code": auth.get("code")
        }

        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)

        return Callback(True, "Success",
                        {
                            "access_token": result_body.get("access_token"),
                            "refresh_token": result_body.get("refresh_token"),
                            "id_token": result_body.get("id_token"),
                        })

    except Exception as exc:
        print("ERROR:", exc)
        logging.error("CRM.Outlook.login() ERROR: " + str(exc))
        return Callback(False, "Error in logging you in. Please try again")


def retrieveAccessToken(auth, companyID):
    try:

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "https://www.thesearchbase.com/api/outlook_callback",
            "refresh_token": auth.get("refresh_token")
        }

        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=json.dumps(body))
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)
        
        if result_body.get("refresh_token"):
            auth = dict(auth)
            auth["refresh_token"] = result_body.get("refresh_token")  

        saveAuth_callback: Callback = helpers.saveNewMailAuth(auth, "Outlook", companyID)
        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, "Access Token retrieved", auth)

    except Exception as exc:
        print("ERROR:", exc)
        logging.error("CRM.Outlook.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


# def sendQuery(auth, query, method, body, companyID, optionalParams=None):
#     try:
#         # get url
#         url = buildUrl(auth, query, optionalParams)
#
#         # set headers
#         headers = {'Content-Type': 'application/json'}
#
#         # test the BhRestToken (rest_token)
#         r = helpers.sendRequest(url, method, headers, json.dumps(body))
#         if r.status_code == 401:  # wrong rest token
#             callback: Callback = retrieveRestToken(auth, companyID)
#             if callback.Success:
#                 url = buildUrl(callback.Data, query, optionalParams)
#
#                 r = helpers.sendRequest(url, method, headers, json.dumps(body))
#                 if not r.ok:
#                     raise Exception(r.text + ". Query could not be sent")
#             else:
#                 raise Exception("Rest token could not be retrieved")
#         elif not r.ok:
#             raise Exception("Rest url for query is incorrect")
#
#         return Callback(True, "Query was successful", r)
#
#     except Exception as exc:
#         logging.error("CRM.Bullhorn.sendQuery() ERROR: " + str(exc))
#         return Callback(False, str(exc))
#
#
# def buildUrl(rest_data, query, optionalParams=None):
#     # set up initial url
#     url = rest_data.get("rest_url", "https://rest91.bullhornstaffing.com/rest-services/5i3n9d/") + query + \
#           "?BhRestToken=" + rest_data.get("rest_token", "none")
#     # add additional params
#     if optionalParams:
#         for param in optionalParams:
#             url += "&" + param
#     # return the url
#     return url

