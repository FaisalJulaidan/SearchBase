from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.Calendar import Google, calendar_services
from utilities import helpers, wrappers, enums

marketplace_router: Blueprint = Blueprint('marketplace_router', __name__, template_folder="../../templates")


# Get connected marketplace items without testing the connection (CRMs, Calendars etc.)
@marketplace_router.route("/marketplace", methods=["GET"])
@jwt_required
def marketplace():
    user = get_jwt_identity()['user']

    if request.method == "GET":

        crm_callback: Callback = crm_services.getAll(user.get("companyID"))
        calendar_callback: Callback = calendar_services.getAll(user.get("companyID"))
        messenger_callback: Callback = messenger_servicess.getAll(user.get("companyID"))

        if not (crm_callback.Success or calendar_callback.Success or messenger_callback.Success):
            return helpers.jsonResponse(False, 400, "Error in fetching marketplace connections")

        return helpers.jsonResponse(True, 200, crm_callback.Message,
                                    {
                                        "crms": helpers.getListFromSQLAlchemyList(crm_callback.Data),
                                        "calendars": helpers.getListFromSQLAlchemyList(calendar_callback.Data),
                                        "messengers": helpers.getListFromSQLAlchemyList(messenger_callback.Data),
                                    })


# ===== Connect ===== #
@marketplace_router.route("/marketplace/testBullhorn", methods=['POST'])
def testBullhorn():
    # Authenticate
    # user = get_jwt_identity()['user']
    if request.method == "POST":
        print(request)
        data = request.json
        print(data)
        crm_callback: Callback = crm_services.getByID(3,1)
        if not crm_callback.Success:
            raise Exception("CRM not found.")

        crm = crm_callback.Data
        callback = crm_services.searchPlacements(crm, 1, data.get("data"))
          # callback: Callback = marketplace_helpers.search(data.get("params"))

        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, "Success", callback.Data)


# ===== Connect ===== #
@marketplace_router.route("/marketplace/connect", methods=['POST'])
@jwt_required
def connect():
    # Authenticate
    user = get_jwt_identity()['user']
    if request.method == "POST":
        data = request.json
        callback: Callback = marketplace_helpers.connect(data.get('type'),
                                                         data.get('auth'),
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

    # Get and test the connection before return
    if request.method == "GET":
        callback: Callback = marketplace_helpers.testConnection(type, user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


    # Get and test the connection before return
    if request.method == "DELETE":
        callback: Callback = marketplace_helpers.disconnect(type, user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message)

@marketplace_router.route("/marketplace/<type>/fetch", methods=["GET"])
@jwt_required
def crm_fetch(type):
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = crm_services.getCRMByType(type, user.get("companyID"))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))

@marketplace_router.route("/marketplace/<type>/save", methods=["POST"])
@jwt_required
def crm_save(type):
    # Authenticate
    user = get_jwt_identity()['user']

    data = request.json
    print(data)
    callback: Callback = crm_services.updateAutopilotConnection(type, data.get("CRMAutoPilotID"), user.get("companyID"))
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


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
@wrappers.validAssistant
def calendar_auth(assistantID):
    params = request.get_json()
    callback: Callback = Google.authorizeUser(params['code'])
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message)


@marketplace_router.route("/marketplace/simple_callback", methods=['GET', 'POST', 'PUT'])
def simple_callback():
    return str(request.url)

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
