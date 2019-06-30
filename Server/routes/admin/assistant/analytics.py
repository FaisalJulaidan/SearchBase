from flask import Blueprint, request, session
from services import analytics_services, assistant_services
from models import Callback, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity

analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")

@analytics_router.route("/assistant/<assistantID>/analytics", methods=['GET'])
@jwt_required
@helpers.validAssistant
def admin_analytics_data(assistant):
    if request.method == "GET":
        callback: Callback = analytics_services.getAnalytics(assistant)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, 'Failed to gather analytics')
        result = helpers.getListFromLimitedQuery(['ID', 'DateTime', 'TimeSpent', 'ApplicationStatus', 'Score', 'UserType'],
                                                 callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, result)



