from flask import Blueprint, render_template, request, redirect, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, Assistant, User
from services import statistics_services, assistant_services, admin_services, user_services, flow_services, \
    profile_services, newsletter_services
from utilities import helpers

assistant_router: Blueprint = Blueprint('assistant_router', __name__, template_folder="../../templates")


@assistant_router.route("/admin/assistant/create", methods=['GET'])
def create_assistant_page():
    if request.method == "GET":
        # Add the template names as they appear here!!!!!!!!
        return admin_services.render("admin/create-assistant.html", templates={'names': ["Recruitment-Basic"]})


@assistant_router.route("/admin/assistant", methods=['POST'])
def assistantttt():
    if request.method == "POST":

        # Get the admin user who is logged in and wants to create a new user.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return redirect("login")
        user: User = callback.Data

        # TODO: do restrictions for assistant creation based on current user's plan
        # callback: Callback = sub_services.getPlanByNickname(session.get('UserPlan', 'er'))
        # if not callback.Success:
        #     return helpers.jsonResponse(False, 401, "You have no plan to create assistant", None)

        name = request.form.get("name", default='').strip()
        welcomeMsg = request.form.get("welcome-message", default='').strip()
        timePopup = request.form.get("timeto-autopop", default='').strip()
        templateName = request.form.get("template-name", default='').strip()
        topBarText = request.form.get("top-bar-text", default='').strip()

        assistant_callback: Callback = assistant_services.create(name, None, welcomeMsg, topBarText, timePopup,
                                                                 user.Company)
        if not assistant_callback.Success:
            return helpers.jsonResponse(False, 400, "Couldn't create the assistant", None)

        if 'none' not in templateName:
            callback_bot: Callback = flow_services.genFlowViaTemplate(assistant_callback.Data, templateName)
            if not callback_bot.Success:
                # if template has an error remove the created assistant
                assistant_services.removeByID(assistant_callback.Data.ID)
                return helpers.jsonResponse(False, 400, "Error with the selected template.", callback_bot.Message)

        return helpers.jsonResponse(True, 200, callback.Message, {'id': assistant_callback.Data.ID})


############# DEPREACTED #############
# get all assistants
# @assistant_router.route("/admin/assistants", methods=['GET'])
def admin_homeDEPREACTED():
    if request.method == "GET":
        callback: Callback = statistics_services.getTotalAll()
        if callback.Success:

            # Get all assistants
            assistants: Callback = assistant_services.getAll(session['CompanyID']).Data

            # If there are assistants then convert them to a list of dict. Otherwise return empty list[].
            if assistants:
                assistants = helpers.getListFromSQLAlchemyList(assistants)
            else:
                assistants = []

            return render_template("admin/dashboard.html",
                                   totalClicks=callback.Data.ProductsReturned,
                                   loadedAnswers=callback.Data.QuestionsAnswered,
                                   assistants=assistants)
        else:

            return redirect('login')

# @assistant_router.route("/profile", methods=['GET'])
# @jwt_required
# def profilePageData():
#     user = get_jwt_identity()['user']
#     print("USER: ", user)
#     if request.method == "GET":
#         email = user.get("email", None)
#
#         print("EMAIL: ", email)
#
#         profile_callback: Callback = profile_services.getUserAndCompany(email)
#         if not profile_callback.Success:
#             return helpers.jsonResponse(True, 200, "Profile has been retrieved 1",
#                                         {"user": None, "email": email, "company": None, "newsletters": None,
#                                          "userSettings": None})
#
#         newsletter_callback: Callback = newsletter_services.checkForNewsletter(email)
#         newsletters = newsletter_callback.Success
#
#         userSettings_callback: Callback = user_services.getUserSettings(user.get("id", None))
#         if not userSettings_callback.Success:
#             return helpers.jsonResponse(True, 200, "Profile has been retrieved 2",
#                                         {"user": profile_callback.Data["user"], "email": email,
#                                          "company": profile_callback.Data["company"], "newsletters": newsletters,
#                                          "userSettings": None})
#
#         return helpers.jsonResponse(True, 200, "Profile has been retrieved 3",
#                                     {"user": profile_callback.Data["user"], "email": email,
#                                      "company": profile_callback.Data["company"], "newsletters": newsletters,
#                                      "userSettings": userSettings_callback.Data})

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
            return helpers.jsonResponse(False, 404, "Cannot get Assistants!",
                                    helpers.getListFromSQLAlchemyList(callback.Data))
        return helpers.jsonResponse(True, 200, "Assistants Returned!",
                                        helpers.getListFromSQLAlchemyList(callback.Data))
    if request.method == "POST":
        data = request.json
        callback: Callback = assistant_services.create(data.get('assistantName'),
                                                       data.get('welcomeMessage'),
                                                       data.get('topBarTitle'),
                                                       data.get('secondsUntilPopup'),
                                                       user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Cannot add Assistant")
        return helpers.jsonResponse(True, 200, "Assistant added successfully!", helpers.getDictFromSQLAlchemyObj(callback.Data))


@assistant_router.route("/assistant/<int:assistantID>", methods=['DELETE', 'PUT'])
@jwt_required
def assistant(assistantID):
    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID)
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!")

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant
    if request.method == "PUT":
        updatedSettings = request.json
        callback: Callback = assistant_services.update(assistantID,
                                                       updatedSettings.get("assistantName"),
                                                       updatedSettings.get("welcomeMessage"),
                                                       updatedSettings.get("topBarTitle"),
                                                       updatedSettings.get("secondsUntilPopup"))
    # Delete assistant
    if request.method == "DELETE":
        callback: Callback = assistant_services.removeByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)

    return helpers.jsonResponse(True, 200, callback.Message, None)


# Activate or deactivate assistant
@assistant_router.route("/assistant/<int:assistantID>/status/<int:statusValue>", methods=['PUT'])
@jwt_required
def assistant_status(assistantID, statusValue):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID)
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!")

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Update assistant status
    if request.method == "PUT":
        callback: Callback = assistant_services.changeStatus(assistant, statusValue)

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, None)
    return helpers.jsonResponse(True, 200, callback.Message, None)
