from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import campaign_services
from utilities import helpers

campaign_router: Blueprint = Blueprint('campaign_router', __name__, template_folder="../../templates")


@campaign_router.route("/send_campaign", methods=['POST'])
@jwt_required
def send_campaign():
    user = get_jwt_identity()['user']

    if request.method == "POST":
        callback: Callback = campaign_services.sendCampaign(request.json, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Campaign has been sent!")
