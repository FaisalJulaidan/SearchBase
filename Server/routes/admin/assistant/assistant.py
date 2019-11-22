from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import assistant_services
from services.user_services import getOwnersOfAssistants
from utilities import helpers, wrappers


import json

assistant_router: Blueprint = Blueprint('assistant_router', __name__, template_folder="../../templates")


# Get all assistants & Add new assistant
@assistant_router.route("/assistants", methods=['GET', 'POST'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistants():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        # Get all assistants
        callback: Callback = assistant_services.getAll(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Assistants")

        callback: Callback = getOwnersOfAssistants(helpers.getListFromLimitedQuery(['ID',
                                                                                    'Name',
                                                                                    'Description',
                                                                                    'Message',
                                                                                    'TopBarText',
                                                                                    'Active',
                                                                                    'OwnerID'],
                                                                                   callback.Data))
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Owners")

        return helpers.jsonResponse(True, 200,
                                    "Assistants Returned!",
                                    {"assistants": callback.Data})
    if request.method == "POST":
        data = request.json
        callback: Callback = assistant_services.create(data.get('assistantName'),
                                                       data.get('assistantDesc'),
                                                       data.get('welcomeMessage'),
                                                       data.get('topBarText'),
                                                       data.get('flow'),
                                                       data.get('template'),
                                                       user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Couldn't create assistant. Please try again")
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


@assistant_router.route("/assistant/<int:assistantID>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!', None)

    if request.method == "GET":
        # Fetch assistant
        callback: Callback = assistant_services.getByID(assistantID, user['companyID'], True)
        # print(helpers.getDictFromSQLAlchemyObj(callback.Data, True))
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Can't fetch assistant")

        # print(json.dumps(callback.Data))
        return helpers.jsonResponse(True, 200,
                                    "Assistant fetched successfully",
                                    helpers.getDictFromSQLAlchemyObj(callback.Data, True))


    # Update assistant
    if request.method == "PUT":
        data = request.json
        callback: Callback = assistant_services.update(assistantID,
                                                       data.get("assistantName"),
                                                       data.get('assistantDesc'),
                                                       data.get("welcomeMessage"),
                                                       data.get("topBarText"),
                                                       user['companyID']
                                                       )
    # Delete assistant
    if request.method == "DELETE":
        callback: Callback = assistant_services.removeByID(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


@assistant_router.route("/assistant/<int:assistantID>/configs", methods=['PUT'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_configs(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant
    if request.method == "PUT":
        updatedSettings = request.json
        callback: Callback = assistant_services.updateConfigs(assistantID,
                                                              updatedSettings.get("assistantName"),
                                                              updatedSettings.get('assistantDesc'),
                                                              updatedSettings.get("welcomeMessage"),
                                                              updatedSettings.get("topBarTitle"),
                                                              updatedSettings.get("secondsUntilPopup"),
                                                              updatedSettings.get("notifyEvery"),
                                                              updatedSettings.get('config'),
                                                              updatedSettings.get("owners"),
                                                              user['companyID']
                                                              )
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


# Activate or deactivate assistant
@assistant_router.route("/assistant/<int:assistantID>/status", methods=['PUT'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_status(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    # Update assistant status
    if request.method == "PUT":
        data = request.json
        callback: Callback = assistant_services.updateStatus(assistantID, data.get('status'), user['companyID'])

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, None)


# Connect assistant to CRM
@assistant_router.route("/assistant/<int:assistantID>/crm", methods=['POST', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_crm_connect(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.connectToCRM(assistantID, request.json.get('CRMID'), user['companyID'])

    if request.method == "DELETE":
        callback: Callback = assistant_services.disconnectFromCRM(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)


# Connect assistant to Calendar
@assistant_router.route("/assistant/<int:assistantID>/calendar", methods=['POST', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_calendar_connect(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.connectToCalendar(assistantID, request.json.get('CalendarID'),
                                                                  user['companyID'])

    if request.method == "DELETE":
        callback: Callback = assistant_services.disconnectFromCalendar(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)


# Connect assistant to Messenger
@assistant_router.route("/assistant/<int:assistantID>/messenger", methods=['POST', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_messenger_connect(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.connectToMessenger(assistantID, request.json.get('messengerID'),
                                                                  user['companyID'])

    if request.method == "DELETE":
        callback: Callback = assistant_services.disconnectFromMessenger(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)

# Connect assistant to AutoPilot
@assistant_router.route("/assistant/<int:assistantID>/auto_pilot", methods=['POST', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_auto_pilot_connect(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.connectToAutoPilot(assistantID,
                                                                   request.json.get('AutoPilotID'),
                                                                   user['companyID'])

    if request.method == "DELETE":
        callback: Callback = assistant_services.disconnectFromCRM(assistantID,
                                                                  user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)


# Upload and delete custom assistant logo
@assistant_router.route("/assistant/<int:assistantID>/logo", methods=['POST', 'DELETE'])
@jwt_required
@wrappers.AccessAssistantsRequired
def assistant_logo(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!')
    if request.method == "POST":
        callback: Callback = assistant_services.uploadLogo(request.files['file'], assistantID, user['companyID'])

    if request.method == "DELETE":
        callback: Callback = assistant_services.deleteLogo(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
