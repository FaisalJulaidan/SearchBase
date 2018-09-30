from models import Callback, User, UserSettings, db
from datetime import datetime
from flask import session

from services import user_services, role_services, sub_services, company_services
from utilities import helpers


def signup(email, firstname, surname, password, companyName, companyPhoneNumber, websiteURL) -> Callback:

    # Validate Email
    if not helpers.isValidEmail(email):
        return Callback(False, 'Invalid Email.')

    # Check if user exists
    user = user_services.getByEmail(email).Data
    if user:
        return Callback(False, 'User already exists.')

    # Create a company plus the Stripe customer and link it with the company
    company_callback: Callback = company_services.create(name=companyName, url=websiteURL, ownerEmail=email)
    if not company_callback.Success:
        return Callback(False, company_callback.Message)
    company = company_callback.Data

    # Create owner, admin, user roles for the new company
    ownerRole: Callback = role_services.create('Owner', True, True, True, True, company)
    adminRole: Callback = role_services.create('Admin', True, True, True, False, company)
    userRole: Callback = role_services.create('User', True, False, False, False, company)
    if not (ownerRole.Success or adminRole.Success or userRole.Success) :
        return Callback(False, 'Could not create roles for the new user.')

    # Create a new user with its associated company and owner role
    user_callback = user_services.create(firstname, surname, email, password, companyPhoneNumber, company, ownerRole.Data)

    # Create userSettings for this user
    db.session.add(UserSettings(User=user_callback.Data))

    # Subscribe to basic plan with 14 trial days
    sub_callback: Callback = sub_services.subscribe(company=company, planID='plan_D3lpeLZ3EV8IfA', trialDays=14)

    # If subscription failed, remove the new created company and user
    if not sub_callback.Success:
        # Removing the company will cascade and remove the new created user and roles as well.
        print('remove company')
        company_services.removeByName(companyName)
        return sub_callback

    # ###############
    # Just for testing, But to be REMOVED because user has to verify this manually
    # user_services.verifyByEmail(email)
    # ###############

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
    if not password_to_check == user.Password:
        print("Invalid request: Incorrect Password")
        return Callback(False, "Incorrect Password.")

    if not user.Verified:
        print("Account is not verified!")
        return Callback(False, "Account is not verified.")

    # If all the tests are valid then do login process
    session['Logged_in'] = True
    session['UserID'] = user.ID
    session['CompanyID'] = user.CompanyID
    session['UserEmail'] = user.Email
    session['UserPlan'] = helpers.getPlanNickname(user.Company.SubID)
    session['RoleID'] = user.RoleID
    print(session)

    # Set LastAccess
    user.LastAccess = datetime.now()

    # Save db changes
    db.session.commit()

    return Callback(True, "Login Successful")
