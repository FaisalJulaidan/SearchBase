from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, StoredFileInfo
from services import stored_file_services

from utilities import helpers

files_router: Blueprint = Blueprint('files_router', __name__, template_folder="../../templates")

# Auth this?
# Get connected marketplace items without testing the connection (CRMs, Calendars etc.)
@files_router.route("/files/delete", methods=["GET"])
def get_unused_files():
    FileList: Callback = stored_file_services.getUnusedAndDelete()

    if not FileList.Success:
        return helpers.jsonResponse(False, 400, FileList.Message)

    return helpers.jsonResponse(True, 200, "Gathered filelist", helpers.getListFromSQLAlchemyList(FileList.Data))
