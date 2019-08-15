from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback
from services.Marketplace import marketplace_helpers
from utilities import helpers

files_router: Blueprint = Blueprint('files_router', __name__, template_folder="../../templates")

# Auth this?
# Get connected marketplace items without testing the connection (CRMs, Calendars etc.)
@files_router.route("/files/unused", methods=["GET"])
def get_unused_files():


