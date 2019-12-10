from flask import Blueprint, request
from models import Callback
from utilities import helpers, wrappers
from services import databases_services
from flask_jwt_extended import jwt_required, get_jwt_identity


database_router: Blueprint = Blueprint('database_router', __name__, template_folder="../../templates")

# Get databases list, and create a new database
@database_router.route("/databases", methods=['GET', 'POST'])
@jwt_required
@wrappers.AccessDatabasesRequired
def get_databasesList():

    # Authenticate
    user = get_jwt_identity()['user']

    # Get all databases list (not their content)
    if request.method == "GET":
        callback: Callback = databases_services.getDatabasesList(user['companyID'])
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getListFromSQLAlchemyList(callback.Data))

    # Upload a new database
    if request.method == "POST":
        callback: Callback = databases_services.uploadDatabase(request.json, user['companyID'])
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)
        return helpers.jsonResponse(True, 200, callback.Message, helpers.getDictFromSQLAlchemyObj(callback.Data))


@database_router.route("/databases/<int:databaseID>/page/<int:pageNumber>", methods=['GET'])
@jwt_required
@wrappers.AccessDatabasesRequired
def get_database(databaseID, pageNumber):

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, "")
    if request.method == "GET":
        callback = databases_services.fetchDatabase(databaseID, user['companyID'], pageNumber)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@database_router.route("/databases/<int:databaseID>/available_candidates", methods=['GET'])
@jwt_required
@wrappers.AccessDatabasesRequired
def get_available_candidates(databaseID):

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, "")
    if request.method == "GET":
        callback = databases_services.fetchAvailableCandidates(databaseID, user['companyID'])

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, helpers.getListFromSQLAlchemyList(callback.Data))


# Delete a database and update basic database info
@database_router.route("/databases/<int:databaseID>", methods=['DELETE', 'PUT'])
@jwt_required
@wrappers.AccessDatabasesRequired
def delete_update_database(databaseID):

    # Authenticate
    user = get_jwt_identity()['user']

    callback: Callback = Callback(False, "")
    if request.method == "DELETE":
        callback = databases_services.deleteDatabase(databaseID, user['companyID'])

    if request.method == "PUT":
        data = request.json
        callback = databases_services.updateDatabase(databaseID, data.get('databaseName'), user['companyID'])

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
