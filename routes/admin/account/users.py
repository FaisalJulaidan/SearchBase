from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services import user_services, user_management_services, role_services
from utilities import helpers

users_router: Blueprint = Blueprint('users_router', __name__, template_folder="../../templates")


@users_router.route("/users", methods=['GET', 'POST', 'PUT'])
@jwt_required
def users():
    user = get_jwt_identity()['user']

    if request.method == "GET":

        users_callback: Callback = user_services.getAllByCompanyID(user.get('companyID'))
        roles_callback: Callback = role_services.getAllByCompanyID(user.get('companyID'))
        if not (users_callback.Success or roles_callback.Success):
            return helpers.jsonResponse(False, 400, "could not retrieve list of Users")

        users =[]
        for user in users_callback.Data:
            users.append({
                'user': helpers.getDictFromSQLAlchemyObj(user),
                'role': helpers.getDictFromSQLAlchemyObj(user.Role),
            })

        return helpers.jsonResponse(True,
                                    200,
                                    "Users have been retrieved",
                                    {'users': users, 'roles': helpers.getListFromSQLAlchemyList(roles_callback.Data)})

    if request.method == "POST":

        add_user_callback: Callback = user_management_services.addUser(request.form.get("name"),
                                                                       request.form.get("email"),
                                                                       request.form.get("type"),
                                                                       user.get('id'))
        if not add_user_callback.Success:
            return helpers.jsonResponse(False, 400, add_user_callback.Message)

        return helpers.jsonResponse(True, 200,
                                    "User has been added and an email with his login details is on its way to him")

        return helpers.jsonResponse(True, 200, "User updated successfully!")


@users_router.route("/user/<int:user_id>", methods=['PUT','DELETE'])
@jwt_required
def user(user_id):
    user = get_jwt_identity()['user']

    if request.method == "PUT":
        data = request.json
        callback: Callback = user_management_services.editUser(user_id,
                                                               data.get("firstname"),
                                                               data.get("surname"),
                                                               data.get("phoneNumber"),
                                                               data.get("roleID"),
                                                               user['id'],
                                                               user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, "User updated successfully")

    if request.method == "DELETE":

        remove_callback: Callback = user_management_services.delete_user_with_permission(user_id, user.get("id"))
        if not remove_callback.Success:
            return helpers.jsonResponse(False, 400, remove_callback.Message)

        return helpers.jsonResponse(True, 200, "User deleted successfully!")
