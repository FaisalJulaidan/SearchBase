from flask import Blueprint, render_template, request, redirect
from services import statistics_services, assistant_services
from models import Callback

homepage_router: Blueprint = Blueprint('homepage_router', __name__ , template_folder="../../templates")


# Dashboard page
@homepage_router.route("/admin/dashboard", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = statistics_services.getTotalAll()

        # def object_as_dict(obj):
        #     return {c.key: getattr(obj, c.key)
        #             for c in inspect(obj).mapper.column_attrs}

        # TESTING
        row = assistant_services.getAll(1)
        print(row)
        # for u in row:
        #     print(u)
            # print(hepler.sobject_as_dict(u))
        # #########

        if callback.Success:
            return render_template("admin/main.html",
                                   totalClicks=callback.Data.ProductsReturned,
                                   loadedAnswers=callback.Data.QuestionsAnswered,
                                   assistants=assistant_services.getAllAsList())
        else:
            print(callback.Message)
            return redirect('login')
