from flask import Blueprint, request, session, jsonify, redirect
from services import user_services, auth_services
from models import Callback, User
admin_api: Blueprint = Blueprint('admin_api', __name__ ,template_folder="../../templates")


# Data for the user which to be displayed on every admin page
@admin_api.route("/admin/getadminpagesdata", methods=['POST'])
def adminPagesData():
    if request.method == "POST" and session.get('Logged_in', False):
        callback: Callback = user_services.getByID(session['UserID'])
        if callback.Success:
            user: User = callback.Data
            return jsonify({
                "name": user.Firstname + " " + user.Surname,
                "EditChatbots": user.Role.EditChatbots,
                "AccessBilling": user.Role.AccessBilling,
                "EditUsers": user.Role.EditUsers
            })
        else:
            print(callback.Message)
            return redirect('login')
    else:
        return redirect('login')


# Data for the user which to be displayed on every admin page
@admin_api.route("/admin/userData", methods=['GET'])
def getUserData():
    if request.method == "GET" and session.get('Logged_in', False):
        callback: Callback = user_services.getByID(session['UserID'])
        if callback.Success:
            user: User = callback.Data
            return jsonify({
                "id": user.ID,
                "email": user.Email,
                "firstname": user.Firstname,
                "surname": user.Surname,
                "stripeID": user.StripeID,
                "subID": user.SubID,
            })
        else:
            print(callback.Message)
            return redirect('login')
    else:
        return redirect('login')
