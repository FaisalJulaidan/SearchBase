from flask import Blueprint, request, redirect, flash
from services import assistant_services
from models import Callback

analytics_router: Blueprint = Blueprint('analytics_router', __name__, template_folder="../../templates")



# TODO implement this
@app.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics(assistantID):
    if request.method == "GET":
        stats = select_from_database_table(
            "SELECT Date, Opened, QuestionsAnswered, ProductsReturned FROM Statistics WHERE AssistantID=?",
            [assistantID], True)
        # use helpers.render
        return render("admin/analytics.html", data=stats)
