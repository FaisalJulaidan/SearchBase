from flask import Blueprint, render_template, request, redirect, session
from services import admin_services, role_services, assistant_services
from models import Callback, Role
from utilties import helpers

assistantManager_router: Blueprint = Blueprint('assistantManager_router', __name__ , template_folder="../../templates")


# get all assistants
@assistantManager_router.route("/admin/assistant/manage", methods=["GET"])
def assistant_manager():

    if request.method == "GET":

        userRoleID = session.get('RoleID', None)
        userRole_callback : Callback = role_services.getByID(userRoleID)
        if not userRole_callback.Success: return admin_services.render("admin/assistant-manager.html")

        userRole_callback = admin_services.convertForJinja(userRole_callback.Data, Role)
        if not userRole_callback.Success: return admin_services.render("admin/assistant-manager.html")

        return admin_services.render("admin/assistant-manager.html", userRole=userRole_callback.Data[0])

@assistantManager_router.route("/admin/assistant/active/<turnto>/<assistantID>", methods=['GET'])
def admin_turn_assistant(turnto, assistantID):

    if request.method == "GET":

        ownership_callback : Callback = assistant_services.checkOwnership(assistantID, session.get('CompanyID', None))
        if not ownership_callback.Success: return helpers.redirectWithMessage("assistant_manager", ownership_callback.Message)

        #Get all assistants in order to check if plan restrictions are good with everything
        assistants_callback : Callback = assistant_services.getAll(session.get('CompanyID', None))
        if not assistants_callback.Success: helpers.redirectWithMessage("assistant_manager", "Error in pre-change checks.")
       
        #if turnto == "True":
        #    numberOfProducts = 0
        #    maxNOP = session.get('UserPlan')['Settings']['MaxProducts']
        #    for record in assistants:
        #        numberOfProducts += count_db("Products", " WHERE AssistantID=?", [record["ID"],])
        #    if numberOfProducts > maxNOP:
        #        return redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP)+ ". In order to activate an assistant you will have to reduce the number of products you currently have: "+str(numberOfProducts)+".")

        #    #Check max number of active bots
        #    numberOfActiveBots = count_db("Assistants", " WHERE CompanyID=? AND Active=?", [session.get('User')['CompanyID'], "True"])
        #    if numberOfActiveBots >= session['UserPlan']['Settings']['ActiveBotsCap']:
        #        return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "You have already reached the maximum amount of Active Assistants. Please deactivate one to proceed.")

        #    message="activated."
        #else:
        #    #Check max number of inactive bots
        #    numberOfInactiveBots = count_db("Assistants", " WHERE CompanyID=? AND Active=?", [session.get('User')['CompanyID'], "False"])
        #    if numberOfInactiveBots >= session['UserPlan']['Settings']['InactiveBotsCap']:
        #        return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "You have already reached the maximum amount of Inactive Assistants. If you wish to deactivate this bot please delete or activate an inactivate assistant")

        #    message="deactivated."
        changeAssistantStatus_callback : Callback = assistant_services.changeStatus(assistantID, turnto)

        return helpers.redirectWithMessageAndAssistantID("assistant_manager", assistantID, changeAssistantStatus_callback.Message)

@assistantManager_router.route("/admin/assistant/delete/<assistantID>", methods=['GET'])
def admin_assistant_delete(assistantID):

    if request.method == "GET":

        ownership_callback : Callback = assistant_services.checkOwnership(assistantID, session.get('CompanyID', None))
        if not ownership_callback.Success: return helpers.redirectWithMessage("assistant_manager", ownership_callback.Message)

        deleteAssistant_callback : Callback = assistant_services.removeByID(assistantID)
        
        return helpers.redirectWithMessage("assistant_manager", deleteAssistant_callback.Message)
