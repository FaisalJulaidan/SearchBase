import os
from datetime import timedelta

import requests
from models import Callback, Calendar, db
from sqlalchemy import exc
from utilities import helpers, enums
from services import appointment_services
from models import Appointment, Conversation, Company, Assistant, User
from datetime import datetime
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
        events = eventList.json()['items']
        eventCount = len(events)

        appointments = db.session.query(Appointment).join(Conversation).join(Assistant).join(Company).filter(Company.ID == companyID).all()
        user: User = db.session.query(User).join(Company).filter(Company.ID == companyID).first()

        rs = []
        for appointment in appointments:
            event = None
            for idx, item in enumerate(events):
                # Invalid format, delete event
                if 'description' not in item:
                    rs.append(grequests.delete(eventURL + "/" + item['id'], headers=headers))
                    continue
                if not item['description'].startswith("A_ID"):
                    rs.append(grequests.delete(eventURL + "/" + item['id'], headers=headers))
                    continue
                
                desc = item['description'].split("<br>")
                appointmentDetails = desc[0].split(".")
                eventStatus = appointmentDetails[2]
                aid = hashids.decrypt(appointmentDetails[1])[0]
                
                # event is not the current appointment we are looping through
                if aid != appointment.ID:
                    # Google has unknown event
                    if idx == eventCount:
                        rs.append(grequests.delete(eventURL + "/" + item['id'], headers=headers))
                    continue          

                event = {"data": item, "status": eventStatus, aid: aid}             

            if event is None:
                # Create new appointment
                rs.append(grequests.post(eventURL, headers=headers, json=createEvent(appointment, user)))
                continue

            # Google Appointment matches but is rejected so needs to be removed
            if appointment.Status == enums.Status.Rejected:
              rs.append(grequests.delete(eventURL + "/" + event['data']['id'], headers=headers))
              continue

            # Google Appointment matches but status is same as one in our db so no change is necessary
            if ((appointment.Status == enums.Status.Accepted and event['status'] == "1") or \
                  appointment.Status == enums.Status.Pending and event['status'] == "0"):
                continue
            
            # Update existing appointment     
            rs.append(grequests.patch(eventURL+ "/" + event['data']['id'], headers=headers, json=createEvent(appointment, user)))
            
        grequests.map(rs)

        # GET https://www.googleapis.com/calendar/v3/calendars/calendarId/events
    except Exception as exc:
        helpers.logError("Google.syncAppointments(): " + str(exc))


def createEvent(appointment, user):
  appointmentToken = appointment_services.generateEmailUrl(appointment.ID) if appointment.Status == enums.Status.Pending else None
  appointmentStatus = "Appointment pending approval " if appointment.Status == enums.Status.Pending else "Appointment "
  eventTitle = appointmentStatus + "with {}".format(appointment.Conversation.Name) if appointment.Conversation.Name is not None else appointmentStatus
  
  id = hashids.encrypt(appointment.ID)
  #TODO: Needs to change to whatever environment is using
  appointmentURL = "{}/appointment_status?token={}".format(helpers.getDomain(3000), appointmentToken)
  status = 0 if appointment.Status == enums.Status.Pending else 1
  eventDetails = "A_ID.{}.{}".format(id, status)

  if appointment.Status == enums.Status.Pending:
    eventDesc = "{}<br><a href='{}'>Accept Appointment</a>".format(eventDetails, appointmentURL)
  else:
    eventDesc = "{}<br>Appointment {}".format(eventDetails, appointment.Status.value)
  
  return { 
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
