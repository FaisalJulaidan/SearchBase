import requests
from models import Callback, ChatbotSession
import json
import logging
from enums import DataType as DT
def login(domain, username, password):
    try:

        url =  "https://developerconnection.adaptondemand.com/WebApp/api/domains/" + domain + "/logon"
        headers = {'Content-Type': 'application/json'}

        # Credentials
        body = {
            "username":username,
            "password":password,
            "profile":"CoreProfile",
            "locale":"en_GB",
            "timezone":"GMT",
            "dateFormat":0,
            "timeFormat":0
        }

        # Send request
        r = requests.post(url, headers=headers, data= json.dumps(body))

        # When not ok
        if not r.ok:
            print("CRM.Adapt.login() Unsuccessful Login: " + r.text)
            logging.error("CRM.Adapt.login() Unsuccessful Login for Username: "
                          + username + " Domain: " + domain + " Error: " + r.text)
            return Callback(False, 'Cannot login to Adapt CRM')

        return Callback(True, 'Logged in successfully', r.json()['SID'])

    except Exception as exc:
        print("CRM.Adapt.login() ERROR: ", exc)
        logging.error("CRM.Adapt.login() ERROR: " + str(exc)
                      + " Username: " + username
                      + " Domain: " + domain)


def insertCandidate(domain, username, password, session: ChatbotSession) -> Callback:
    try:
        callback: Callback = login(domain, username, password)
        if not callback.Success:
            return callback

        url =  "https://developerconnection.adaptondemand.com/WebApp/api/v1/candidates"
        headers = {'Content-Type': 'application/json', 'x-adapt-sid': callback.Data }

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
        if not r.ok:
            print("CRM.Adapt.insertCandidate() Unsuccessful Insertion" + " Error: " + r.text)
            logging.error("CRM.Adapt.insertCandidate() Unsuccessful Insertion for Username: "
                          + username + " Domain: " + domain + " Error: " + r.text)
            return Callback(False, 'Cannot insert candidate')

        print(r.text)
        return Callback(True, 'Candidate inserted successfully')

    except Exception as exc:
        print("CRM.Adapt.insertCandidate() ERROR: ", exc)
        logging.error("CRM.Adapt.insertCandidate() ERROR: " + str(exc)
                      + " Username: " + username
                      + " Domain: " + domain)


def insertClient(domain, username, password, session: ChatbotSession) -> Callback:
    try:
        callback: Callback = login(domain, username, password)
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
        if not r.ok:
            print("CRM.Adapt.insertClient() Unsuccessful Insertion" + " Error: " + r.text)
            logging.error("CRM.Adapt.insertClient() Unsuccessful Insertion for Username: "
                          + username + " Domain: " + domain + " Error: " + r.text)
            return Callback(False, 'Cannot insert client')

        print(r.text)
        return Callback(True, 'Client inserted successfully')

    except Exception as exc:
        print("CRM.Adapt.insertClient() ERROR: ", exc)
        logging.error("CRM.Adapt.insertClient() ERROR: " + str(exc)
                      + " Username: " + username
                      + " Domain: " + domain)