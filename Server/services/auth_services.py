from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, create_refresh_token
from models import Callback, User, db
from services import user_services, role_services, sub_services, company_services, mail_services
from utilities import helpers
from config import BaseConfig


jwt = JWTManager()

@jwt.invalid_token_loader
def my_expired_token_callback(error):
    return helpers.jsonResponse(False, 401, "Session has expired")


def signup(details) -> Callback:

    try:
        email = details['email']
        
        # Validate Email
        if not helpers.isValidEmail(email):
            return Callback(False, 'Invalid Email')
        

        # Check if user exists
        if user_services.getByEmail(email).Data:
            return Callback(False, 'Email already exists')

        # Company
        # Create a company plus the Stripe customer and link it with the company
        company_callback: Callback = company_services.create(name=details['companyName'],
                                                             url=details['websiteURL'],
                                                             ownerEmail=email)
        if not company_callback.Success:
            return Callback(False, company_callback.Message)
        company = company_callback.Data

        # Roles
        # Create owner, admin, user roles for the new company
        adminRole: Callback = role_services.create('Admin', True, True, True, True, False, company.ID)
        userRole: Callback = role_services.create('User', True, False, False, False, False, company.ID)
        if not (adminRole.Success or userRole.Success):
            return Callback(False, 'Could not create roles for the new user')

        # User
        # Create a new user with its associated company and owner role
        user_callback = user_services.create(details['firstName'],
                                             details['lastName'],
                                             email,
                                             details['password'],
                                             details['telephone'],
                                             company.ID,
                                             2,
                                             details['timeZone']) # RoleID = 2 -> Owner


        # Subscribe to basic plan with 14 trial days
        # sub_callback: Callback = sub_services.subscribe(company=company, planID='plan_D3lpeLZ3EV8IfA', trialDays=14)


        # Account Verification
        verify_callback: Callback = mail_services\
            .sendVerificationEmail(details['firstName'], details['lastName'], email, company.Name, company.ID)

        # Send us mail that someone has registered
        notify_us_callback: Callback = mail_services.sendNewCompanyHasRegistered(details['firstName'] + details['lastName'],
                                                                                 email,
                                                                                 company.Name,
                                                                                 company.ID,
                                                                                 details['telephone'])

        # If subscription failed, remove the new created company and user
        if not (user_callback.Success or verify_callback.Success or notify_us_callback.Success):
            # Removing the company will cascade and remove the new created user and roles as well.
            company_services.removeByName(company.Name)
            return user_callback

        # ###############
        # Just for testing, But to be REMOVED because user has to verify account manually
        # user_services.verifyByEmail(email)
        # ###############

        # Return a callback with a message
        return Callback(True, "Signed up successfully", company.ID)

    except Exception as exc:
        helpers.logError("auth_services.signup(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Failed to signup", None)


def authenticate(email: str, password_to_check: str) -> Callback:
    try:
        # Login Exception Handling
        if not (email or password_to_check):
            return Callback(False, "Email or password not received. Please try again!")

        user_callback: Callback = user_services.getByEmail(email.lower())
        # If user is not found
        if not user_callback.Success:
            return Callback(False, "Record with the current email or password was not found")

        # Get the user from the callback object
        user: User = user_callback.Data
        if not password_to_check == user.Password:
            return Callback(False, "Record with the current email or password was not found")

        if not user.Verified:
            return Callback(False, "Account is not verified.")

        if not user.Company.Active:
            return Callback(False, "Please, wait for SearchBase team to activate your account")

        # If all the tests are valid then do login process
        data = {'user': {
                         "email": user.Email,
                         "username": user.Firstname + ' ' + user.Surname,
                         "lastAccess": user.LastAccess,
                         "phoneNumber": user.PhoneNumber,
                         "timezone": user.TimeZone
                         # "plan": helpers.getPlanNickname(user.Company.SubID),
                         },
                'role': helpers.getDictFromSQLAlchemyObj(user.Role),
                'company': helpers.getDictFromSQLAlchemyObj(user.Company)  # BUG: Stored as list currently
        }
        # print("here")
        # print(helpers.getListFromSQLAlchemyList(user.Company.Plan))
        time_now = datetime.now()
        # for security, hide them in the token
        tokenData = {'user': {"id": user.ID, "companyID": user.CompanyID, "email": user.Email, "roleID": user.RoleID}}

        # Create the JWT token
        access_token = create_access_token(identity=tokenData)
        refresh_token = create_refresh_token(identity=tokenData)
        data['token'] = access_token
        data['refresh'] = refresh_token
        data['expiresIn'] = datetime.now() + BaseConfig.JWT_ACCESS_TOKEN_EXPIRES

        # Set LastAccess
        user.LastAccess = time_now
        db.session.commit()

        return Callback(True, "Authorised!", data)
    except Exception as exc:
        helpers.logError("auth_services.authenticate(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Unauthorised!", None)


def refreshToken() -> Callback:
    try:
        current_user = get_jwt_identity()

        # get the user requesting token refresh
        user_callback: Callback = user_services.getByEmail(current_user.get("user").get("email").lower())
        if not user_callback.Success:
            raise Exception("Your login was not recognised")

        # check if the LastAccess token in the db is the same as the one the jwt user has.
        # the db one would change if another user logs in after them
        # if not str(user_callback.Data.LastAccess) == current_user.get("user").get("log_time"):
        #     raise Exception("Your account was logged in somewhere else")

        data = {'token': create_access_token(identity=current_user),
                'expiresIn': datetime.now() + BaseConfig.JWT_ACCESS_TOKEN_EXPIRES,
                'company': helpers.getDictFromSQLAlchemyObj(user_callback.Data.Company)} # with new permissions maybe
        return Callback(True, "Authorised!", data)
    except Exception as exc:
        helpers.logError("auth_services.refreshToken(): " + str(exc))
        return Callback(False, "Unauthorised!", None)
