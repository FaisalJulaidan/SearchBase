from flask import Blueprint, render_template, request, redirect, session
from services import statistics_services, assistant_services,admin_services, sub_services
from models import Callback, Assistant
from utilties import helpers

assistant_router: Blueprint = Blueprint('assistant_router', __name__ , template_folder="../../templates")



@assistant_router.route("/admin/assistant/create", methods=['GET'])
def create_assistant_page():
    if request.method == "GET":
        return admin_services.render("admin/create-assistant.html")

@assistant_router.route("/admin/assistant/", methods=['POST'])
def assistant(assistantID):
    if request.method == "POST":
        callback: Callback = sub_services.getPlanByNickname(session.get('UserPlan', 'er'))
        if not callback.Success:
            return helpers.jsonResponse(False, 401, "You have no plan to create assistant", None)




        assistant: Assistant = callback.Data

        if assistant.CompanyID != session.get('CompanyID', 0):
            return helpers.jsonResponse(False, 401, "You'r not authorised to delete this assistant", None)

        callback: Callback = assistant_services.removeByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)

        return helpers.jsonResponse(True, 200, callback.Message, None)

# get all assistants
@assistant_router.route("/admin/assistants", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = statistics_services.getTotalAll()
        if callback.Success:

            # Get all assistants
            assistants: Callback = assistant_services.getAll(session['CompanyID']).Data

            # If there are assistants then convert them to a list of dict. Otherwise return empty list[].
            if assistants: assistants = helpers.getListFromSQLAlchemyList(assistants)
            else: assistants = []

            print(assistants)
            return render_template("admin/dashboard.html",
                                   totalClicks=callback.Data.ProductsReturned,
                                   loadedAnswers=callback.Data.QuestionsAnswered,
                                   assistants=assistants)
        else:
            print(callback.Message)
            return redirect('login')


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

