from flask import Blueprint, render_template, request, redirect, session
from services import statistics_services, assistant_services,user_services, auth_services
from models import Callback

settings_router: Blueprint = Blueprint('settings_router', __name__, template_folder="../../templates")


@settings_router.route("/admin/assistant/<assistantID>/settings", methods=['GET', 'POST'])
def admin_assistant_edit(assistantID):
    if request.method == "GET" and auth_services.isLogged():
        callback: Callback = assistant_services.getByID(assistantID)
        if callback.Success:
            message = callback.Data.Message
            autoPop = callback.Data.SecondsUntilPopup
            nickname = callback.Data.Nickname
            active = callback.Data.Active
            return render_template("admin/edit-assistant.html",
                                   autopop=autoPop, message=message, id=assistantID,
                                   nickname=nickname, active=active)
        else:
            print(callback.Message)
            return redirect('login')
    else:
        return redirect('login')

    # elif request.method == "POST":
    #     email = session.get('User')['Email']
    #     company = get_company(email)
    #     if company is None or "Error" in company:
    #         return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting the company's records!")
    #     else:
    #         assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
    #                                                [assistantID, company[0]])
    #         if assistant is None or "Error" in assistant:
    #             return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting the assistant's records!")
    #         else:
    #             nickname = request.form.get("nickname", default="Error")
    #             message = request.form.get("welcome-message", default="Error")
    #             popuptime = request.form.get("timeto-autopop", default="Error")
    #             autopopup = request.form.get("switch-autopop", default="off")
    #
    #             if message is "Error" or nickname is "Error" or (popuptime is "Error" and autopopup is not "off"):
    #                 return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting your inputs!")
    #             else:
    #                 if autopopup == "off":
    #                     secondsUntilPopup = "Off"
    #                 else:
    #                     secondsUntilPopup = popuptime
    #                 updateAssistant = update_table(
    #                     "UPDATE Assistants SET Message=?, SecondsUntilPopup=?, Nickname=? WHERE ID=? AND CompanyID=?",
    #                     [message, secondsUntilPopup, nickname, assistantID, company[0]])
    #
    #                 if "Error" in updateAssistant:
    #                     return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in updating assistant!")
    #                 else:
    #                     return redirect("/admin/assistant/{}/settings".format(assistantID))
