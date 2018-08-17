from flask import Blueprint, request, session, jsonify, redirect
from services import user_services
from models import Callback

admin_api: Blueprint = Blueprint('admin_api', __name__ ,template_folder="../../templates")


#data for the user which to be displayed on every admin page
@admin_api.route("/admin/getadminpagesdata", methods=['POST'])
def adminPagesData():
    if request.method == "POST":
        callback: Callback = user_services.getUserFromSession()
        if callback.Success:
            user = callback.Data
            callback: Callback = user_services.getByID(user.ID)
            if callback.Success:
                return jsonify({
                    "name": callback.data.Firstname + " " + callback.data.Surname,
                    "EditChatbots": callback.data.Role.EditChatbots,
                    "AccessBilling": callback.data.Role.AccessBilling,
                    "EditUsers": callback.data.Role.EditUsers
                })
            else:
                print(callback.Message)
                return redirect('login')
        else:
            print(callback.Message)
            return redirect('login')



#data for the user which to be displayed on every admin page
@admin_api.route("/admin/userData", methods=['GET'])
def getUserData():
    if request.method == "GET":
        callback: Callback = user_services.getUserFromSession()
        if callback.Success:
            user = callback.Data
            callback: Callback = user_services.getByID(user.ID)
            if callback.Success:
                return jsonify({
                    "id": callback.Data.ID,
                    "email": callback.Data.Email,
                    "firstname": callback.Data.Firstname,
                    "surname": callback.Data.Surname,
                    "stripeID": callback.Data.StripeID,
                    "subID": callback.Data.SubID,
                })
            else:
                print(callback.Message)
                return redirect('login')
        else:
            print(callback.Message)
            return redirect('login')
