from flask import Blueprint, request, session
from services import admin_services, analytics_services, assistant_services
from models import Callback

dashboard_router: Blueprint = Blueprint('dashboard_router', __name__, template_folder="../../templates")


@dashboard_router.route("/admin/dashboard", methods=['GET'])
def admin_home():
    if request.method == "GET":
        #callback: Callback = user_services.getByID(session.get('UserID', 0))

        #if not callback.Success:
        #        print(callback.Message)
        #        return redirect('login')
        #user: User = callback.Data
        chatbots_callback : Callback = assistant_services.getAll(session.get('CompanyID', None))
        if not chatbots_callback.Success: 
            print("1")
            return admin_services.render("admin/dashboard.html")

        assistants = chatbots_callback.Data

        totalClicks_callback : Callback = analytics_services.getTotalUsersForCompany(assistants)
        if not totalClicks_callback.Success: 
            print("2")
            return admin_services.render("admin/dashboard.html")

        totalSolutions_callback : Callback = analytics_services.getTotalReturnedSolutionsForCompany(assistants)
        if not totalSolutions_callback.Success: 
            print("3")
            return admin_services.render("admin/dashboard.html")

        return admin_services.render("admin/dashboard.html", totalClicks = totalClicks_callback.Data, totalSolutions = totalSolutions_callback.Data)


    # c_callback: Callback = company_services.getByID(1)
    # company = c_callback.Data
    # json = company.Assistants[0].to_dict(max_nesting=1)

    # q_callback: Callback = questions_services.getByAssistantID(1)
    # questions = q_callback.Data
    # print(questions[0].to_dict(max_nesting=2))
