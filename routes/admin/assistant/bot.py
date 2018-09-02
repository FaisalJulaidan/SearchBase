from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, questions_services, company_services, bot_services
from models import Callback, Company, Assistant
from utilties import helpers

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
