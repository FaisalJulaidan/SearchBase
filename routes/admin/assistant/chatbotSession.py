from flask import Blueprint, request, send_from_directory
from services import chatbotSession_services, assistant_services, dataCategories_services
from models import Callback, ChatbotSession, Assistant
from utilities import helpers
from config import BaseConfig
from enums import UserType
from flask_jwt_extended import jwt_required, get_jwt_identity

chatbotSession_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# Get all assistant's user inputs
@chatbotSession_router.route("/assistant/<int:assistantID>/chatbotSessions", methods=["GET", "DELETE"])
@jwt_required
def chatbotSession(assistantID):

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
    # Get the assistant's user inputs/chatbot sessions
    if request.method == "GET":
        s_callback: Callback = chatbotSession_services.getByAssistantID(assistantID)

        # Return response
        if not s_callback.Success:
            return helpers.jsonResponse(False, 400, "Error in retrieving sessions.")
        return helpers.jsonResponse(True, 200, s_callback.Message,
                                    {'sessionsList': s_callback.Data,
                                     'userTypes': [uiv.value for uiv in UserType],
                                     'filesPath': BaseConfig.USER_FILES
                                     })


    # Clear all user inputs/chatbot sessions
    if request.method == "DELETE":
        callback: Callback = chatbotSession_services.deleteAll(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

@chatbotSession_router.route("/assistant/<int:assistantID>/chatbotSessions/<path:path>", methods=['GET'])
@jwt_required
@helpers.gzipped
def chatbotSession_file_uploads(assistantID, path):
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

    # Security procedure ->
    # the id of the user input session is included in the name of the file after "_" symbol, but encrypted
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


@chatbotSession_router.route("/assistant/<assistantID>/chatbotSessions/<sessionID>", methods=["DELETE"])
def chatbotSession_delete_record(assistantID, sessionID):

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

    if request.method == "DELETE":

        callback : Callback = chatbotSession_services.deleteByID(sessionID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

