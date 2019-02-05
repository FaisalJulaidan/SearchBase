from flask import Blueprint, request
from models import Callback
from utilities import helpers
from services import databases_services
from flask_jwt_extended import jwt_required


database_router: Blueprint = Blueprint('database_router', __name__, template_folder="../../templates")

@database_router.route("/database/options", methods=['GET'])
@jwt_required
def get_databaseOptions():
    if request.method == "GET":
        callback: Callback = databases_services.getOptions()
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "These are the options the database provides.", callback.Data)
