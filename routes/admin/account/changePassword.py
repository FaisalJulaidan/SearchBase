from services import admin_services, user_services
from models import Callback
from flask import Blueprint, request, redirect, session
from utilties import helpers

changePassword_router: Blueprint = Blueprint('changePassword_router', __name__ ,template_folder="../../templates")
@changePassword_router.route("/admin/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return admin_services.render("/accounts/changepassword.html")
    else:

        currentPassword = request.form.get("currentPassword", default="Error")
        newPassword = request.form.get("newPassword", default="Error")
        
        if currentPassword is "Error" or newPassword is "Error":
            return helpers.redirectWithMessage("change_password", "Could not retrieve all written information.")
        
        changePassword_callback : Callback = user_services.changePasswordByID(session.get('userID', None), newPassword, currentPassword)

        return helpers.redirectWithMessage("change_password", changePassword_callback.Message)