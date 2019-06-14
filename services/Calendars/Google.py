from authlib.flask.client import OAuth

from flask import url_for

def authurl():
    oauth = OAuth()
    gcalendar = oauth.register(
        name='gcalendar',
        client_id='623652835897-tj9rf1v6hd1tak5bv5hr4bq9hrvjns95.apps.googleusercontent.com',
        client_secret='ndbyEpx-yfXNl872hIwySuUI',
        request_token_url='https://accounts.google.com/o/oauth2/token"',
        request_token_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token"',
        access_token_params=None,
        refresh_token_url=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/auth/calendar.events',
        client_kwargs=None,
    )

    return gcalendar.authorize_redirect(url_for('authorized', _external=True))