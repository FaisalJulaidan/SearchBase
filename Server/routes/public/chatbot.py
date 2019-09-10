import uuid

from flask import Blueprint, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from models import Callback, db, Conversation, Assistant, StoredFile, StoredFileInfo
from services import conversation_services, flow_services, databases_services, stored_file_services, mail_services
from services.Marketplace.CRM import crm_services
from utilities import helpers, enums, wrappers
from utilities.helpers import logError, limiter

import json

chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)


# Requests limiter:
# TODO: Place this in helpers for request restrictions elsewhere


@chatbot_router.after_request
def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
#     r.headers['Access-Control-Allow-Origin'] = '*'
#     r.headers['Access-Control-Allow-Headers'] = '*'
#     r.headers['Access-Control-Allow-Methods'] = '*'
    return r


# To give an access to the static/widgets/chatbot folder
@chatbot_router.route("/static/widgets/chatbot/<path:path>", methods=['GET'])
@wrappers.gzipped
def get_chatbot_static(path):
    if request.method == "GET":
        return send_from_directory('static/widgets/chatbot/', path)


# To load the loadChatbo
@chatbot_router.route("/widgets/chatbot", methods=['GET'])
@wrappers.gzipped
def get_widget():
    if request.method == "GET":
        return send_from_directory('static/js',
                                   'loadChatbot.js')


# LEGACY CODE
# TO BE REMOVED
# To load the loadChatbot
@chatbot_router.route("/widgets/chatbot.js", methods=['GET'])
@wrappers.gzipped
def get_widget_legacy():
    if request.method == "GET":
        return send_from_directory('static/js',
                                   'loadChatbot.js')


@chatbot_router.route("/assistant/<string:assistantHashID>/chatbot/solutions", methods=['POST'])
def getSolutions_forChatbot(assistantHashID):
    if request.method == "POST":
        # chatbot collected information
        data = request.json

        # If showTop is 0 then skip below return nothing and don't even call solutions_services
        if data['showTop'] > 0:
            callback: Callback = databases_services.scan(data, assistantHashID)
            if not callback.Success:
                return helpers.jsonResponseFlask(False, 400, callback.Message)
            return helpers.jsonResponseFlask(True, 200, "Solutions list is here!", callback.Data)
        return helpers.jsonResponseFlask(True, 200, "show top is 0", [])


@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot", methods=['GET', 'POST'])
@limiter.limit("480/day;1/hour", methods=['POST'], error_message='User Chatbot Spam (429)')  # NOTE: Need to see if this works (what error is given?)
def chatbot(assistantIDAsHash):
    if request.method == "GET":
        print("A GET request is being sent...")
        # Get blocks for the chatbot to use
        callback: Callback = flow_services.getChatbot(assistantIDAsHash)
        if not callback.Success:
            return helpers.jsonResponseFlask(False, 400, callback.Message)
        return helpers.jsonResponseFlask(True, 200, "No Message", callback.Data)

    # Process sent data coming from the chatbot
    if request.method == "POST":
        print("A POST request is being sent...")

        # Chatbot collected information
        data = json.loads(request.form.get('conversation'))
        callback: Callback = conversation_services.processConversation(assistantIDAsHash, data)

        file_callback: Callback = Callback(True, '')
        if request.files:
            file_callback = conversation_services.uploadFiles(request.files.getlist('file'), callback.Data[0], callback.Data[1], request.form.get('keys'))

        if not (callback.Success and file_callback.Success):
            return helpers.jsonResponseFlask(False, 400, callback.Message, callback.Data)

        return helpers.jsonResponseFlask(True, 200,
                                    "Collected data is successfully processed")
