from flask import Blueprint, request, redirect, session
from services import solutions_services, admin_services, assistant_services
from models import Callback, Solution
from utilities import helpers

solutions_router: Blueprint = Blueprint('Solutions_router', __name__, template_folder="../../templates")

@solutions_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
def admin_solutions(assistantID):
    if request.method == "GET":

        solutions_callback: Callback = solutions_services.getByAssistantID(assistantID)

        #if it coudnt find anything assume its empty
        if not solutions_callback.Success: solutions_callback.Data = []
        print(solutions_callback.Data)
        #convert solutions to dics
        if type(solutions_callback.Data) is Solution:
            solutions = [helpers.getDictFromSQLAlchemyObj(solutions_callback.Data)]
        else:
            solutions = helpers.getListFromSQLAlchemyList(solutions_callback.Data)

        return admin_services.render("admin/solutions.html", data=solutions, id=assistantID)

    elif request.method == 'POST':
        companyID = session.get('CompanyID', None)
        if not companyID: return helpers.redirectWithMessage("admin_solutions", "Could not retrieve company's ID")

        # Get all company assistants (needed for totalproducts check)
        assistant_callback : Callback = assistant_services.getAll(companyID)
        if not assistant_callback.Success: return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, assistant_callback.Message)

        # Get all previous solutions
        solutions_callback: Callback = solutions_services.getByAssistantID(assistantID)
        currentSolutions = solutions_callback.Data
        if not solutions_callback.Success: solutions_callback.Data = []
        #currentProducts -> solutions_callback

        # Delete old solutions so the new one can be put it
        deleteOldData : bool = solutions_services.deleteAllByAssistantID(assistantID)
        if not deleteOldData: 
            solutions_services.addOldByAssitantID(assistantID,
                                                  "Could not delete old data in order to put the new one."
                                                  " Old records were lost.",
                                                  currentSolutions)
            return helpers.redirectWithMessageAndAssistantID("admin_solutions",
                                                             assistantID,
                                                             "Could not delete old data in order to put the new one."
                                                             " Old records are restored")

        # The form submits each cell individiually so here it counts how many records there are so it can then initiate a loop
        NumberOfSolutions = 1
        for key in request.form:
            if "product_ID" in key:
                NumberOfSolutions += 1

        for i in range(1, NumberOfSolutions):
            # TODO add more info to these error messages
            id = request.form.get("product_ID" + str(i), default=None)

            name = request.form.get("product_Name" + str(i), default=None)

            brand = request.form.get("product_Brand" + str(i), default=None)

            model = request.form.get("product_Model" + str(i), default=None)

            price = request.form.get("product_Price" + str(i), default=None)

            keywords = request.form.get("product_Keywords" + str(i), default=None)

            discount = request.form.get("product_Discount" + str(i), default=None)

            url = request.form.get("product_URL" + str(i), default=None)

            if not (id or name  or brand  or model  or price  or keywords  or discount  or url):
                solutions_services.deleteByAssitantID(assistantID, "Could not retrieve part of the new data." + str(i) + " records have been added after deletion of the old ones.")
                solutions_services.addOldByAssitantID(assistantID, "Could not retrieve part of the new data. Solutions have been emptied.", currentSolutions)
                return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, "Could not retrieve part of the new data. Process aborted and old data has been restored.")

            #add in http:// in their url if they havent so later html accepts it as a link
            if "http" not in url:
                url = "http://" + url

            #get user's sub plan
            #print("session.get('UserPlan', None): ", session.get('UserPlan', None))
            #plan_callback : Callback = sub_services.getPlanByNickname(session.get('UserPlan', None)) #change to userPlan 
            plan_callback : Callback = Callback(True, "Plan Found", "basic")
            if not plan_callback.Success: return helpers.redirectWithMessage("admin_solutions", "Could not retrieve Sub Plan for max products check.")

            #count how much products they have in total
            numberOfProducts = 0
            for record in assistant_callback.Data:
                recordsCount = solutions_services.countRecordsByAssistantID(record.ID)
                numberOfProducts += recordsCount

            #see if they have reached the limit of how many solutions they can have
            #if numberOfProducts > plan_callback.Data.MaxProducts:
            if numberOfProducts > 5:
                return helpers.redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP) + ". Solutions after " + name + " have not been added.")

            print("New Record: ", assistantID, id, name, brand, model, price, keywords, discount, url)
            createSolution_callback : Callback = solutions_services.createNew(assistantID, id, name, brand, model, price, keywords, discount, url)
            
            if not createSolution_callback.Success:
                solutions_services.deleteByAssitantID(assistantID, "Could not create one of the new solutions: "+id+" "+name+"." + str(i) + " records have been added after deletion of the old ones.")
                solutions_services.addOldByAssitantID(assistantID, "Could not create on of the new solutions. Solutions have been emptied.", currentSolutions)
                return helpers.redirectWithMessageAndAssistantID("admin_solutions", assistantID, "Could not create one of the new solutions: " + id + " " + name + ". Reverting to old ones")
        return redirect("/admin/assistant/{}/solutions".format(assistantID))

# TODO improve
@solutions_router.route("/admin/assistant/<assistantID>/solutions/file", methods=['POST'])
def admin_products_file_upload(assistantID):
    checkAssistantID(assistantID)
    if request.method == "POST":
        if not session['UserPlan']['Settings']['ImportDatabase']:
            return "You do not have access to uploading database feature."
        msg = ""
        if 'productFile' not in request.files:
            msg = "Error no file given."
        else:
            email = session.get('User')['Email']
            company = get_company(email)
            if company is None or "Error" in company:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                # TODO handle this better
            else:
                assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                       [assistantID, company[0]])
                if assistant is None:
                    abort(status.HTTP_404_NOT_FOUND)
                elif "Error" in assistant:
                    abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    productFile = request.files["productFile"]
                    if productFile.filename == "":
                        msg = "Error no filename"
                    elif productFile and allowed_product_file(productFile.filename):
                        ext = productFile.filename.rsplit('.', 1)[1].lower()
                        if not os.path.isdir(PRODUCT_FILES):
                            os.makedirs(PRODUCT_FILES)
                        filename = secure_filename(productFile.filename)
                        filepath = os.path.join(PRODUCT_FILES, filename)
                        productFile.save(filepath)

                        if str(ext).lower() == "json":
                            json_file = open(PRODUCT_FILES + "/" + productFile.filename, "r")
                            data = load(json_file)
                            print(len(data))
                            print(data[0])
                            for i in range(0, len(data)):
                                id = data[i]["ProductID"]
                                name = data[i]["ProductName"]
                                brand = data[i]["ProductBrand"]
                                model = data[i]["ProductModel"]
                                price = data[i]["ProductPrice"]
                                keywords = data[i]["ProductKeywords"]
                                discount = data[i]["ProductDiscount"]
                                url = data[i]["ProductURL"]
                                insertProduct = insert_into_database_table(
                                    "INSERT INTO Products (AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) VALUES (?,?,?,?,?,?,?,?,?);",
                                    (assistantID, id, name, brand, model, price, keywords, discount, url))
                                # TODO check insertProduct for errors
                        elif str(ext).lower() == "xml":
                            xmldoc = minidom.parse(PRODUCT_FILES + "/" + productFile.filename)
                            productList = xmldoc.getElementsByTagName("product")
                            for product in productList:
                                try:
                                    id = product.getElementsByTagName("ProductID")[0].childNodes[0].data
                                    name = product.getElementsByTagName("ProductName")[0].childNodes[0].data
                                    brand = product.getElementsByTagName("ProductBrand")[0].childNodes[0].data
                                    model = product.getElementsByTagName("ProductModel")[0].childNodes[0].data
                                    price = product.getElementsByTagName("ProductPrice")[0].childNodes[0].data
                                    keywords = product.getElementsByTagName("ProductKeywords")[0].childNodes[0].data
                                    discount = product.getElementsByTagName("ProductDiscount")[0].childNodes[0].data
                                    url = product.getElementsByTagName("ProductURL")[0].childNodes[0].data
                                    insertProduct = insert_into_database_table(
                                        "INSERT INTO Products (AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) VALUES (?,?,?,?,?,?,?,?,?);",
                                        (assistantID, id, name, brand, model, price, keywords, discount, url))
                                    # TODO check insertProduct for errors
                                except IndexError:
                                    msg = "Invalid xml file"
                                    print(msg)
                        else:
                            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

                        os.remove(PRODUCT_FILES + "/" + productFile.filename)
                    else:
                        msg = "Error not allowed that type of file."
                        print(msg)
                return msg


