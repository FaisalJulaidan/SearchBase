from flask import Blueprint, render_template, request

homepage_router: Blueprint = Blueprint('homepage_router', __name__ ,template_folder="../../templates")

# Admin pages
@homepage_router.route("/admin/homepage", methods=['GET'])
def admin_home():
    if request.method == "GET":
        sendEmail = False
        # email = session.get('User')['Email']
        email = 'Email'
        statistics = [get_total_statistics(3, email), get_total_statistics(5, email)]
        if sendEmail:
            print('test')
            # assistants = get_assistants(email)
            # if assistants == "Error":
            #     return render_template("admin/main.html", stats=statistics, assistantIDs=[])
            # assistantIDs = []
            # for assistant in assistants:
            #     assistantIDs.append(assistant[0])
            # return render_template("admin/main.html", stats=statistics, assistantIDs=assistantIDs)
        else:
            return render_template("admin/main.html") #,stats=statistics)

# def get_total_statistics(num:int, email:str):
#     try:
#         assistant = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;",[get_company(email)[0]])
#         statistics = select_from_database_table("SELECT * FROM Statistics WHERE AssistantID=?;", [assistant[0]])
#         total = 0
#         try:
#             for c in statistics[num]:
#                 total += int(c)
#         except:
#             total = statistics[num]
#     except:
#         total = 0
#     return total
