from services import profile_services, admin_services
from models import Callback
from flask import Blueprint, request, redirect, session
from utilties import helpers

profile_router: Blueprint = Blueprint('profile_router', __name__ ,template_folder="../../templates")


@profile_router.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        email = session.get('UserEmail', None)

        profile_callback : Callback = profile_services.getUserAndCompany(email)
        if not profile_callback.Success:
            return admin_services.render("admin/profile.html", user=None, email=email, company=None)

        return admin_services.render("admin/profile.html", user=profile_callback.Data["user"], email=email, company=profile_callback.Data["company"])

    elif request.method == "POST":
        curEmail = session.get('UserEmail', None)

        names = request.form.get("names", default="Error")
        newEmail = request.form.get("email", default="error").lower()
        companyName = request.form.get("companyName", default="Error")

        if names is "Error" and newEmail is "error" and companyName is "Error":
            return helpers.redirectWithMessage("profilePage", "Could not retrieve all written information.")

        names = names.split(" ")
        name1 = names[0]
        name2 = names[1]
            
        updateUser_callback : Callback = profile_services.updateUser(name1, name2, newEmail, session.get('UserID', 0))
        if not updateUser_callback.Success: return helpers.redirectWithMessage("profilePage", "Could not update User's information.")

        updateCompany_callback : Callback = profile_services.updateCompany(companyName, session.get('CompanyID', 0))
        if not updateCompany_callback.Success: return helpers.redirectWithMessage("profilePage", "Could not update Company's information.")

        return helpers.redirectWithMessage("profilePage", "User and Company information has been updated.")
