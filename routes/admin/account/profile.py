from flask_jwt_extended import jwt_required, get_jwt_identity

from services import newsletter_services, user_services, company_services
from models import Callback, User
from flask import Blueprint, request
from utilities import helpers

profile_router: Blueprint = Blueprint('profile_router', __name__, template_folder="../../templates")

# DEPRECATED
# @profile_router.route("/admin/profile", methods=['GET'])
# def profilePage():
#     if request.method == "GET":
#         return admin_services.render("admin/profile.html")


@profile_router.route("/profile", methods=['GET', 'POST'])
@jwt_required
def profile():

    # Authenticate
    user = get_jwt_identity()['user']

    # Get profile details
    if request.method == "GET":
        email = user.get("email", None)

        # Get user record
        user_callback: Callback = user_services.getByEmail(email)
        if not user_callback.Success:
            return helpers.jsonResponse(True, 200, "Conversation has been retrieved 1",
                                        {"user": None, "email": email, "company": None, "newsletters": None,
                                         "userSettings": None})
        user : User = user_callback.Data

        # Check newsletter
        newsletter_callback: Callback = newsletter_services.checkForNewsletter(email)
        newsletters = newsletter_callback.Success

        # Get user's settings
        userSettings_callback: Callback = user_services.getUserSettings(user.ID)
        if not userSettings_callback.Success or not userSettings_callback.Data:
            return helpers.jsonResponse(True, 200, "Conversation has been retrieved 2",
                                        {"user": helpers.getDictFromSQLAlchemyObj(user), "email": email,
                                         "company": helpers.getDictFromSQLAlchemyObj(user.Company), "newsletters": newsletters,
                                         "userSettings": None})

        return helpers.jsonResponse(True, 200, "Conversation has been retrieved 3",
                                    {"user": helpers.getDictFromSQLAlchemyObj(user), "email": email,
                                     "company": helpers.getDictFromSQLAlchemyObj(user.Company), "newsletters": newsletters,
                                     "userSettings": helpers.getDictFromSQLAlchemyObj(userSettings_callback.Data)})

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
        userID = user.get("id", 0)
        email = user.get("email", None)

        newsletters = request.json.get("newsletters", "Error")
        tracking = request.json.get("trackData", "Error")
        techSupport = request.json.get("techSupport", "Error")
        notifications = request.json.get("statNotifications", "Error")
        accountSpecialist = request.json.get("accountSpecialist", "Error")

        if newsletters == "Error" or tracking == "Error" or techSupport == "Error" or notifications == "Error" or accountSpecialist == "Error":
            return helpers.jsonResponse(False, 400, "Input could not be received", None)

        # update newsletters
        if newsletters:
            newsletter_callback: Callback = newsletter_services.checkForNewsletter(email)
            if not newsletter_callback.Success:
                newsletter_callback: Callback = newsletter_services.addNewsletterPerson(email)
        else:
            newsletter_callback: Callback = newsletter_services.removeNewsletterPerson(email)
        if not newsletter_callback.Success:
            return helpers.jsonResponse(False, 400,
                                        newsletter_callback.Message + " Company and User information has been updated.",
                                        None)

        # update user settings
        userSettings_callback: Callback = user_services.updateUserSettings(userID, tracking, techSupport,
                                                                           accountSpecialist, notifications)

        if not userSettings_callback.Success:
            return helpers.jsonResponse(False, 400,
                                        userSettings_callback.Message + " Company, User information and newsletters has been updated.",
                                        None)

        return helpers.jsonResponse(True, 200, "Data Settings have been updated.", None)
