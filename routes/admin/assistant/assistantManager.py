from flask import Blueprint, render_template, request, redirect, session
from services import admin_services, role_services
from models import Callback, Role

assistantManager_router: Blueprint = Blueprint('assistantManager_router', __name__ , template_folder="../../templates")


# get all assistants
@assistantManager_router.route("/admin/assistant/manage", methods=["GET"])
def assistant_manager():

    if request.method == "GET":

        userRoleID = session.get('RoleID', None)
        userRole_callback : Callback = role_services.getByID(userRoleID)
        if not userRole_callback.Success: return admin_services.render("admin/assistant-manager.html")

        userRole_callback = admin_services.convertForJinja(userRole_callback.Data, Role)
        if not userRole_callback.Success: return admin_services.render("admin/assistant-manager.html")

        return admin_services.render("admin/assistant-manager.html", userRole=userRole_callback.Data[0])

