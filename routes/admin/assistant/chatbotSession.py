from flask import Blueprint, request, send_from_directory
from services import chatbotSession_services, assistant_services
from models import Callback, ChatbotSession, Assistant
from utilities import helpers
from config import BaseConfig
from flask_jwt_extended import jwt_required, get_jwt_identity

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# Get all assistant's user inputs
@userInput_router.route("/assistant/<int:assistantID>/userinput", methods=["GET", "DELETE"])
@jwt_required
def user_input(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID)
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!")

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Get the assistant's user inputs/chatbot sessions
    if request.method == "GET":
        callback: Callback = chatbotSession_services.getByAssistantID(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, {'data': helpers.getListFromSQLAlchemyList(callback.Data),
                                                                  'filesPath': BaseConfig.USER_FILES})


    # Clear all user inputs/chatbot sessions
    if request.method == "DELETE":
        callback: Callback = chatbotSession_services.deleteAll(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

@userInput_router.route("/assistant/<int:assistantID>/userinput/<path:path>", methods=['GET'])
@jwt_required
@helpers.gzipped
def user_input_file_uploads(assistantID, path):
    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID)
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!")

    # the id of the user input session is included in the name of the file after "_" character, but encrypted
    try:
        id = helpers.decrypt_id(path[path.index('_')+1:path.index('.')])[0]
        if not id: raise Exception
    except Exception as exc:
        return helpers.jsonResponse(False, 404, "File not found.", None)


    ui_callback: Callback = chatbotSession_services.getByID(id, assistant)
    if not ui_callback.Success:
        return helpers.jsonResponse(False, 404, "File not found.", None)
    user_input: ChatbotSession = ui_callback.Data

    # Check if this user has access to user input session
    if assistant != user_input.Assistant:
        return helpers.jsonResponse(False, 401, "File access is unauthorised!")

    if request.method == "GET":
        return send_from_directory('static/file_uploads/user_files', path)


@userInput_router.route("/admin/assistant/<assistantID>/<recordID>/delete", methods=["GET"])
def admin_record_delete(assistantID, recordID):

    if request.method == "GET":
        deleteRecord_callback : Callback = chatbotSession_services.deleteByID(recordID)

        return str(deleteRecord_callback.Success)

@userInput_router.route("/admin/assistant/<assistantID>/deleteAll", methods=["GET"])
def admin_record_delete_all(assistantID):

    if request.method == "GET":
        deleteRecords_callback : Callback = chatbotSession_services.deleteAll(assistantID)

        return helpers.redirectWithMessageAndAssistantID("admin_user_input", assistantID, deleteRecords_callback.Message)