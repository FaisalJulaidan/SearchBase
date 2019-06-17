from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services.Marketplace.CRM import crm_services
from services.Marketplace.Mail import Outlook
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


@crm_router.route("/outlook_callback", methods=['GET', 'POST', 'PUT'])
def outlook_callback():
    print("request.args: ", request.args)
    print(": ", request.args.get("code"))
    print("request.form: ", request.form)
    print("request.json: ", request.json)
    print("request.url: ", request.url)
    print("method: ", request.method)

    args = request.args
    if args.get("error") or (not args.get("code") or not args.get("state")):
        return helpers.jsonResponse(False, 400, args.get("error_description") or "User error in request")

    login_callback: Callback = Outlook.login(args)
    if not login_callback.Success:
        return helpers.jsonResponse(False, 400, login_callback.Message)
    print("login_callback.Data: ", login_callback.Data)
    return helpers.jsonResponse(True, 200, "Success")


@crm_router.route("/custom_test", methods=['GET', 'POST', 'PUT'])
def test():
    if request.method == "POST":
        return Outlook.login({"username": "info thesearchbase", "password": "TH3T3CHBR@S"}).Message
