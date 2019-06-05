from flask import Blueprint, request, session
from services import analytics_services, assistant_services
from models import Callback, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity

analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")

@analytics_router.route("/assistant/<assistantID>/analytics", methods=['GET'])
@jwt_required
@helpers.validAssistant
def admin_analytics_data(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        # result = []
        callback: Callback = analytics_services.getAnalytics(assistantID, user['companyID'])
        if not callback.Success:
            print(callback.Message, callback.Data)
            return helpers.jsonResponse(False, 400, 'Failed to gather analytics')
        try:
            result = helpers.getDictFromLimitedQuery(['ID', 'DateTime', 'TimeSpent', 'Status', 'Score', 'UserType'],
                                                     callback.Data)
        except Exception as e:
            print(e)
            return helpers.jsonResponse(False, 400, 'Failed to gather analytics')
        return helpers.jsonResponse(True, 200, callback.Message, result)



