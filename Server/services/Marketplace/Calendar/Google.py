import json
import os
from datetime import datetime, timedelta

import dateutil
import requests
from models import Callback, Calendar, db
from sqlalchemy import exc
from utilities import helpers, enums
from services import appointment_services
from models import Appointment, Conversation, Company, Assistant, User
from datetime import datetime, timezone
import dateutil
import grequests
from hashids import Hashids
from config import BaseConfig


hashids = Hashids(salt=BaseConfig.HASH_IDS_SALT, min_length=5)

# TODO - csrf - if necessary
# TODO - need to get company id automatically


# Gets a new token, and refreshes it if the expiry has passed
def getToken(type, companyID, test=False):
    cal = db.session.query(Calendar) \
        .filter(Calendar.CompanyID == companyID) \
        .filter(Calendar.Type == type) \
        .first()

    if cal is None:
        return None
    try:
        expiry = dateutil.parser.parse(cal.Auth['expiry'])
        if expiry < datetime.now() or test==True:
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
        return None
        
def testConnection(auth, companyID: int):
    try:
        if 'refresh' in auth:
          token = getToken(enums.Calendar.Google, companyID, True)
          return Callback(True, 'Succesfully connected') if token is not None else Callback(False, 'Connection test failed')
        elif 'code' in auth:
          return authorizeUser(auth['code'], companyID)
    except: 
        helpers.logError("Google.testConnection(): " + str(exc))
        return Callback(False, "Google test failed")

def authorizeUser(code, companyID: int):
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
            raise Exception(
                "Please go to https://myaccount.google.com/permissions and reset permissions with our app, then try again")

        # need to get company id automatically
        tokenInfo = {
            'expiry': (datetime.now() + timedelta(seconds=resp.json()['expires_in'])).isoformat(),
            'access': resp.json()['access_token'],
            'refresh': resp.json()['refresh_token']
        }
        return Callback(True, 'User authorized successfully', tokenInfo)
    except exc.IntegrityError as e:
        db.session.rollback()
        return Callback(False,
                        "You already have authorization data relating to your google calendar in the database, please remove these keys first.")
    except Exception as e:
        return Callback(False, str(e))

def sync(companyID):
    try:
        token = getToken(enums.Calendar.Google, companyID)
        if token is None:
            return Callback(False, "Calendar needs to be set up before it is synced")
        calendarID = getCalendar(companyID)
        syncAppointments(calendarID, token, companyID)
        return Callback(False, "Calendar succesfully synced")
    except Exception as exc:
        helpers.logError("Google.sync(): " + str(exc))
        return Callback(False, "Calendar sync failed")

def getCalendar(companyID):
    try:
        token = getToken(enums.Calendar.Google, companyID)
        calendar = db.session.query(Calendar) \
            .filter(Calendar.CompanyID == companyID) \
            .filter(Calendar.Type == enums.Calendar.Google) \
            .first()

        calendarID = None
        if calendar.MetaData is None:
            calendarID = createCalendar(token)
            # copy pre existing data?
            calendar.MetaData = {'calendarID': calendarID}
            db.session.commit()
        else:
            calendarID = calendar.MetaData['calendarID']
            if not verifyCalendarExists(calendarID, token):
                calendarID = createCalendar(token)
                calendar.MetaData = {'calendarID': calendarID}
                db.session.commit()
        return calendarID
    except Exception as exc:
        helpers.logError("Google.getCalendar(): " + str(exc))


def syncAppointments(calendarID, token, companyID):
    try:
        headers = {'Authorization': 'Bearer ' + token}
        eventURL = "https://www.googleapis.com/calendar/v3/calendars/{}/events".format(calendarID)

        eventList = requests.get(eventURL, headers=headers)

        appointments = db.session.query(Appointment).join(Conversation).join(Assistant).join(Company).filter(Company.ID == companyID).all()
        user: User = db.session.query(User).join(Company).filter(Company.ID == companyID).first()

        #TODO: Encode

        events = {}
        for event in eventList.json()['items']:
            if event['description'].startswith("A_ID"):
                desc = event['description'].split("<br>")
                appointmentDetails = desc[0].split(".")
                aid = hashids.decrypt(appointmentDetails[1])[0]
                events[aid] = {'id': event['id'], 'status': appointmentDetails[2]}

        requestList = []
        removeList = []
        ignoreList = []

        for key, val in events.items():
            valid = False
            for appointment in appointments:
                if (appointment.Status == enums.Status.Accepted or appointment.Status == enums.Status.Rejected) and val['status'] == "1":
                    ignoreList.append(key)
                    continue
                elif appointment.Status == enums.Status.Pending and val['status'] == "0":
                    ignoreList.append(key)
                    continue
                if key == appointment.ID:
                    valid = True
                    continue
            if valid == False:
                removeList.append(val['id'])


        for appointment in appointments:
            if appointment.ID in ignoreList:
                print("ignore")
                continue
            eventID = None
            if appointment.ID in events:
                eventID = events[appointment.ID]
            appointmentToken = appointment_services.generateEmailUrl(appointment.ID) if appointment.Status == enums.Status.Pending else None
            appointmentStatus = "Appointment pending approval " if appointment.Status.value == enums.Status.Pending.value else "Appointment "
            eventTitle = appointmentStatus + "with {}".format(appointment.Conversation.Name)
            
            id = hashids.encrypt(appointment.ID)
            #TODO: Needs to change to whatever environment is using
            appointmentURL = "http://localhost:3000/appointment_status?token={}".format(appointmentToken)
            status = 0 if appointment.Status.value == enums.Status.Pending.value else 1
            eventDetails = "A_ID.{}.{}".format(id, status)

            if appointment.Status.value == enums.Status.Pending.value:
              eventDesc = "{}<br><a href='{}'>Accept Appointment</a>".format(eventDetails, appointmentURL)
            else:
              eventDesc = "{}<br>Appointment accepted".format(eventDetails)
            
            
            data = { 
                'summary': eventTitle,
                'description': eventDesc,
                'start': {
                    'dateTime': appointment.DateTime.astimezone().isoformat(),
                    'timeZone': user.TimeZone
                },
                'end': {
                    'dateTime': appointment.DateTime.astimezone().isoformat(),
                    'timeZone': user.TimeZone
                }
            }

            requestList.append({'data': data, 'eventID': eventID})

        rs = []
        for request in requestList:
            if request['eventID'] is None:
                rs.append(grequests.post(eventURL, headers=headers, json=request['data']))
            else:
                rs.append(grequests.patch(eventURL+ "/" + request['eventID'], headers=headers, json=request['data']))

        for request in removeList:
            rs.append(grequests.delete(eventURL + "/" + request, headers=headers))

        grequests.map(rs)

        
        # GET https://www.googleapis.com/calendar/v3/calendars/calendarId/events

        

        # rs = (grequests.post(u, json=formattedData) for u in requestList)
        # grequests.map(rs, exception_handler=handleExceptions)
    except Exception as exc:
        helpers.logError("Google.syncAppointments(): " + str(exc))



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
        calendarID = getCalendar(companyID, token)

        headers = {'Authorization': 'Bearer ' + token}
        data = {'summary': eventName,
                'description': description,
                'start': {'dateTime': start.isoformat()},
                'end': {'dateTime': end.isoformat()}}
        helpers.HPrint(json.dumps(data))
        resp = requests.post("https://www.googleapis.com/calendar/v3/calendars/{}/events".format(calendarID), json=data,
                             headers=headers)
        return Callback(True, 'Successfully added event')
    except Exception as e:
        helpers.HPrint(str(e))


def createCalendar(token):
    try:
        auth = {'Authorization': 'Bearer ' + token}
        data = {'summary': 'TSB Appointments'}
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
