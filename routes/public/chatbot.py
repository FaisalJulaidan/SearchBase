import os
from config import BaseConfig
from flask import Blueprint, render_template, request, send_from_directory
from utilities import helpers
from models import Callback, Assistant, db, ChatbotSession
from services import assistant_services, bot_services, chatbot_services, solutions_services
from werkzeug.utils import secure_filename
import uuid
from flask_cors import CORS

chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)


# Two functions to get assistant via id and hashids to avoid duplicate code in every route function
def getAssistantByHashID(hashID):
    assistantID = helpers.decrypt_id(hashID)
    if len(assistantID) == 0:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    return getAssistant(assistantID[0])


def getAssistant(id):
    callback: Callback = assistant_services.getByID(id)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    return callback.Data


@chatbot_router.route("/test", methods=['GET'])
def t():
    if request.method == "GET":
        return render_template("test-chatbot.html")


@chatbot_router.route("/chatbottemplate/<assistantID>", methods=['GET'])
def test_chatbot_page(assistantID):
    if request.method == "GET":
        return render_template("chatbot-template.html")


@chatbot_router.route("/chatbottemplate_production/<assistantID>", methods=['GET'])
def test_chatbot_page2(assistantID):
    if request.method == "GET":
        return render_template("chatbot-template_production.html")


@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot", methods=['GET', 'POST'])
def chatbot(assistantIDAsHash):

    # Found the assistant using the hashid and not id
    assistant: Assistant = getAssistantByHashID(assistantIDAsHash)

    if request.method == "GET":
        # Get blocks for the chatbot to use
        data: dict = bot_services.getChatbot(assistant)
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

    # Found the assistant using the hashid and not id
    assistant: Assistant = getAssistantByHashID(assistantIDAsHash)

    if request.method == "POST":
        # chatbot collected information
        data = request.get_json(silent=True)
        solutions = []

        # If showTop is 0 then skip below return nothing and don't even call solutions_services
        if data['showTop'] > 0:
            getSolutionRecord_callback : Callback = solutions_services.getSolutionByAssistantID(assistant.ID)

            s_callback = solutions_services.getBasedOnKeywords(assistantID=assistant.ID, keywords=data['keywords'], solutionsRecord=getSolutionRecord_callback, max=data['showTop'])
            if not s_callback.Success:
                return helpers.jsonResponse(False, 400, s_callback.Message)

        return helpers.jsonResponse(True, 200, "Solution list is here!", {'solutions': s_callback.Data, "solutionsLink" : {"Success" : True,
        "webLink" : getSolutionRecord_callback.Data.WebLink, "solutionsRef" : getSolutionRecord_callback.Data.IDReference}})


@chatbot_router.route("/userdownloads/<path:path>", methods=['GET'])
def assistant_userdownloads(path):
    if request.method == "GET":
        return send_from_directory('static/user_downloads/', path)


@chatbot_router.route("/getpopupsettings/<string:assistantIDAsHash>", methods=['GET'])
def get_pop_settings(assistantIDAsHash):

    # Found the assistant using the hashid and not id
    assistant: Assistant = getAssistantByHashID(assistantIDAsHash)

    if request.method == "GET":
        data = {"SecondsUntilPopUp": assistant.SecondsUntilPopup, "TopBarText": assistant.TopBarText}
        return helpers.jsonResponse(True, 200, "Pop up settings retrieved", data)


@chatbot_router.route("/assistant/<int:sessionID>/file", methods=['POST'])
def chatbot_upload_files(sessionID):
    callback: Callback = chatbot_services.getBySessionID(sessionID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Session not found.", None)
    userInput: ChatbotSession = callback.Data

    if request.method == "POST":
        data = request.get_json(silent=True)
        if request.method == 'POST':

            try:
                # check if the post request has the file part
                if 'file' not in request.files:
                    return helpers.jsonResponse(False, 404, "No file part")
                file = request.files['file']

                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    return helpers.jsonResponse(False, 404, "No selected file")

                filename = str(uuid.uuid4()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
                file.save(os.path.join(BaseConfig.USER_FILES, filename))
                userInput.FilePath = filename

            except Exception as exc:
                return helpers.jsonResponse(False, 404, "Couldn't save the file")


            # if file and allowed_file(file.filename):
            #     filename = secure_filename(file.filename)
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #     return redirect(url_for('uploaded_file',
            #                             filename=filename))

            db.session.commit()
            return helpers.jsonResponse(True, 200, "file uploaded successfully!!")
