from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, company_services, bot_services
from models import db, Callback, Company, Assistant, ValidationType, User
from utilties import helpers, json_utils

bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")


@bot_router.route("/admin/assistant/<int:assistantID>/bot", methods=['GET', 'POST'])
def bot_controller(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')


@bot_router.route("/test/<int:assistantID>", methods=['POST', 'GET', 'PUT', 'DELETE'])
# @bot_router.route("/admin/assistant/<int:assistantID>/bot/data", methods=['GET', 'POST'])
def bot(assistantID):

    if request.method == "GET":

        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        # Get bot data (Blocks, Assistant...)
        data = bot_services.getBot(assistant)

        return helpers.jsonResponse(True, 200, "No Message", data)

    # Add a block
    if request.method == "POST":

        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data
        data = request.get_json(silent=True)
        callback: Callback = bot_services.addBlock(data, assistant)

        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

    # Update the blocks
    if request.method == "PUT":

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
