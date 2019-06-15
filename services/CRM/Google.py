from models import Callback, Calendar, db
import enums
import requests
import os


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
        new = Calendar(Auth=resp.json()['refresh_token'], Type=enums.Calendar.Google, CompanyID=2)
        db.session.add(new)
        db.session.commit()
        return Callback(True, 'User authorized succesfully')
    except Exception as e:
        return Callback(False, str(e))
