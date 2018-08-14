from flask import Blueprint, render_template, request, redirect
from services import statistics_services, assistant_services
from models import Callback

homepage_router: Blueprint = Blueprint('homepage_router', __name__ , template_folder="../../templates")

# Admin pages
@homepage_router.route("/admin/homepage", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = statistics_services.getTotalAll()
        if callback.Success:
            return render_template("admin/main.html",
                                   totalClicks=callback.Data.ProductsReturned,
                                   loadedAnswers=callback.Data.QuestionsAnswered,
                                   assistants=assistant_services.getAllAsList())
        else:
            print(callback.Message)
            return redirect('login')
