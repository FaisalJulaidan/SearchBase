import json

import requests
from sqlalchemy import and_

from enums import Calendar as Calendar_Enum, CRM as CRM_Enum
from models import db, Callback, CRM, Calendar
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import calendar_services
from utilities import helpers


# process the redirect from the auth callback
def auth(type, details, companyID):
    try:

        # find the type and redirect to its service
        if CRM_Enum.has_value(type):
            callback: Callback = crm_services.connect(type, details, companyID)
        elif Calendar_Enum.has_value(type):
            callback: Callback = calendar_services.connect(type, details, companyID)
        else:
            callback = Callback(False, "The Marketplace object did not match any on the system")

        return callback

    except Exception as exc:
        helpers.logError("Marketplace.marketplace_helpers.processRedirect() ERROR: " + str(exc))
        return Callback(False, str(exc))


# send request with dynamic method
def sendRequest(url, method, headers, data=None):
    request = None
    if method is "put":
        request = requests.put(url, headers=headers, data=data)
    elif method is "post":
        request = requests.post(url, headers=headers, data=data)
    elif method is "get":
        request = requests.get(url, headers=headers, data=data)
    return request


# save the CRM Auth by companyID and CRM Type
def saveNewCRMAuth(auth, marketplaceItemName, companyID):
    try:
        crm = db.session.query(CRM).filter(and_(CRM.CompanyID == companyID, CRM.Type == marketplaceItemName)).first()
        crm.Auth = dict(auth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.saveNewCRMAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))


# save the Calendar Auth by companyID and Calendar Type
def saveNewCalendarAuth(auth, marketplaceItemName, companyID):
    try:
        calendar = db.session.query(Calendar).filter(and_(Calendar.CompanyID == companyID,
                                                          Calendar.Type == marketplaceItemName)).first()
        calendar.Auth = dict(auth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.marketplace_helpers.saveNewCalendarAuth() ERROR: " + str(exc))
        return Callback(False, str(exc))
