import logging

import requests
from sqlalchemy import and_

from models import db, Callback, CRM


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
        logging.error("CRM.Bullhorn.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))


def saveNewMailAuth(auth, marketplaceItemName, companyID):
    try:
        crm = db.session.query(CRM).filter(and_(CRM.CompanyID == companyID, CRM.Type == marketplaceItemName)).first()  # TODO
        crm.Auth = dict(auth)
        db.session.commit()
        return Callback(True, "New auth has been saved")

    except Exception as exc:
        db.session.rollback()
        logging.error("CRM.Bullhorn.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, str(exc))
