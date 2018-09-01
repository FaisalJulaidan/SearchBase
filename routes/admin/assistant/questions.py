from flask import Blueprint, request, flash
from services import admin_services, questions_services
from models import Callback, Question
from utilties import helpers

questions_router: Blueprint = Blueprint('questions_router', __name__, template_folder="../../templates")

@questions_router.route("/admin/assistant/<assistantID>/questions", methods=['GET', 'POST'])
def admin_questions(assistantID):
    if request.method == "GET":
        callback: Callback = questions_services.getByAssistantID(assistantID)

        if not callback.Success:
            flash({'type': 'danger', 'msg': callback.Message})
            return admin_services.render("admin/questions.html")

        questionList = helpers.getListFromSQLAlchemyList(callback.Data)
        return admin_services.render("admin/questions.html", data=questionList, id=assistantID)

    elif request.method == "POST":
        callback: Callback = questions_services.reset(assistantID)
        if callback.Success:
            requestedQuestions = request.json
            isAllAdded = True

            for rq_question in requestedQuestions:
                callback: Callback = questions_services.add(Question(Question=rq_question['Question'],
                                                                     Type=rq_question['Type'],
                                                                     AssistantID=assistantID))
                if not callback.Success:
                    print(callback.Message)
                    flash({'type': 'danger', 'msg': 'Cannot update questions for this assistant'})
                    isAllAdded = False
                    break

            if isAllAdded:
                flash({'type': 'success', 'msg': str(len(requestedQuestions)) + ' Questions updated successfully'})
        return 'Done'

