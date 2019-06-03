from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
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
            return helpers.jsonResponse(False, 404, "Cannot get Assistants!")

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
                                                       data.get('config'),
                                                       user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


@assistant_router.route("/assistant/<int:assistantID>", methods=['DELETE', 'PUT'])
@jwt_required
def assistant(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant
    if request.method == "PUT":
        updatedSettings = request.json
        callback: Callback = assistant_services.update(assistantID,
                                                       updatedSettings.get("assistantName"),
                                                       updatedSettings.get("welcomeMessage"),
                                                       updatedSettings.get("topBarTitle"),
                                                       updatedSettings.get("secondsUntilPopup"),
                                                       updatedSettings.get("alertsEnabled"),
                                                       updatedSettings.get("alertEvery"),
                                                       updatedSettings.get('config'),
                                                       user['companyID']
                                                       )
    # Delete assistant
    if request.method == "DELETE":
        callback: Callback = assistant_services.removeByID(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


# Activate or deactivate assistant
@assistant_router.route("/assistant/<int:assistantID>/status", methods=['PUT'])
@jwt_required
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


# Connect assistant to AutoPilot
@assistant_router.route("/assistant/<int:assistantID>/auto_pilot", methods=['POST', 'DELETE'])
@jwt_required
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



@assistant_router.route("/assistant/<int:assistantID>/logo", methods=['POST', 'DELETE'])
@jwt_required
def assistant_logo(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!', None)
    # Upload the logo
    if request.method == 'POST':
        if 'file' not in request.files:
            return helpers.jsonResponse(False, 404, "No file part")

        callback: Callback = assistant_services.uploadLogo(assistantID, request.files['file'], user['companyID'])

    # Delete existing logo
    if request.method == 'DELETE':
        callback: Callback = assistant_services.deleteLogo(assistantID, user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)
