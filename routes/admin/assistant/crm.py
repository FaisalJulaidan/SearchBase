from flask import Blueprint, request
from services import assistant_services
from services.CRM import crm_services
from models import Callback, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


crm_router: Blueprint = Blueprint('crm_router', __name__, template_folder="../../templates")


@crm_router.route("/assistant/<int:assistantID>/crm/connect", methods=['POST'])
@jwt_required
def connect_crm(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, security_callback.Data, security_callback.Message, None)
    assistant: Assistant = security_callback.Data

    # Connect to crm
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.connect(assistant, request.json) # crm details passed (auth, type)

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


@crm_router.route("/assistant/<int:assistantID>/crm/test", methods=['POST'])
@jwt_required
def test_crm_connection(assistantID):

    # No need for assistant authentication because testing crm connection should be public however at least
    # at least the user has to be logged in and has to token included in the request to minimise security risks

    # Connect to crm
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.testConnection(request.json) # crm details passed (auth, type)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)