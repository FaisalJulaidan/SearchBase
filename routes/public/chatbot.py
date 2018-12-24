import os
from config import BaseConfig
from flask import Blueprint, render_template, request, send_from_directory
from utilities import helpers
from models import Callback, Assistant, db, ChatbotSession
from services import assistant_services, flow_services, chatbot_services, solutions_services
from werkzeug.utils import secure_filename
import uuid
from flask_cors import CORS
from utilities.helpers import gzipped
chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)

# Two functions to get assistant via id and hashids to avoid duplicate code in every route function
def getAssistantByHashID(hashID):
    assistantID = helpers.decrypt_id(hashID)
    if len(assistantID) == 0:
        return Callback(False, "Assistant not found!", None)

    callback: Callback = assistant_services.getByID(assistantID[0])
    if not callback.Success:
        return Callback(False, "Assistant not found!", None)
    assistant: Assistant = callback.Data

    # Check if assistant is active excluding on test page
    requestHeader = str(request.headers.get("Referer"))
    if not assistant.Active and (("connect" not in requestHeader or "/admin/assistant/" not in requestHeader) and ("chatbottemplate_production" not in requestHeader)):
        return Callback(False, "Assistant is not active.", None)
    return callback



@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot", methods=['GET', 'POST'])
def chatbot(assistantIDAsHash):

    # Find the assistant by hashid and not id
    callback: Callback = getAssistantByHashID(assistantIDAsHash)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, callback.Message, callback.Data)
    assistant: Assistant = callback.Data

    if request.method == "GET":
        # Get blocks for the chatbot to use
        data: dict = flow_services.getChatbot(assistant)
        return helpers.jsonResponse(True, 200, "No Message", data)

    # Process sent data coming from the chatbot
    if request.method == "POST":

        # Chatbot collected information
        data = request.get_json(silent=True)
        ch_callback: Callback = chatbot_services.processData(assistant, data)

        if not ch_callback.Success:
            return helpers.jsonResponse(False, 400, ch_callback.Message, ch_callback.Data)

        return helpers.jsonResponse(True, 200, "Collected data is successfully processed", {'sessionID': ch_callback.Data.ID})


@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot/solutions", methods=['POST'])
def getSolutions_forChatbot(assistantIDAsHash):

    # Since this route is broken, return empty an list of solutions to continue development
    return helpers.jsonResponse(True, 200, "TEST TEST", [])
    #######################################################################################

    # Find the assistant by hashid and not id
    callback: Callback = getAssistantByHashID(assistantIDAsHash)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, callback.Message, callback.Data)
    assistant: Assistant = callback.Data

    if request.method == "POST":
        # chatbot collected information
        data = request.json
        solutions = []

        # If showTop is 0 then skip below return nothing and don't even call solutions_services
        if data['showTop'] > 0:
            getSolutionRecord_callback: Callback = solutions_services.getFirstSolutionRecord(assistant.ID)#TODO change this to solutionID and func
            if not getSolutionRecord_callback.Success:
                return helpers.jsonResponse(False, 400, getSolutionRecord_callback.Message)

            s_callback = solutions_services.getBasedOnKeywords(assistantID=assistant.ID, keywords=data['keywords'], solutionsRecord=getSolutionRecord_callback, max=data['showTop'])
            if not s_callback.Success:
                return helpers.jsonResponse(False, 400, s_callback.Message)

        return helpers.jsonResponse(True, 200, "Solution list is here!", s_callback.Data)


@chatbot_router.route("/userdownloads/<path:path>", methods=['GET'])
@gzipped
def assistant_userdownloads(path):
    if request.method == "GET":
        return send_from_directory('static/user_downloads/', path)


@chatbot_router.route("/getpopupsettings/<string:assistantIDAsHash>", methods=['GET'])
def get_pop_settings(assistantIDAsHash):

    # Find the assistant by hashid and not id
    callback: Callback = getAssistantByHashID(assistantIDAsHash)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, callback.Message, callback.Data)
    assistant: Assistant = callback.Data

    if request.method == "GET":
        return helpers.jsonResponse(True, 200, "Pop up settings retrieved",
                                    {"SecondsUntilPopUp": assistant.SecondsUntilPopup,
                                     "TopBarText": assistant.TopBarText})


@chatbot_router.route("/assistant/<int:sessionID>/file", methods=['POST'])
def chatbot_upload_files(sessionID):
    callback: Callback = chatbot_services.getBySessionID(sessionID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Session not found.", None)
    userInput: ChatbotSession = callback.Data

    if request.method == "POST":
        data = request.json
        if request.method == 'POST':

            try:
                # check if the post request has the file part
                if 'file' not in request.files:
                    return helpers.jsonResponse(False, 404, "No file part")
                file = request.files['file']

                if file.filename == '':
                    return helpers.jsonResponse(False, 404, "No selected file")

                filename = str(uuid.uuid4()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
                file.save(os.path.join(BaseConfig.USER_FILES, filename))
                userInput.FilePath = filename

            except Exception as exc:
                return helpers.jsonResponse(False, 404, "Couldn't save the file")

            db.session.commit()
            return helpers.jsonResponse(True, 200, "File uploaded successfully!!")
