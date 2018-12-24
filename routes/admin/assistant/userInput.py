from flask import Blueprint, render_template, request, redirect, session
from services import admin_services, userInput_services, assistant_services
from models import Callback, ChatbotSession, Assistant
from utilities import helpers
from config import BaseConfig
from flask_jwt_extended import jwt_required, get_jwt_identity

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# Get all assistant's user inputs
@userInput_router.route("/assistant/<int:assistantID>/userinput", methods=["GET", "DELETE"])
@jwt_required
def admin_user_input(assistantID):

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
        callback: Callback = userInput_services.getByAssistantID(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, {'data': helpers.getListFromSQLAlchemyList(callback.Data),
                                                                  'filesPath': BaseConfig.USER_FILES})


    # Clear all user inputs/chatbot sessions
    if request.method == "DELETE":
        callback: Callback = userInput_services.deleteAll(assistantID)
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)



@userInput_router.route("/admin/assistant/<assistantID>/<recordID>/delete", methods=["GET"])
def admin_record_delete(assistantID, recordID):

    if request.method == "GET":
        deleteRecord_callback : Callback = userInput_services.deleteByID(recordID)

        return str(deleteRecord_callback.Success)

@userInput_router.route("/admin/assistant/<assistantID>/deleteAll", methods=["GET"])
def admin_record_delete_all(assistantID):

    if request.method == "GET":
        deleteRecords_callback : Callback = userInput_services.deleteAll(assistantID)

        return helpers.redirectWithMessageAndAssistantID("admin_user_input", assistantID, deleteRecords_callback.Message)