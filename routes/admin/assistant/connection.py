from flask import Blueprint, request
from services import admin_services
from utilities import helpers

connection_router: Blueprint = Blueprint('connection_router', __name__, template_folder="../../templates")


@connection_router.route("/assistant/<int:assistantID>/connect", methods=['GET'])
def admin_connect(assistantID):
    if request.method == "GET":
        return admin_services.render("admin/connect.html", assistantID=helpers.encrypt_id(assistantID))