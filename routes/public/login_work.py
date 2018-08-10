from datetime import timedelta
from json import dumps

from flask import Blueprint, request, session, escape
import utilties.helpers as helpers
from services.users_services import UserServices
login_router = Blueprint('public_router',__name__,template_folder="../templates")

@login_router.route("/login", methods=['POST'])
def login():
    if request.method == "POST":
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)

        email = request.form.get("email", default="Error")
        password_to_check = request.form.get("password", default="Error")

        if email == "Error" or password_to_check == "Error":
            print("Invalid request: Email or password not received!")
            return helpers.redirectWithMessage("login", "You entered an incorrect username or password.")

        else:
            email = email.lower()

            users = UserServices.getUsers()
                # If user exists
            for user in users:
                if user["Email"] == email:
                    password = user['Password']
                    if helpers.hash_password(password_to_check, password) == password:
                        verified = user['Verified']

                        # If credentials are correct and users' account is verified
                        if verified == "True":
                            messages = dumps({"email": escape(email)})

                            # Set the session for the logged in user
                            session['User'] = user
                            session['Logged_in'] = True

                            #TODO: assistansServices.getAssistans(company.id)
                            # Store user assistants if they exist, in the session
                            # assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?;", [user['CompanyID']])

                            #Store users access permisions
                            session['UserAssistants'] = assistants
                            permissionsDic = {}
                            permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]
                            if "Owner" in session.get('User')['AccessLevel']:
                                permissions = permissions["AdminPermissions"].split(";")
                                for perm in permissions:
                                    if perm:
                                        permissionsDic[perm.split(":")[0]] = True
                            else:
                                permissions = permissions[session.get('User')['AccessLevel']+"Permissions"].split(";")
                                for perm in permissions:
                                    if perm:
                                        if "True" in perm.split(":")[1]:
                                            permBool = True
                                        else:
                                            permBool = False
                                        permissionsDic[perm.split(":")[0]] = permBool
                            session['Permissions'] = dict(permissionsDic)

                            # Set user plan e.g. (Basic, Ultimate...)
                            session['UserPlan'] = {}
                            session['UserPlan']['Nickname'] =  getPlanNickname(user['SubID'])
                            if getPlanNickname(user['SubID']) is None:
                                session['UserPlan']['Settings'] = NoPlan
                            elif "Basic" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = BasicPlan
                            elif "Advanced" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = AdvancedPlan
                            elif "Ultimate" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = UltimatePlan

                            # Test session specific values
                            print(session)

                            return redirect("/admin/homepage", code=302)

                        else:
                            return redirectWithMessage("login", "Please verify your account before you log in.")
            return redirectWithMessage("login", "You entered an incorrect username or password.")
