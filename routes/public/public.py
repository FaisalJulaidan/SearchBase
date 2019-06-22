import os

from flask import Blueprint, render_template, request, send_from_directory, redirect
from flask_cors import CORS
from flask_mail import Message

from models import Callback
from services import user_services, mail_services
from services.mail_services import mail
from utilities import helpers

public_router = Blueprint('public_router', __name__, template_folder="../templates", static_folder='static')
CORS(public_router)


# ======== Server React =========== #
def serve(path=''):
    if path != "" and os.path.exists("static/react_app/" + path):
        return send_from_directory('static/react_app', path)
    else:
        return send_from_directory('static/react_app', 'index.html')


# Serve React App
@public_router.route('/login')
def login():
    return serve()


@public_router.route('/signup')
def signup():
    return serve()


@public_router.route('/forget_password')
def forget_password():
    return serve()


@public_router.route('/reset_password/<payload>')
def reset_password(payload):
    return serve()

@public_router.route('/appointments_picker/<payload>')
def appointments_picker(payload):
    return serve()

@public_router.route('/dashboard', defaults={'path': ''})
@public_router.route('/dashboard/<path:path>')
def dashboard(path):
    return serve(path)


# ======== Static Pages =========== #

@public_router.route("/", methods=['GET'])
def index_page():
    if request.method == "GET":
        return render_template("index.html")


@public_router.route("/mail/arrange_demo", methods=['POST'])
def register_interest():
    if request.method == "POST":
        email = request.form.get("user_email", default=None)

        if not email:
            return "Could not retrieve some of your inputs"

        requestDemo_callback: Callback = mail_services.sendDemoRequest(email)
        return requestDemo_callback.Message


@public_router.route("/mail/contact_us", methods=['POST'])
def contact_us():
    if request.method == "POST":
        name = request.form.get("sendingName", default=None)
        email = request.form.get("sendingEmail", default=None)
        message = request.form.get("sendMessage", default=None)

        if not name or not email or not message:
            return "Could not retrieve some of your inputs"

        contactUs_callback: Callback = mail_services.contactUsIndex(name, email, message)
        return contactUs_callback.Message


@public_router.route("/features", methods=['GET'])
def features():
    if request.method == "GET":
        return render_template("features.html")


@public_router.route("/dataRetrieval", methods=['GET'])
def data_retrieval():
    if request.method == "GET":
        return render_template("retrieval.html")


@public_router.route("/dataCollection", methods=['GET'])
def data_collection():
    if request.method == "GET":
        return render_template("collection.html")


@public_router.route("/CvParsing", methods=['GET'])
def cv_parsing():
    if request.method == "GET":
        return render_template("CvParsing.html")


@public_router.route("/FeedbackCollector", methods=['GET'])
def feedback_collector():
    if request.method == "GET":
        return render_template("Feedback.html")


@public_router.route("/about", methods=['GET'])
def about():
    if request.method == "GET":
        return render_template("about.html")


@public_router.route("/contact", methods=['GET'])
def contactpage():
    if request.method == "GET":
        return render_template("contact.html")


# Terms and conditions page route
@public_router.route("/termsandconditions", methods=['GET'])
def terms_and_conditions():
    if request.method == "GET":
        return render_template("terms.html")


@public_router.route("/privacy", methods=['GET'])
def privacy():
    if request.method == "GET":
        return render_template("privacy-policy.html")



@public_router.route("/send/mail", methods=['GET', 'POST'])
def sendEmail():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        mailFirstname = request.form.get("sendingName", default="Error")
        mailUserEmail = request.form.get("sendingEmail", default="Error")
        mailUserMessage = request.form.get("sendMessage", default="Error")

        msg = Message(mailFirstname + " from " + mailUserEmail + " has sent you a message.",
                      sender=mailUserEmail,
                      recipients=["thesearchbase@gmail.com"])
        msg.body = mailFirstname + " said: " + mailUserMessage + " their email is: " + mailUserEmail
        mail.send(msg)
        return render_template("index.html")

# Account verification route
@public_router.route("/account/verify/<payload>", methods=['GET'])
def verify_account(payload):
    if request.method == "GET":
        try:
            data = helpers.verificationSigner.loads(payload, salt='email-confirm-key')
            email = data.split(";")[0]
            user_callback: Callback = user_services.verifyByEmail(email)
            if not user_callback.Success: raise Exception(user_callback.Message)

            return redirect("/login")

        except Exception as e:
            return redirect("/login")


# Set Candidate meeting routes
@public_router.route("/candidate-meeting/<payload>", methods=['GET', 'POST'])
def candidate_meeting(payload):
    if request.method == "GET":
        data = helpers.verificationSigner.loads(payload, salt='email-confirm-key')
        email = data.split(";")[0]
        user_callback: Callback = user_services.verifyByEmail(email)
        if not user_callback.Success: raise Exception(user_callback.Message)

        return redirect("/login")

    if request.method == "POST":
        data = request.json