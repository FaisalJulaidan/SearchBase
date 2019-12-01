from models import db, Callback, Webhook
from typing import List
from sqlalchemy import and_
from utilities import helpers, enums
from hashlib import sha256
import requests
import datetime
import grequests


# To implement:

# Ping client on create

class webhookException(Exception):
    pass


def webhooks(companyID: int) -> Callback:
    try:
        webhooks: List[Webhook] = db.session.query(Webhook).filter(Webhook.CompanyID == companyID).all()

        if webhooks is None:
            raise webhookException("No webhooks found")

        return Callback(True, "Webhooks gathered successfully", webhooks)

    except webhookException as e:
        helpers.logError("webhook_serivces.webhooks(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("webhook_serivces.webhooks(): " + str(e))
        return Callback(False, 'Failed to gather webhooks', None)


def webhook(ID: int, companyID: int) -> Callback:
    try:
        webhook: Webhook = db.session.query(Webhook).filter(
            and_(Webhook.CompanyID == companyID, Webhook.ID == ID)).first()

        if webhook is None:
            raise webhookException("Webhook with specified ID not found")

        return Callback(True, "Webhook gathered successfully", webhook)
    except webhookException as e:
        helpers.logError("webhook_serivces.webhook(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("webhook_serivces.webhook(): " + str(e))
        return Callback(False, "Failed to get webhooks", None)


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
            return Callback(False,
                            "Trying to subscribe to webhook(s): {} that do not exist".format(invalidSubscriptions),
                            None)

        if len(resp['inputs']['subscriptions']) == 0:
            return Callback(False, "You must subscribe to at least one event!", None)

        # sha encoded stored, only
        secret = None if resp['inputs']['secret'] is None else sha256(
            resp['inputs']['secret'].encode('utf-8')).hexdigest()

        # ping request
        Headers = {} if resp['inputs']['secret'] is None else {'Authorization': 'Bearer {}'.format(secret)}
        ping = requests.post(resp['inputs']['url'], headers=Headers)

        if ping.status_code != 200:
            return Callback(False,
                            "Ping request returned status code {}, please check the URL supplied, or your server!".format(
                                ping.status_code), None)

        webhook: Webhook = Webhook(URL=resp['inputs']['url'],
                                   CompanyID=companyID,
                                   Subscriptions=",".join(resp['inputs']['subscriptions']),
                                   Secret=secret)

        db.session.add(webhook)
        db.session.commit()

        return Callback(True, "Webhook created successfully", helpers.getDictFromSQLAlchemyObj(webhook))

    except requests.exceptions.InvalidURL as e:
        return Callback(False, "URL {} is not valid".format(resp['inputs']['url']), None)
    except helpers.requestException as e:
        helpers.logError("webhook_services.createWebhook(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("webhook_services.createWebhook(): " + str(e))
        return Callback(False, "Failed to create webhook", None)


def saveWebhook(id: int, req, companyID: int) -> Callback:
    try:
        resp: dict = helpers.validateRequest(req, {"url": {"type": str, "required": True},
                                                   "secret": {"type": str, "required": False},
                                                   "subscriptions": {"type": List, "required": True}})

        invalidSubscriptions = []

        for subscription in resp['inputs']['subscriptions']:
            if not enums.Webhooks.has_value(subscription):
                invalidSubscriptions.append(subscription)

        if len(invalidSubscriptions) != 0:
            return Callback(False,
                            "Trying to subscribe to webhook(s): {} that do not exist".format(invalidSubscriptions),
                            None)

        if len(resp['inputs']['subscriptions']) == 0:
            return Callback(False, "You must subscribe to at least one event!", None)

        # sha encoded stored, only
        secret = None if resp['inputs']['secret'] is None else sha256(
            resp['inputs']['secret'].encode('utf-8')).hexdigest()

        # ping request
        Headers = {} if resp['inputs']['secret'] is None else {'Authorization': 'Bearer {}'.format(secret)}
        ping = requests.post(resp['inputs']['url'], headers=Headers)

        if ping.status_code != 200:
            return Callback(False,
                            "Ping request returned status code {}, please check the URL supplied, or your server!".format(
                                ping.status_code), None)

        webhook: Webhook = db.session.query(Webhook).filter(
            and_(Webhook.CompanyID == companyID, Webhook.ID == id)).first()

        if webhook is None:
            return Callback(False, "No webhook found!", None)

        if secret != "":
            webhook.Secret = secret
        webhook.URL = resp['inputs']['url']
        webhook.Subscriptions = ",".join(resp['inputs']['subscriptions'])

        db.session.commit()

        return Callback(True, "Webhook saved succesfully", helpers.getDictFromSQLAlchemyObj(webhook))

    except requests.exceptions.InvalidURL as e:
        return Callback(False, "URL {} is not valid".format(resp['inputs']['url']), None)
    except helpers.requestException as e:
        helpers.logError("webhook_serivces.saveWebhook(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("webhook_serivces.saveWebhook(): " + str(e))
        return Callback(False, "Failed to save webhook", None)


def deleteWebhook(id: int, companyID: int) -> Callback:
    try:
        webhook: Webhook = db.session.query(Webhook).filter(
            and_(Webhook.CompanyID == companyID, Webhook.ID == id)).first()
        if webhook is None:
            raise Exception('You do not own this webhook')

        db.session.delete(webhook)
        db.session.commit()

        return Callback(True, "Deleted webhook")
    except Exception as e:
        helpers.logError("webhook_services.deleteWebhook(): " + str(e))
        return Callback(False, "Failed to delete webhook", None)


def fireRequests(data, companyID: int, event: enums.Webhooks):
    def handleExceptions(request, exception):
        helpers.logError(str(exception))
        # print(exception)
        # save error in db

    try:
        webhooks: List[Webhook] = db.session.query(Webhook).filter(Webhook.CompanyID == companyID).all()
        requestList = []
        for webhook in webhooks:
            if event.value in webhook.Subscriptions.split(","):
                requestList.append(webhook.URL)
                webhook.LastSent = datetime.datetime.utcnow()

        formattedData = {
            "event": event.value,
            "data": data
        }

        rs = (grequests.post(u, json=formattedData) for u in requestList)
        grequests.map(rs, exception_handler=handleExceptions)
    except Exception as e:
        helpers.logError("webhook_services.fireRequests(): " + str(e))
        return Callback(False, "Failed to fire all requests", None)

# def ping(webhookID: int) -> Callback:
