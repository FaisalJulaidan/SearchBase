from services import profile_services, admin_services, newsletter_services, user_services
from models import Callback
from flask import Blueprint, request, redirect, session
from utilities import helpers

profile_router: Blueprint = Blueprint('profile_router', __name__ ,template_folder="../../templates")


@profile_router.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        email = session.get('UserEmail', None)

        profile_callback : Callback = profile_services.getUserAndCompany(email)
        if not profile_callback.Success: return admin_services.render("admin/profile.html", user=None, email=email, company=None, newsletters=None, userSettings=None)

        newsletter_callback : Callback = newsletter_services.checkForNewsletter(email)
        newsletters = newsletter_callback.Success

        userSettings_callback : Callback = user_services.getUserSettings(session.get('UserID', None))
        if not userSettings_callback.Success: return admin_services.render("admin/profile.html", user=profile_callback.Data["user"], company=profile_callback.Data["company"], newsletters=newsletters, userSettings=None)

        return admin_services.render("admin/profile.html", user=profile_callback.Data["user"], company=profile_callback.Data["company"], newsletters=newsletters, userSettings=userSettings_callback.Data)

    elif request.method == "POST":
        curEmail = session.get('UserEmail', None)
        userID = session.get('UserID', None)

        names = request.form.get("names", default="Error")
        newEmail = request.form.get("email", default="error").lower()
        companyName = request.form.get("companyName", default="Error")
        newsletters = request.form.get("newsletters", default="Error")
        tracking = request.form.get("tracking", default="")
        techSupport = request.form.get("techSupport", default="")
        notifications = request.form.get("notifications", default="")
        accountSpecialist = request.form.get("accountSpecialist", default="")

        if names is "Error" and newEmail is "error" and companyName is "Error":
            return helpers.redirectWithMessage("profilePage", "Could not retrieve all written information.")

        names = names.split(" ")
        name1 = names[0]
        name2 = names[1]
            
        #update user data
        updateUser_callback : Callback = profile_services.updateUser(name1, name2, newEmail, session.get('UserID', 0))
        if not updateUser_callback.Success: return helpers.redirectWithMessage("profilePage", "Could not update User's information.")

        updateCompany_callback : Callback = profile_services.updateCompany(companyName, session.get('CompanyID', 0))
        if not updateCompany_callback.Success: return helpers.redirectWithMessage("profilePage", "Could not update Company's information. User information has been updated.")

        #update newsletters
        if newsletters == "newlettersON":
            newsletter_callback : Callback = newsletter_services.checkForNewsletter(newEmail)
            if not newsletter_callback.Success:
                newsletter_callback : Callback = newsletter_services.addNewsletterPerson(newEmail)
        elif newsletters is "Error":
            newsletter_callback : Callback = newsletter_services.removeNewsletterPerson(newEmail)
        if not newsletter_callback.Success: return helpers.redirectWithMessage("profilePage", newsletter_callback.Message + " Company and User information has been updated.")

        #update user settings
        tracking = bool(tracking)
        techSupport = bool(techSupport)
        accountSpecialist = bool(accountSpecialist)
        notifications = bool(notifications)

        userSettings_callback : Callback = user_services.createUpdateUserSettings(userID, tracking, techSupport, accountSpecialist, notifications)
        if not userSettings_callback.Success: return helpers.redirectWithMessage("profilePage", userSettings_callback.Message + " Company, User information and newsletters has been updated.")

        return helpers.redirectWithMessage("profilePage", "Records have been updated.")
