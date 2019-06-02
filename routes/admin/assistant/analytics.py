from flask import Blueprint, request, session
from services import analytics_services, assistant_services
from models import Callback, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")



@analytics_router.route("/assistant/<assistantID>/analytics", methods=['GET'])
@jwt_required
def admin_analytics_data(assistantID):

    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        callback: Callback = analytics_services.getAnalytics(assistant, periodSpace=1, topSolustions=5)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, callback.Message, callback.Data)

        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)



