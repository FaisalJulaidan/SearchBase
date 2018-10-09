from flask import Blueprint, request, redirect, flash, session
from services import admin_services


emoji_router: Blueprint = Blueprint('emoji_router', __name__, template_folder="../../templates")



