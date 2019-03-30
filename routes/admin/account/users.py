from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import user_services, user_management_services
from utilities import helpers

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


@users_router.route("/users", methods=['GET', 'POST', 'PUT'])
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

        # get the new user's details
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("type")

        # Get the admin user who is logged in and wants to create a new user.
        user_callback: Callback = user_services.getByID(user.get('id'))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        # check if the user can edit users, the email is valid and the role of the new user is valid
        if not user_callback.Data.Role.EditUsers \
                or (role != "Admin" and role != "User") \
                or not helpers.isValidEmail(email):
            return helpers.jsonResponse(False, 400, "Please make sure you entered all data correctly and have the " +
                                        "necessary permission to do this action")

        # add the user
        add_user_callback: Callback = user_management_services.addAdditionalUser(name, email, role, user_callback.Data)
        if not add_user_callback.Success:
            return helpers.jsonResponse(False, 400, add_user_callback.Message)

        return helpers.jsonResponse(True, 200,
                                    "User has been added and an email with his login details is on its way to him")

    if request.method == "PUT":
        # get the new information
        user_id = request.json.get("ID", 0)
        names = request.json.get("Fullname").split(" ")
        email = request.json.get("Email")
        new_role = request.json.get("RoleName")

        # Get the admin user who is logged in and wants to edit.
        user_callback: Callback = user_services.getByID(user.get('id'))
        if not user_callback.Success:
            return helpers.jsonResponse(False, 400, user_callback.Message)

        # check if the email is valid and if the user has permission to edit users and if his new role is valid
        if not helpers.isValidEmail(email) or not user_callback.Data.Role.EditUsersor \
                or (new_role != "Admin" and new_role != "User"):
            return helpers.jsonResponse(False, 400, "Please make sure you entered all data correctly and have the " +
                                        "necessary permission to do this action")

        # Update the user (userToUpdate)
        update_callback: Callback = user_management_services.updateAsOwner(user_id, names[0], names[-1], email,
                                                                           new_role)
        if not update_callback.Success:
            return helpers.jsonResponse(False, 400, update_callback.Message)

        return helpers.jsonResponse(True, 200, "User updated successfully!")


@users_router.route("/user/<int:user_id>", methods=['DELETE'])
@jwt_required
def user(user_id):
    user = get_jwt_identity()['user']

    if request.method == "DELETE":

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
