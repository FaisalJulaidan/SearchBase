from flask import Blueprint, render_template, request, redirect
from services import statistics_services, assistant_services, user_services, auth_services
from models import Callback

homepage_router: Blueprint = Blueprint('homepage_router', __name__, template_folder="../../templates")


# Dashboard page
@homepage_router.route("/admin/dashboard", methods=['GET'])
def admin_home():
    if request.method == "GET" and auth_services.isLogged():
        callback: Callback = user_services.getUserFromSession()
        user = callback.Data
        print(user)
        callback: Callback = statistics_services.getTotalAll(user.Company.Assistants)
        if callback.Success:
            return render_template("admin/main.html",
                                       totalClicks=callback.Data.ProductsReturned,
                                       loadedAnswers=callback.Data.QuestionsAnswered,
                                       assistants=assistant_services.getAll(user.CompanyID))
        else:
            print(callback.Message)
            return redirect('login')
    else:
        return redirect('login')
