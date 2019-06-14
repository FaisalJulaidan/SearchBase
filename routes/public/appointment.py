import os

from flask import Blueprint, render_template, request, send_from_directory, redirect
from flask_cors import CORS
from flask_mail import Message

from models import Callback
from services import user_services, mail_services
from services.mail_services import mail
from utilities import helpers

appointment_router = Blueprint('appointment_router', __name__, template_folder="../templates", static_folder='static')


# Set Candidate meeting routes
@appointment_router.route("/candidate-appointment/<payload>", methods=['GET', 'POST'])
def candidate_appointment(payload):
    if request.method == "GET":
        data = helpers.verificationSigner.loads(payload, salt='email-confirm-key')
        email = data.split(";")[0]
        user_callback: Callback = user_services.verifyByEmail(email)
        if not user_callback.Success: raise Exception(user_callback.Message)

        return redirect("/login")

    if request.method == "POST":
        data = request.json