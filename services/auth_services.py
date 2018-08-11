import sqlalchemy.exc

from models import Callback, User, Company
from utilties import helpers

from flask import session, escape
from json import dumps

from services import user_services, assistant_services, role_services, sub_services, company_services
from validate_email import validate_email


def signup(email, firstname, surname, password, companyName, companySize, companyPhoneNumber, websiteURL):

    # Validate Email
    if validate_email(email):
        return Callback(False, 'Invalid Email.')

    # Check if user exists
    user = user_services.getByEmail(email)
    if user:
        return Callback(False, 'User already exists.')

    # Create a new user with its associated company and role
    role = role_services.getByName('Admin')
    company = Company(Name=companyName, Size=companySize, PhoneNumber=companyPhoneNumber, URL=websiteURL)
    user = user_services.createUser(firstname, surname, email, password, company, role)

    # Subscribe to basic plan with 14 trial days
    callback: Callback = sub_services.subscribe(email=email, planNickname='basic', trialDays=14)

    # if subscription failed, remove the new created company and user
    if not callback.Success:
        company_services.removeByName(companyName)
        user_services.removeByEmail(email)
        return callback

    # Return a callback with a message
    return Callback(True, 'Signed up successfully!')



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
