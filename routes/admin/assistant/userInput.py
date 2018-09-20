from flask import Blueprint, render_template, request, redirect, session
from services import  admin_services, userInput_services
from models import Callback, ChatbotSession

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# get all assistants
@userInput_router.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):

    if request.method == "GET":
        # question_callback : Callback = questions_services.getByAssistantID(assistantID)
        # if not question_callback.Success : return admin_services.render("admin/data-storage.html")
        #
        # data=[]
        #
        # for question in question_callback.Data:
        #
        #     userInput_callback : Callback = userInput_services.getByQuestionID(question.ID)
        #     if not userInput_callback.Success : return admin_services.render("admin/data-storage.html")
        #
        #     userInputData = admin_services.convertForJinja(userInput_callback.Data)
        #
        #     data.append(userInputData)

        return admin_services.render("admin/data-storage.html", data={})


