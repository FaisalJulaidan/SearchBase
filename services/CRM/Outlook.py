import logging
import os
from urllib.parse import urlencode

import requests
from flask import current_app
from msal import PublicClientApplication

from models import Callback
from authlib.flask.client import OAuth

# Client ID and secret
client_id = os.environ['OUTLOOK_CLIENT_ID']
client_secret = os.environ['OUTLOOK_CLIENT_SECRET']
app = PublicClientApplication(client_id)


def login(auth):
    try:
        print("auth", auth)
        oauth = OAuth()
        oauth.init_app(current_app)

        oauth.register(
            name='outlook',
            client_id=client_id,
            client_secret=client_secret,
            access_token_url='https://login.microsoftonline.com/thesearchbase.onmicrosoft.com/oauth2/v2.0/authorize',
            access_token_params={"grant_type": "authorization_code", "redirect_uri": "https://www.thesearchbase.com/api/crm_callback"},
            refresh_token_url=None,
            authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=' + client_id +
                          '&response_type=code&scope=Mail.Read+offline_access+openid+profile',
            client_kwargs=None,
        )
        print(1)
        client = oauth.create_client("outlook")
        client.authorize_redirect("https://www.thesearchbase.com/api/crm_callback")
        print(2)
        token = client.authorize_access_token()
        print("token", token)
        return Callback(True, "Success")

    except Exception as exc:
        print("ERROR: ", exc)
        logging.error("CRM.Outlook.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


# # Constant strings for OAuth2 flow
# # The OAuth authority
# authority = 'https://login.microsoftonline.com'
#
# # The authorize URL that initiates the OAuth2 client credential flow for admin consent
# authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')
#
# # The token issuing endpoint
# token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')
#
# # The scopes required by the app
# scopes = ['openid',
#           'User.Read',
#           'Mail.Read']
#
# auth_redirect_uri = "https://login.microsoftonline.com/common/oauth2/v2.0/token"


# def get_signin_url(redirect_uri):
#     # Build the query parameters for the signin url
#     params = {'client_id': client_id,
#               'redirect_uri': redirect_uri,
#               'response_type': 'code',
#               'scope': ' '.join(str(i) for i in scopes)
#               }
#
#     signin_url = authorize_url.format(urlencode(params))
#
#     return signin_url


# def login(auth):
#     try:
#         print("auth", auth)
#         # We now check the cache to see
#         # whether we already have some accounts that the end user already used to sign in before.
#         accounts = app.get_accounts()
#         result = None
#         if accounts:
#             # If so, you could then somehow display these accounts and let end user choose
#             print("Pick the account you want to use to proceed:")
#             for a in accounts:
#                 print('a["username"]', a["username"])
#             # Assuming the end user chose this one
#             chosen = accounts[0]
#             # Now let's try to find a token in cache for this account
#             result = app.acquire_token_silent("User.Read", account=chosen)
#         if not result:
#             # So no suitable token exists in cache. Let's get a new one from AAD.
#             print(auth["username"], auth["password"])
#             result = app.get_authorization_request_url(scopes=["Mail.Read"])
#             print("result", result)
#             r = requests.get(result)
#         if "access_token" in result:
#             print('result["access_token"]', result["access_token"])  # Yay!
#         else:
#             print('result.get("error")', result.get("error"))
#             print('result.get("error_description")', result.get("error_description"))
#             print('result.get("correlation_id")', result.get("correlation_id"))  # You may need this when reporting a bug
#
#         return Callback(True, "Success")
#
#     except Exception as exc:
#         print(exc)
#         logging.error("CRM.Outlook.login() ERROR: " + str(exc))
#         return Callback(False, str(exc))
