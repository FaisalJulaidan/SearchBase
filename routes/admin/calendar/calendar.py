from flask import Blueprint, request, session
from services.Calendars import Google
from models import Callback, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity

calendar_router: Blueprint = Blueprint('calendar_router', __name__, template_folder="../../templates")

@calendar_router.route("/calendar/authorize", methods=['GET'])
# @jwt_required
def admin_analytics_data(assistant):
    return Google.authurl()



