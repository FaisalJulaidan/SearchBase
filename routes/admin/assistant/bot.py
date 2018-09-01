from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, questions_services, company_services
from models import Callback, Company, Assistant
from utilties import helpers

bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")

bot_currentVersion = "1.0.0"

@bot_router.route("/admin/assistant/<int:assistantID>/bot", methods=['GET', 'POST'])
def bot(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')


@bot_router.route("/admin/assistant/<int:assistantID>/bot/questions", methods=['GET', 'POST'])
def get_botQuestions(assistantID):
    if request.method == "GET":
        res = {
            "botVersion": "1.0.0",
            "assistant": {
                "id": 1,
                "name": "Helper"
            },
            "questions":
                [
                    {
                        "id": 1,
                        "type": "FileUpload",
                        "question": "Upload Your CV",
                        "fileTypes": ["GIF", "PGN"],
                        "action": "GoToNextQuestion",
                        "questionIdToGo": None
                    },
                    {
                        "id": 2,
                        "type": "OpenAnswers",
                        "question": "What's your email?",
                        "answer": "faisal@hotmail.com",
                        "validation": "email",
                        "keywords": [],
                        "action": "GoToSpecificQuestion",
                        "questionIdToGo": 6
                    },
                    {
                        "id": 3,
                        "type": "PredefinedAnswers",
                        "question": "Do You Smoke?",
                        "answer": "Yes",
                        "keywords": ["smoker"],
                        "storeDB": True,
                        "action": "GoToSpecificQuestion",
                        "questionIdToGo": 1
                    }
                ]
        }
        return json.dumps({'success': True, 'msg': "Assistant found :).", 'data': res}), \
               200, {'ContentType': 'application/json'}





        # # Get assistant using <assistantID>
        # callback: Callback = assistant_services.getByID(assistantID)
        # if not callback.Success:
        #     return json.dumps({'success': False, 'msg': "Assistant not found."}), \
        #            404, {'ContentType': 'application/json'}
        # assistant: Assistant = callback.Data
        #
        # # Get questions
        # questions = assistant.Questions
        #
        # # Convert them to JSON
        # questionsJSON = {'botVersion': bot_currentVersion, 'questions': []}
        # for question in questions:
        #     questionsJSON['questions'].append(question)
        #
        # return admin_services.render('admin/bot.html')
