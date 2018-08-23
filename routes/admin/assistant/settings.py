from flask import Blueprint, request, redirect, flash
from services import assistant_services,admin_services
from models import Callback, Assistant

settings_router: Blueprint = Blueprint('settings_router', __name__, template_folder="../../templates")


@settings_router.route("/admin/assistant/<assistantID>/settings", methods=['GET', 'POST'])
def admin_assistant_edit(assistantID):
    if request.method == "GET":
        callback: Callback = assistant_services.getByID(assistantID)
        if callback.Success:
            assistant: Assistant = callback.Data
            return admin_services.render("admin/edit-assistant.html",
                                         message=assistant.Message,
                                         autopop=assistant.SecondsUntilPopup,
                                         nickname=assistant.Nickname,
                                         active=assistant.Active,
                                         id=assistant.ID)
        else:
            print(callback.Message)
            return redirect('login')

    elif request.method == "POST":
        nickname = request.form.get("nickname", default=False)
        message = request.form.get("welcome-message", default=False)
        autopopup = request.form.get("switch-autopop", default=False) # true / false
        popuptime = request.form.get("timeto-autopop", default=False) # float 1.0


        if not message or \
           not nickname or \
           (not popuptime and not autopopup):
            flash({'type': 'danger', 'msg': 'Error in getting your inputs!'})
            return redirect("/admin/assistant/{}/settings".format(assistantID))
        else:
            if not autopopup:
                secondsUntilPopup = 0.0
            else:
                secondsUntilPopup = popuptime

            callback: Callback = assistant_services.update(id=assistantID,
                                                           nickname=nickname, message=message,
                                                           secondsUntilPopup=secondsUntilPopup)
            if callback.Success:
                flash({'type': 'success', 'msg': nickname + ' Updated Successfully'})
                return redirect("/admin/assistant/{}/settings".format(assistantID))
            else:
                flash({'type': 'danger', 'msg': 'Error in updating ' + nickname})
                return redirect("/admin/assistant/{}/settings".format(assistantID))
