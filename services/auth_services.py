import sqlalchemy.exc

from models import Callback, User
from utilties import helpers

from flask import session, escape
from json import dumps

from services import assistant_services

def login(email: str, password_to_check: str) -> Callback:
    # if email == "Error" or password_to_check == "Error":
    #     print("Invalid request: Email or password not received!")
    #     return Callback(False, "You entered an incorrect username or password.")

    # email = email.lower()

    # test input
    email = "email5"

    user: User = User.query.filter(User.Email == email).first()

    if user.Email == email:
        password = user.Password
        # todo REMINDER remove the testing if statements
        # if helpers.hash_password(password_to_check, password) == password:
        if not helpers.hash_password(password_to_check, password) == password:
            # If credentials are correct and users' account is verified

            # if user.Verified:
            if not user.Verified:
                messages = dumps({"email": escape(email)})
                # Set the session for the logged in user

                # It fires an error TODO
                # session['User'] = user

                session['Logged_in'] = True

                # Store user assistants if they exist, in the session
                assistant = assistant_services.getByID(user.Company.ID)

                #Store users access permisions
                # It fires an error TODO
                # session['UserAssistants'] = assistant


                # permissionsDic = {}
                # permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]

                # if "Owner" in session.get('User')['AccessLevel']:
                #     permissions = permissions["AdminPermissions"].split(";")
                #         for perm in permissions:
                #             if perm:
                #                 permissionsDic[perm.split(":")[0]] = True
    #                 else:
    #                     permissions = permissions[session.get('User')['AccessLevel']+"Permissions"].split(";")
    #                     for perm in permissions:
    #                         if perm:
    #                             if "True" in perm.split(":")[1]:
    #                                 permBool = True
    #                             else:
    #                                 permBool = False
    #                             permissionsDic[perm.split(":")[0]] = permBool
    #                 session['Permissions'] = dict(permissionsDic)
    #
    #                 # Set user plan e.g. (Basic, Ultimate...)
    #                 session['UserPlan'] = {}
    #                 session['UserPlan']['Nickname'] =  getPlanNickname(user['SubID'])
    #                 if getPlanNickname(user['SubID']) is None:
    #                     session['UserPlan']['Settings'] = NoPlan
    #                 elif "Basic" in getPlanNickname(user['SubID']):
    #                     session['UserPlan']['Settings'] = BasicPlan
    #                 elif "Advanced" in getPlanNickname(user['SubID']):
    #                     session['UserPlan']['Settings'] = AdvancedPlan
    #                 elif "Ultimate" in getPlanNickname(user['SubID']):
    #                     session['UserPlan']['Settings'] = UltimatePlan
    #
    #                 # Test session specific values
    #                 print(session)
    #
    #                 return redirect("/admin/homepage", code=302)
    #
    #             else:
    #                 return redirectWithMessage("login", "Please verify your account before you log in.")
    # return redirectWithMessage("login", "You entered an incorrect username or password.")
