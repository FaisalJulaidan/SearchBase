from flask import Blueprint, request
from models import Callback
from utilities import helpers
from services import databases_services
from flask_jwt_extended import jwt_required, get_jwt_identity



database_router: Blueprint = Blueprint('database_router', __name__, template_folder="../../templates")

@database_router.route("/databases/options", methods=['GET'])
@jwt_required
def get_databaseOptions():
    if request.method == "GET":
        callback: Callback = databases_services.getOptions()
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "These are the options the database provides.", callback.Data)


@database_router.route("/databases", methods=['GET', 'POST'])
@jwt_required
def get_databasesList():

    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = databases_services.getDatabasesList(user['companyID'])
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getListFromSQLAlchemyList(callback.Data))


@database_router.route("/databases/<int:databaseID>", methods=['GET'])
@jwt_required
def get_database(databaseID):

    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        callback: Callback = databases_services.fetchDatabase(databaseID, user['companyID'])
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)