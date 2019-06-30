from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import auto_pilot_services
from utilities import helpers

auto_pilot_router: Blueprint = Blueprint('auto_pilot_router', __name__, template_folder="../../templates")


# Get all AutoPilots & create new AutoPilot
@auto_pilot_router.route("/auto_pilots", methods=['GET', 'POST'])
@jwt_required
def auto_pilots():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = auto_pilot_services.fetchAll(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getListFromSQLAlchemyList(callback.Data))

    if request.method == "POST":
        callback: Callback = auto_pilot_services.create(request.json.get('name'),
                                                        request.json.get('description'),
                                                        user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


# Update & Delete auto pilots
@auto_pilot_router.route("/auto_pilot/<int:autoPilotID>", methods=['GET', 'DELETE', 'PUT'])
@jwt_required
def auto_pilot(autoPilotID):
    # Authenticate
    user = get_jwt_identity()['user']

    # Get AutoPilot by ID
    if request.method == "GET":
        callback = auto_pilot_services.getByID(autoPilotID, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, auto_pilot_services.parseAutoPilot(callback.Data))

    # Update AutoPilot
    if request.method == "PUT":
        data = request.json
        callback: Callback = auto_pilot_services \
            .update(autoPilotID,
                    data.get('name'),
                    data.get('description'),
                    user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))

    # Delete assistant
    if request.method == "DELETE":
        callback: Callback = auto_pilot_services.removeByID(autoPilotID, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@auto_pilot_router.route("/auto_pilot/<int:autoPilotID>/configs", methods=['PUT'])
@jwt_required
def auto_pilot_configs(autoPilotID):
    # Authenticate
    user = get_jwt_identity()['user']

    # Update AutoPilot extended configs
    if request.method == "PUT":
        data = request.json
        callback: Callback = auto_pilot_services \
            .updateConfigs(autoPilotID,
                           data.get('name'),
                           data.get('description'),
                           data.get('active'),
                           data.get('acceptApplications'),
                           data.get('acceptanceScore'),
                           data.get('sendAcceptanceEmail'),
                           data.get('rejectApplications'),
                           data.get('rejectionScore'),
                           data.get('sendRejectionEmail'),
                           data.get('sendCandidatesAppointments'),
                           data.get('openTimes'),  # TODO OpenTimeSlots & Appointments Feature
                           user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, auto_pilot_services.parseAutoPilot(callback.Data))


@auto_pilot_router.route("/auto_pilot/<int:autoPilotID>/status", methods=['PUT'])
@jwt_required
def auto_pilot_status(autoPilotID):
    # Authenticate
    user = get_jwt_identity()['user']

    # Update AutoPilot status
    if request.method == "PUT":
        data = request.json
        callback: Callback = auto_pilot_services.updateStatus(autoPilotID, data.get('status'), user['companyID'])

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, None)