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

    # Login Exception Handling
    if not (email or password_to_check):
        print("Invalid request: Email or password not received!")
        return Callback(False, "You entered an incorrect username or password.")

    user_callback: Callback = user_services.getByEmail(email.lower())
    # If user is not found
    if not user_callback.Success:
        print("Invalid request: Email not found")
        return Callback(False, "Email not found.")

    # Get the user from the callback object
    user: User = user_callback.Data
    if not helpers.hashPass(password_to_check, user.Password) == user.Password:
        print("Invalid request: Incorrect Password")
        return Callback(False, "Incorrect Password.")

    if not user.Verified:
        print("Invalid request: Account is not verified")
        return Callback(False, "Account is not verified.")

    # If all the tests are valid then do login process
    session['Logged_in'] = True
    session['userID'] = user.ID
    session['UserPlan'] = helpers.getPlanNickname(user.SubID)

    return Callback(True, "Login Successful")
