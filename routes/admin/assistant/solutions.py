from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services, sub_services, company_services
from models import Callback, Solution, Company, Assistant
from utilities import helpers


solutions_router: Blueprint = Blueprint('Solutions_router', __name__, template_folder="../../templates")

@solutions_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
def admin_solutions(assistantID):
    if request.method == "GET":
        solutions_callback: Callback = solutions_services.getFirstByAssistantID(assistantID)
        if not solutions_callback.Success: return admin_services.render("admin/solutions.html", data="", id=assistantID)

        return admin_services.render("admin/solutions.html", data=solutions_callback.Data, id=assistantID)


@solutions_router.route("/admin/solution/<solID>", methods=['PUT', 'DELETE'])
def update_and_delete_solution(solID):

    # Get the admin user who is logged in and wants to edit and delete.
    callback: Callback = company_services.getByID(session.get('CompanyID', 0))
    if not callback.Success:
        return helpers.jsonResponse(False, 400, "An error occurred. Please login again please")
    company: Company = callback.Data

    if request.method == "PUT":

        # Solution info
        id = request.form.get("inputId", default='').strip()
        majorTitle = request.form.get("inputMajorTitle", default='').strip()
        secondaryTitle = request.form.get("inputSecondaryTitle", default='').strip()
        shortDescription = request.form.get("inputShortDescription", default='').strip()
        money = request.form.get("inputMoney", default='').strip()
        keywords = request.form.get("inputKeywords", default='').strip()
        URL = request.form.get("inputURL", default='').strip()

        if not helpers.isStringsLengthGreaterThanZero(majorTitle, money, URL):
            return helpers.jsonResponse(False, 400, "Please provide all required info for the new solution.")

        # Get the solution to be updated.
        if not solID: solID = 0
        callback: Callback = solutions_services.getByID(solID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, this solution doesn't exist")
        solution: Solution = callback.Data

        # Check if the this user is owns that solution.
        if not solution.Assistant.CompanyID == company.ID:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised")


        # Update the solution
        callback: Callback = solutions_services.update(solution, id, majorTitle, money, URL,
                                                       secondaryTitle, shortDescription, keywords)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message,)

        return helpers.jsonResponse(True, 200, "Solution successfully updated.")

    if request.method == "DELETE":

        # Get the solution to be updated.
        if not solID: solID = 0
        callback: Callback = solutions_services.getByID(solID)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, this solution doesn't exist")
        solution: Solution = callback.Data

        # Check if the this user is owns that solution.
        if not solution.Assistant.CompanyID == company.ID:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised")

        # Delete the solution
        callback: Callback = solutions_services.remove(solution)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        return helpers.jsonResponse(True, 200, "Solution successfully removed.")


@solutions_router.route("/admin/assistant/<assistantID>/solution", methods=['POST'])
def create_solution(assistantID):

    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    if request.method == "POST":

        # Solution info
        solutionsID = request.form.get("inputId", default='').strip()
        majorTitle = request.form.get("inputMajorTitle", default='').strip()
        secondaryTitle = request.form.get("inputSecondaryTitle", default='').strip()
        shortDescription = request.form.get("inputShortDescription", default='').strip()
        money = request.form.get("inputMoney", default='').strip()
        keywords = request.form.get("inputKeywords", default='').strip()
        URL = request.form.get("inputURL", default='').strip()

        if not helpers.isStringsLengthGreaterThanZero(majorTitle, money, URL):
            msg = "Please provide all required info for the new solution."
            if not majorTitle or len(majorTitle) < 0:
                msg = "Major title is required."
            elif not money or len(money) < 0:
                msg = "Money/Price is required."
            elif not URL or len(URL) < 0:
                msg = "URL is required."
            return helpers.jsonResponse(False, 400, msg)

        # TODO: add restriction to only add limited number of solution based on plan
        ########## HERE ###########

        # Create the solution
        callback: Callback = solutions_services.createNew(assistant, majorTitle, money, URL,
                                                       solutionsID, secondaryTitle, shortDescription, keywords)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, None)

        return helpers.jsonResponse(True, 200, "Solution successfully added.")


@solutions_router.route("/admin/assistant/<assistantID>/solutions/file", methods=['POST'])
def admin_products_file_upload(assistantID):
    if request.method == "POST":
        fileType = request.form.get("fileType", default=None)
        file = request.files.get("solutionsFile", default=None)

        if not fileType or not file:
            return "File Type or Uploaded File could not be retrieved"

        if fileType == "RDBXML":
            jsonstr_callback : Callback = solutions_services.convertXMLtoJSON(file)
            if not jsonstr_callback.Success: return jsonstr_callback.Message

            saveJson_callback : Callback = solutions_services.createUpdateJSONByAssistantID(assistantID, jsonstr_callback.Data, fileType)
            if saveJson_callback.Success:
                checkForAlerts_callback : Callback = solutions_services.checkAutomaticSolutionAlerts(assistantID)
                if checkForAlerts_callback.Success:
                    if checkForAlerts_callback.Data:
                        sendAlerts_callback : Callback = solutions_services.sendSolutionsAlerts(assistantID)
                        return saveJson_callback.Message + ". " + sendAlerts_callback.Message

            return saveJson_callback.Message
        else:
            return "Please insure you have selected the right File Type option"

@solutions_router.route("/admin/assistant/<assistantID>/saveSolutionWebLink", methods=['POST'])
def admin_save_solution_web_link(assistantID):

    if request.method == "POST":

        webLink = request.form.get("webLink", default=None).strip()
        solutionsRef = request.form.get("solutionsRef", default=None).strip()

        if not webLink or not solutionsRef: return "Input was not retrieved correctly. Please try again"

        updateLinkAndRef_callback : Callback = solutions_services.updateSolutionsLinkAndRef(assistantID, webLink, solutionsRef)

        return updateLinkAndRef_callback.Message

@solutions_router.route("/admin/assistant/<assistantID>/sendSolutionAlerts", methods=['POST'])
def admin_send_solution_alerts(assistantID):

    if request.method == "POST":

        sendAlerts_callback : Callback = solutions_services.sendSolutionsAlerts(assistantID)

        return sendAlerts_callback.Message

@solutions_router.route("/admin/assistant/<assistantID>/automaticSolutionAlerts/<setTo>", methods=['POST'])
def admin_set_automatic_solution_alert(assistantID, setTo):

    if request.method == "POST":

        if setTo == "true":
            setTo = True
        else:
            setTo = False

        setAutomaticSolutionAlerts_callback : Callback = solutions_services.switchAutomaticSolutionAlerts(assistantID, setTo)

        return setAutomaticSolutionAlerts_callback.Message
