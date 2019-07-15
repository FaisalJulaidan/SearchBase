import uuid

from flask import Blueprint, request, send_from_directory
from flask import render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from models import Callback, db, Conversation, Assistant
from services import conversation_services, flow_services, databases_services, stored_file_services, mail_services
from services.Marketplace.CRM import crm_services
from utilities import helpers
from utilities.helpers import logError

chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)


@chatbot_router.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['Access-Control-Allow-Headers'] = '*'
    r.headers['Access-Control-Allow-Methods'] = '*'
    return r


# To give an access to the static/widgets/chatbot folder
@chatbot_router.route("/static/widgets/chatbot/<path:path>", methods=['GET'])
@helpers.gzipped
def get_chatbot_static(path):
    if request.method == "GET":
        return send_from_directory('static/widgets/chatbot/', path)


# To load the loadChatbo
@chatbot_router.route("/widgets/chatbot", methods=['GET'])
@helpers.gzipped
def get_widget():
    if request.method == "GET":
        return send_from_directory('static/js',
                                   'loadChatbot.js')


# LEGACY CODE
# TO BE REMOVED
# To load the loadChatbo
@chatbot_router.route("/widgets/chatbot.js", methods=['GET'])
@helpers.gzipped
def get_widget_legacy():
    if request.method == "GET":
        return send_from_directory('static/js',
                                   'loadChatbot.js')


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
        callback: Callback = conversation_services.processConversation(assistantIDAsHash, data)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)

        return helpers.jsonResponse(True, 200,
                                    "Collected data is successfully processed",
                                    {'sessionID': callback.Data.ID})


@chatbot_router.route("/assistant/<string:assistantHashID>/chatbot/solutions", methods=['POST'])
def getSolutions_forChatbot(assistantHashID):
    if request.method == "POST":
        # chatbot collected information
        data = request.json

        # If showTop is 0 then skip below return nothing and don't even call solutions_services
        if data['showTop'] > 0:
            callback: Callback = databases_services.scan(data, assistantHashID)
            if not callback.Success:
                return helpers.jsonResponse(False, 400, callback.Message)
            return helpers.jsonResponse(True, 200, "Solutions list is here!", callback.Data)
        return helpers.jsonResponse(True, 200, "show top is 0", [])


@chatbot_router.route("/assistant/<string:assistantIDAsHash>/chatbot/<int:sessionID>/file", methods=['POST'])
def chatbot_upload_files(assistantIDAsHash, sessionID):
    callback: Callback = conversation_services.getByID(sessionID, helpers.decodeID(assistantIDAsHash)[0])
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Session not found.", None)
    conversation: Conversation = callback.Data

    if request.method == 'POST':

        try:
            assistant: Assistant = conversation.Assistant
            # Check if the post request has the file part
            if 'file' not in request.files:
                return helpers.jsonResponse(False, 404, "No file part")

            files = request.files.getlist('file')
            filenames = ''

            for file in files:

                if file.filename == '':
                    return helpers.jsonResponse(False, 404, "No selected file")
                # Generate unique name: hash_sessionIDEncrypted.extension
                filename = str(uuid.uuid4()) + '_' + helpers.encodeID(sessionID) + '.' + \
                           secure_filename(file.filename).rsplit('.', 1)[1].lower()

                # Upload file to DigitalOcean Space
                upload_callback: Callback = stored_file_services.uploadFile(file, filename,
                                                                            stored_file_services.USER_FILES_PATH,
                                                                            True)

                if not upload_callback.Success:
                    filename = 'fileCorrupted'

                # if there is multiple files, split there name by commas to store a ref of the uploaded files in DB
                if filenames == '':
                    filenames = filename
                else:
                    filenames += ',' + filename

            # Store filePaths in the DB as reference
            dbRef_callback: Callback = stored_file_services.createRef(filenames, conversation)
            if not dbRef_callback.Success:
                logError("Couldn't Save Stored Files Reference For: " + str(filenames))
                raise Exception(dbRef_callback.Message)

            # Save changes
            db.session.commit()

            # Notify company of new conversation
            if assistant.NotifyEvery == 0:
                mail_services.notifyNewConversation(assistant, conversation)

            if assistant.CRM:
                # Send through CRM
                sendCRMFile_callback: Callback = crm_services.uploadFile(assistant, dbRef_callback.Data)
                if not sendCRMFile_callback:
                    # TODO we should not raise expcetion just becuase CRM fail beucase this mean the chatbot will fail too
                    # TODO but instead we should log this in the db and notify
                    raise Exception("Could not submit file to CRM")

        except Exception as exc:
            return helpers.jsonResponse(False, 404, "I am having difficulties saving your uploaded the files :(")
        return helpers.jsonResponse(True, 200, "File uploaded successfully!!")
