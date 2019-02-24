from flask import Blueprint, request
from services import assistant_services, flow_services, user_services
from models import Callback, Assistant, User, BlockGroup
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


flow_router: Blueprint = Blueprint('flow_router', __name__, template_folder="../../templates")


@flow_router.route("/assistant/<int:assistantID>/flow", methods=['PUT'])
@jwt_required
def flow(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, security_callback.Data, security_callback.Message, None)
    assistant: Assistant = security_callback.Data

    # Update the blocks
    if request.method == "PUT":
        data = request.json
        callback: Callback = flow_services.updateFlow(data.get('flow'), assistant)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)