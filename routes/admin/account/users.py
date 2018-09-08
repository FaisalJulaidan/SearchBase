from flask import jsonify, json
from services import user_services, admin_services, role_services, company_services, mail_services
from models import Callback, db, User, Company
from flask import Blueprint, request, redirect, session
from utilties import helpers, json_utils

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


# Update roles
@users_router.route("/admin/roles", methods=['PUT'])
def update_roles():
    if request.method == "PUT":

        # Get the admin user who is logged in and wants to edit.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, your account doesn't exist. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if not adminUser.Role.Name == 'Owner':
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised. Only owners are")

        # New roles values
        values = request.form.get("data", default=None)
        if not values:
            return helpers.jsonResponse(False, 400, "Please provide all required info for the roles.")
        values = json.loads(values)

        try:
            currentRoles = adminUser.Company.Roles
            for role in currentRoles:
                for newRole in values:
                    if role.ID == int(newRole['ID']):
                        role.EditChatbots = newRole['EditChatbots']
                        role.EditUsers = newRole['EditUsers']
                        role.DeleteUsers = newRole['DeleteUsers']
                        role.AccessBilling = newRole['AccessBilling']
            # Save changes
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return helpers.jsonResponse(False, 400, "An error occurred! Try again please.")

        print("Success >> roles updated")
        return helpers.jsonResponse(True, 200, "Roles updated successfully!")


# Get all users for logged in company
@users_router.route("/admin/users", methods=['GET'])
def admin_users():
    if request.method == "GET":
        users_callback: Callback = user_services.getAllByCompanyID(session.get('CompanyID', 0))
        role_callback: Callback =  role_services.getAllByCompanyID(session.get('CompanyID', 0))

        roles = []
        userWithRoles = []
        if users_callback.Success and role_callback.Success:
            users = helpers.getListFromSQLAlchemyList(users_callback.Data)
            roles = helpers.getListFromSQLAlchemyList(role_callback.Data)
            userWithRoles = helpers.mergeRolesToUserLists(users, roles)

        return admin_services.render("admin/users.html", users=userWithRoles, roles=roles)


# Create a new user under the logged in user's company
@users_router.route("/admin/user", methods=['POST'])
def admin_users_add():
    if request.method == "POST":

        # Get the admin user who is logged in and wants to create a new user.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised to create a new user.
        if not adminUser.Role.EditUsers:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised to create a user")

        # If authorised then complete the process
        # Get submitted user info
        firstname = request.form.get("firstname", default='').strip()
        surname = request.form.get("surname", default='').strip()
        email = request.form.get("email", default='').strip()
        role = request.form.get("role", default='').strip()

        # Check if info valid
        if not helpers.isStringsLengthGreaterThanZero(firstname, surname, email, role):
            return helpers.jsonResponse(False, 400, "Please provide all required info for the new user.")

        # Validate the given email
        if not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 400, "Please provide a valid email.")

        # Check if email is already used
        user: User = user_services.getByEmail(email).Data
        if user:
            return helpers.jsonResponse(False, 400, "Email is already on use.")

        # Get the role to be assigned for the user
        callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.Company.ID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, role + " role does not exist.")
        role = callback.Data

        # Create the new user for the company
        callback: Callback = user_services.create(firstname, surname, email, 'passwordToBeChanged',
                                                  adminUser.Company, role, verified=True)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry couldn't create the user. Try again!")

        email_callback : Callback = mail_services.addedNewUserEmail(session.get('UserEmail', "Error"), email)
        if not email_callback.Success:
            return json.dumps({'success': False, 'msg': " New user was created but could not send email with login information. Please delete and readd the user."}), \
                   400, {'ContentType': 'application/json'}

        return json.dumps({'success': True, 'msg': " User has been created successfully!"}), \
                   200, {'ContentType': 'application/json'}


# Update user with id <userID>
@users_router.route("/admin/user/<userID>", methods=['PUT'])
def update_user(userID):
    if request.method == "PUT":

        # User info
        firstname = request.form.get("firstname", default='').strip()
        surname = request.form.get("surname", default='').strip()
        email = request.form.get("email", default='').strip()
        role = request.form.get("role", default='').strip()

        if not helpers.isStringsLengthGreaterThanZero(firstname, surname, email, role):
            return helpers.jsonResponse(False, 400, "Please provide all required info for the new user.")

        # Validate the given email
        if not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 400, "Please provide a valid email.")

        # Get the user to be updated.
        if not userID: userID = 0
        callback: Callback = user_services.getByID(userID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, but this user doesn't exist")
        userToUpdate: User = callback.Data

        # Get the admin user who is logged in and wants to edit.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, you account doesn't exist. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if (not adminUser.Role.EditUsers) or \
                userToUpdate.CompanyID != adminUser.CompanyID or \
                userToUpdate.Role.Name == adminUser.Role.Name or \
                userToUpdate.Role.Name == 'Owner':
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised")

        # Get the role to be assigned for the userToUpdate
        callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.Company.ID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, role + " role does not exist.")
        role = callback.Data

        # Update the user (userToUpdate)
        callback: Callback = user_services.updateAsOwner(userToUpdate.ID, firstname, surname, email, role)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry couldn't update the user. Please try again!")

        print("Success >> user updated")
        return helpers.jsonResponse(True, 200, "User updated successfully!")



@users_router.route("/admin/user/<userID>", methods=['DELETE'])
def delete_user(userID):
    if request.method == "DELETE":

        # Get the user to be deleted.
        if not userID: userID = 0
        callback: Callback = user_services.getByID(userID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, but this user doesn't exist")
        userToBeDeleted: User = callback.Data

        # Get the admin user who is logged in and wants to delete.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if (not adminUser.Role.DeleteUsers) or\
                userToBeDeleted.CompanyID != adminUser.CompanyID or \
                userToBeDeleted.Role.Name == adminUser.Role.Name or \
                userToBeDeleted.Role.Name == 'Owner':
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised")

        # Delete the user
        callback: Callback = user_services.removeByID(userToBeDeleted.ID)
        if not callback.Success:
            return helpers.jsonResponse(False, 500, "Sorry, error occurred. Try again please!")

        print("Success.  " + userID)
        return helpers.jsonResponse(True, 200, "User deleted successfully!")


