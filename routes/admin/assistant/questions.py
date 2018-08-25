from flask import Blueprint, request, redirect,flash
from services import assistant_services, admin_services, questions_services
from models import Callback, Question
from utilties import helpers

questions_router: Blueprint = Blueprint('questions_router', __name__, template_folder="../../templates")

@questions_router.route("/admin/assistant/<assistantID>/questions", methods=['GET', 'POST'])
def admin_questions(assistantID):
    if request.method == "GET":
        callback: Callback = questions_services.getByAssistantID(assistantID)

        if not callback.Success:
            flash({'type': 'danger', 'msg': 'Error in getting your questions!'})
            return admin_services.render("admin/questions.html")

        questionList = helpers.getListFromSQLAlchemyList(callback.Data)
        return admin_services.render("admin/questions.html", data=questionList, id=assistantID)

    elif request.method == "POST":
        callback: Callback = questions_services.getByAssistantID(assistantID)
        if callback.Success:
            requestedQuestions = request.json
            databaseQuestions = helpers.getListFromSQLAlchemyList(callback.Data)

            deletedIDs = set()
            for rq in requestedQuestions:
                for dbq in databaseQuestions:
                    if not dbq.get('ID') == rq.get('ID'):
                        deletedIDs.add(dbq.get('ID'))

            # loop in questions and update and add the others
            for id in deletedIDs:
                # delete id
                pass
            for question in requestedQuestions:
                if question['ID']:
                    # update question
                    pass
                else:
                    # insert question with new id
                    pass

        # assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
        #                                        [assistantID, company[0]])
        # if assistant is None or "Error" in assistant:
        #     return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting assitant's records!")
        # else:
        #     currentQuestions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
        #                                                   [assistantID], True)
        #     if currentQuestions is None or "Error" in currentQuestions:
        #         return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting old questions!")
        #
        #     updatedQuestions = []
        #     noq = request.form.get("noq-hidden", default="Error")
        #     for i in range(1, int(noq) + 1):
        #         question = request.form.get("question" + str(i), default="Error")
        #         if question != "Error":
        #             updatedQuestions.append(question)
        #         else:
        #             return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting new questions!")
        #
        #     i = -1
        #     if (len(updatedQuestions) + 1 < len(currentQuestions) + 1):
        #         for b in range(len(updatedQuestions) + 1, len(currentQuestions) + 1):
        #             questionID = currentQuestions[i][0]
        #             question = currentQuestions[i][2]
        #
        #             deleteQuestion = delete_from_table("DELETE FROM Questions WHERE AssistantID=? AND Question=?;", [assistantID, escape(question)])
        #             if deleteQuestion is None or "Error" in deleteQuestion:
        #                 return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 1 Error in updating questions!")
        #
        #             deleteAnswers = delete_from_table(DATABASE, "DELETE FROM Answers WHERE QuestionID=?;", [questionID])
        #             if deleteAnswers is None or "Error" in deleteAnswers:
        #                 return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in removing deleted question's answers!")
        #     for q in updatedQuestions:
        #         i += 1
        #         qType = request.form.get("qType" + str(i))
        #         if i >= len(currentQuestions):
        #             insertQuestion = insert_into_database_table(
        #                 "INSERT INTO Questions ('AssistantID', 'Question', 'Type')"
        #                 "VALUES (?,?,?);", (assistantID, q, qType))
        #             if insertQuestion is None or "Error" in insertQuestion:
        #                 return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 2 Error in updating questions!")
        #         else:
        #             updateQuestion = update_table("UPDATE Questions SET Question=?, Type=? WHERE Question=?;", [escape(q), qType, currentQuestions[i][2]])
        #             if updateQuestion is None or "Error" in updateQuestion:
        #                 return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 3 Error in updating questions!")
        #
        return redirect("/admin/assistant/{}/questions".format(assistantID))

