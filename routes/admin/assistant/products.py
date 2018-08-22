from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services
from models import Callback
from utilties import helpers

products_router: Blueprint = Blueprint('products_router', __name__, template_folder="../../templates")

@products_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
def admin_solutions(assistantID):
# Evgeniy make the get request running :)
    if request.method == "GET":

        solutions_callback: Callback = solutions_services.getByAssistantID(assistantID)

        if not solutions_callback.Success: solutions_callback.Data = []

        solutions = helpers.getListFromSQLAlchemyList(solutions_callback.Data)

        return admin_services.render("admin/solutions.html", data=solutions, id=assistantID)

    elif request.method == 'POST':
        companyID = session.get('companyID', None)
        if not companyID: return helpers.redirectWithMessage("admin_solutions", "Could not retrive company's ID")

        #get all company assistants (needed for totalproducts check)
        assistant_callback : Callback = assistant_services.getAll(companyID)
        if not assistant_callback.Success: return helpers.redirectWithMessage("admin_solutions", assistant_callback.Message)

        #get all previous solutions
        solutions_callback: Callback = solutions_services.getByAssistantID(assistantID)
        currentSolutions = solutions_callback.Data
        if not solutions_callback.Success: solutions_callback.Data = []
        #currentProducts -> solutions_callback

        #delete old solutions so the new one can be put it
        deleteOldData : bool = solutions_services.deleteAllByAssistantID(assistantID)
        if not deleteOldData: return helpers.redirectWithMessage("admin_solutions", "Could not delete old data in order to put the new one.")

        nop = 1
        for key in request.form:
            print("key: ", key)
            if "product_ID" in key:
                nop += 1

        for i in range(1, nop):
            # TODO add more info to these error messages
            id = request.form.get("product_ID" + str(i), default="Error")
            if id is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product ID")
            name = request.form.get("product_Name" + str(i), default="Error")
            if name is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product name")
            brand = request.form.get("product_Brand" + str(i), default="Error")
            if brand is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product brand")
            model = request.form.get("product_Model" + str(i), default="Error")
            if model is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product model")
            price = request.form.get("product_Price" + str(i), default="Error")
            if price is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product price")
            keywords = request.form.get("product_Keywords" + str(i), default="Error")
            if keywords is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product keywords")
            discount = request.form.get("product_Discount" + str(i), default="Error")
            if discount is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product discount")
            url = request.form.get("product_URL" + str(i), default="Error")
            if url is "Error":
                abort(status.HTTP_400_BAD_REQUEST, "Error with product url")
            if "http" not in url:
                url = "http://" + url

            #see if they have reached the limit
            numberOfProducts = 0
            maxNOP = session['UserPlan']['Settings']['MaxProducts']
            for record in assistant_callback.Data:
                numberOfProducts += count_db("Products", " WHERE AssistantID=?", [record["ID"],])
            if numberOfProducts > maxNOP:
                return redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP)+ ". Solutions after " + name + " have not been added.")

            insertProduct = insert_into_database_table(
                "INSERT INTO Products (AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) "
                "VALUES (?,?,?,?,?,?,?,?,?);", (
                    assistantID, id, name, brand, model, price,
                    keywords, discount, url))
            # TODO try to recover by re-adding old data if insertProduct fails
        return redirect("/admin/assistant/{}/solutions".format(assistantID))

# TODO improve
@products_router.route("/admin/assistant/<assistantID>/solutions/file", methods=['POST'])
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


