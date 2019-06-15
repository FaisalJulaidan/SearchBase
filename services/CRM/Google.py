from models import Callback
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

        # new = Calendar(Auth=r['code'], Type=enums.Calendar.Google, CompanyID=2)
        # db.session.add(new)
        # db.session.commit()
    except Exception as e:
        print(e)
    return '123'

