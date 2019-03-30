from flask import Blueprint, request
from flask import json
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, db, User
from services import user_services, role_services, user_management_services
from utilities import helpers

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


@users_router.route("/users", methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required
def users():
    user = get_jwt_identity()['user']

    if request.method == "GET":

        # Data is already converted to javascript lists (needed)
        callback: Callback = user_services.getUsersWithRolesByCompanyID(user.get('companyID'))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Users could not been retrieved")

        return helpers.jsonResponse(True, 200, "Users have been retrieved",
                                    {"users": callback.Data["users"], "roles": callback.Data["roles"]})

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("type")

        # Get the admin user who is logged in and wants to create a new user.
        user_callback: Callback = user_services.getByID(user.get('id'))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        if not user_callback.Data.Role.EditUsers \
                or (role != "Admin" and role != "User") \
                or not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 400, "Please make sure you entered all data correctly and have the " +
                                        "necessary permission to do this action")

        add_user_callback: Callback = user_management_services.addAdditionalUser(name, email, role, user_callback.Data)
        if not add_user_callback.Success:
            return helpers.jsonResponse(False, 400, add_user_callback.Message)

        return helpers.jsonResponse(True, 200,
                                    "User has been added and an email with his login details is on its way to him")

    if request.method == "PUT":
        # User info
        user_id = request.json.get("ID", 0)
        first_name = request.json.get("Firstname")
        surname = request.json.get("Surname")
        email = request.json.get("Email")
        new_role = request.json.get("RoleName")

        # Get the admin user who is logged in and wants to edit.
        user_callback: Callback = user_services.getByID(user.get('id'))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        if not (first_name and surname and email)\
                or not helpers.isValidEmail(email)\
                or not user_callback.Data.Role.EditUsers:
            return helpers.jsonResponse(False, 400, "Please make sure you entered all data correctly and have the " +
                                        "necessary permission to do this action")

        # Update the user (userToUpdate)
        update_callback: Callback = user_management_services.updateAsOwner(user_id, first_name, surname, email,
                                                                           new_role)
        if not update_callback.Success:
            return helpers.jsonResponse(False, 400, update_callback.Message)

        return helpers.jsonResponse(True, 200, "User updated successfully!")

    if request.method == "DELETE":

        # Get the user to be deleted.
        user_id = request.json.get("ID")

        # Get the admin user who is logged in and wants to delete.
        user_callback: Callback = user_services.getByID(user.get('id'))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        # Check if the admin user is authorised for such an operation.
        if not user_callback.Data.Role.DeleteUsers:
            return helpers.jsonResponse(False, 400, "You're not authorised to delete users")

        # Delete the user
        remove_callback: Callback = user_services.removeByID(user_id)
        if not remove_callback.Success:
            return helpers.jsonResponse(False, 400, remove_callback.Message)

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
                for new_role in values:
                    if role.ID == int(new_role['ID']):
                        role.EditChatbots = new_role['EditChatbots']
                        role.EditUsers = new_role['EditUsers']
                        role.DeleteUsers = new_role['DeleteUsers']
                        role.AccessBilling = new_role['AccessBilling']
            # Save changes
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return helpers.jsonResponse(False, 400, "An error occurred! Try again please.")

        print("Success >> roles updated")
        return helpers.jsonResponse(True, 200, "Roles updated successfully!")
