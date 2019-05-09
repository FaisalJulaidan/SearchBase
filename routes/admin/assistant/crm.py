from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services.CRM import crm_services
from utilities import helpers

crm_router: Blueprint = Blueprint('crm_router', __name__, template_folder="../../templates")

# Get all company CRMs
@crm_router.route("/crm", methods=["GET"])
@jwt_required
def crm_connect():
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "GET":
        callback: Callback = crm_services.getAll(user.get("companyID"))  # crm details passed: auth, type

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


# Connect CRM
@crm_router.route("/crm/connect", methods=["POST"])
@jwt_required
def crm_connect():
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.connect(user.get("companyID"), request.json)  # crm details passed: auth, type

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


# Edit/Disconnect CRM
@crm_router.route("/crm/<int:crm_id>", methods=["PUT", "DELETE"])
@jwt_required
def crm_control(crm_id):
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "PUT":
        callback: Callback = crm_services.update(crm_id, user.get("companyID"), request.json)

    if request.method == "DELETE":
        callback: Callback = crm_services.disconnect(crm_id, user.get("companyID"))

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


# Test CRM
@crm_router.route("/crm/test", methods=['POST'])
@jwt_required
def test_crm_connection():
    # No need for assistant authentication because testing crm connection should be public however at least
    # the user has to be logged in and has the token included in the request to minimise security risks

    # Connect to crm
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.testConnection(request.json)  # crm details passed (auth, type)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
