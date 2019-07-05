import json
import os

import requests

from models import Callback
from services.Marketplace import marketplace_helpers
from services.Marketplace.Calendar import calendar_services
from utilities import helpers

CLIENT_ID = os.environ['OUTLOOK_CLIENT_ID']
CLIENT_SECRET = os.environ['OUTLOOK_CLIENT_SECRET']

"""
Event takes in:
 {
     "name": "Event name",
     "description": "What appears in the email as main text",
     "start": "2020-02-02T18:00:00", (start date and time)
     "end": "2020-02-02T19:00:00", (end date and time)
     "attendees": [{
            "email": "evgeniybtonchev@gmail.com",
            "name": "Evgeniy"
     }] (list of objects)
 }
 attendees get emailed to accept the event
 owner of the logged in account automatically gets the event in their calendar without having to accept
"""

def testConnection(auth, companyID):
    try:
        if auth.get("refresh_token"):
            return retrieveAccessToken(auth, companyID)
        elif auth.get("code"):
            return login(auth)
        else:
            return Callback(False, "Parameters for connection were not provided")

    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Outlook.testConnection() ERROR: " + str(exc))
        return Callback(False, "Error in testing connection")


def login(auth):
    from utilities import helpers
    try:

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": helpers.getDomain() + "/dashboard/marketplace/Outlook",
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
        helpers.logError("Marketplace.Calendar.Outlook.login() ERROR: " + str(exc))
        return Callback(False, "Error in logging you in. Please try again")


def retrieveAccessToken(auth, companyID):
    from utilities import helpers
    try:
        auth = dict(auth)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": helpers.getDomain() + "/dashboard/marketplace/Outlook",
            "refresh_token": auth.get("refresh_token")
        }

        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        get_access_token = requests.post(url, headers=headers, data=body)
        if not get_access_token.ok:
            raise Exception(get_access_token.text)

        result_body = json.loads(get_access_token.text)

        auth["access_token"] = result_body.get("access_token")
        if result_body.get("refresh_token"):
            auth["refresh_token"] = result_body.get("refresh_token")

        saveAuth_callback: Callback = calendar_services.updateByType("Outlook", auth, None, companyID)
        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, "Access Token retrieved", auth)

    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Outlook.retrieveAccessToken() ERROR: " + str(exc))
        return Callback(False, "Could not retrieve access token")


def sendQuery(auth, query, method, body, companyID, optionalParams=None):
    try:
        # get url
        url = buildUrl(query, optionalParams)

        # set headers
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer " + auth.get("access_token")}

        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))

        if r.status_code == 401:  # wrong access token
            callback: Callback = retrieveAccessToken(auth, companyID)
            if not callback.Success:
                raise Exception(callback.Message)

            headers["Authorization"] = "Bearer " + callback.Data.get("access_token")
            r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
            if not r.ok and not r.status_code == 409:
                raise Exception(r.text + ". Query could not be sent")

        elif not r.ok and not r.status_code == 409:
            raise Exception(r.text + ". Unexpected error occurred when calling the API")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Bullhorn.sendQuery() ERROR: " + str(exc))
        return Callback(False, "Query could not be sent")


def buildUrl(query, optionalParams=None):
    # set up initial url
    url = "https://graph.microsoft.com/v1.0/me/" + query
    # add additional params
    if optionalParams:
        for param in optionalParams:
            url += "&" + param
    # return the url
    return url


def getCalendars(auth, companyID):
    try:

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "calendars", "get", {}, companyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        result_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Data.text, result_body)
    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Outlook.getCalendars() ERROR: " + str(exc))
        return Callback(False, "Could not retrieve calendars")


def addCalendar(auth, companyID):
    try:
        body = {
            "Name": "TheSearchBase"
        }

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "calendars", "post", body, companyID)
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        if sendQuery_callback.Data.status_code == 409:  # calendar already exists - needs to be retrieved
            calendars_callback: Callback = getCalendars(auth, companyID)
            if not calendars_callback.Success:
                raise Exception(calendars_callback.Message)

            record = helpers.objectListContains(calendars_callback.Data["value"],
                                                lambda x: x["name"] == "TheSearchBase")

            if not record:
                raise Exception("Could not get the existing TheSearchBase calendar")
            calendarID = record["id"]
        else:  # calendar was created
            result_body = json.loads(sendQuery_callback.Data.text)
            calendarID = result_body["Id"]

        update_callback: Callback = calendar_services.updateByType("Outlook",
                                                                   auth,
                                                                   {"calendarID": str(calendarID)},
                                                                   companyID)
        if not update_callback.Success:
            raise Exception(update_callback.Message)

        return Callback(True, sendQuery_callback.Data.text, update_callback.Data)

    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Outlook.addCalendar() ERROR: " + str(exc))
        return Callback(False, "Could not add calendar")


def addEvent(calendar, eventDetails):
    try:
        if not calendar.MetaData.get("companyID"):
            createCalendar_callback: Callback = addCalendar(calendar.Auth, calendar.CompanyID)
            if not createCalendar_callback.Success:
                raise Exception(createCalendar_callback.Message)
            calendar = createCalendar_callback.Data

        body = {
            "Subject": eventDetails.get("name"),
            "Body": {
                "ContentType": "HTML",
                "Content": eventDetails.get("description")
            },
            "Start": {
                "DateTime": eventDetails.get("start"),  # "2014-02-02T18:00:00"
                "TimeZone": "Pacific Standard Time"
            },
            "End": {
                "DateTime": eventDetails.get("end"),  # "2014-02-02T19:00:00"
                "TimeZone": "Pacific Standard Time"
            },
            "Attendees": []
        }

        for attendee in eventDetails.get("attendees"):
            body["Attendees"].append({
                "EmailAddress": {
                    "Address": attendee.get("email"),
                    "Name": attendee.get("name", "Name Unknown")
                },
                "Type": "Required"
            })

        # send query
        sendQuery_callback: Callback = sendQuery(calendar.Auth,
                                                 "calendars/" + str(
                                                     calendar.MetaData["calendarID"]) + "/events",
                                                 "post", body, calendar.CompanyID)

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)
    except Exception as exc:
        helpers.logError("Marketplace.Calendar.Outlook.addEvent() ERROR: " + str(exc))
        return Callback(False, "Adding the event failed")
