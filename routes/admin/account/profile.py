from flask_jwt_extended import jwt_required, get_jwt_identity

from services import newsletter_services, user_services, company_services
from models import Callback, User
from flask import Blueprint, request
from utilities import helpers

profile_router: Blueprint = Blueprint('profile_router', __name__, template_folder="../../templates")


@profile_router.route("/profile", methods=['GET', 'POST'])
@jwt_required
def profile():

    # Authenticate
    user = get_jwt_identity()['user']

    # Get profile details
    if request.method == "GET":

        # Get user profile
        user_callback: Callback = user_services.getProfile(user.get('id', 0))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, " Could not retrieve profile", user_callback.Data)
        return helpers.jsonResponse(True, 200, "Profile retrieved successfully", user_callback.Data)


    # Update profile details
    if request.method == "POST":
        name = request.json.get("name", None)
        newEmail = request.json.get("email", None)
        companyName = request.json.get("companyName", None)

        if not(name or newEmail or companyName):
            return helpers.jsonResponse(False, 400, "Data missing..", None)

        firstname = name.strip().split(' ')[0]
        surname = ' '.join((name + ' ').split(' ')[1:]).strip()


        # update user details
        callback: Callback = user_services.updateUser(firstname, surname, newEmail.lower(), user.get("id", 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Could not update User's information.", None)

        callback: Callback = company_services.updateCompany(companyName, user.get("companyID", 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400,"Could not update Company's information.", None)

        return helpers.jsonResponse(True, 200, "Conversation has been updated.", None)


@profile_router.route("/profile/settings", methods=['POST'])
@jwt_required
def profile_settings():
    user = get_jwt_identity()['user']
    if request.method == "POST":


        data = request.json

        # update newsletters
        newsletter_callback = (False, "")
        if data.get("newsletters"):
            newsletter_callback: Callback = newsletter_services.checkForNewsletter(user.get("email"))
            if not newsletter_callback.Success:
                newsletter_callback: Callback = newsletter_services.addNewsletterPerson(user.get("email"))
        elif data.get("newsletters") is False:
            newsletter_callback: Callback = newsletter_services.removeNewsletterPerson(user.get("email"))

        if not newsletter_callback.Success:
            return helpers.jsonResponse(False, 400, newsletter_callback.Message)

        # update user settings
        userSettings_callback: Callback = user_services.updateUserSettings(data.get("id"),
                                                                           data.get("tracking"),
                                                                           data.get("techSupport"),
                                                                           data.get("accountSpecialist"),
                                                                           data.get("notifications"))

        if not userSettings_callback.Success:
            return helpers.jsonResponse(False, 400, userSettings_callback.Message)

        return helpers.jsonResponse(True, 200, "Data Settings have been updated.", None)


@profile_router.route("/profile/password", methods=['POST'])
@jwt_required
def change_password():

    # Authenticate
    user = get_jwt_identity()['user']

    # Get profile details
    if request.method == "POST":
        data = request.json
        # Get user profile
        callback: Callback = user_services.changePasswordByID(user.get('id', 0), data['newPassword'], data['oldPassword'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "Password updated successfully", callback.Data)