import requests
from models import Callback, ChatbotSession
import json
import logging
from enums import DataType as DT


def login(auth):
    try:
        url =  "https://developerconnection.adaptondemand.com/WebApp/api/domains/" + auth['domain'] + "/logon"
        headers = {'Content-Type': 'application/json'}

        # Send request
        del auth['domain'] # because Adapt doesn't require this in the auth POST request
        r = requests.post(url, headers=headers, data=json.dumps(auth))



        # When not ok
        if not r.ok: raise Exception(r.text)

        # Logged in successfully
        return Callback(True, 'Logged in successfully', r.json()['SID'])

    except Exception as exc:
        logging.error("CRM.Adapt.login() ERROR: " + str(exc)
                      + " Username: " + auth.get('username', 'Unknown')
                      + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, str(exc))


def insertCandidate(auth, session: ChatbotSession) -> Callback:
    try:
        callback: Callback = login(auth)
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
                "FIRST_NAME": " ".join(session.Data.get('keywordsByDataType')
                                       .get(DT.CandidateName.value['name'], "Unavailable - TSB")),
                "LAST_NAME": " ",
                "SALUTATION": " "
            },
            "EMAIL": [
                {
                    "OCC_ID": "Home",
                    "EMAIL_ADD": session.Data.get('keywordsByDataType')
                                     .get(DT.CandidateEmail.value['name'], ["Unavailable@TSB.com"])[0]
                }
            ],
            "TELEPHONE": [
                {
                    "OCC_ID": "Mobile",
                    "TEL_NUMBER": session.Data.get('keywordsByDataType')
                        .get(DT.CandidateLocation.value['name'], ["Unavailable - TSB"])[0]
                }
            ],
            "ADDRESS": [{
                "OCC_ID": "Primary",
                "STREET1": " ".join(session.Data.get('keywordsByDataType')
                                    .get(DT.CandidateLocation.value['name'], "Unavailable - TSB")),
            }],
        }

        # Send request
        r = requests.post(url, headers=headers, data= json.dumps(body))

        # When not ok
        if not r.ok: raise Exception

        return Callback(True, 'Candidate inserted successfully')

    except Exception as exc:
        logging.error("CRM.Adapt.insertCandidate() ERROR: " + str(exc)
                      + " Username: " + auth.get('username', 'Unknown')
                      + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, 'Cannot insert candidate')


def insertClient(auth, session: ChatbotSession) -> Callback:
    try:
        callback: Callback = login(auth)
        if not callback.Success:
            return callback

        url =  "https://developerconnection.adaptondemand.com/WebApp/api/v1/companies"
        headers = {'Content-Type': 'application/json', 'x-adapt-sid': callback.Data }

        # New candidate details
        body = {
            "CLIENT_GEN": {
                "CLIENT_TYPE": 8252178,
                "NAME":" ".join(session.Data.get('keywordsByDataType')
                                .get(DT.ClientName.value['name'], "Unavailable - TSB"))
            },
            "TELEPHONE": [
                {
                    "OCC_ID": "Work",
                    "TEL_NUMBER": session.Data.get('keywordsByDataType')
                        .get(DT.ClientTelephone.value['name'], ["Unavailable - TSB"])[0]
                }
            ],
            "ADDRESS": [{
                "OCC_ID": "Primary",
                "STREET1": " ".join(session.Data.get('keywordsByDataType')
                                    .get(DT.ClientLocation.value['name'], "Unavailable - TSB")),
            }],
            "NOTES": " ".join(session.Data.get('keywordsByDataType')
                             .get(DT.ClientEmail.value['name'], "Unavailable - TSB")),
        }

        # Send request
        r = requests.post(url, headers=headers, data= json.dumps(body))

        # When not ok
        if not r.ok: raise Exception

        return Callback(True, 'Client inserted successfully')

    except Exception as exc:
        logging.error("CRM.Adapt.insertClient() ERROR: " + str(exc)
                      + " Username: " + auth.get('username', 'Unknown')
                      + " Domain: " + auth.get('domain', 'Unknown'))
        return Callback(False, 'Cannot insert client')