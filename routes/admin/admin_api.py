from flask import Blueprint, request, session, jsonify
from services import user_services



admin_api: Blueprint = Blueprint('admin_api', __name__ ,template_folder="../../templates")

#data for the user which to be displayed on every admin page
@admin_api.route("/admin/getadminpagesdata", methods=['POST'])
def adminPagesData():
    if request.method == "POST":
        user = user_services.getByID(session['userID'])


        json = {
            "name": user.Firstname + " " + user.Surname,
            "EditChatbots":user.Role.EditChatbots,
            "AccessBilling":user.Role.AccessBilling,
            "EditUsers":user.Role.EditUsers
        }
        return jsonify(json)



#data for the user which to be displayed on every admin page
@admin_api.route("/admin/userData", methods=['GET'])
def getUserData():
    if request.method == "GET":
        user = user_services.getByID(session['userID'])
        userDict = {
            "id": user.ID,
            "email": user.Email,
            "firstname": user.Firstname,
            "surname": user.Surname,
            "stripeID": user.StripeID,
            "subID": user.SubID,
        }
        return jsonify(userDict)
