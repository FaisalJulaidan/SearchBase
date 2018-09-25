from flask import Blueprint, request, redirect, flash, session
from services import admin_services, assistant_services
from models import Callback

connection_router: Blueprint = Blueprint('connection_router', __name__, template_folder="../../templates")

@connection_router.route("/admin/assistant/<assistantID>/connect", methods=['GET'])
def admin_connect(assistantID):
    if request.method == "GET":
        return admin_services.render("admin/connect.html", assistantID=assistantID)