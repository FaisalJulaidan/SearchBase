from flask import Blueprint, request, redirect, flash, session, json
from services import admin_services, assistant_services, company_services, bot_services, user_services
from models import db, Callback, Assistant, Block, User
from utilties import helpers
from sqlalchemy.sql import exists, func


bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")


@bot_router.route("/admin/assistant/<int:assistantID>/bot", methods=['GET', 'POST'])
def bot_controller(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')


@bot_router.route("/test/<int:assistantID>", methods=['POST', 'GET', 'PUT'])
# @bot_router.route("/admin/assistant/<int:assistantID>/bot/data", methods=['GET', 'POST'])
def bot(assistantID):
    # For all type of requests, get the assistant
    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    if request.method == "GET":
        assistant: Assistant = callback.Data
        # Get bot data (Blocks, Assistant...)
        data: dict = bot_services.getBot(assistant)
        return helpers.jsonResponse(True, 200, "No Message", data)

    # Add a block
    if request.method == "POST":
        # Get new block data from the request's body
        data = request.get_json(silent=True)
        callback: Callback = bot_services.addBlock(data, assistant)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

    # Update the blocks
    if request.method == "PUT":
        data = request.get_json(silent=True)
        callback: Callback = bot_services.updateBot(data, assistant)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@bot_router.route("/test/<int:blockID>", methods=['DELETE'])
# @bot_router.route("/admin/assistant/bot/block/<int:blockID>", methods=['DELETE'])
def delete_block(blockID):
    if request.method == "DELETE":

        # Get the user who is logged in and wants to delete.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, your account doesn't exist. Try again please!")
        user: User = callback.Data

        # Check if this user is authorised for such an operation.
        if not user.Role.EditChatbots:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised for deleting blocks.")

        # Delete the block
        callback: Callback = bot_services.deleteBlockByID(blockID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message)


@bot_router.route("/admin/assistant/bot/options", methods=['GET'])
def get_botFeatures():
    if request.method == "GET":
        return helpers.jsonResponse(True, 200, "These are the options the bot provide.", bot_services.getOptions())
