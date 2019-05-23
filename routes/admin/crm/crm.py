from flask import Blueprint, request
from flask_apscheduler import json
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from models import Callback
from services.CRM import crm_services, Bullhorn
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
            crm['Status'] = crm_services.testConnection({'auth': crm['Auth'], 'type': crm['Type']}).Success

        return helpers.jsonResponse(True, 200, callback.Message, crms)


# Connect CRM
@crm_router.route("/crm/connect", methods=["POST"])
@jwt_required
def crm_connect():
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.connect(user.get("companyID"), request.json)  # crm details passed: auth, type

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
    return helpers.jsonResponse(True, 200, callback.Message)


# Test CRM
@crm_router.route("/crm/test", methods=['POST'])
@jwt_required
def test_crm_connection():
    # No need for assistant authentication because testing crm connection should be public however at least
    # the user has to be logged in and has the token included in the request to minimise security risks
    # Connect to crm
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.testConnection(request.json)  # crm details passed (auth, type)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


@crm_router.route("/bullhorn_callback", methods=['GET', 'POST', 'PUT'])
def bullhorn_callback():
    logging.error("request.method: ")
    logging.error(request.method)
    logging.error("request.args: ")
    logging.error(request.args)
    logging.error("request.url: ")
    logging.error(request.url)
    logging.error("request.form: ")
    logging.error(request.form)
    logging.error("request.json: ")
    logging.error(request.json)
    logging.error("request.headers: ")
    logging.error(request.headers)
    print("request.method: ")
    print(request.method)
    print("request.args: ")
    print(request.args)
    print("request.url: ")
    print(request.url)
    print("request.form: ")
    print(request.form)
    print("request.json: ")
    print(request.json)
    print("request.headers: ")
    print(request.headers)
    return str(request.url)
