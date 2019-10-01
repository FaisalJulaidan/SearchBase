from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import user_services, company_services
from utilities import helpers

account_router: Blueprint = Blueprint('account_router', __name__, template_folder="../../templates")


@account_router.route("/account", methods=['GET'])
@jwt_required
def account():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":

        # Get user profile
        user_callback: Callback = user_services.getProfile(user.get('id', 0))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, "Could not retrieve profile", user_callback.Data)
        return helpers.jsonResponse(True, 200, "Profile retrieved successfully", user_callback.Data)


@account_router.route("/profile", methods=['POST'])
@jwt_required
def profile():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "POST":
        data = request.json
        callback: Callback = user_services.updateUser(data.get("firstname"),
                                                      data.get("surname"),
                                                      data.get("phoneNumber"),
                                                      data.get("chatbotNotifications"),
                                                      data.get("newsletters"),
                                                      data.get("timeZone"),
                                                      user.get("id", 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Could not update profile details.", None)
        return helpers.jsonResponse(True, 200, "Profile has been updated.", None)

@account_router.route("/profile/password", methods=['POST'])
@jwt_required
def change_password():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "POST":
        data = request.json
        callback: Callback = user_services.updatePasswordByID(user.get('id', 0),
                                                              data['newPassword'],
                                                              data['oldPassword'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "Password updated successfully", callback.Data)


@account_router.route("/company", methods=['POST'])
@jwt_required
def profile_settings():
    user = get_jwt_identity()['user']
    if request.method == "POST":

        data = request.json
        callback: Callback = company_services.update(data.get("companyName"),
                                                     data.get("websiteURL"),
                                                     data.get("trackData"),
                                                     data.get("techSupport"),
                                                     data.get("accountSpecialist"),
                                                     user.get('companyID'))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, "Data Settings have been updated.", None)


@account_router.route("/company/logo", methods=['POST', 'DELETE'])
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
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
