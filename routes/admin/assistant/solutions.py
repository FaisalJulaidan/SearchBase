from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services, sub_services, company_services
from models import Callback, Solution, Company, Assistant
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


solutions_router: Blueprint = Blueprint('Solutions_router', __name__, template_folder="../../templates")

# @solutions_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
# def admin_solutions(assistantID):
#
#     if request.method == "GET":
#         return admin_services.render("admin/solutions.html", id=assistantID)


@solutions_router.route("/assistant/<assistantID>/solutionsData", methods=['GET', 'PUT', 'POST', 'DELETE'])
@jwt_required
def admin_solutions_data(assistantID):

    if request.method == "GET":
        solutions_callback: Callback = solutions_services.getAllByAssistantID(assistantID)
        if not solutions_callback.Success: return helpers.jsonResponse(False, 400, "Solutions could not be retrieved")

        returnData = []

        for solution in solutions_callback.Data:
            displayTitles_callback : Callback = solutions_services.getDisplayTitlesOfRecords(solution)
            if not displayTitles_callback.Success:
                returnData.append({"Solution" : admin_services.convertForJinja(solution, Solution).Data[0], "DisplayTitles": None})
                continue
            returnData.append({"Solution" : admin_services.convertForJinja(solution, Solution).Data[0], "DisplayTitles": displayTitles_callback.Data})

        return helpers.jsonResponse(True, 200, "Solutions have been retrieved", returnData)

    if request.method == "PUT":
        fileName = request.form.get("name", None)
        fileType = request.form.get("type", None)
        if not fileName or not fileType:
            return helpers.jsonResponse(False, 403, "File name or type could not be retrieved")

        if fileType == "RDB XML File Export":
            file = request.files.get("uploadFile", None)
            if not file:
                return helpers.jsonResponse(False, 403, "Uploaded File could not be retrieved")

            jsonstr_callback : Callback = solutions_services.convertXMLtoJSON(file)
            if not jsonstr_callback.Success:
                return helpers.jsonResponse(False, 403, jsonstr_callback.Message)

            saveJson_callback : Callback = solutions_services.createNew(assistantID, jsonstr_callback.Data, fileType, fileName)
            if not saveJson_callback.Success:
                return helpers.jsonResponse(False, 403, saveJson_callback.Message)
            returnMessage = saveJson_callback.Message
        else:
            return helpers.jsonResponse(False, 403, "Please insure you have selected the right File Type option")

        return helpers.jsonResponse(True, 200, returnMessage)
        # UPDATE UPLOADED FILES:
        #
        #     jsonstr_callback : Callback = solutions_services.convertXMLtoJSON(file)
        #     if not jsonstr_callback.Success: return jsonstr_callback.Message
        #
        #     saveJson_callback : Callback = solutions_services.updateByID(int(solutionSelect), jsonstr_callback.Data, fileType, fileName)
        #     if saveJson_callback.Success:
        #         checkForAlerts_callback : Callback = solutions_services.checkAutomaticSolutionAlerts(int(solutionSelect))
        #         if checkForAlerts_callback.Success:
        #             if checkForAlerts_callback.Data:
        #                 sendAlerts_callback : Callback = solutions_services.sendSolutionsAlerts(int(solutionSelect))
        #                 return saveJson_callback.Message + ". " + sendAlerts_callback.Message
        # else:
        #     return "Please insure you have selected the right File Type option"


@solutions_router.route("/assistant/<assistantID>/savedisplaytitles/<solutionID>", methods=['POST'])
@jwt_required
def admin_save_display_titles(assistantID, solutionID):

    if request.method == "POST":

        titlesArray = {"titleValues" : [], "solutionDescription": ""}
        for i in range(0, 50):
            record = request.form.get("titleSelect"+str(i), default=None)
            if not record: continue
            titlesArray["titleValues"].append(record.strip())

        titlesArray["solutionDescription"] = request.form.get("description", default=None)
        conditions_callback = solutions_services.saveDisplayTitles(solutionID, titlesArray)
        return conditions_callback.Message

@solutions_router.route("/assistant/<assistantID>/savesolutionweblink/<solutionID>", methods=['POST'])
@jwt_required
def admin_save_solution_web_link(assistantID, solutionID):

    if request.method == "POST":

        webLink = request.form.get("webLink", default=None)
        solutionsRef = request.form.get("solutionsRef", default=None)

        if not webLink or not solutionsRef: return "Input was not retrieved correctly. Please try again"

        webLink = webLink.strip()
        solutionsRef = solutionsRef.strip()

        updateLinkAndRef_callback : Callback = solutions_services.updateSolutionsLinkAndRef(solutionID, webLink, solutionsRef)

        return updateLinkAndRef_callback.Message

@solutions_router.route("/assistant/<assistantID>/requiredfilters/<solutionID>", methods=['POST'])
@jwt_required
def admin_save_required_filters(assistantID, solutionID):

    if request.method == "POST":

        conditionsArray = {"filterValues" : []}

        for i in range(0, 50):
            record = request.form.get("conditionInput"+str(i), default=None)
            if not record: continue
            print("record: ", record)
            record = record.split(",")
            record = [x.strip() for x in record if not x.strip() == ""]
            conditionsArray["filterValues"].append(record)

        conditionsArray["requiredConditionsNumber"] = request.form.get("conditionsNumberInput", default=0)

        conditions_callback = solutions_services.saveRequiredFilters(solutionID, conditionsArray)
        return conditions_callback.Message

@solutions_router.route("/assistant/<assistantID>/sendsolutionalerts/<solutionID>", methods=['POST'])
@jwt_required
def admin_send_solution_alerts(assistantID, solutionID):

    if request.method == "POST":

        sendAlerts_callback : Callback = solutions_services.sendSolutionsAlerts(assistantID, solutionID)

        return sendAlerts_callback.Message

@solutions_router.route("/assistant/<assistantID>/automaticsolutionalerts/<solutionID>/<setTo>", methods=['POST'])
@jwt_required
def admin_set_automatic_solution_alert(assistantID, solutionID, setTo):

    if request.method == "POST":

        if setTo == "true":
            setTo = True
        else:
            setTo = False

        setAutomaticSolutionAlerts_callback : Callback = solutions_services.switchAutomaticSolutionAlerts(solutionID, setTo)

        return setAutomaticSolutionAlerts_callback.Message
