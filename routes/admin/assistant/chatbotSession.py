from flask import Blueprint, request, send_from_directory, send_file
from services import chatbotSession_services, assistant_services, stored_file_services
from models import Callback, ChatbotSession, Assistant
from utilities import helpers
from config import BaseConfig
from enums import UserType, DataType
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import io

chatbotSession_router: Blueprint = Blueprint('chatbotSession_router', __name__ , template_folder="../../templates")


# Get all assistant's user inputs
@chatbotSession_router.route("/assistant/<int:assistantID>/chatbotSessions", methods=["GET", "DELETE"])
@jwt_required
def chatbotSession(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    #############
    # Get the assistant's user inputs/chatbot sessions
    if request.method == "GET":
        s_callback: Callback = chatbotSession_services.getAllByAssistantID(assistantID)

        # Return response
        if not s_callback.Success:
            return helpers.jsonResponse(False, 400, "Error in retrieving sessions.")
        return helpers.jsonResponse(True, 200, s_callback.Message,
                                    {'sessionsList': helpers.getListFromSQLAlchemyList(s_callback.Data),
                                     'userTypes': [ut.value for ut in UserType],
                                     'dataTypes': [dt.value for dt in DataType],
                                     'filesPath': BaseConfig.USER_FILES
                                     })


    # Clear all user inputs/chatbot sessions
    if request.method == "DELETE":
        callback: Callback = chatbotSession_services.deleteAll(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

# Download files
@chatbotSession_router.route("/assistant/<int:assistantID>/chatbotSessions/<filename>", methods=['GET'])
@jwt_required
@helpers.gzipped
def chatbotSession_file_uploads(assistantID, filename):
    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    # Security procedure ->
    # the id of the user input session is included in the name of the file after "_" symbol, but encrypted
    try:
        id = helpers.decrypt_id(filename[filename.index('_')+1:filename.index('.')])[0]
        if not id: raise Exception
    except Exception as exc:
        return helpers.jsonResponse(False, 404, "File not found.", None)

    # Get associated chatbotSession with this file
    cs_callback: Callback = chatbotSession_services.getByID(id, assistantID)
    if not cs_callback.Success:
        return helpers.jsonResponse(False, 404, "File not found.", None)
    session: ChatbotSession = cs_callback.Data

    # Check if this user has access to user input session
    if assistant != session.Assistant:
        return helpers.jsonResponse(False, 401, "File access is unauthorised!")


    if request.method == "GET":
        callback: Callback = stored_file_services.downloadFile(filename)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "File not found.", None)

        file = callback.Data
        return send_file(
            io.BytesIO(file.get()['Body'].read()),
            mimetype=file.get()['ContentType']
        )


@chatbotSession_router.route("/assistant/<assistantID>/chatbotSessions/<sessionID>", methods=["DELETE"])
@jwt_required
def chatbotSession_delete_record(assistantID, sessionID):

    # Authenticate
    user = get_jwt_identity()['user']
    # check if the assistant that has the session is owned by this company (user)
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)

    if request.method == "DELETE":
        callback : Callback = chatbotSession_services.deleteByID(sessionID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

