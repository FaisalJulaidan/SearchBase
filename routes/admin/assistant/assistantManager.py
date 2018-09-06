from flask import Blueprint, render_template, request, redirect, session
from services import admin_services
from models import Callback

assistantManager_router: Blueprint = Blueprint('assistantManager_router', __name__ , template_folder="../../templates")


# get all assistants
@assistantManager_router.route("/admin/assistant/manage", methods=["GET"])
def assistant_manager():

    if request.method == "GET":
        
        return admin_services.render("admin/assistant-manager.html")

