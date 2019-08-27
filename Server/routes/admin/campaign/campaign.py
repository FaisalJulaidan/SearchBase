from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import campaign_services, assistant_services, databases_services
from utilities import helpers, wrappers

campaign_router: Blueprint = Blueprint('campaign_router', __name__, template_folder="../../templates")


@campaign_router.route("/campaign_data", methods=['GET', 'POST'])
@jwt_required
@wrappers.AccessAssistantsRequired
def fill_assistants():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        # Get all assistants
        callback: Callback = assistant_services.getAllFull(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Assistants")

        # fetch assistants, their crms and messengers
        assistants = []
        records = callback.Data
        for i in range(0, len(records)):
            assistants.append({"assistant": helpers.getDictFromSQLAlchemyObj(records[i]),
                           "crm": helpers.getDictFromSQLAlchemyObj(records[i].CRM),
                           "messaging_service": helpers.getDictFromSQLAlchemyObj(records[i].Messenger)})

        # fetch databases
        callback: Callback = databases_services.getDatabasesList(user['companyID'])
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)

        return helpers.jsonResponse(True, 200, "Data Returned!",
                                    {
                                        "assistants": assistants,
                                        "databases": helpers.getListFromSQLAlchemyList(callback.Data)
                                    })


@campaign_router.route("/send_campaign", methods=['POST'])
@jwt_required
def send_campaign():
    user = get_jwt_identity()['user']

    if request.method == "POST":
        callback: Callback = campaign_services.sendCampaign(request.json, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been sent!")
