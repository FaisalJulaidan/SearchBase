from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import company_services
from utilities import helpers

company_router: Blueprint = Blueprint('company_router', __name__, template_folder="../../templates")


@company_router.route("/company/logo", methods=['POST', 'DELETE'])
@jwt_required
def company_logo():

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, 'Error!', None)
    # Upload the logo
    if request.method == 'POST':
        if 'file' not in request.files:
            return helpers.jsonResponse(False, 404, "No file part")

        callback: Callback = company_services.uploadLogo(request.files['file'], user['companyID'])

    # Delete existing logo
    if request.method == 'DELETE':
        callback: Callback = company_services.deleteLogo(user['companyID'])

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)
