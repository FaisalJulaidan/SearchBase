import json

import requests

from utilities.enums import DataType as DT
from models import Callback, Conversation
from utilities import helpers


def testConnection(auth):
    try:
        return Callback(login(auth).Success, "Message", auth)

    except Exception as exc:
        return Callback(False, "Connection test failed")


def login(auth):
    try:
        authCopy = dict(auth)  # we took copy to delete domain later only from the copy
        url = "https://developerconnection.adaptondemand.com/WebApp/api/domains/" \
              + auth.get('domain', 'Unknown') + "/logon"
        headers = {'Content-Type': 'application/json'}

        # Send request
        authCopy.pop('domain', '')  # because Adapt doesn't require this in the auth POST request
        r = requests.post(url, headers=headers, data=json.dumps(authCopy))

        # When not ok
        if not r.ok: return Callback(False, r.json().get('ERROR_MSG', r.text))

        # Logged in successfully
        return Callback(True, 'Logged in successfully', r.json()['SID'])

    except Exception as exc:
        helpers.logError("CRM.Adapt.login() ERROR: " + str(exc)
                         + " Username: " + auth.get('username', 'Unknown')
                         + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, str(exc))


def insertCandidate(auth, data) -> Callback:
    try:
        callback: Callback = login(auth) # callback.Data is the SID used in authorised requests
        if not callback.Success:
            return callback

        url = "https://developerconnection.adaptondemand.com/WebApp/api/v1/candidates"
        headers = {'Content-Type': 'application/json', 'x-adapt-sid': callback.Data}

        # New candidate details
        body = {
            "availableRoles": ["TEMP_CAND", "PERM_CAND"],
            "defaultRole": "TEMP_CAND",
            "PERSON_GEN": {
                "TITLE": 1303812,
                "FIRST_NAME": data.get("firstName"),
                "LAST_NAME": data.get("lastName"),
                "SALUTATION": " "
            },
            "EMAIL": [
                {
                    "OCC_ID": "Home",
                    "EMAIL_ADD": data.get("email")
                }
            ],
            "TELEPHONE": [
                {
                    "OCC_ID": "Mobile",
                    "TEL_NUMBER": data.get("mobile")
                }
            ],
            "ADDRESS": [{
                "OCC_ID": "Primary",
                "STREET1": data.get("street"),
                "TOWN": data.get("city"),
                "POST_CODE": data.get("postCode"),
            }],
        }

        # Send request to insert new candidate
        r = requests.post(url, headers=headers, data=json.dumps(body))

        # When not ok (Error)
        if not r.ok: raise Exception(r.json().get('ERROR_MSG', r.text))

        return Callback(True, r.text)

    except Exception as exc:
        helpers.logError("CRM.Adapt.insertCandidate() ERROR: " + str(exc)
                         + " Username: " + auth.get('username', 'Unknown')
                         + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, str(exc))


def insertClient(auth, data) -> Callback:
    try:
        callback: Callback = login(auth)
        if not callback.Success:
            return callback

        url = "https://developerconnection.adaptondemand.com/WebApp/api/v1/companies"
        headers = {'Content-Type': 'application/json', 'x-adapt-sid': callback.Data}

        # New candidate details
        body = {
            "CLIENT_GEN": {
                "CLIENT_TYPE": 8252178,
                "NAME": data.get("name"),
            },
            "TELEPHONE": [
                {
                    "OCC_ID": "Work",
                    "TEL_NUMBER": data.get("mobile")
                }
            ],
            "ADDRESS": [{
                "OCC_ID": "Primary",
                "STREET1": data.get("city"),
            }],
            "NOTES": data.get("email", "NotProvided@adapt.required"),
        }

        # Send request to insert new client
        r = requests.post(url, headers=headers, data=json.dumps(body))

        # When not ok
        if not r.ok: raise Exception(r.json().get('ERROR_MSG', r.text))

        return Callback(True, r.text)

    except Exception as exc:
        helpers.logError("CRM.Adapt.insertClient() ERROR: " + str(exc)
                         + " Username: " + auth.get('username', 'Unknown')
                         + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, str(exc))
