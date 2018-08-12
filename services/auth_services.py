import sqlalchemy.exc

from models import Callback, User
from utilties import helpers

from flask import session, escape
from json import dumps

from services import assistant_services, user_services

def login(email: str, password_to_check: str) -> Callback:
    # if email == "Error" or password_to_check == "Error":
    #     print("Invalid request: Email or password not received!")
    #     return Callback(False, "You entered an incorrect username or password.")

    # email = email.lower()

    # test input
    email = "email5"

    # user: User = User.query.filter(User.Email == email).first()
    user: User = user_services.getByEmail(email)

    if user:
        password = user.Password
        # todo REMINDER remove the testing if statements
        # if helpers.hash_password(password_to_check, password) == password:
        if not helpers.hashPass(password_to_check, password) == password:
            # If credentials are correct and users' account is verified

            # if user.Verified:
            if not user.Verified:
                # messages = dumps({"email": escape(email)})
                # Set the session for the logged in user

                # It fires an error TODO

                session['User'] = helpers.toJSON(user,User)

                session['Logged_in'] = True

                # Store user assistants if they exist, in the session
                # assistant = assistant_services.getByID(user.Company.ID)

                # Store users access permisions
                # It fires an error TODO
                # session['UserAssistants'] = assistant

                    # Set user plan e.g. (Basic, Ultimate...)
                    # session['UsersPlan'] = {}
                    # session['UserPlan']['Nickname'] =  helpers.getPlanNickname(user['SubID'])
                    #
                    # if helpers.getPlanNickname(user['SubID']) is None:
                    #     session['UserPlan']['Settings'] = helpers.UserPlans["NoPlan"]
                    #
                    # elif "Basic" in helpers.getPlanNickname(user['SubID']):
                    #     session['UserPlan']['Settings'] = helpers.UserPlans["BasicPlan"]
                    #
                    # elif "Advanced" in helpers.getPlanNickname(user['SubID']):
                    #     session['UserPlan']['Settings'] = helpers.UserPlans["AdvancedPlan"]
                    #
                    # elif "Ultimate" in helpers.getPlanNickname(user['SubID']):
                    #     session['UserPlan']['Settings'] = helpers.UserPlans["UltimatePlan"]

                    # Test session specific values
    #                 print(session)
    #
                    # return redirect("/admin/homepage", code=302)
    #
    #             else:
    #                 return redirectWithMessage("login", "Please verify your account before you log in.")
    # return redirectWithMessage("login", "You entered an incorrect username or password.")

