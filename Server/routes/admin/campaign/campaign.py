from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import campaign_services
from utilities import helpers

campaign_router: Blueprint = Blueprint('campaign_router', __name__, template_folder="../../templates")


@campaign_router.route("/campaign/action", methods=['GET', 'POST'])
@jwt_required
def fill_assistants():
    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        # fetch Campaigns
        campaigns_callback: Callback = campaign_services.getAll(user['companyID'])
        if not campaigns_callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Campaigns")

        return helpers.jsonResponse(True, 200, "Data Returned!",
                                    {"campaigns": helpers.getListFromSQLAlchemyList(campaigns_callback.Data)})

    if request.method == "POST":
        callback: Callback = campaign_services.prepareCampaign(request.json, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been prepared!", callback.Data)

    if request.method == "PUT":
        callback: Callback = campaign_services.sendCampaign(request.json, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been sent!")


@campaign_router.route("/campaign", methods=['POST'])
@jwt_required
def campaign():
    user = get_jwt_identity()['user']

    if request.method == "POST":
        callback: Callback = campaign_services.save(request.json, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been saved!", callback.Data)


@campaign_router.route("/campaign/<int:campaignID>", methods=['GET', 'POST', 'DELETE'])
@jwt_required
def campaign_id(campaignID):
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = campaign_services.getByID(campaignID, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        campaignOptions_callback: Callback = campaign_services.getCampaignOptions(user['companyID'])
        if not campaignOptions_callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Campaigns Options")

        return helpers.jsonResponse(True, 200, "Campaign has been retrieved!", {"campaign": callback.Data,
                                                                                "campaignOptions": {
                                                                                    campaignOptions_callback.Data
                                                                                }})

    if request.method == "POST":
        callback: Callback = campaign_services.save(request.json, user['companyID'], campaignID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been saved!", callback.Data)

    if request.method == "DELETE":
        callback: Callback = campaign_services.removeByID(campaignID, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been saved!", callback.Data)
