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


# OAuth2
# auth
# /marketplace/oath2 test, connect and delete
#/marketplace/simple_auth  test, connect, and delete

# Get connected marketplace items with testing the connection (CRMs, Calendars etc.)
@marketplace_router.route("/marketplace", methods=["GET"])
@jwt_required
def get_marketplace():
    user = get_jwt_identity()['user']

    if request.method == "GET":
        crm_callback: Callback = crm_services.getAll(user.get("companyID"))
        calendar_callback: Callback = calendar_services.getAll(user.get("companyID"))

        if not (crm_callback.Success or calendar_callback.Success):
            return helpers.jsonResponse(False, 400, crm_callback.Message)

        return helpers.jsonResponse(True, 200, crm_callback.Message,
                                    {
                                      "crms": helpers.getListFromSQLAlchemyList(crm_callback.Data),
                                      "calendar": helpers.getListFromSQLAlchemyList(calendar_callback.Data),
                                    })


# ===== Connect ===== #
# Connect CRM
@marketplace_router.route("/marketplace/simple_auth", methods=["POST"])
@jwt_required
def simple_auth():

    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "POST":
        data = request.json
        callback: Callback = marketplace_helpers.simpleAuth(data.get('type'),
                                                            data.get('details'),
                                                            user.get("companyID"))

        callback.Data = helpers.getDictFromSQLAlchemyObj(callback.Data)
        callback.Data['Status'] = True

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@marketplace_router.route("/marketplace/oauth2", methods=['POST'])
def marketplace_callback():

    # Authenticate
    user = get_jwt_identity()['user']
    if request.method == "POST":
        data = request.json
        callback: Callback = marketplace_helpers.oAuth2(data.get('type'),
                                                        data.get('details'),
                                                        user.get("companyID"))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Success")


# ===== Disconnect ===== #
# Disconnect a CRM
@marketplace_router.route("/marketplace/crm/<crm_id>", methods=["GET", "DELETE"])
@jwt_required
def crm_control(crm_id):

    # Authenticate
    user = get_jwt_identity()['user']

    # Get a crm and test the connection before return
    if request.method == "GET":
        callback: Callback = crm_services.getCRMByID(crm_id, user.get("companyID"))

        crm = helpers.getDictFromSQLAlchemyObj(callback.Data)
        # Test connection
        crm['Status'] = crm_services.testConnection(crm['Type'], crm['Auth'], user.get("companyID")).Success

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

    # Delete a crm
    if request.method == "DELETE":
        callback: Callback = crm_services.disconnect(crm_id, user.get("companyID"))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Disconnect a Calendar
@marketplace_router.route("/marketplace/calendar/<calendar_id>", methods=["GET", "DELETE"])
@jwt_required
def crm_control(calendar_id):

    # Authenticate
    user = get_jwt_identity()['user']

    # Get a calendar and test the connection before return
    if request.method == "GET":
        callback: Callback = calendar_services.getCalendarByID(calendar_id, user.get("companyID"))

        calendar = helpers.getDictFromSQLAlchemyObj(callback.Data)
        # Test connection
        calendar['Status'] = calendar_services.testConnection(calendar['Type'], calendar['Auth'], user.get("companyID")).Success

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)

    # Delete a calendar
    if request.method == "DELETE":
        callback: Callback = calendar_services.disconnect(calendar_id, user.get("companyID"))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
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
