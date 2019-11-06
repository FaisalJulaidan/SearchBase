import os

from flask import Blueprint, render_template, request, send_from_directory, make_response, redirect
from flask_cors import CORS
from flask_mail import Message

from models import Callback
from services import mail_services, url_services, sub_services
from services.mail_services import mail
from utilities import helpers

public_router = Blueprint('public_router', __name__, template_folder="../templates", static_folder='static')
CORS(public_router)


# ======== Server React =========== #
# Serve React App
@public_router.route('/', defaults={'path': ''})
@public_router.route('/<path:path>')
def serve(path):
    if os.environ['FLASK_ENV'] == 'development':
        return redirect("http://localhost:3000/" + path, code=302)

    if path != "" and os.path.exists("static/react_app/" + path):
        return send_from_directory("static/react_app/", path)
    else:
        return send_from_directory("static/react_app/", 'index.html')

@public_router.route('/u/<string:key>')
def url_shortener(key):
    urlshotener: Callback = url_services.getByKey(key)
    
    if (urlshotener.Success):
        return redirect(urlshotener.Data)
    else:
        return '123'
        # need to return 404?


# LEGACY CODE
# TO BE REMOVED
# To redirect old chatbot direct link to the newer one
@public_router.route("/api/assistant/<string:assistantIDAsHash>/chatbot_direct_link", methods=['GET'])
def chatbot_direct_link123(assistantIDAsHash):
    return redirect("/chatbot_direct_link/" + assistantIDAsHash, code=302)

# ======== Static Pages =========== #


@public_router.route("/mail/arrange_demo", methods=['POST'])
def register_interest():
    if request.method == "POST":

        callback: Callback = mail_services.sendDemoRequest(request.json)

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, callback.Message)

@public_router.route("/pricing/gen_checkout_url", methods=['POST'])
def generateCheckoutURL():
    callback: Callback = sub_services.generateCheckoutURL(request.json)

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)

    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

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

# Stripe webhook URLS
@public_router.route("/stripe_webhook", methods=['POST'])
def stripe_webhook():
    print("lolol")
    callback: Callback = sub_services.handleStripeWebhook(request)

    # To tell stripe whether the request was succesful
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)

# Old website routes, To be deleted.
#
# @public_router.route("/features", methods=['GET'])
# def features():
#     if request.method == "GET":
#         return render_template("features.html")
#
#
# @public_router.route("/dataRetrieval", methods=['GET'])
# def data_retrieval():
#     if request.method == "GET":
#         return render_template("retrieval.html")
#
#
# @public_router.route("/dataCollection", methods=['GET'])
# def data_collection():
#     if request.method == "GET":
#         return render_template("collection.html")
#
#
# @public_router.route("/CvParsing", methods=['GET'])
# def cv_parsing():
#     if request.method == "GET":
#         return render_template("CvParsing.html")
#
#
# @public_router.route("/FeedbackCollector", methods=['GET'])
# def feedback_collector():
#     if request.method == "GET":
#         return render_template("Feedback.html")
#
#
# @public_router.route("/about", methods=['GET'])
# def about():
#     if request.method == "GET":
#         return render_template("about.html")
#
#
# @public_router.route("/contact", methods=['GET'])
# def contactpage():
#     if request.method == "GET":
#         return render_template("contact.html")
#
#
# # Terms and conditions page route
# @public_router.route("/termsandconditions", methods=['GET'])
# def terms_and_conditions():
#     if request.method == "GET":
#         return render_template("terms.html")
#
#
# @public_router.route("/privacy", methods=['GET'])
# def privacy():
#     if request.method == "GET":
#         return render_template("privacy-policy.html")



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
