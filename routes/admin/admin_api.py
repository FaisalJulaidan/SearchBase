from flask import Blueprint,request

admin_api: Blueprint = Blueprint('admin_api', __name__ ,template_folder="../../templates")

#data for the user which to be displayed on every admin page
@admin_api.route("/admin/getadminpagesdata", methods=['POST'])
def adminPagesData():
    if request.method == "POST":
        # email = session.get('User')['Email']
        # users = query_db("SELECT * FROM Users")
        # If user exists
        # for user in users:
        #     if user["Email"] == email:
        #         returnString = ""
        #         permissions = ""
        #         for key,value in session['Permissions'].items():
        #             permissions+= key + ":" + str(value) + ";"
        #         planSettings = ""
        #         for key,value in session['UserPlan']['Settings'].items():
        #             planSettings += key + ":" + str(value) + ";"
        #         return user["Firstname"] + "&&&" + permissions + "&&&" + planSettings
        return "wait...Who are you?"



#data for the user which to be displayed on every admin page
@admin_api.route("/admin/userData", methods=['GET'])
def getUserData():
    if request.method == "GET":
        print('test')
        # userDict = {
        #     "id": session['User']['ID'],
        #     "email": session['User']['Email'],
        #     "firstname": session['User']['Firstname'],
        #     "surname": session['User']['Surname'],
        #     "stripeID": session['User']['StripeID'],
        #     "subID": session['User']['SubID'],
        #
        # }
        # return jsonify(userDict)
