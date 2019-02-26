from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory
from itsdangerous import URLSafeTimedSerializer
from models import Callback
from services import user_services, auth_services, mail_services, jwt_auth_services
from utilities import helpers
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity

auth_router = Blueprint('auth_router', __name__)
verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')


@auth_router.route("/auth", methods=['POST'])
def authenticate():
    if request.method == "POST":

        data = request.get_json(silent=True)

        callback: Callback = jwt_auth_services.authenticate(data.get('email'), data.get('password'))
        if callback.Success:
            return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
        else:
            print(callback.Message)
            return helpers.jsonResponse(False, 401, callback.Message, callback.Data)


# Refresh token endpoint
@auth_router.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    callback = jwt_auth_services.refreshToken()
    if callback.Success:
        return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
    else:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)

@auth_router.route("/signup", methods=['POST'])
def signup_process():
    if request.method == "POST":
        callback: Callback = jwt_auth_services.signup(request.json)
        if callback.Success:
            return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
        else:
            return helpers.jsonResponse(False, 401, callback.Message, callback.Data)


@auth_router.route("/account/verify/<payload>", methods=['GET'])
def verify_account(payload):
    if request.method == "GET":
        try:
            data = verificationSigner.loads(payload)
            email = data.split(";")[0]
            user_callback: Callback = user_services.verifyByEmail(email)
            if not user_callback.Success: raise Exception(user_callback.Message)

            return send_from_directory('static/react_app', 'index.html')

        except Exception as e:
            print(e)
            return send_from_directory('static/react_app', 'index.html')
