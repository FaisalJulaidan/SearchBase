from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services, sub_services
from models import Callback, Product
from utilties import helpers

bot_router: Blueprint = Blueprint('bot_router', __name__, template_folder="../../templates")

@bot_router.route("/admin/assistant/<assistantID>/bot", methods=['GET', 'POST'])
def bot(assistantID):
    if request.method == "GET":
        return admin_services.render('admin/bot.html')
