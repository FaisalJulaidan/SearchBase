from models import db, Callback, Webhook
from typing import List
from sqlalchemy import and_
from utilities import helpers, enums
from hashlib import sha256
import requests

# To implement:

# Ping client on create

def webhooks(companyID: int) -> Callback:
    try:
        webhooks: List[Webhook] = db.session.query(Webhook).filter(Webhook.CompanyID == companyID).all()

        if webhooks is None:
            raise Exception("No webhooks found")

        return Callback(True, "Webhooks gathered succesfully", webhooks)

    except Exception as e:
        helpers.logError("webhook_serivces.webhooks(): " + str(e))
        return Callback(False, str(e), None)

def webhook(ID: int, companyID: int) -> Callback:
    try:
        webhook: Webhook = db.session.query(Webhook).filter(and_(Webhook.CompanyID == companyID, Webhook.ID == ID)).first()

        if webhook is None:
            raise Exception("Webhook with specified ID not found")

        return Callback(True, "Webhook gathered succesfully", webhook)

    except Exception as e:
        helpers.logError("webhook_serivces.webhook(): " + str(e))
        return Callback(False, str(e), None)

def createWebhook(req, companyID: int) -> Callback:
    try:
        resp: dict = helpers.validateRequest(req, {"url": {"type": str, "required": True},
                                                                  "secret": {"type": str, "required": False},
                                                                  "subscriptions": {"type": List, "required": True}})

        invalidSubscriptions = []

        for subscription in resp['inputs']['subscriptions']:
            if not enums.Webhooks.has_value(subscription):
                invalidSubscriptions.append(subscription)

        if len(invalidSubscriptions) != 0:
            return Callback(False, "Trying to subscribe to webhook(s): {} that do not exist".format(invalidSubscriptions), None)


        #sha encoded stored, only
        secret = None if resp['inputs']['secret'] is None else sha256(resp['inputs']['secret'].encode('utf-8')).hexdigest()

        #ping request
        Headers = {} if resp['inputs']['secret'] is None else {'Authorization': 'Bearer {}'.format(secret)}
        ping = requests.post(resp['inputs']['url'], headers=Headers)
        if ping.status_code != 200:
            return Callback(False, "Ping request returned status code {}, please check the URL supplied, or your server!".format(ping.status_code), None)

        webhook: Webhook = Webhook(URL=resp['inputs']['url'],
                                   CompanyID=companyID,
                                   Subscriptions=",".join(resp['inputs']['subscriptions']),
                                   Secret=secret)

        db.session.add(webhook)
        db.session.commit()

        return Callback(True, "Webhook created succesfully", helpers.getDictFromSQLAlchemyObj(webhook))

    except requests.exceptions.InvalidURL as e:
        return Callback(False, "URL {} is not valid".format(resp['inputs']['url']), None)
    except Exception as e:
        helpers.logError("webhook_serivces.createWebhook(): " + str(e))
        return Callback(False, str(e), None)

def availableWebhooks() -> Callback:
    try:
        return Callback(True, "Gathered list of webhooks", [e.value for e in enums.Webhooks])
    except Exception as e:
        helpers.logError("webhook_serivces.availableWebhooks(): " + str(e))
        return Callback(False, "Failed to gather list of webhooks", None)


# def ping(webhookID: int) -> Callback: