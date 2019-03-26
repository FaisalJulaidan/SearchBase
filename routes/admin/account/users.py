from flask import Blueprint, request
from flask import json
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, db, User
from services import user_services, role_services
from utilities import helpers

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


@users_router.route("/users", methods=['GET'])
@jwt_required
def users():
    user = get_jwt_identity()['user']
    print("user: ", user)

    if request.method == "GET":

        # Data is already converted to javascript lists (needed)
        callback: Callback = user_services.getUsersWithRolesByCompanyID(user.get('companyID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Users could not been retrieved")

        return helpers.jsonResponse(True, 200, "Users have been retrieved",
                                    {"users": callback.Data["users"], "roles": callback.Data["roles"]})

    if request.method == "PUT":

        name = request.form.get("name", None)  # .strip() them
        email = request.form.get("email", None)
        role = request.form.get("type", None)

        if not (name and email and role):
            return helpers.jsonResponse(False, 400, "Could not retrieve all of the submitted data")

        # Get the admin user who is logged in and wants to create a new user.
        user_callback: Callback = user_services.getByID(user.get('id', 0))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        if not user_callback.Data.Role.EditUsers \
                or (role != "Admin" and role != "User") \
                or not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 401, "Please make sure you entered all data correctly and have the " +
                                        "necessary permission to do this action")
        names = name.strip().split(" ")
        addUser_callback: Callback = user_services.createAdditional(names[0], names[-1], email, role,
                                                                    user_callback.Data)
        if not addUser_callback.Success:
            return helpers.jsonResponse(False, 400, addUser_callback.Message)

        return helpers.jsonResponse(True, 200,
                                    "User has been added and an email with his login details is on its way to him")

    if request.method == "POST":

        # User info
        userID = request.json.get("ID", 0)
        firstname = request.json.get("Firstname", '').strip()
        surname = request.json.get("Surname", '').strip()
        email = request.json.get("Email", '').strip()
        role = request.json.get("Role", {}).get("Name", None)
        newRole = request.json.get("RoleName", {}).strip()

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

    if request.method == "DELETE":

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
