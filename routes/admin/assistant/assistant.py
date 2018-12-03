from flask import Blueprint, render_template, request, redirect, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, Assistant, User
from services import statistics_services, assistant_services, admin_services, user_services, bot_services
from utilities import helpers

assistant_router: Blueprint = Blueprint('assistant_router', __name__, template_folder="../../templates")


@assistant_router.route("/admin/assistant/create", methods=['GET'])
def create_assistant_page():
    if request.method == "GET":
        # Add the template names as they appear here!!!!!!!!
        return admin_services.render("admin/create-assistant.html", templates={'names': ["Recruitment-Basic"]})


@assistant_router.route("/admin/assistant", methods=['POST'])
def assistant():
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
            callback_bot: Callback = bot_services.genBotViaTemplate(assistant_callback.Data, templateName)
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


# get all assistants
@assistant_router.route("/admin/assistants", methods=['GET'])
@jwt_required
def admin_home():
    if request.method == "GET":
        # Get all assistants
        print("hey")
        current_user = get_jwt_identity()

        return helpers.jsonResponse(True, 200, "Assistants Returned!", 'Yay')

        callback: Callback = assistant_services.getAll(session['CompanyID'])

        if callback.Success:
            return helpers.jsonResponse(True, 200, "Assistants Returned!", callback.Data)
        else:
            return helpers.jsonResponse(False, 401, "Cannot get Assistants!", callback.Data)


@assistant_router.route("/admin/assistant/<int:assistantID>", methods=['DELETE'])
def assistant_delete(assistantID):
    if request.method == "DELETE":
        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        if assistant.CompanyID != session.get('CompanyID', 0):
            return helpers.jsonResponse(False, 401, "You'r not authorised to delete this assistant", None)

        callback: Callback = assistant_services.removeByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)

        return helpers.jsonResponse(True, 200, callback.Message, None)
