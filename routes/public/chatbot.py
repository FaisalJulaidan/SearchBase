from flask import Blueprint, request, send_from_directory
from flask import render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import Callback, db, Conversation
from services import conversation_services, flow_services, databases_services, stored_file_services, mail_services
from services.CRM import crm_services
from utilities import helpers
import uuid, logging

chatbot_router = Blueprint('chatbot_router', __name__, template_folder="../templates")
CORS(chatbot_router)



@chatbot_router.route("/widgets/<path:path>", methods=['GET'])
@helpers.gzipped
def get_widget(path):
    if request.method == "GET":
        return send_from_directory('static/widgets/', path)

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

        # Notify company about the new chatbot session
        mail_services.notifyNewConversation(assistantIDAsHash)

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


@chatbot_router.route("/assistant/<string:assistantIDAsHash>/session/<int:sessionID>/file", methods=['POST'])
def chatbot_upload_files(assistantIDAsHash, sessionID):

    callback: Callback = conversation_services.getByID(sessionID, helpers.decode_id(assistantIDAsHash)[0])
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Session not found.", None)
    session: Conversation = callback.Data

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
                filename = str(uuid.uuid4()) + '_' + helpers.encode_id(sessionID) + '.' + \
                           secure_filename(file.filename).rsplit('.', 1)[1].lower()

                # Upload file to DigitalOcean Space
                upload_callback : Callback = stored_file_services.uploadFile(file,
                                                                             filename,
                                                                             stored_file_services.USER_FILES_PATH,
                                                                             True)

                if not upload_callback.Success:
                    filename = 'fileCorrupted'

                # if there is multiple files, split there name by commas to store a ref of the uploaded files in DB
                if filenames == '': filenames = filename
                else: filenames+= ',' + filename

            # Store filePaths in the DB as reference
            dbRef_callback : Callback = stored_file_services.createRef(filenames, session)
            if not dbRef_callback.Success:
                logging.error("Couldn't Save Stored Files Reference For: " + str(filenames))
                raise Exception(dbRef_callback.Message)

            # Save changes
            db.session.commit()

            if callback.Data.Assistant.CRM:
                # Send through CRM
                sendCRMFile_callback: Callback = crm_services.uploadFile(callback.Data.Assistant, dbRef_callback.Data)
                if not sendCRMFile_callback:
                    raise Exception("Could not submit file to CRM")

        except Exception as exc:
            return helpers.jsonResponse(False, 404, "Couldn't save the file")

        return helpers.jsonResponse(True, 200, "File uploaded successfully!!")
