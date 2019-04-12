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

        add_user_callback: Callback = user_management_services.add_user_with_permission(request.form.get("name"),
                                                                                        request.form.get("email"),
                                                                                        request.form.get("type"),
                                                                                        user.get('id'))
        if not add_user_callback.Success:
            return helpers.jsonResponse(False, 400, add_user_callback.Message)

        return helpers.jsonResponse(True, 200,
                                    "User has been added and an email with his login details is on its way to him")

    if request.method == "PUT":

        update_callback: Callback = user_management_services.update_user_with_permission(request.json.get("ID", 0),
                                                                                         request.json.get("Fullname").split(" ")[0],
                                                                                         request.json.get("Fullname").split(" ")[-1],
                                                                                         request.json.get("Email"),
                                                                                         request.json.get("RoleName"),
                                                                                         user.get('id'))
        if not update_callback.Success:
            return helpers.jsonResponse(False, 400, update_callback.Message)

        return helpers.jsonResponse(True, 200, "User updated successfully!")


@users_router.route("/user/<int:user_id>", methods=['DELETE'])
@jwt_required
def user(user_id):
    user = get_jwt_identity()['user']

    if request.method == "DELETE":

        remove_callback: Callback = user_management_services.delete_user_with_permission(user_id, user.get("id"))
        if not remove_callback.Success:
            return helpers.jsonResponse(False, 400, remove_callback.Message)

        return helpers.jsonResponse(True, 200, "User deleted successfully!")
