from flask import Blueprint, render_template, request, redirect, session
from services import  admin_services, userInput_services
from models import Callback, ChatbotSession
from config import BaseConfig

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# get all assistants
@userInput_router.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):

    if request.method == "GET":
        userInput_callback : Callback = userInput_services.getByAssistantID(assistantID)
        if not userInput_callback.Success : return admin_services.render("admin/data-storage.html", data=[], route=[])
        result = []
        for d in userInput_callback.Data:
            result.append({'data': d.Data, 'filePath': d.FilePath})
        print(result)
        route = BaseConfig.USER_FILES
        return admin_services.render("admin/data-storage.html", data=result, route=route)

