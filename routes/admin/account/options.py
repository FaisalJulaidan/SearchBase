

from flask import Blueprint, request

from models import Callback
from services import options_services
from utilities import helpers
from flask_jwt_extended import jwt_required

options_router: Blueprint = Blueprint('options_router', __name__, template_folder="../../templates")


@options_router.route("/options", methods=['GET'])
@jwt_required
def get_options():

    if request.method == "GET":
        callback: Callback = options_services.getOptions()
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "", callback.Data)