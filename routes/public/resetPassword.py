from flask import Blueprint, request, redirect

from models import Callback
from services import user_services, company_services, mail_services
from utilities import helpers


resetPassword_router: Blueprint = Blueprint('resetPassword_router', __name__, template_folder="../../templates")

# Send reset email
@resetPassword_router.route("/reset_password", methods=["POST"])
def reset_password():

    if request.method == "POST":
        email = request.json.get("email", "").lower()

        if not email:
            return helpers.jsonResponse(False, 400, "Provide your email")

        company_callback: Callback = company_services.getByEmail(email)
        if not company_callback.Success:
            return helpers.jsonResponse(False, 400, company_callback.Message)

        mail_callback: Callback = mail_services.sendPasswordResetEmail(email, company_callback.Data.ID)
        if not mail_callback.Success:
            return helpers.jsonResponse(False, 400, mail_callback.Message)

        return helpers.jsonResponse(True, 200, mail_callback.Message)


@resetPassword_router.route("/reset_password/<payload>", methods=['POST'])
def reset_password_verify(payload):
    if request.method == "POST":

        try:
            data = helpers.verificationSigner.loads(payload, salt='reset-pass-key', max_age=1800) # expires in 30mins
            email = data.split(";")[0].lower()
            password = request.json.get("password", "").lower()

            if not password:
                return helpers.jsonResponse(False, 400, "Server did not manage to receive your new password")

            changePassword_callback: Callback = user_services.changePasswordByEmail(email, password)
            if not changePassword_callback.Success:
                return helpers.jsonResponse(False, 400, changePassword_callback.Message)

            return helpers.jsonResponse(True, 200, changePassword_callback.Message)
        except Exception:
            return helpers.jsonResponse(False, 400, "Could not update your password")
