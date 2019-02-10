import random
import string

from flask import Blueprint, request, redirect
from flask import json

from models import Callback, db, User
from services import user_services, admin_services, role_services, mail_services
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


# Update roles
@users_router.route("/roles", methods=['PUT'])
@jwt_required
def update_roles():
    user = get_jwt_identity()['user']

    if request.method == "PUT":

        # Get the admin user who is logged in and wants to edit.
        callback: Callback = user_services.getByID(user.get('id', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, your account doesn't exist. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if not adminUser.Role.Name == 'Owner':
            return helpers.jsonResponse(False, 401,
                                        "Sorry, You're not authorised. Only owners are allowed to edit user's permissions.")

        # New roles values
        values = request.form.get("data", None)
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
@users_router.route("/users", methods=['GET'])
@jwt_required
def users():
    user = get_jwt_identity()['user']

    if request.method == "GET":

        users_callback: Callback = user_services.getAllByCompanyID(user.get('companyID', 0))
        role_callback: Callback = role_services.getAllByCompanyID(user.get('companyID', 0))

        roles = []
        userWithRoles = []
        if users_callback.Success and role_callback.Success:
            users = helpers.getListFromSQLAlchemyList(users_callback.Data)
            roles = helpers.getListFromSQLAlchemyList(role_callback.Data)
            userWithRoles = helpers.mergeRolesToUserLists(users, roles)

        return helpers.jsonResponse(True, 200, "Users have been retrieved",
                                    {"users": userWithRoles, "roles": roles})


# Create a new user under the logged in user's company
@users_router.route("/user", methods=['PUT', 'POST'])
@jwt_required
def user():
    user = get_jwt_identity()['user']

    if request.method == "PUT":

        # Get the admin user who is logged in and wants to create a new user.
        callback: Callback = user_services.getByID(user.get('id', 0))
        if not callback.Success:
            return redirect("login")
        adminUser: User = callback.Data

        # Check if the admin user is authorised to create a new user.
        if not adminUser.Role.EditUsers:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised to create a user")

        # If authorised then complete the process
        # Get submitted user info
        name = request.form.get("name", '').strip()
        firstname = name.split(" ")[0]
        surname = name.split(" ")[len(name.split(" ")) - 1]
        email = request.form.get("email", '').strip()
        role = request.form.get("type", "")
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))

        if role != "Admin" and role != "User":
            return helpers.jsonResponse(False, 400, "Role must be Admin or User")

        # Check if info valid
        if not helpers.isStringsLengthGreaterThanZero(firstname, surname, email, role):
            return helpers.jsonResponse(False, 400, "Please provide all required info for the new user.")

        # Validate the given email
        if not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 400, "Please provide a valid email.")

        # Check if email is already used
        userTest: User = user_services.getByEmail(email).Data
        if userTest:
            return helpers.jsonResponse(False, 400, "Email is already on use.")

        # Get the role to be assigned for the user
        callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.Company.ID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, role + " role does not exist.")
        role = callback.Data

        # Create the new user for the company
        callback: Callback = user_services.create(firstname, surname, email, password, "00000",
                                                  adminUser.Company, role, verified=True)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry couldn't create the user. Try again!")

        email_callback: Callback = mail_services.addedNewUserEmail(user.get('email', "Error"), email, password)
        if not email_callback.Success:
            return json.dumps({'success': False,
                               'msg': " New user was created but could not send email with login information. Please delete and readd the user."}), \
                   400, {'ContentType': 'application/json'}

        return json.dumps({'success': True, 'msg': " User has been created successfully!"}), \
               200, {'ContentType': 'application/json'}

    if request.method == "POST":

        # User info
        userID = request.json.get("ID", 0)
        firstname = request.json.get("Firstname", '').strip()
        surname = request.json.get("Surname", '').strip()
        email = request.json.get("Email", '').strip()
        role = request.json.get("Role", {}).get("Name", None)

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
        callback: Callback = user_services.getByID(user.get('id', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, you account doesn't exist. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if not adminUser.Role.EditUsers:
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


@users_router.route("/user_delete", methods=['POST'])
@jwt_required
def user_delete():
    user = get_jwt_identity()['user']

    if request.method == "POST":

        # Get the user to be deleted.
        userID = request.json.get("ID", 0)
        if not userID: userID = 0
        callback: Callback = user_services.getByID(userID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, but this user doesn't exist")
        userToBeDeleted: User = callback.Data

        # Get the admin user who is logged in and wants to delete.
        callback: Callback = user_services.getByID(user.get('id', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred. Try again please!")
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if not adminUser.Role.DeleteUsers:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised")

        # Delete the user
        callback: Callback = user_services.removeByID(userToBeDeleted.ID)
        if not callback.Success:
            return helpers.jsonResponse(False, 500, "Sorry, error occurred. Try again please!")

        return helpers.jsonResponse(True, 200, "User deleted successfully!")
