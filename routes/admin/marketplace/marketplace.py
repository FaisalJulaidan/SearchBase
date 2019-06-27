from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import Google, calendar_services
from utilities import helpers

marketplace_router: Blueprint = Blueprint('marketplace_router', __name__, template_folder="../../templates")


# Get connected marketplace items without testing the connection (CRMs, Calendars etc.)
@marketplace_router.route("/marketplace", methods=["GET"])
@jwt_required
def marketplace():
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
@marketplace_router.route("/marketplace/connect", methods=['POST'])
def connect():
    # Authenticate
    user = get_jwt_identity()['user']
    if request.method == "POST":
        data = request.json
        callback: Callback = marketplace_helpers.connect(data.get('type'),
                                                         data.get('details'),
                                                         user.get("companyID"))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, "Success")


# ===== Ping Connection & Disconnect ===== #
# Get and ping connection & Disconnect a marketplace

@marketplace_router.route("/marketplace/<type>", methods=["GET", "DELETE"])
@jwt_required
def crm(type):
    # Authenticate
    user = get_jwt_identity()['user']

    # Get a crm and test the connection before return
    if request.method == "GET":
        callback: Callback = marketplace_helpers.testConnection(type, user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


    # Get a crm and test the connection before return
    if request.method == "DELETE":
        callback: Callback = marketplace_helpers.testConnection(type, user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# @marketplace_router.route("/marketplace/crm/<crm_id>", methods=["GET", "DELETE"])
# @jwt_required
# def crm(crm_id):
#     # Authenticate
#     user = get_jwt_identity()['user']
#
#     # Get a crm and test the connection before return
#     if request.method == "GET":
#         callback: Callback = crm_services.getCRMByID(crm_id, user.get("companyID"))
#
#         crm = helpers.getDictFromSQLAlchemyObj(callback.Data)
#         # Test connection
#         crm['Status'] = crm_services.testConnection(crm['Type'], crm['Auth'], user.get("companyID")).Success
#
#         if not callback.Success:
#             return helpers.jsonResponse(False, 400, callback.Message)
#         return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
#
#     # Delete a crm
#     if request.method == "DELETE":
#         callback: Callback = crm_services.disconnect(crm_id, user.get("companyID"))
#
#         if not callback.Success:
#             return helpers.jsonResponse(False, 400, callback.Message)
#         return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
#
#
# # Get and test connection & Disconnect a Calendar
# @marketplace_router.route("/marketplace/calendar/<calendar_id>", methods=["GET", "DELETE"])
# @jwt_required
# def calendar(calendar_id):
#     # Authenticate
#     user = get_jwt_identity()['user']
#
#     # Get a calendar and test the connection before return
#     if request.method == "GET":
#         callback: Callback = calendar_services.getCalendarByID(calendar_id, user.get("companyID"))
#
#         calendar = helpers.getDictFromSQLAlchemyObj(callback.Data)
#         # Test connection
#         calendar['Status'] = calendar_services.testConnection(calendar['Type'], calendar['Auth'],
#                                                               user.get("companyID")).Success
#
#         if not callback.Success:
#             return helpers.jsonResponse(False, 400, callback.Message)
#         return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
#
#     # Delete a calendar
#     if request.method == "DELETE":
#         callback: Callback = calendar_services.disconnect(calendar_id, user.get("companyID"))
#
#         if not callback.Success:
#             return helpers.jsonResponse(False, 400, callback.Message)
#         return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


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
