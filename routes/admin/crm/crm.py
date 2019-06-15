import logging

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

import requests
import os
from models import Callback, Calendar, db
import enums
from services.CRM import crm_services, Bullhorn, Google
from utilities import helpers

crm_router: Blueprint = Blueprint('crm_router', __name__, template_folder="../../templates")


# Get all company CRMs and check their connections before returning them
@crm_router.route("/crm", methods=["GET"])
@jwt_required
def get_crms():
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = crm_services.getAll(user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        crms = helpers.getListFromSQLAlchemyList(callback.Data)
        for crm in crms:
            crm['Status'] = crm_services.testConnection({'auth': crm['Auth'], 'type': crm['Type']}, user.get("companyID")).Success

        return helpers.jsonResponse(True, 200, callback.Message, crms)


# Connect CRM
@crm_router.route("/crm/connect", methods=["POST"])
@jwt_required
def crm_connect():
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.connect(user.get("companyID"), request.json)  # crm details passed: auth, type

        callback.Data = helpers.getDictFromSQLAlchemyObj(callback.Data)
        callback.Data['Status'] = True

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Edit/Disconnect CRM
@crm_router.route("/crm/<int:crm_id>", methods=["PUT", "DELETE"])
@jwt_required
def crm_control(crm_id):
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "PUT":
        callback: Callback = crm_services.update(crm_id, user.get("companyID"), request.json)

    if request.method == "DELETE":
        callback: Callback = crm_services.disconnect(crm_id, user.get("companyID"))

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Test CRM
@crm_router.route("/crm/test", methods=['POST'])
@jwt_required
def test_crm_connection():
    # No need for assistant authentication because testing crm connection should be public however at least
    # the user has to be logged in and has the token included in the request to minimise security risks
    # Connect to crm
    user = get_jwt_identity()['user']
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.testConnection(request.json, user.get("companyID"))  # crm details passed (auth, type)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


@crm_router.route("/crm/recruiter_value_report", methods=['POST'])
@jwt_required
def recruiter_value_report():
    user = get_jwt_identity()['user']

    if request.method == "POST":
        data_callback: Callback = crm_services.produceRecruiterValueReport(user.get("companyID"),
                                                                           request.json.get("crm_type"))
        if not data_callback.Success:
            return helpers.jsonResponse(False, 400, data_callback.Message)

        return helpers.jsonResponse(True, 200, data_callback.Message, data_callback.Data)


@crm_router.route("/bullhorn_callback", methods=['GET', 'POST', 'PUT'])
def bullhorn_callback():
    return str(request.url)


@crm_router.route("/crm_callback", methods=['GET', 'POST', 'PUT'])
def crm_callback():
    return str(request.url)


@crm_router.route("/calendar/google/authorize", methods=['GET', 'POST'])
# @jwt_required
def calendar_auth():
    params = request.get_json()
    try:
        resp = requests.post("https://oauth2.googleapis.com/token",
                        data={
                            'code': params['code'],
                            'client_secret': os.environ['GOOGLE_CALENDAR_CLIENT_SECRET'],
                            'client_id': os.environ['GOOGLE_CALENDAR_CLIENT_ID'],
                            'redirect_uri': os.environ['GOOGLE_CALENDAR_REDIRECT_URI'],
                            'grant_type': 'authorization_code'
                        })
        print(resp.text)
        if 'error' in resp.json():
            raise Exception(resp.json()['error_description'])

        # new = Calendar(Auth=r['code'], Type=enums.Calendar.Google, CompanyID=2)
        # db.session.add(new)
        # db.session.commit()
    except Exception as e:
        print(e)
    return '123'

#probably remove this later on, just for consistency
@crm_router.route("/calendar/google/getRedirectURI", methods=['GET'])
def get_redirect_uri():
    return os.environ['GOOGLE_CALENDAR_REDIRECT_URI']



