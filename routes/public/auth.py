from flask import Blueprint, request, redirect
from flask_jwt_extended import jwt_refresh_token_required
from models import Callback
from services import user_services, auth_services
from utilities import helpers

auth_router = Blueprint('auth_router', __name__)


@auth_router.route("/auth", methods=['POST'])
def authenticate():
    if request.method == "POST":
        # os.command(['bash', 'deploy.sh'])
        data = request.get_json(silent=True)

        callback: Callback = auth_services.authenticate(data.get('email'), data.get('password'))
        if callback.Success:
            return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
        else:
            print(callback.Message)
            return helpers.jsonResponse(False, 401, callback.Message, callback.Data)


# Refresh token endpoint
@auth_router.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    callback = auth_services.refreshToken()
    if callback.Success:
        return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
    else:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)


@auth_router.route("/signup", methods=['POST'])
def signup_process():
    if request.method == "POST":
        callback: Callback = auth_services.signup(request.json)
        if not callback.Success:
            return helpers.jsonResponse(False, 401, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@auth_router.route("verify_account/<payload>", methods=['POST'])  # TODO
def verify_account(payload):
    if request.method == "POST":
        try:
            data = helpers.verificationSigner.loads(payload, salt='email-confirm-key')
            print(data)
            email = data.split(";")[0]

            callback: Callback = user_services.verifyByEmail(email)
            if not callback.Success:
                raise Exception("Couldn't verify your account")

            return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

        except Exception as exc:
            helpers.logError("auth_router.verify_account(): ====> " + str(exc))
            return helpers.jsonResponse(False, 400, "Couldn't verify your account")