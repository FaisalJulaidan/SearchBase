from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from typing import List
from models import Callback, Assistant, Conversation, Appointment
from services import webhook_services
from utilities import helpers

webhook_router: Blueprint = Blueprint('webhook_router', __name__, template_folder="../../templates")


@webhook_router.route("/webhooks", methods=['GET'])
@jwt_required
def getWebhooks():
    user = get_jwt_identity()['user']

    callback: Callback = webhook_services.webhooks(user.get('companyID'))

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getListFromSQLAlchemyList(callback.Data))
    else:
        return helpers.jsonResponse(False, 401, callback.Message)


@webhook_router.route("/webhook", methods=['POST'])
@jwt_required
def postWebhook():
    user = get_jwt_identity()['user']

    req = request.get_json()

    callback: Callback = webhook_services.createWebhook(req, user.get('companyID'))

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)


@webhook_router.route("/webhook/<webhookID>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def webhook(webhookID):
    user = get_jwt_identity()['user']
    callback: Callback = Callback(False, "Error")

    if request.method == "GET":
        callback: Callback = webhook_services.webhook(webhookID, user.get('companyID'))

    if request.method == "PUT":
        req = request.get_json()
        callback: Callback = webhook_services.saveWebhook(webhookID, req, user.get('companyID'))

    if request.method == "DELETE":
        callback: Callback = webhook_services.deleteWebhook(webhookID, user.get('companyID'))

    if not callback.Success:
        return helpers.jsonResponse(False, 401, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@webhook_router.route("/test", methods=['POST'])
def pong():
    print(request.get_json())
    return helpers.jsonResponse(True, 200, 'Pong')
