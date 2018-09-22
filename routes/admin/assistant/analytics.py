from flask import Blueprint, request, session
from services import analytics_services, admin_services, assistant_services
from models import Callback, Assistant
from utilties import helpers

analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")


@analytics_router.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics_page(assistantID):
    if request.method == "GET":
        return admin_services.render("admin/analytics.html")


@analytics_router.route("/admin/assistant/<assistantID>/analytics/data", methods=['GET'])
def admin_analytics_data(assistantID):
    if request.method == "GET":
        callback: Callback = assistant_services.getByID(assistantID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data

        if assistant.CompanyID != session.get('CompanyID', 0):
            return helpers.jsonResponse(False, 401, "You're not authorized to view this info", None)

        callback: Callback = analytics_services.getAnalytics(assistant, periodSpace=1, topSolustions=5)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, callback.Message, callback.Data)

        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
