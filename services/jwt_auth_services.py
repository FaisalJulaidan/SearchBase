from datetime import datetime

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, create_refresh_token

from models import Callback, User, UserSettings, db
from services import user_services, role_services, sub_services, company_services
from utilities import helpers

jwt = JWTManager()


@jwt.invalid_token_loader
def my_expired_token_callback(error):
    return helpers.jsonResponse(False, 401, "Invalid Token ☹")


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
    if not (ownerRole.Success or adminRole.Success or userRole.Success):
        return Callback(False, 'Could not create roles for the new user.')

    # Create a new user with its associated company and owner role
    user_callback = user_services.create(firstname, surname, email, password, companyPhoneNumber, company,
                                         ownerRole.Data)

    try:
        # Create userSettings for this user
        db.session.add(UserSettings(User=user_callback.Data))
    except Exception as e:
        db.session.rollback()
    # finally:
    # db.session.close()

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


def authenticate(email: str, password_to_check: str) -> Callback:
    try:
        # Login Exception Handling
        if not (email or password_to_check):
            print("Invalid request: Email or password not received!")
            return Callback(False, "Email or password not received. Please try again!")

        user_callback: Callback = user_services.getByEmail(email.lower())
        # If user is not found
        if not user_callback.Success:
            print("Invalid request: Email not found")
            return Callback(False, "Record with the current email or password was not found")

        # Get the user from the callback object
        user: User = user_callback.Data
        if not password_to_check == user.Password:
            print("Invalid request: Incorrect Password")
            return Callback(False, "Record with the current email or password was not found")

        if not user.Verified:
            return Callback(False, "Account is not verified.")

        # If all the tests are valid then do login process
        data = {'user': {"id": user.ID,
                         "companyID": user.CompanyID,
                         "email": user.Email,
                         "plan": helpers.getPlanNickname(user.Company.SubID),
                         "roleID": user.RoleID
                         }
                }

        access_token = create_access_token(identity=data)
        refresh_token = create_refresh_token(identity=data)
        data['user']['token'] = access_token
        data['user']['refresh'] = refresh_token
        print(data)

        # Set LastAccess
        user.LastAccess = datetime.now()
        db.session.commit()

        return Callback(True, "Authorised!", data)
    except Exception as e:
        print(e)
        db.session.rollback()
        return Callback(False, "Unauthorised!", None)
    # finally:
    # db.session.close()


def refreshToken() -> Callback:
    try:
        current_user = get_jwt_identity()
        print("current user: ", current_user)
        data = {'token': create_access_token(identity=current_user)}
        return Callback(True, "Authorised!", data)
    except Exception as e:
        return Callback(False, "Unauthorised!", None)
