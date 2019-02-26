from services import admin_services, user_services, company_services, mail_services
from models import Callback
from flask import Blueprint, request, redirect, render_template
from utilities import helpers
from itsdangerous import URLSafeTimedSerializer

resetPassword_router: Blueprint = Blueprint('resetPassword_router', __name__ ,template_folder="../../templates")
verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')

@resetPassword_router.route("/account/resetpassword", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        msg = helpers.checkForMessage()
        return render_template("accounts/resetpassword.html", msg=msg)
    else:
         email = request.form.get("email", default="").lower()

         company_callback : Callback = company_services.getByEmail(email)
         if not company_callback.Success: return helpers.redirectWithMessage("reset_password", "User with that email does not exist.")

         mail_callback : Callback = mail_services.sendPasswordResetEmail(email, company_callback.Data.ID)

         return helpers.redirectWithMessage("reset_password", mail_callback.Message)

@resetPassword_router.route("/account/resetpassword/<payload>", methods=['GET', 'POST'])
def reset_password_verify(payload):
    if request.method == "GET":
        try:
            data = verificationSigner.loads(payload)
            email = data.split(";")[0].lower()
            companyID = int(data.split(";")[1])

            company_callback : Callback = company_services.getByEmail(email)
            if not company_callback.Success: raise Exception
            if not company_callback.Data.ID is companyID: raise Exception

        except:
            return helpers.hardRedirectWithMessage("login", "The link you requested is invalid.")

        return render_template("accounts/set_resetpassword.html", email=email, payload=payload)

    if request.method == "POST":
        email = request.form.get("email", default="Error").lower()
        password = request.form.get("password", default="Error")

        changePassword_callback : Callback = user_services.changePasswordByEmail(email, password)
        if not changePassword_callback.Success : return helpers.redirectWithMessage("reset_password", changePassword_callback.Message + ". Please try again.")

        return helpers.hardRedirectWithMessage("login", changePassword_callback.Message) 