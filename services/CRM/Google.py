from models import Callback, Calendar, db
from datetime import datetime, timedelta, timezone
from utilities import helpers
import enums
import requests
import os
import dateutil
import json
from sqlalchemy import exc

#todo - csrf - if necessary
#todo - need to get company id automatically


#Gets a new token, and refreshes it if the expiry has passed
def getToken(type, companyID):
    cal = db.session.query(Calendar)\
                    .filter(Calendar.CompanyID == companyID)\
                    .filter(Calendar.Type == type)\
                    .first()
    try:
        expiry = dateutil.parser.parse(cal.Auth['expiry'])
        if expiry < datetime.now():
            resp = requests.post("https://oauth2.googleapis.com/token",
                                 data={
                                     'refresh_token': cal.Auth['refresh'],
                                     'client_secret': os.environ['GOOGLE_CALENDAR_CLIENT_SECRET'],
                                     'client_id': os.environ['GOOGLE_CALENDAR_CLIENT_ID'],
                                     'grant_type': 'refresh_token'
                                 })
            tokenInfo = {
                'expiry': (datetime.now() + timedelta(seconds=resp.json()['expires_in'])).isoformat(),
                'access': resp.json()['access_token'],
                'refresh': cal.Auth['refresh']
            }
            cal.Auth = tokenInfo
            db.session.commit()
            return resp.json()['access_token']
        else:
            return cal.Auth['access']
    except Exception as e:
        print(e)

def authorizeUser(code):
    try:
        resp = requests.post("https://oauth2.googleapis.com/token",
                             data={
                                 'code': code,
                                 'client_secret': os.environ['GOOGLE_CALENDAR_CLIENT_SECRET'],
                                 'client_id': os.environ['GOOGLE_CALENDAR_CLIENT_ID'],
                                 'redirect_uri': os.environ['GOOGLE_CALENDAR_REDIRECT_URI'],
                                 'grant_type': 'authorization_code'
                             })
        if 'error' in resp.json():
            raise Exception(resp.json()['error_description'])
        if 'refresh_token' not in resp.json():
            raise Exception("Please go to https://myaccount.google.com/permissions and reset permissions with our app, then try again")

        #need to get company id automatically
        tokenInfo = {
            'expiry': (datetime.now() + timedelta(seconds=resp.json()['expires_in'])).isoformat(),
            'access': resp.json()['access_token'],
            'refresh': resp.json()['refresh_token']
        }
        cal = Calendar(Auth=tokenInfo, Type=enums.Calendar.Google, CompanyID=2)
        db.session.add(cal)
        db.session.commit()
        return Callback(True, 'User authorized succesfully')
    except exc.IntegrityError as e:
        db.session.rollback()
        return Callback(False, "You already have authorization data relating to your google calendar in the database, please remove these keys first.")
    except Exception as e:
        print(e)
        return Callback(False, str(e))

'''Add event function'''
''' Params
    @companyID - The company ID the calendar relates to
    @eventName - The name of the event, presented on the calendar
    @description - Description of the event, presented on the calendar
    @start - start date of the event (RFC 3339 - SEND WITH TIMEZONE)
    @end - end date of the event (RFC 3339 - SEND WITH TIMEZONE)
'''

def addEvent(companyID, eventName, description, start, end):
    try:
        start = dateutil.parser.parse(start)
        end = dateutil.parser.parse(end)

        token = getToken(enums.Calendar.Google, companyID)
        calendar = db.session.query(Calendar)\
            .filter(Calendar.CompanyID == companyID) \
            .filter(Calendar.Type == enums.Calendar.Google)\
            .first()

        calendarID = None
        if calendar.MetaData is None:
            calendarID = createCalendar(token)
            #copy pre existing data?
            calendar.MetaData = {'calendarID': calendarID}
        else:
            calendarID = calendar.MetaData['calendarID']
            if not verifyCalendarExists(calendarID, token):
                calendarID = createCalendar(token)
                calendar.MetaData = {'calendarID': calendarID}

        db.session.commit()

        headers = {'Authorization': 'Bearer ' + token}
        data = {'summary' : eventName,
                'description': description,
                'start': {'dateTime': start.isoformat()},
                'end': {'dateTime': end.isoformat()}}
        helpers.HPrint(json.dumps(data))
        resp = requests.post("https://www.googleapis.com/calendar/v3/calendars/{}/events".format(calendarID), json=data, headers=headers)
        return Callback(True, 'Successfully added event')
    except Exception as e:
        helpers.HPrint(str(e))


def createCalendar(token):
    try:
        auth = {'Authorization': 'Bearer ' + token}
        data = {'summary' : 'TSB Appointments'}
        resp = requests.post("https://www.googleapis.com/calendar/v3/calendars", json=data, headers=auth)
        if 'error' in resp.json():
            raise Exception(resp.json()["error"])
        return resp.json()['id']
    except Exception as e:
        helpers.HPrint(str(e))

def verifyCalendarExists(id, token):
    try:
        auth = {'Authorization': 'Bearer ' + token}
        resp = requests.get("https://www.googleapis.com/calendar/v3/users/me/calendarList", headers=auth)
        print(resp.json())
        if 'error' in resp.json():
            raise Exception(resp.json()['error'])
        else:
            for item in resp.json()['items']:
                if item['id'] == id:
                    return True
            return False
    except Exception as e:
        helpers.HPrint(str(e))
        return False
