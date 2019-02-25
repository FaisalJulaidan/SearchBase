from datetime import datetime, timedelta

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, create_refresh_token

from models import Callback, User, UserSettings, db
from services import user_services, role_services, sub_services, company_services
from utilities import helpers

jwt = JWTManager()
tokenExpiresIn = 15 # in minutes

@jwt.invalid_token_loader
def my_expired_token_callback(error):
    return helpers.jsonResponse(False, 401, "Token expired")


def signup(details) -> Callback:
    # Validate Email
    if not helpers.isValidEmail(details['email']):
        return Callback(False, 'Invalid Email.')

    # Check if user exists
    user = user_services.getByEmail(details['email']).Data
    if user:
        return Callback(False, 'User already exists.')

    # Company
    # Create a company plus the Stripe customer and link it with the company
    company_callback: Callback = company_services.create(name=details['companyName'],
                                                         url=details['websiteURL'],
                                                         ownerEmail=details['email'])
    if not company_callback.Success:
        return Callback(False, company_callback.Message)
    company = company_callback.Data

    # Roles
    # Create owner, admin, user roles for the new company
    ownerRole: Callback = role_services.create('Owner', True, True, True, True, company)
    adminRole: Callback = role_services.create('Admin', True, True, True, False, company)
    userRole: Callback = role_services.create('User', True, False, False, False, company)
    if not (ownerRole.Success or adminRole.Success or userRole.Success):
        return Callback(False, 'Could not create roles for the new user.')

    # User
    # Create a new user with its associated company and owner role
    user_callback = user_services.create(details['firstName'],
                                         details['lastName'],
                                         details['email'],
                                         details['password'],
                                         details['telephone'],
                                         company,
                                         ownerRole.Data)

    # Create userSettings for this user
    db.session.add(UserSettings(User=user_callback.Data))


    # Subscribe to basic plan with 14 trial days
    sub_callback: Callback = sub_services.subscribe(company=company, planID='plan_D3lpeLZ3EV8IfA', trialDays=14)

    # If subscription failed, remove the new created company and user
    if not sub_callback.Success:
        # Removing the company will cascade and remove the new created user and roles as well.
        print('remove company')
        company_services.removeByName(details['companyName'])
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
                         "username": user.Firstname + ' ' + user.Surname,
                         "lastAccess": user.LastAccess,
                         "phoneNumber": user.PhoneNumber,
                         "plan": helpers.getPlanNickname(user.Company.SubID),
                         "roleID": user.RoleID
                         }
                }

        access_token = create_access_token(identity=data)
        refresh_token = create_refresh_token(identity=data)
        data['token'] = access_token
        data['refresh'] = refresh_token
        data['expiresIn'] = datetime.now() + timedelta(minutes=tokenExpiresIn) # add 15 minutes from now

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
        data = {'token': create_access_token(identity=current_user),
                'expiresIn': datetime.now() + timedelta(minutes=refreshTokenExpiresIn)}
        return Callback(True, "Authorised!", data)
    except Exception as e:
        return Callback(False, "Unauthorised!", None)
