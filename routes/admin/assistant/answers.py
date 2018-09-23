from flask import Blueprint, request, flash
from services import admin_services, answer_services
from models import Callback
from utilities import helpers
from json import dumps

answers_router: Blueprint = Blueprint('answers_router', __name__, template_folder="../../templates")


# # TODO rewrite
# @answers_router.route("/admin/assistant/<assistantID>/answers", methods=['GET', 'POST'])
# def admin_answers(assistantID):
#     if request.method == "GET":
#         callback: Callback = questions_services.getByAssistantID(assistantID)
#         if not callback.Success:
#             flash({'type': 'danger', 'msg': callback.Message})
#             return admin_services.render("admin/answers.html")
#         questions = helpers.getListFromSQLAlchemyList(callback.Data)
#
#         return admin_services.render("admin/answers.html",
#                                      questions=questions)


# TODO rewrite
@answers_router.route("/admin/assistant/<assistantID>/answers", methods=['GET', 'POST'])
def admin_answers(assistantID):
    if request.method == "GET":
        # callback: Callback = questions_services.getByAssistantID(assistantID)
        # if not callback.Success:
        #     flash({'type': 'danger', 'msg': callback.Message})
        #     return admin_services.render("admin/answers.html")
        #
        # questions = helpers.getListFromSQLAlchemyList(callback.Data)
        # answers = []
        #
        # for question in questions:
        #     callback: Callback = answer_services.getByQuestionID(question['ID'])
        #     if not callback.Success:
        #         flash({'type': 'danger', 'msg': callback.Message})
        #         return admin_services.render("admin/answers.html")
        #     answers.append(helpers.getListFromSQLAlchemyList(callback.Data))

        return admin_services.render("admin/answers.html", questions={}, answers={})

    elif request.method == "POST":
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                     "Error in getting company's records!")
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None or "Error" in assistant:
                return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                         "Error in getting assistant's records!")
            else:
                selected_question = request.form.get("question", default="Error")  # question_text;question_type
                if "Error" in selected_question:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                             "Error in getting selected question!")

                question = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=? AND Question=?;",
                                                      [assistantID, selected_question.split(";")[0]])
                if question is None or "Error" in question:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                             "Error in getting question's records")

                questionID = question[0]
                currentAnswers = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;", [questionID])
                if currentAnswers is None or "Error" in currentAnswers:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                             "Error in getting old answers!")
                if (currentAnswers is not None):
                    deleteOldQuestions = delete_from_table("DELETE FROM Answers WHERE QuestionID=?;", [questionID])
                    if deleteOldQuestions is None or "Error" in deleteOldQuestions:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                                 "Error in deleting old answers!")

                noa = 1
                for key in request.form:
                    if "pname" in key:
                        noa += 1

                for i in range(1, noa):
                    answer = request.form.get("pname" + str(i), default="Error")
                    try:
                        keyword = request.form.getlist("keywords" + str(i))
                    except:
                        keyword = "Error"
                    keyword = ','.join(keyword)
                    action = request.form.get("action" + str(i), default="None")
                    if action != "Next Question by Order" and not session['UserPlan']['Settings']['ExtendedLogic']:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                                 "It appears you tried to access extended logic without having access to it. Action aborted!")
                    if "Error" in answer or "Error" in keyword or "Error" in action:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                                 "Error in getting your input.")
                    insertAnswer = insert_into_database_table(
                        "INSERT INTO Answers (QuestionID, Answer, Keyword, Action) VALUES (?,?,?,?);",
                        (questionID, answer, keyword, action))
                    if insertAnswer is None or "Error" in insertAnswer:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID,
                                                                 "Error in updating answers!")

                return redirect("/admin/assistant/{}/answers".format(assistantID) + "?res=" + str(noa) + "")

@answers_router.route("/admin/assistant/<assistantID>/answers/getAnswers/<questionID>", methods=['GET'])
def admin_answers_api(assistantID,questionID):
    callback: Callback = answer_services.getByQuestionID(questionID)
    if not callback.Success:
        flash({'type': 'danger', 'msg': callback.Message})
        return {"error": callback.Message}
    answers = helpers.getListFromSQLAlchemyList(callback.Data)
    return dumps(answers)
