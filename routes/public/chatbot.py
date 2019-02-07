import os
import uuid

from flask import Blueprint, request, send_from_directory
from flask import render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import BaseConfig
from models import Callback, Assistant, db, ChatbotSession
from services import assistant_services, flow_services, chatbot_services, solutions_services
from utilities import helpers

chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)



@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot_direct_link", methods=['GET'])
def chatbot_direct_link(assistantIDAsHash):
    if request.method == "GET":
        return render_template("chatbot_direct_link.html", assistantID=assistantIDAsHash)

@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot", methods=['GET', 'POST'])
def chatbot(assistantIDAsHash):

    if request.method == "GET":
        # Get blocks for the chatbot to use
        callback: Callback = flow_services.getChatbot(assistantIDAsHash)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, "No Message", callback.Data)

    # Process sent data coming from the chatbot
    if request.method == "POST":

        # Chatbot collected information
        data = request.json
        callback: Callback = chatbot_services.processData(assistantIDAsHash, data)

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)

        return helpers.jsonResponse(True, 200, "Collected data is successfully processed", {'sessionID': callback.Data.ID})


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


@chatbot_router.route("/widgets/<path:path>", methods=['GET'])
@helpers.gzipped
def assistant_userdownloads(path):
    if request.method == "GET":
        return send_from_directory('static/widgets/', path)



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
                # Check if the post request has the file part
                if 'file' not in request.files:
                    return helpers.jsonResponse(False, 404, "No file part")
                filenames = ''
                for file in request.files.getlist('file'):
                    if file.filename == '':
                        return helpers.jsonResponse(False, 404, "No selected file")

                    # Generate unique name: hash_sessionIDEncrypted.extension
                    filename = str(uuid.uuid4()) + '_' + helpers.encrypt_id(sessionID) + '.' + \
                               secure_filename(file.filename).rsplit('.', 1)[1].lower()
                    # Save file in the server
                    file.save(os.path.join(BaseConfig.USER_FILES, filename))

                    # if there is multiple files, split there name by commas
                    if filenames == '':
                        filenames = filename
                    else:
                        filenames+= ',' + filename

                # Store filenames in the DB
                userInput.FilePath = filenames

            except Exception as exc:
                print(exc)
                return helpers.jsonResponse(False, 404, "Couldn't save the file")
            # Save changes
            db.session.commit()
            return helpers.jsonResponse(True, 200, "File uploaded successfully!!")
