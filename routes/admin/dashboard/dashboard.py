from flask import Blueprint, request, redirect, session
from services import statistics_services, user_services, admin_services
from models import Callback, User


dashboard_router: Blueprint = Blueprint('dashboard_router', __name__, template_folder="../../templates")


@dashboard_router.route("/admin/dashboard", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = user_services.getByID(session.get('userID', 0))
        if callback.Success:
            user: User = callback.Data
            callback: Callback = statistics_services.getTotalAll(user.Company.Assistants)
            if callback.Success:
                return admin_services.render("admin/main.html",
                                             totalClicks=callback.Data.ProductsReturned,
                                             loadedAnswers=callback.Data.QuestionsAnswered)
            else:
                print(callback.Message)
                return redirect('login')
        else:
            return redirect('login')
