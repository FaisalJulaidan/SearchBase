from services import admin_services, user_services
from models import Callback
from flask import Blueprint, request, session
from utilities import helpers

changePassword_router: Blueprint = Blueprint('changePassword_router', __name__ ,template_folder="../../templates")
@changePassword_router.route("/admin/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return admin_services.render("/accounts/changepassword.html")
    else:

        currentPassword = request.form.get("currentPassword", default="")
        newPassword = request.form.get("newPassword", default="")
        
        if not currentPassword or not newPassword:
            return helpers.redirectWithMessage("change_password", "Could not retrieve all written information.")

        changePassword_callback : Callback = user_services.changePasswordByID(session.get('UserID', None), newPassword, currentPassword)

        return helpers.redirectWithMessage("change_password", changePassword_callback.Message)