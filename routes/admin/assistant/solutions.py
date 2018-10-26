from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services, sub_services, company_services
from models import Callback, Solution, Company, Assistant
from utilities import helpers


solutions_router: Blueprint = Blueprint('Solutions_router', __name__, template_folder="../../templates")

@solutions_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
def admin_solutions(assistantID):
    if request.method == "GET":

        # solutions_callback: Callback = solutions_services.getAllByAssistantID(assistantID)
        # solutions = []
        # if solutions_callback.Success:
        #     solutions = solutions_callback.Data
        # print(solutions)
        # return admin_services.render("admin/solutions.html", data=solutions, id=assistantID)
        return admin_services.render("admin/solutions.html", id=assistantID)

    # elif request.method == 'POST':
    #     companyID = session.get('CompanyID', None)
    #     if not companyID: return helpers.redirectWithMessage("admin_solutions", "Could not retrieve company's ID")
    #
    #     # Get all company assistants (needed for totalproducts check)
    #     assistant_callback : Callback = assistant_services.getAll(companyID)
    #     if not assistant_callback.Success: return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, assistant_callback.Message)
    #
    #     # Get all previous solutions
    #     solutions_callback: Callback = solutions_services.getByAssistantID(assistantID)
    #     currentSolutions = solutions_callback.Data
    #     if not solutions_callback.Success: solutions_callback.Data = []
    #     #currentProducts -> solutions_callback
    #
    #     # Delete old solutions so the new one can be put it
    #     deleteOldData : bool = solutions_services.deleteAllByAssistantID(assistantID)
    #     if not deleteOldData:
    #         solutions_services.addOldByAssitantID(assistantID,
    #                                               "Could not delete old data in order to put the new one."
    #                                               " Old records were lost.",
    #                                               currentSolutions)
    #         return helpers.redirectWithMessageAndAssistantID("admin_solutions",
    #                                                          assistantID,
    #                                                          "Could not delete old data in order to put the new one."
    #                                                          " Old records are restored")
    #
    #     # The form submits each cell individiually so here it counts how many records there are so it can then initiate a loop
    #     NumberOfSolutions = 1
    #     for key in request.form:
    #         if "product_ID" in key:
    #             NumberOfSolutions += 1
    #
    #     for i in range(1, NumberOfSolutions):
    #         # TODO add more info to these error messages
    #         id = request.form.get("product_ID" + str(i), default=None)
    #
    #         name = request.form.get("product_Name" + str(i), default=None)
    #
    #         brand = request.form.get("product_Brand" + str(i), default=None)
    #
    #         model = request.form.get("product_Model" + str(i), default=None)
    #
    #         price = request.form.get("product_Price" + str(i), default=None)
    #
    #         keywords = request.form.get("product_Keywords" + str(i), default=None)
    #
    #         discount = request.form.get("product_Discount" + str(i), default=None)
    #
    #         url = request.form.get("product_URL" + str(i), default=None)
    #
    #         if not (id or name  or brand  or model  or price  or keywords  or discount  or url):
    #             solutions_services.deleteByAssitantID(assistantID, "Could not retrieve part of the new data." + str(i) + " records have been added after deletion of the old ones.")
    #             solutions_services.addOldByAssitantID(assistantID, "Could not retrieve part of the new data. Solutions have been emptied.", currentSolutions)
    #             return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, "Could not retrieve part of the new data. Process aborted and old data has been restored.")
    #
    #         #add in http:// in their url if they havent so later html accepts it as a link
    #         if "http" not in url:
    #             url = "http://" + url
    #
    #         #get user's sub plan
    #         #print("session.get('UserPlan', None): ", session.get('UserPlan', None))
    #         #plan_callback : Callback = sub_services.getPlanByNickname(session.get('UserPlan', None)) #change to userPlan
    #         plan_callback : Callback = Callback(True, "Plan Found", "basic")
    #         if not plan_callback.Success: return helpers.redirectWithMessage("admin_solutions", "Could not retrieve Sub Plan for max products check.")
    #
    #         #count how much products they have in total
    #         numberOfProducts = 0
    #         for record in assistant_callback.Data:
    #             recordsCount = solutions_services.countRecordsByAssistantID(record.ID)
    #             numberOfProducts += recordsCount
    #
    #         #see if they have reached the limit of how many solutions they can have
    #         #if numberOfProducts > plan_callback.Data.MaxProducts:
    #         if numberOfProducts > 5:
    #             return helpers.redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP)+ ". Solutions after " + name + " have not been added.")
    #
    #         print("New Record: ", assistantID, id, name, brand, model, price, keywords, discount, url)
    #         createSolution_callback : Callback = solutions_services.createNew(assistantID, id, name, brand, model, price, keywords, discount, url)
    #
    #         if not createSolution_callback.Success:
    #             solutions_services.deleteByAssitantID(assistantID, "Could not create one of the new solutions: "+id+" "+name+"." + str(i) + " records have been added after deletion of the old ones.")
    #             solutions_services.addOldByAssitantID(assistantID, "Could not create on of the new solutions. Solutions have been emptied.", currentSolutions)
    #             return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, "Could not create one of the new solutions: "+id+" "+name+". Reverting to old ones")
    #     return redirect("/admin/assistant/{}/solutions".format(assistantID))


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


#https://pypi.org/project/xmljson/     to json
#https://docs.python.org/3/library/xml.etree.elementtree.html   handle xml
# TODO improve
@solutions_router.route("/admin/assistant/<assistantID>/solutions/file", methods=['POST'])
def admin_products_file_upload(assistantID):
    if request.method == "POST":
        fileType = request.form.get("fileType", default=None)
        file = request.files.get("solutionsFile", default=None)

        if not fileType or not file:
            return "File Type or Uploaded File could not be retrieved"

        if fileType == "RBDXML":
            jsonstr_callback : Callback = solutions_services.convertXMLtoJSON(file)
            if not jsonstr_callback.Success: return jsonstr_callback.Message

            print(jsonstr_callback.Data)
            saveJson_callback : Callback = solutions_services.createUpdateJSONByAssistantID(assistantID, jsonstr_callback.Data)

            return saveJson_callback.Message
        else:
            return "Please insure you have selected the right File Type option"
