from flask import Blueprint, request, redirect, flash, session
from services import admin_services


emoji_router: Blueprint = Blueprint('emoji_router', __name__, template_folder="../../templates")


@emoji_router.route("/admin/emoji-converter", methods=['GET'])
def admin_emoji():
    if request.method == "GET":
        return admin_services.render("admin/emoji.html")
