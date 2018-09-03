from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, questions_services, company_services, bot_services
from models import Callback, Company, Assistant, UserInputValidation
from utilties import helpers, json_utils

bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")


@bot_router.route("/admin/assistant/<int:assistantID>/bot", methods=['GET', 'POST'])
def bot(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')


@bot_router.route("/admin/assistant/<int:assistantID>/bot/questions", methods=['GET', 'POST'])
def get_botQuestions(assistantID):
    if request.method == "GET":

        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        # Get bot data (Questions, Assistant...)
        data = bot_services.botBuilder(assistant)

        return helpers.jsonResponse(True, 200, "No Message", data)


@bot_router.route("/admin/assistant/bot/features", methods=['GET'])
def get_botFeatures():
    if request.method == "GET":
        return helpers.jsonResponse(True, 200, "These are the features the bot provide.", bot_services.getFeatures())


@bot_router.route("/admin/assistant/bot/j", methods=['GET'])
def validate_json():
    if request.method == "GET":
        json = {
                "action": "Show Solutions",
                "fileTypes": [
                  "gif",
                  "pdf"
                ],
                "id": 3,
                "order": 3,
                "question": "Upload your CV",
                "questionToGoID": None,
                "storeInDB": True,
                "type": "File Upload"
                }

        json_utils.validateSchema(json, 'questionFU.json')
        return helpers.jsonResponse(True, 200, "These are the features the bot provide.",
                                    {"hi": "hi"})