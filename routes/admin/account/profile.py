from flask_jwt_extended import jwt_required, get_jwt_identity

from services import profile_services, admin_services, newsletter_services, user_services
from models import Callback
from flask import Blueprint, request
from utilities import helpers

profile_router: Blueprint = Blueprint('profile_router', __name__, template_folder="../../templates")

# DEPRECATED
# @profile_router.route("/admin/profile", methods=['GET'])
# def profilePage():
#     if request.method == "GET":
#         return admin_services.render("admin/profile.html")


@profile_router.route("/profile", methods=['GET'])
@jwt_required
def profilePageData():
    if request.method == "GET":
        user = get_jwt_identity()['user']

        if request.method == "GET":
            email = user.get("email", None)

            profile_callback: Callback = profile_services.getUserAndCompany(email)
            if not profile_callback.Success:
                return helpers.jsonResponse(True, 200, "Profile has been retrieved 1",
                                            {"user": None, "email": email, "company": None, "newsletters": None,
                                             "userSettings": None})

            newsletter_callback: Callback = newsletter_services.checkForNewsletter(email)
            newsletters = newsletter_callback.Success

            userSettings_callback: Callback = user_services.getUserSettings(user.get("id", 0))

            if not userSettings_callback.Success or not userSettings_callback.Data:
                return helpers.jsonResponse(True, 200, "Profile has been retrieved 2",
                                            {"user": profile_callback.Data["user"], "email": email,
                                             "company": profile_callback.Data["company"], "newsletters": newsletters,
                                             "userSettings": None})

            return helpers.jsonResponse(True, 200, "Profile has been retrieved 3",
                                        {"user": profile_callback.Data["user"], "email": email,
                                         "company": profile_callback.Data["company"], "newsletters": newsletters,
                                         "userSettings": helpers.getDictFromSQLAlchemyObj(userSettings_callback.Data)})


@profile_router.route("/profile/profiledetails", methods=['POST'])
@jwt_required
def profileDetails():
    user = get_jwt_identity()['user']
    if request.method == "POST":
        names = request.json.get("name", "Error")
        newEmail = request.json.get("email", "error").lower()
        companyName = request.json.get("companyName", "Error")

        if names is "Error" and newEmail is "error" and companyName is "Error":
            return helpers.jsonResponse(False, 400, "Could not retrieve all written information.", None)

        names = names.split(" ")
        name1 = names[0]
        name2 = names[1]

        # update user details
        updateUser_callback: Callback = profile_services.updateUser(name1, name2, newEmail, user.get("id", 0))
        if not updateUser_callback.Success:
            return helpers.jsonResponse(False, 400, "Could not update User's information.", None)

        updateCompany_callback: Callback = profile_services.updateCompany(companyName, user.get("companyID", 0))
        if not updateCompany_callback.Success:
            return helpers.jsonResponse(False, 400,
                                        "Could not update Company's information. User information has been updated.",
                                        None)

        return helpers.jsonResponse(True, 200, "Records have been updated.", None)


@profile_router.route("/profile/datasettings", methods=['POST'])
@jwt_required
def dataSettings():
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
        userSettings_callback: Callback = user_services.createUpdateUserSettings(userID, tracking, techSupport,
                                                                                 accountSpecialist, notifications)

        if not userSettings_callback.Success:
            return helpers.jsonResponse(False, 400,
                                        userSettings_callback.Message + " Company, User information and newsletters has been updated.",
                                        None)

        return helpers.jsonResponse(True, 200, "Data Settings have been updated.", None)
