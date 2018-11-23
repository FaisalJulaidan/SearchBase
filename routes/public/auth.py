from flask import Blueprint, render_template, request, session, redirect, url_for
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

        email: str = request.form.get("email", default=None)
        password_to_check: str = request.form.get("password", default=None)
        print(email, password_to_check)
        callback: Callback = jwt_auth_services.authenticate(email, password_to_check)

        if callback.Success:
            return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
        else:
            return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)


# Refresh token endpoint
@auth_router.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    callback = jwt_auth_services.refreshToken()
    if callback.Success:
        return helpers.jsonResponse(True, 200, "Authorised!", callback.Data)
    else:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)


@auth_router.route('/logout',  methods=['GET'])
def logout():

    # Will clear out the session.
    return redirect(url_for('public_router.login'))


# TODO improve verification
@auth_router.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == "GET":
        msg = helpers.checkForMessage()
        return render_template("signup.html", msg=msg)

    elif request.method == "POST":

        # User info
        email = request.form.get("email", default=None)
        fullname = request.form.get("fullname", default=None)
        password = request.form.get("password", default=None)

        # Company info
        name = request.form.get("companyName", default=None)
        # size = request.form.get("companySize", default=None)
        url = request.form.get("websiteURL", default=None)
        phone = request.form.get("phoneNumber", default=None)

        if not (fullname and email and password
                and name and url):
            return helpers.redirectWithMessage("signup", "Error in getting all input information.")

        # Split fullname
        firstname = fullname.strip().split(" ")[0]
        surname = fullname.strip().split(" ")[1]

        # Signup new user
        signup_callback: Callback = auth_services.signup(email.lower(), firstname, surname, password, name, phone, url)
        if not signup_callback.Success:
            print(signup_callback.Message)
            return helpers.redirectWithMessage("signup", signup_callback.Message)

        # Send verification email
        mail_callback: Callback = mail_services.sendVerificationEmail(email, name)

        # If error while sending verification email
        if not mail_callback.Success:
            helpers.redirectWithMessage('signup', 'Signed up successfully but > ' + mail_callback.Message
                                        + '. Please contact TheSearchBaseStaff to activate your account.')

        return helpers.redirectWithMessage("login", "We have sent you a verification email. Please use it to complete the sign up process.")

@auth_router.route("/account/verify/<payload>", methods=['GET'])
def verify_account(payload):
    if request.method == "GET":
        try:
            data = verificationSigner.loads(payload)
            email = data.split(";")[0]
            user_callback : Callback = user_services.verifyByEmail(email)
            if not user_callback.Success: raise Exception(user_callback.Message)

            return helpers.redirectWithMessage("login", "Your email has been verified. You can now access your account.")

        except Exception as e:
            print(e)
            return helpers.redirectWithMessage("login", "Email verification link failed. Please contact Customer Support in order to resolve this.")
