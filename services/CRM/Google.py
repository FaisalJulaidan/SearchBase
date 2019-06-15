from models import Callback, Calendar, db
from datetime import datetime, timedelta
import enums
import requests
import os
import json
import dateutil

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
            db.session.save(cal)
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
        print(getToken(enums.Calendar.Google, 2))
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
    except Exception as e:
        return Callback(False, str(e))
