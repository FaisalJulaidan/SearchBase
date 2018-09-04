from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, company_services, bot_services
from models import db, Callback, Company, Assistant, ValidationType, User
from utilties import helpers, json_utils

bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")


@bot_router.route("/admin/assistant/<int:assistantID>/bot", methods=['GET', 'POST'])
def bot(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')


# @bot_router.route("/admin/assistant/<int:assistantID>/bot/questions", methods=['GET', 'POST'])
@bot_router.route("/test/<int:assistantID>", methods=['POST', 'GET'])
def get_botQuestions(assistantID):
    if request.method == "GET":
        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        # Get bot data (Blocks, Assistant...)
        data = bot_services.getBot(assistant)

        return helpers.jsonResponse(True, 200, "No Message", data)

    if request.method == "POST":


        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data
        data = request.get_json(silent=True)
        callback: Callback = bot_services.updateBot(data, assistant)

        return helpers.jsonResponse(True, 200, callback.Message, callback.Data )


@bot_router.route("/admin/assistant/bot/options", methods=['GET'])
def get_botFeatures():
    if request.method == "GET":
        return helpers.jsonResponse(True, 200, "These are the options the bot provide.", bot_services.getOptions())


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
                "questionToGoID": 1,
                "storeInDB": True,
                "type": "File Upload"
                }
        try:
            json_utils.validateSchema(json, 'fileUpload.json')
        except Exception as exc:
            print(exc.args)

        return helpers.jsonResponse(True, 200, "These are the features the bot provide.",
                                    {"hi": "hi"})
