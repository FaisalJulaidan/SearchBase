from flask import Blueprint, request, render_template, redirect, send_from_directory
from itsdangerous import URLSafeTimedSerializer

from models import Callback
from services import user_services, company_services, mail_services
from utilities import helpers

resetPassword_router: Blueprint = Blueprint('resetPassword_router', __name__, template_folder="../../templates")
verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')


@resetPassword_router.route("/reset_password", methods=["POST"])
def reset_password():
    if request.method == "POST":
        email = request.json.get("email", "").lower()

        if not email:
            return helpers.jsonResponse(False, 400, "Could not receive email")

        company_callback: Callback = company_services.getByEmail(email)
        if not company_callback.Success:
            return helpers.jsonResponse(False, 400, company_callback.Message)

        mail_callback: Callback = mail_services.sendPasswordResetEmail(email, company_callback.Data.ID)
        if not mail_callback.Success:
            return helpers.jsonResponse(False, 400, mail_callback.Message)

        return helpers.jsonResponse(True, 200, mail_callback.Message)


@resetPassword_router.route("/reset_password/<payload>", methods=['GET', 'PUT', 'POST'])
def reset_password_verify(payload):
    if request.method == "GET":
        return send_from_directory('static/react_app', 'index.html')

    if request.method == "PUT":
        try:
            data = verificationSigner.loads(payload)
            email = data.split(";")[0].lower()
            companyID = int(data.split(";")[1])

            company_callback: Callback = company_services.getByEmail(email)
            if not company_callback.Success:
                raise Exception
            if not company_callback.Data.ID is companyID:
                raise Exception

        except:
            return redirect("/login")

        return redirect("/login")

    if request.method == "POST":
        email = request.form.get("email", "Error").lower()
        password = request.form.get("password", "Error")

        changePassword_callback: Callback = user_services.changePasswordByEmail(email, password)
        if not changePassword_callback.Success:
            return redirect("/login")

        return redirect("/login")
