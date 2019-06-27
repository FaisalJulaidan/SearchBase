import json

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import assistant_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services, Bullhorn
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import Outlook, Google, calendar_services
from utilities import helpers

from datetime import datetime

marketplace_router: Blueprint = Blueprint('marketplace_router', __name__, template_folder="../../templates")


# Get and delete all connected marketplace items (CRMs, Calendars etc.)
@marketplace_router.route("/marketplace", methods=["GET"])
@jwt_required
def get_marketplace():
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = crm_services.getAll(user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        crms = helpers.getListFromSQLAlchemyList(callback.Data)
        # for crm in crms:
        #     crm['Status'] = crm_services.testConnection(user.get("companyID"), {'auth': crm['Auth'], 'type': crm['Type']}).Success
        data = {"crms": crms, "companyID": user.get("companyID")}

        return helpers.jsonResponse(True, 200, callback.Message, data)


# Edit/Disconnect Marketplace item (CRMs, Calendars etc.)
@marketplace_router.route("/crm/<int:crm_id>", methods=["PUT", "DELETE"])
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

# OAuth2
# auth
# /marketplace/oath2
#/marketplace/auth

# Connect CRM
@marketplace_router.route("/crm/connect", methods=["POST"])
@jwt_required
def crm_connect():
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.connect(user.get("companyID"), request.json)  # marketplace details passed: auth, type

        callback.Data = helpers.getDictFromSQLAlchemyObj(callback.Data)
        callback.Data['Status'] = True

    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)





# Test CRM
@marketplace_router.route("/crm/test", methods=['POST'])
@jwt_required
def test_crm_connection():
    # No need for assistant authentication because testing marketplace connection should be public however at least
    # the user has to be logged in and has the token included in the request to minimise security risks
    # Connect to marketplace
    user = get_jwt_identity()['user']
    callback: Callback = Callback(False, '')
    if request.method == "POST":
        callback: Callback = crm_services.testConnection(user.get("companyID"), request.json)  # marketplace details passed (auth, type)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


@marketplace_router.route("/crm/recruiter_value_report", methods=['POST'])
@jwt_required
def recruiter_value_report():
    user = get_jwt_identity()['user']

    if request.method == "POST":
        data_callback: Callback = crm_services.produceRecruiterValueReport(user.get("companyID"),
                                                                           request.json.get("crm_type"))
        if not data_callback.Success:
            return helpers.jsonResponse(False, 400, data_callback.Message)

        return helpers.jsonResponse(True, 200, data_callback.Message, data_callback.Data)


@marketplace_router.route("/calendar/<assistantID>/Google/authorize", methods=['GET', 'POST'])
@jwt_required
@helpers.validAssistant
def calendar_auth(assistantID):
    params = request.get_json()
    callback: Callback = Google.authorizeUser(params['code'])
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)



@marketplace_router.route("/marketplace_callback", methods=['GET', 'POST', 'PUT'])
def marketplace_callback():

    callback: Callback = marketplace_helpers.processRedirect(request.args)

    if not callback.Success:
        return "Retrieving authorisation code failed. Please try again later."

    return "Authorisation completed. You can now close this window."



# post method, only adds events
# @marketplace_router.route("/calendar/<hashedAssistantID>/event", methods=['POST'])
# def calendar_add_event(hashedAssistantID):
#     if request.method == "POST":
#         body = request.json
#
#         callback: Callback = calendar_services.addEvent(body, assistantID=hashedAssistantID)
#         if not callback.Success:
#             return helpers.jsonResponse(False, 400, callback.Message)
#         return helpers.jsonResponse(True, 200, callback.Message)

# @marketplace_router.route("/marketplace_test", methods=['GET', 'POST', 'PUT'])
# def testtss():
#     assistant = assistant_services.getByID(1, 1).Data
#     return Outlook.addEvent(assistant.Calendar.Auth, assistant, assistant.CompanyID).Message
