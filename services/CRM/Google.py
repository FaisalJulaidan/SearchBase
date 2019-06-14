from flask import url_for, current_app
from authlib.flask.client import OAuth

from oauth2client import client

import pickle
import os


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authurl():
    return '123'
    # creds = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    #
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         #FILE TO BE MOVED
    #         print(os.path)
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             os.path.abspath(os.environ["GOOGLE_CALENDAR_SECRET"]), SCOPES)
    #         creds = flow.run_local_server(host="localhost", port=3000)
    #     # Save the credentials for the next run
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    # service = build('calendar', 'v3', credentials=creds)
    # CLIENT_SECRET_FILE = '/path/to/client_secret.json'
    #
    # # Exchange auth code for access token, refresh token, and ID token
    # credentials = client.credentials_from_clientsecrets_and_code(
    #     CLIENT_SECRET_FILE,
    #     ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
    #     auth_code)
    #
    # # Call Google API
    # http_auth = credentials.authorize(httplib2.Http())
    # drive_service = discovery.build('drive', 'v3', http=http_auth)
    # appfolder = drive_service.files().get(fileId='appfolder').execute()
    #
    # # Get profile info from ID token
    # userid = credentials.id_token['sub']
    # email = credentials.id_token['email']
    # print(service)
