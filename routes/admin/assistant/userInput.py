from flask import Blueprint, render_template, request, redirect, session
from services import statistics_services, assistant_services
from models import Callback
from utilties import helpers

userInput_router: Blueprint = Blueprint('userInput_router', __name__ , template_folder="../../templates")


# get all assistants
@userInput_router.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):

    if request.method == "GET":
        email = session.get('User')['Email']
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=?", [assistantID,])
        if assistant is None or "Error" in assistant:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                    [assistantID], True)
            data = []
            print("questions: ", questions)
            #dataTuple = tuple(["Null"])
            for i in range(0, len(questions)):
                question = questions[i]
                print("question: ", question)
                questionID = question[0]
                print("questionID: ", questionID)
                print(query_db("SELECT * FROM UserInput"), [])
                userInput = select_from_database_table("SELECT * FROM UserInput WHERE QuestionID=?", [questionID], True)
                print("userInput: ", userInput)
                if userInput and userInput is not None:
                    for record in userInput:
                        print("record: ", record)
                        data.append(record)
            print("data:", data)
            return render("admin/data-storage.html", data=data)


