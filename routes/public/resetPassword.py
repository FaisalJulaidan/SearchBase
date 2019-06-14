from flask import Blueprint, request

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

        # Check if user exists
        user_callback: Callback = user_services.getByEmail(email)
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        # Send a reset password email . The email will contain a token that has the email encrypted in it
        mail_callback: Callback = mail_services.sendPasswordResetEmail(email, user_callback.Data.ID)
        if not mail_callback.Success:
            return helpers.jsonResponse(False, 400, mail_callback.Message)

        return helpers.jsonResponse(True, 200, mail_callback.Message)


@resetPassword_router.route("/reset_password/<payload>", methods=['POST'])
def reset_password_verify(payload):
    if request.method == "POST":
        try:
            data = helpers.verificationSigner.loads(payload, salt='reset-pass-key', max_age=1800)  # expires in 30mins
            email = data.split(";")[0].lower()
            password = request.json.get("password", None)

            # Check if password exist
            if not password:
                return helpers.jsonResponse(False, 400, "Server did not manage to receive your new password")

            # Update password using the email included in the token (payload)
            resetPassword_callback: Callback = user_services.updatePasswordByEmail(email, password)
            if not resetPassword_callback.Success:
                return helpers.jsonResponse(False, 400, resetPassword_callback.Message)

            return helpers.jsonResponse(True, 200, resetPassword_callback.Message)
        except Exception as e:
            print(e)
            return helpers.jsonResponse(False, 400, "Could not update your password")
