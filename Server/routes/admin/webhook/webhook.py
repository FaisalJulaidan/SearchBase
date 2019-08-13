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

@webhook_router.route("/webhook/<webhookid>", methods=['GET'])
@jwt_required
def getWebhook(webhookid):
    user = get_jwt_identity()['user']

    callback: Callback = webhook_services.webhook(webhookid, user.get('companyID'))

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
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

@webhook_router.route("/webhooks/available", methods=['GET'])
@jwt_required
def getAvailableWebhooks():
    callback: Callback = webhook_services.availableWebhooks()
    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)


@webhook_router.route("/webhook/<webhookid>", methods=['GET'])
@jwt_required
def getawa(webhookid):
    user = get_jwt_identity()['user']

    callback: Callback = webhook_services.webhook(webhookid, user.get('companyID'))

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)

@webhook_router.route("/test", methods=['POST'])
def pong():
    print(request.headers)
    return helpers.jsonResponse(True, 200, 'Pong')