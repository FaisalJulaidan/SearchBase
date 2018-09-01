from flask import Blueprint, request, redirect, session
from services import statistics_services, user_services, admin_services, sub_services, company_services, questions_services
from models import Callback, User, Plan


dashboard_router: Blueprint = Blueprint('dashboard_router', __name__, template_folder="../../templates")


@dashboard_router.route("/admin/dashboard", methods=['GET'])
def admin_home():
    if request.method == "GET":
        callback: Callback = user_services.getByID(session.get('UserID', 0))

        # c_callback: Callback = company_services.getByID(1)
        # company = c_callback.Data
        # json = company.Assistants[0].to_dict(max_nesting=1)

        # q_callback: Callback = questions_services.getByAssistantID(1)
        # questions = q_callback.Data
        # print(questions[0].to_dict(max_nesting=2))

        if callback.Success:
            user: User = callback.Data
            print(user.to_json(max_nesting=1))
            callback: Callback = statistics_services.getTotalAll(user.Company.Assistants)
            if callback.Success:
                return admin_services.render("admin/dashboard.html",
                                             totalClicks=callback.Data.ProductsReturned,
                                             loadedAnswers=callback.Data.QuestionsAnswered)
            else:
                print(callback.Message)
                return redirect('login')
        else:
            return redirect('login')
