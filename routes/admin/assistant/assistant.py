from flask import Blueprint, render_template, request, redirect
from services import statistics_services, assistant_services
from models import Callback

assistant_router: Blueprint = Blueprint('assistant_router', __name__ , template_folder="../../templates")


# get all assistants
@assistant_router.route("/admin/assistants", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = statistics_services.getTotalAll()
        if callback.Success:
            return render_template("admin/dashboard.html",
                                   totalClicks=callback.Data.ProductsReturned,
                                   loadedAnswers=callback.Data.QuestionsAnswered,
                                   assistants=assistant_services.getAllAsList())
        else:
            print(callback.Message)
            return redirect('login')


