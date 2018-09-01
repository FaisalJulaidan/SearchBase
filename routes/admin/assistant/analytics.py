from flask import Blueprint, request, redirect, flash
from services import analytics_services, admin_services
from models import Callback, Statistics
from utilties import helpers

analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")


@analytics_router.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics(assistantID):
    if request.method == "GET":

        stats_callback : Callback = analytics_services.getStatistics(assistantID)
        if not stats_callback : stats = []
        else: stats = stats_callback.Data
        
        if type(stats) is Statistics:
            stats = [helpers.getDictFromSQLAlchemyObj(stats)]
        else:
            stats = helpers.getListFromSQLAlchemyList(stats)

        print(stats)

        return admin_services.render("admin/analytics.html", data=stats)
