import json
import logging

import requests
from sqlalchemy import and_

from enums import Calendar as Calendar_Enum, CRM as CRM_Enum
from models import db, Callback, CRM, Calendar
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import calendar_services
from utilities import helpers


def processRedirect(args):
    try:
        args = dict(args)

        state = json.loads(args.get("state")[0])

        if args.get("error") or not (args.get("code") and args.get("state")):
            return Callback(False, args.get("error_description") or "Required parameters were not provided")

        args["type"] = state.get("type")

        if CRM_Enum.has_value(args["type"]):
            callback: Callback = crm_services.connect(int(state.get("companyID")), args)
        elif Calendar_Enum.has_value(args["type"]):
            callback: Callback = calendar_services.connect(int(state.get("companyID")), args)
        else:
            callback = Callback(False, "The Marketplace object did not match any on the system")

        return callback

    except Exception as exc:
        helpers.logError("marketplace_helpers.processRedirect() ERROR: " + str(exc))
        return Callback(False, str(exc))


def sendRequest(url, method, headers, data=None):
    request = None
    if method is "put":
        request = requests.put(url, headers=headers, data=data)
    elif method is "post":
        request = requests.post(url, headers=headers, data=data)
    elif method is "get":
        request = requests.get(url, headers=headers, data=data)
    return request


def saveNewCRMAuth(auth, marketplaceItemName, companyID):
    try:
        crm = db.session.query(CRM).filter(and_(CRM.CompanyID == companyID, CRM.Type == marketplaceItemName)).first()  # TODO
        crm.Auth = dict(auth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("marketplace_helpers.saveNewCRMAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))


def saveNewCalendarAuth(auth, marketplaceItemName, companyID):
    try:
        calendar = db.session.query(Calendar).filter(and_(Calendar.CompanyID == companyID, Calendar.Type == marketplaceItemName)).first()  # TODO
        calendar.Auth = dict(auth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("marketplace_helpers.saveNewCalendarAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))
