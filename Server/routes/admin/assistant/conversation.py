from flask import Blueprint, request, send_file
from services import conversation_services, assistant_services, stored_file_services
from models import Callback, Conversation, Assistant
from utilities import helpers
from config import BaseConfig
from utilities.enums import UserType, DataType
from flask_jwt_extended import jwt_required, get_jwt_identity

conversation_router: Blueprint = Blueprint('conversation_router', __name__ , template_folder="../../templates")


# Get all assistant's user inputs
@conversation_router.route("/assistant/<int:assistantID>/conversations", methods=["GET", "DELETE"])
@jwt_required
def conversation(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.")

    #############
    # Get the assistant's user inputs/chatbot conversation
    if request.method == "GET":
        s_callback: Callback = conversation_services.getAllByAssistantID(assistantID)
        # Return response
        if not s_callback.Success:
            return helpers.jsonResponse(False, 400, "Error in retrieving conversation.")
        return helpers.jsonResponse(True, 200, s_callback.Message,
                                    {'conversationsList': helpers.getListFromSQLAlchemyList(s_callback.Data, True)})


    # Clear all user inputs/chatbot conversation
    if request.method == "DELETE":
        callback: Callback = conversation_services.deleteAll(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

# Download files
@conversation_router.route("/assistant/<int:assistantID>/conversation/<filename>", methods=['GET'])
@jwt_required
@helpers.gzipped
def conversation_file_uploads(assistantID, filename):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.")
    assistant: Assistant = security_callback.Data

    # Security procedure ->
    # the id of the Conversation is included in the name of the file after "_" symbol, but encrypted
    try:
        id = helpers.decodeID(filename[filename.index('_') + 1:filename.index('.')])[0]
        if not id: raise Exception
    except Exception as exc:
        return helpers.jsonResponse(False, 404, "File not found.")

    # Get associated Conversation with this file
    cs_callback: Callback = conversation_services.getByID(id, assistantID)
    if not cs_callback.Success:
        return helpers.jsonResponse(False, 404, "File not found.")
    conversation: Conversation = cs_callback.Data


    # Check if this user has access to user input conversation
    if assistant != conversation.Assistant or (not conversation.StoredFile):
        return helpers.jsonResponse(False, 401, "File access is unauthorised!")


    if request.method == "GET":
        callback: Callback = stored_file_services.genPresigendURL(filename, stored_file_services.USER_FILES_PATH)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "File not found.")

        file = callback.Data
        return helpers.jsonResponse(True, 200, callback.Message, {'url': callback.Data})


@conversation_router.route("/assistant/<assistantID>/conversation/<conversationID>", methods=["DELETE"])
@jwt_required
def conversation_delete_record(assistantID, conversationID):

    # Authenticate
    user = get_jwt_identity()['user']
    # check if the assistant that has the session is owned by this company (user)
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.")

    if request.method == "DELETE":
        callback : Callback = conversation_services.deleteByID(conversationID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@conversation_router.route("/assistant/<assistantID>/conversation/<conversationID>/status", methods=["PUT"])
@jwt_required
def conversation_status(assistantID, conversationID):

    # Authenticate
    user = get_jwt_identity()['user']
    # check if the assistant that has the session is owned by this company (user)
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.")

    if request.method == "PUT":
        data = request.json
        callback : Callback = conversation_services.updateStatus(conversationID, assistantID, data.get('newStatus'))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
