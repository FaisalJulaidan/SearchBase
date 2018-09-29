from flask import Blueprint, render_template, request, redirect, session
from services import  admin_services, userInput_services
from models import Callback, ChatbotSession
from config import BaseConfig
from utilities import helpers

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# get all assistants
@userInput_router.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):

    if request.method == "GET":
        userInput_callback : Callback = userInput_services.getByAssistantID(assistantID)
        if not userInput_callback.Success : return admin_services.render("admin/data-storage.html", data=[], route=[])
        result = []
        for d in userInput_callback.Data:
            result.append({'id': d.ID, 'data': d.Data, 'filePath': d.FilePath, "dateTime": d.DateTime})
        route = BaseConfig.USER_FILES
        return admin_services.render("admin/data-storage.html", assistantID=assistantID, data=result, route=route)


@userInput_router.route("/admin/assistant/<assistantID>/<recordID>/delete", methods=["GET"])
def admin_record_delete(assistantID, recordID):

    if request.method == "GET":
        deleteRecord_callback : Callback = userInput_services.deleteByID(recordID)

        return str(deleteRecord_callback.Success)

@userInput_router.route("/admin/assistant/<assistantID>/deleteAll", methods=["GET"])
def admin_record_delete_all(assistantID):

    if request.method == "GET":
        deleteRecords_callback : Callback = userInput_services.deleteAll(assistantID)

        return helpers.redirectWithMessageAndAssistantID("admin_user_input", assistantID, deleteRecords_callback.Message)