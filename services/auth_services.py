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

    user: User = user_services.getByEmail(email)

    if user:
        # todo REMINDER remove the testing if statements
        # if helpers.hash_password(password_to_check, password) == password:
        if not helpers.hashPass(password_to_check, user.Password) == user.Password:
            # [*] store user.ID in session
            # [*] store is logged_in = true in session
            # [*] store UserPlan in session

            # If credentials are correct and users' account is verified
            # if user.Verified:
            if not user.Verified:
                session['Logged_in'] = True
                session['user.ID'] = user.ID

                planNickname = helpers.getPlanNickname(user.SubID)

                # Set user plan e.g. (Basic, Ultimate...)
                session['UserPlan'] = {
                    'Nickname':'',
                    'Settings':''
                }
                session['UserPlan']['Nickname'] = planNickname

                if planNickname is None:
                    session['UserPlan']['Settings'] = helpers.UserPlans["NoPlan"]

                elif "Basic" in planNickname:
                    session['UserPlan']['Settings'] = helpers.UserPlans["BasicPlan"]

                elif "Advanced" in planNickname:
                    session['UserPlan']['Settings'] = helpers.UserPlans["AdvancedPlan"]

                elif "Ultimate" in planNickname:
                    session['UserPlan']['Settings'] = helpers.UserPlans["UltimatePlan"]

                # return redirect("/admin/homepage", code=302)
                return Callback(True, "You entered an incorrect username or password.")
    #
    #             else:
    #                 return redirectWithMessage("login", "Please verify your account before you log in.")
    # return redirectWithMessage("login", "You entered an incorrect username or password.")
