import sqlalchemy.exc

from models import Callback, User, Company
from utilties import helpers

from flask import session, escape
from json import dumps

from services import user_services, assistant_services, role_services, sub_services, company_services
from utilties import helpers



def signup(email, firstname, surname, password, companyName, companySize, companyPhoneNumber, websiteURL) -> Callback:

    # Validate Email
    if helpers.isValidEmail(email):
        return Callback(False, 'Invalid Email.')

    # Check if user exists
    user = user_services.getByEmail(email)
    if user:
        return Callback(False, 'User already exists.')


    # Create a new user with its associated company and role
    role = role_services.getByName('Admin')
    company = Company(Name=companyName, Size=companySize, PhoneNumber=companyPhoneNumber, URL=websiteURL)
    user = user_services.create(firstname, surname, email, password, company, role)

    # Subscribe to basic plan with 14 trial days
    sub_callback: Callback = sub_services.subscribe(email=email, planNickname='basic', trialDays=14)

    # if subscription failed, remove the new created company and user
    if not sub_callback.Success:
        company_services.removeByName(companyName)
        user_services.removeByEmail(email)
        return sub_callback

    # Update new user subID and cusID
    user_services.updateSubID(email, sub_callback.Data['subID'])
    user_services.updateStripeID(email, sub_callback.Data['stripeID'])

    # Return a callback with a message
    return Callback(True, 'Signed up successfully!')



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
