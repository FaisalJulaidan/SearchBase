from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, Assistant
from services import assistant_services
from utilities import helpers

assistant_router: Blueprint = Blueprint('assistant_router', __name__, template_folder="../../templates")


# Get all assistants & Add new assistant
@assistant_router.route("/assistants", methods=['GET', 'POST'])
@jwt_required
def assistants():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        # Get all assistants
        callback: Callback = assistant_services.getAll(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot get Assistants!",
                                    helpers.getListFromSQLAlchemyList(callback.Data))

        # notifications_callback: Callback = assistant_services.getAllNotificationsRegisters()
        # if notifications_callback.Success:
        #     registers = helpers.getListFromSQLAlchemyList(notifications_callback.Data)
        # else:
        #     registers = {}

        return helpers.jsonResponse(True, 200, "Assistants Returned!",
                                    {"assistants": helpers.getListFromSQLAlchemyList(callback.Data)})
    if request.method == "POST":
        data = request.json
        callback: Callback = assistant_services.create(data.get('assistantName'),
                                                       data.get('welcomeMessage'),
                                                       data.get('topBarTitle'),
                                                       data.get('secondsUntilPopup'),
                                                       data.get('alertsEnabled'),
                                                       data.get('alertEvery'),
                                                       data.get('template'),
                                                       user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Cannot add Assistant")
        return helpers.jsonResponse(True, 200, "Assistant added successfully!", helpers.getDictFromSQLAlchemyObj(callback.Data))


@assistant_router.route("/assistant/<int:assistantID>", methods=['DELETE', 'PUT'])
@jwt_required
def assistant(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, security_callback.Message)
    assistant: Assistant = security_callback.Data

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant
    if request.method == "PUT":
        updatedSettings = request.json
        callback: Callback = assistant_services.update(assistantID,
                                                       updatedSettings.get("assistantName", "None"),
                                                       updatedSettings.get("welcomeMessage", "None"),
                                                       updatedSettings.get("topBarTitle", "None"),
                                                       updatedSettings.get("secondsUntilPopup", "None"),
                                                       updatedSettings.get("alertsEnabled", False),
                                                       updatedSettings.get("alertEvery", 24))
    # Delete assistant
    if request.method == "DELETE":
        callback: Callback = assistant_services.removeByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)

    return helpers.jsonResponse(True, 200, callback.Message, None)


# Activate or deactivate assistant
@assistant_router.route("/assistant/<int:assistantID>/status", methods=['PUT'])
@jwt_required
def assistant_status(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, security_callback.Message)
    assistant: Assistant = security_callback.Data

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant status
    if request.method == "PUT":
        data = request.json
        callback: Callback = assistant_services.changeStatus(assistant, data.get('status'))

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)


# Connect assistant to CRM
@assistant_router.route("/assistant/<int:assistant_id>/crm/<int:crm_id>", methods=['POST'])
@jwt_required
def assistant_crm_connect(assistant_id, crm_id):
    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistant_id, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, security_callback.Message)
    assistant: Assistant = security_callback.Data

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.connect_to_crm(assistant, crm_id)

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)


# Disconnect assistant from CRM
@assistant_router.route("/assistant/<int:assistant_id>/crm/disconnect", methods=['DELETE'])
@jwt_required
def assistant_crm_disconnect(assistant_id):

    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistant_id, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, security_callback.Message)
    assistant: Assistant = security_callback.Data

    callback: Callback = Callback(False, 'Error!')
    if request.method == "DELETE":
        callback: Callback = assistant_services.disconnect_from_crm(assistant)

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)
