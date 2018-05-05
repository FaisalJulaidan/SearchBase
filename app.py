import os
import sqlite3
import stripe
from flask_mail import Mail, Message
from werkzeug import secure_filename
from flask import Flask, redirect, request, render_template, jsonify, make_response, send_from_directory, send_file, \
    url_for, escape
from datetime import datetime
import string
from bcrypt import hashpw, gensalt
import json
from xml.dom import minidom

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

COMPUTERDATABASE = APP_ROOT + "/computers.db"
USERDATABASE = APP_ROOT + "/users.db"
QUESTIONDATABASE = APP_ROOT + "/questions.db"
PRODUCTDATABASE = APP_ROOT + "/products.db"
STATISTICSDATABASE = APP_ROOT + "/statistics.db"
# USERPREFERENCES = APP_ROOT + "/userpreferences.db"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PRODUCT_IMAGES = os.path.join(APP_ROOT, 'static/file_uploads/product_images')
PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'

stripe.api_key = secret_key

# stripe_keys = {
#   'secret_key': os.environ['SECRET_KEY'],
#   'publishable_key': os.environ['PUBLISHABLE_KEY']
# }

# stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, static_folder='static')
mail = Mail(app)

app.config['PRODUCT_IMAGES'] = PRODUCT_IMAGES
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG', 'json', 'JSON', 'csv', 'CSV', 'xml', 'xml'])

# salt = generate_random_salt()

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='thesearchbase@gmail.com',
    MAIL_PASSWORD='pilbvnczzdgxkyzy'
)
mail = Mail(app)


# code to ensure user is loged in
@app.before_request
def before_request():
    theurl = str(request.url_rule)
    if ("admin" not in theurl):
        print("Ignore before request for: ", theurl)
        return None
    print("USER EMAIL: " + str(request.cookies.get("UserEmail")))
    if (request.cookies.get("UserEmail") == None):
        print("User not logged in")
        return redirect("/login", code=302)
    print("Before request checking: ", theurl, " ep: ", request.endpoint)
    if (request.cookies.get("UserEmail") == 'None') and request.endpoint != 'login':
        return render_template("userlogin.html", msg="Please log in first!")
    print("Before Request checks out")
    return None


@app.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        # print(hash_password("test"))
        print(update_table(USERDATABASE, "UPDATE Users SET Password=? WHERE ContactEmail=?",
                           [hash_password(u"test"), "test5@test.test"]))
        return render_template("index.html")


@app.route("/productfile", methods=['GET', 'POST'])
def uploadProductFile():
    if request.method == "GET":
        return app.send_static_file("uploadProduct.html")
    else:
        if 'productFile' not in request.files:
            msg = "Error no file given."
        else:
            productFile = request.files["productFile"]
            email = request.cookies.get("UserEmail")
            if productFile.filename == "":
                msg = "Error no filename"
            elif productFile and allowed_file(productFile.filename):
                ext = productFile.filename.rsplit('.', 1)[1].lower()
                if (not os.path.isdir(PRODUCT_FILES)):
                    os.makedirs(PRODUCT_FILES)
                filename = secure_filename(productFile.filename)
                filepath = os.path.join(PRODUCT_FILES, filename)
                productFile.save(filepath)

                if str(ext).lower() == "json":
                    json_file = open(PRODUCT_FILES + "/" + productFile.filename, "r")
                    data = json.load(json_file)
                    for i in range(0, len(data)):
                        msg = productIntoDatabase(email, data[i]["ProductID"], data[i]["ProductName"], data[i]["ProductBrand"], data[i]["ProductModel"], data[i]["ProductPrice"], data[i]["ProductKeywords"], data[i]["ProductDiscount"], data[i]["ProductURL"], data[i]["ProductImage"])
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
                            try:
                                image = product.getElementsByTagName("ProductImage")[0].childNodes[0].data
                                msg = productIntoDatabase(email, id, name, brand, model, price, keywords, discount, url, image)
                            except IndexError:
                                msg = productIntoDatabase(email, id, name, brand, model, price, keywords, discount, url)
                        except IndexError:
                            msg = "Invalid xml file"
                            print(msg)
                else:
                    msg = "File not implemented yet"
                    pass
            else:
                msg = "Error not allowed that type of file."
        return msg

def productIntoDatabase(email, id="", name="", brand="", model="", price="", keywords="",discount="", url="", image=""):
    msg = insert_into_database_table(PRODUCTDATABASE, "INSERT INTO \"" + email + "\" (ProductID, ProductName, ProductBrand, ProductModel, ProductPrice, ProductKeywords, ProductDiscount, ProductURL, ProductImage) VALUES (?,?,?,?,?,?,?,?,?)",
                                     (id, name, brand, model, price, keywords, discount, url, image))
    return msg

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS


class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


@app.route("/<route>", methods=['GET', 'POST'])
def getTemplate(route):
    if request.method == "GET":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users;")
        cns = cur.fetchall()
        for record in cns:
            if route == record[4]:
                conn = sqlite3.connect(QUESTIONDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + record[7] + "\"")
                data = cur.fetchall()
                conn.close()
                date = datetime.now().strftime("%Y-%m")
                conn = sqlite3.connect(STATISTICSDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + route + "\" WHERE Date=?;", [date])
                stats = cur.fetchall()
                if not stats:
                    print(stats)
                    cur.execute("INSERT INTO \"" + route + "\" ('Date', 'AssistantOpened', 'QuestionsAnswered', 'ProductsReturned')\
									VALUES (?,?,?,?)", (date, "1", "0", "0"))
                else:
                    cur.execute("UPDATE \"" + route + "\" SET AssistantOpened = \"" + str(
                        int(stats[0][1]) + 1) + "\" WHERE Date = \"" + date + "\"")
                conn.commit()
                conn.close()
                return render_template("dynamic-template.html", data=data, user=route)
    if request.method == "POST":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users;")
        cns = cur.fetchall()
        for record in cns:
            if route == record[4]:
                conn = sqlite3.connect(PRODUCTDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + record[7] + "\"")
                data = cur.fetchall()
                conn.close()
                keywords = []
                budget = []
                for i in range(1, int(request.form["numberOfKeywords"]) + 1):
                    if "-" in request.form["keyword" + str(i)]:
                        budget = request.form["keyword" + str(i)].split("-")
                    else:
                        keywords.append(request.form["keyword" + str(i)])
                keywordsmatch = []
                i = -1
                for item in data:
                    keywordsmatch.append(0)
                    i += 1
                    datakwords = item[5].split(",")
                    for word in keywords:
                        for dw in datakwords:
                            if (word == dw):
                                keywordsmatch[i] += 1
                exitAtLength = 0
                while (True):
                    for p in range(0, len(keywordsmatch) - 1):
                        if (keywordsmatch[p] < keywordsmatch[p + 1]):
                            keywordsmatch.insert(p, keywordsmatch.pop(p + 1))
                            data.insert(p, data.pop(p + 1))
                            exitAtLength = 0
                            break
                    exitAtLength += 1
                    if (exitAtLength == 5):
                        break
                substract = 0
                for p in range(0, len(keywordsmatch)):
                    if (keywordsmatch[p] == 0):
                        data.pop(p - substract)
                        substract += 1
                DD = Del()
                dl = len(data) - 1
                i = 0
                while (i <= dl):
                    print(dl, " ", i, " ", len(data))
                    item = data[i]
                    itemprice = item[4].translate(DD)
                    print(budget)
                    print(itemprice)
                    print((int(itemprice) < int(budget[0])) or (int(itemprice) > int(budget[1])))
                    if ((int(itemprice) < int(budget[0])) or (int(itemprice) > int(budget[1]))):
                        print(item)
                        print(data.index(item))
                        print(data.pop(data.index(item)))
                        print(data)
                        i -= 1
                        dl -= 1
                    i += 1
                while (len(data) > 9):
                    data.pop()
                if not data:
                    return "We could not find anything that matched your seach criteria. Please try different filter options."
                datastring = ""
                for i in data:
                    for c in i:
                        datastring += str(c) + "|||"
                    datastring = datastring[:-3]
                    datastring += "&&&"
                conn.close()
                date = datetime.now().strftime("%Y-%m")
                conn = sqlite3.connect(STATISTICSDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + route + "\" WHERE Date=?;", [date])
                stats = cur.fetchall()
                print(stats)
                questionsAnswered = request.form["questionsAnswered"]
                if not stats:
                    cur.execute("INSERT INTO \"" + route + "\" ('Date', 'AssistantOpened', 'QuestionsAnswered', 'ProductsReturned')\
									VALUES (?,?,?,?)", (date, "0", questionsAnswered, len(data)))
                else:
                    print(len(data))
                    cur.execute("UPDATE \"" + route + "\" SET ProductsReturned = \"" + str(
                        int(stats[0][3]) + len(data)) + "\" WHERE Date = \"" + date + "\"")
                    cur.execute("UPDATE \"" + route + "\" SET QuestionsAnswered = \"" + str(
                        int(stats[0][2]) + int(questionsAnswered)) + "\" WHERE Date = \"" + date + "\"")
                conn.commit()
                cur.execute("SELECT * FROM \"" + route + "\" WHERE Date=?;", [date])
                stats = cur.fetchall()
                print(stats)
                conn.close()
                return jsonify(datastring)


@app.route("/demo", methods=['GET'])
def demopage():
    if request.method == "GET":
        return render_template("demo.html")


@app.route("/pokajimiuserite6519", methods=['GET'])
def doit():
    if request.method == "GET":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users;")
        data = cur.fetchall()
        return render_template("display-template.html", data=data)


@app.route("/popup", methods=['GET'])
def popup():
    if request.method == "GET":
        return render_template("pop-test.html")


@app.route("/recruitment-demo", methods=['GET'])
def popup2():
    if request.method == "GET":
        return render_template("pop-test2.html")


@app.route("/demo/construction", methods=['GET'])
def demopageconstruction():
    if request.method == "GET":
        return render_template("demo-construction.html")


@app.route("/demo/education", methods=['GET'])
def demopageeducation():
    if request.method == "GET":
        return render_template("demo-education.html")


@app.route("/demo/fashion", methods=['GET'])
def demopagefashion():
    if request.method == "GET":
        return render_template("demo-fashion.html")


@app.route("/demo/industrial", methods=['GET'])
def demopageIndustrial():
    if request.method == "GET":
        return render_template("demo-industrial.html")


@app.route("/demo/pharmaceutical", methods=['GET'])
def demopagepharmaceutical():
    if request.method == "GET":
        return render_template("demo-pharmaceutical.html")


@app.route("/demo/technology", methods=['GET'])
def demopagetechnology():
    if request.method == "GET":
        return render_template("demo-technology.html")


@app.route("/about", methods=['GET'])
def aboutpage():
    if request.method == "GET":
        return render_template("about.html")


@app.route("/features", methods=['GET'])
def featurespage():
    if request.method == "GET":
        return render_template("features.html")


@app.route("/pricing", methods=['GET'])
def pricingpage():
    if request.method == "GET":
        return render_template("Pricing.html")


@app.route("/contact", methods=['GET'])
def contactpage():
    if request.method == "GET":
        return render_template("contact.html")


email = ""


@app.route("/login", methods=['GET', 'POST'])
def loginpage():
    if request.method == "GET":
        return render_template("Login.html")
    elif request.method == 'POST':
        email = request.form.get("email", default="Error")
        password = request.form.get("pass", default="Error")

        data = select_from_database_table(USERDATABASE, "SELECT * FROM Users WHERE ContactEmail=?", [email])
        if data is not None:
            datapass = data[10]
            print(datapass)
            if hash_password(password, datapass) == datapass:
                user = data[1] + " " + data[3]
                return render_template("admin-main.html", msg=email, user=user)
            else:
                # else denying the login
                return render_template('Login.html', data="User name and password does not match!")
        else:
            return render_template('Login.html', data="User doesn't exist!")


def select_from_database_table(database, sql_statement, array_of_terms=None, all=False):
    data = "Error"
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        if (all):
            data = cur.fetchall()
        else:
            data = cur.fetchone()
    except sqlite3.ProgrammingError as e:
        print("Error in select operation," + str(e))
    except sqlite3.OperationalError as e:
        print(str(e))
    finally:
        conn.close()
        return data


def insert_into_database_table(database, sql_statement, tuple_of_terms):
    msg = "Error"
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, tuple_of_terms)
        conn.commit()
        msg = "Record successfully added."
    except sqlite3.ProgrammingError as e:
        conn.rollback()
        msg = "Error in insert operation: " + str(e)
    except Exception as e:
        msg = str(e)
    finally:
        conn.close()
        print(msg)
        return msg


def update_table(database, sql_statement, array_of_terms):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        conn.commit()
        msg = "Record successfully updated."
    except sqlite3.ProgrammingError as e:
        conn.rollback()
        msg = "Error in update operation" + str(e)
        print(msg)
    finally:
        conn.close()
        return msg


def delete_from_table(database, sql_statement, array_of_terms):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms);
        conn.commit()
        if cur.rowcount == 1:
            msg = "Record successfully deleted."
        else:
            msg = "Record not deleted may not exist"
    except sqlite3.ProgrammingError as e:
        conn.rollback()
        msg = "Error in delete operation" + str(e)
    finally:
        conn.close()
        return msg


@app.route("/signupform", methods=['GET', 'POST'])
def signpage():
    if request.method == "GET":
        return render_template("Signup.html")
    if request.method == 'POST':

        # collecting the text data from the front end
        userTitle = request.form.get("title", default="Error")
        userFirstname = request.form.get("firstname", default="Error")
        userSecondname = request.form.get("surname", default="Error")
        userCompanyName = request.form.get("companyName", default="Error")
        userPositionCompany = request.form.get("userPosition", default="Error")
        userCompanyAddress = request.form.get("companyAddress", default="Error")
        userEmail = request.form.get("contactEmail", default="Error")
        userContactNumber = request.form.get("contactNumber", default="Error")
        userCountry = request.form.get("country", default="Error")
        userPassword = request.form.get("pass", default="Error")
        pass_hashed = hash_password(userPassword)

        # injecting the text data into the database
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT ContactEmail FROM Users WHERE ContactEmail=?", [userEmail])
        demail = cur.fetchall()
        if demail:
            return render_template("Signup.html", msg="Email already exists")
        cur.execute("SELECT CompanyName FROM Users WHERE ContactEmail=?", [userEmail])
        demail = cur.fetchall()
        if demail:
            return render_template("Signup.html", msg="Company already exists")
        cur.execute("INSERT INTO Users ('Title', 'Firstname', 'Surname', 'CompanyName', 'UserPosition', 'CompanyAddress', 'ContactEmail', 'ContactNumber', 'Country', 'Password')\
						VALUES (?,?,?,?,?,?,?,?,?,?)", (
            userTitle, userFirstname, userSecondname, userCompanyName, userPositionCompany, userCompanyAddress,
            userEmail,
            userContactNumber, userCountry, pass_hashed))
        conn.commit()
        print("User details added!")
        conn.close()

        # creating user's tables in databases
        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE \"" + userEmail + "\" ( Question text NOT NULL, 'Answer1' text, 'Answer2' text, 'Answer3' text, 'Answer4' text, 'Answer5' text, 'Answer6' text, 'Answer7' text, 'Answer8' text, 'Answer9' text, 'Answer10' text, 'Answer11' text, 'Answer12' text)")
        conn.commit()
        conn.close()
        conn = sqlite3.connect(PRODUCTDATABASE)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE \"" + userEmail + "\" ( ProductID text, ProductName text, ProductBrand text, ProductModel text, ProductPrice text ProductFeatures text, ProductKeywords text, ProductDiscount text, ProductURL text, ProductImage text)")
        conn.commit()
        conn.close()
        conn = sqlite3.connect(STATISTICSDATABASE)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE \"" + userCompanyName + "\" ( `Date` TEXT, `AssistantOpened` TEXT, `QuestionsAnswered` TEXT, `ProductsReturned` TEXT )")
        conn.commit()
        conn.close()
        # conn = sqlite3.connect(USERPREFERENCES)
        # cur = conn.cursor()
        # cur.execute("CREATE TABLE \""+userEmail+"\" ( `Date` TEXT, `AssistantOpened` TEXT, `QuestionsAnswered` TEXT, `ProductsReturned` TEXT )")
        # cur.execute("INSERT INTO \""+userEmail+"\" ('PricingQuestion') VALUES (?)", ("0"))
        # conn.commit()
        # conn.close()

        # sending registration confirmation email to the user.
        msg = Message("Thank you for registering, " + userFirstname,
                      sender="thesearchbase@gmail.com",
                      recipients=[userEmail])
        msg.body = "We appriciate you registering with TheSaerchBase. A whole new world of possibilities is ahead of you."
        mail.send(msg)

        # sending the regstration confirmation email to us
        msg = Message("A new user has signed up!",
                      sender="thesearchbase@gmail.com",
                      recipients=["thesearchbase@gmail.com"])
        msg.body = "Title: " + userTitle + "Name: " + userFirstname + userSecondname + "Email: " + userEmail + "Number: " + userContactNumber
        mail.send(msg)

        return render_template("Login.html")


def hash_password(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


# Admin pages

@app.route("/admin/homepage", methods=['GET'])
def adminHomePage():
    if request.method == "GET":
        return render_template("admin-main.html")


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_EXTENSIONS


@app.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM Users WHERE ContactEmail = \"" + user_mail + "\"")
        data = cur.fetchall()
        conn.close()
        return render_template("admin-profile.html", data=data)
    if request.method == "POST":
        names = request.form.get("names");
        address = request.form.get("address");
        compN = request.form.get("compN");
        cID = request.form.get("cID");
        names = names.split(" ")
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        # cur.execute("UPDATE table SET ProductsReturned = new value WHERE Date = \""+date+"\"")
        cur.execute("UPDATE Users SET Firstname = \"" + names[0] + "\" WHERE CompanyID = \"" + cID + "\"")
        cur.execute("UPDATE Users SET Surname = \"" + names[1] + "\" WHERE CompanyID = \"" + cID + "\"")
        cur.execute("UPDATE Users SET CompanyAddress = \"" + address + "\" WHERE CompanyID = \"" + cID + "\"")
        cur.execute("UPDATE Users SET CompanyName = \"" + compN + "\" WHERE CompanyID = \"" + cID + "\"")
        conn.commit()
        conn.close()
        return redirect("/admin/profile", code=302)


@app.route("/admin/Questions", methods=['GET', 'POST'])
def adminAddQuestion():
    if request.method == "GET":
        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        mes = cur.fetchall()
        conn.close()
        return render_template("admin-form-add-question.html", data=mes)
    if request.method == "POST":
        questions = []
        for i in range(1, 11):
            if (request.form.get("question" + str(i)) != None):
                questions.append(request.form.get("question" + str(i)))

        # conn = sqlite3.connect(USERPREFERENCES)
        # cur = conn.cursor()
        # cur.execute("UPDATE \""+user_mail+"\" SET PricingQuestion = " + request.form.get("pricing-question"))
        # conn.commit()
        # conn.close()

        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        print(questions)
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        tempData = cur.fetchall()
        cur.execute("CREATE TABLE IF NOT EXISTS \'" + user_mail + "\' (\
		Question text NOT NULL, 'Answer1' text, 'Answer2' text, 'Answer3' text, 'Answer4' text,\
		 'Answer5' text, 'Answer6' text, 'Answer7' text, 'Answer8' text, 'Answer9' text, 'Answer10' text,\
		  'Answer11' text, 'Answer12' text)")
        conn.commit()
        i = -1
        print(tempData)
        if (len(questions) + 1 < len(tempData) + 1):
            for b in range(len(questions) + 1, len(tempData) + 1):
                print("DELETING: ", tempData[i][0])
                cur.execute("DELETE FROM \"" + user_mail + "\" WHERE Question = \"" + tempData[i][0] + "\"")
        for q in questions:
            i += 1
            try:
                if (tempData[i][0] != None):
                    print("UPDATING: ", tempData[i][0], " TO ", q)
                    cur.execute(
                        "UPDATE \"" + user_mail + "\" SET Question = \"" + q + "\" WHERE Question = \"" + tempData[i][
                            0] + "\"")
            except:
                print("INSERTING NEW: ", q)
                cur.execute("INSERT INTO \'" + user_mail + "\'('Question') VALUES (?)", (q,))
        conn.commit()
        conn.close()
        return redirect("/admin/Questions", code=302)


@app.route("/admin/Answers", methods=['GET', 'POST'])
def adminAnswers():
    if request.method == "GET":
        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        mes = cur.fetchall()
        conn.close()
        return render_template("admin-form-add-answer.html", msg=mes)
    if request.method == "POST":
        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        answers = []
        selected_question = request.form.get("question")
        user_mail = request.cookies.get("UserEmail")
        for i in range(1, 13):
            if (request.form.get("pname" + str(i)) != None):
                try:
                    if (request.files['file' + str(i)].filename == ""):
                        print('no file given')
                        if (request.form.get("delPic" + str(i)) != "yes"):
                            cur.execute("SELECT Answer" + str(
                                i) + " FROM \"" + user_mail + "\" WHERE Question=\"" + selected_question + "\"")
                            data = cur.fetchall()
                            link = data[0][0].split(";")[2]
                            answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                                "keywords" + str(i)) + ";" + link)
                        else:
                            answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                                "keywords" + str(i)) + ";../static/img/core-img/android-icon-72x72.png")
                    else:
                        file = request.files['file' + str(i)]
                        if file.filename == '':
                            print('No file name')
                        elif file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            filePath = os.path.join(app.config['PRODUCT_IMAGES'], filename)
                        file.save(filePath)
                        filePath = filePath.split("TheSearchBase")[len(filePath.split("TheSearchBase")) - 1]
                        # temporay string
                        tempList = list(filePath)
                        tempString = ""
                        for char in tempList:
                            if (char == "\\"):
                                char = "/"
                            tempString += char
                        filePath = tempString
                        # tempString = filePath.split("\\")
                        # filePath = tempString[0] + "/" + tempString[1]
                        answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                            "keywords" + str(i)) + ";.." + filePath)
                except:
                    if (request.form.get("delPic" + str(i)) != "yes"):
                        cur.execute("SELECT Answer" + str(
                            i) + " FROM \"" + user_mail + "\" WHERE Question=\"" + selected_question + "\"")
                        data = cur.fetchall()
                        print(data)
                        if data == [(None,)]:
                            answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                                "keywords" + str(i)) + ";../static/img/core-img/android-icon-72x72.png")
                        else:
                            link = data[0][0].split(";")[2]
                            answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                                "keywords" + str(i)) + ";" + link)
                    else:
                        answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                            "keywords" + str(i)) + ";../static/img/core-img/android-icon-72x72.png")
        c = 0
        for a in answers:
            c += 1
            cur.execute("UPDATE \"" + user_mail + "\" SET Answer" + str(
                c) + " = \"" + a + "\" WHERE Question = \"" + selected_question + "\"")
            conn.commit()
        for b in range(c + 1, 13):
            cur.execute("UPDATE \"" + user_mail + "\" SET Answer" + str(
                b) + " = \"\" WHERE Question = \"" + selected_question + "\"")
            conn.commit()
        conn.close()
        return redirect("/admin/Answers", code=302)


@app.route("/admin/Products", methods=['GET', 'POST'])
def adminAddProduct():
    if request.method == "GET":
        conn = sqlite3.connect(PRODUCTDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        mes = cur.fetchall()
        conn.close()
        return render_template("admin-form-add-product.html", data=mes)
    if request.method == 'POST':
        filePath = 'no file upload so far'
        msg = ''
        if request.method == 'POST':
            i = 0;
            product_id = []
            name = []
            brand = []
            model = []
            price = []
            keywords = []
            discount = []
            url = []
            file_path = []
            while (True):
                i += 1
                if (request.form.get("product_ID" + str(i), default="Error") == "Error"):
                    break
                product_id.append(request.form.get("product_ID" + str(i), default="Error"))
                name.append(request.form.get("product_Name" + str(i), default="Error"))
                brand.append(request.form.get("product_Brand" + str(i), default="Error"))
                model.append(request.form.get("product_Model" + str(i), default="Error"))
                price.append(request.form.get("product_Price" + str(i), default="Error"))
                keywords.append(request.form.get("product_Keywords" + str(i), default="Error"))
                discount.append(request.form.get("product_Discount" + str(i), default="Error"))
                url.append(request.form.get("product_URL" + str(i), default="Error"))
                try:
                    if (request.files['product_image' + str(i)].filename == ""):
                        print('no file given')
                    else:
                        file = request.files['product_image' + str(i)]
                        if file.filename == '':
                            print('No file name')
                        elif file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            filePath = os.path.join(app.config['PRODUCT_IMAGES'], filename)
                        file.save(filePath)
                        filePath = filePath.split("TheSearchBase")[len(filePath.split("TheSearchBase")) - 1]
                        tempList = list(filePath)
                        tempString = ""
                        for char in tempList:
                            if (char == "\\"):
                                char = "/"
                            tempString += char
                        filePath = tempString
                        filePath = ".." + filePath
                except:
                    conn = sqlite3.connect(PRODUCTDATABASE)
                    cur = conn.cursor()
                    user_mail = request.cookies.get("UserEmail")
                    cur.execute("SELECT * FROM \"" + user_mail + "\" WHERE ProductID=\"" + product_id[
                        len(product_id) - 1] + "\"")
                    mes = cur.fetchall()
                    if mes == []:
                        filePath = "../static/img/core-img/android-icon-72x72.png"
                    else:
                        filePath = mes[0][8]
                    conn.close()
                file_path.append(filePath)
            try:
                conn = sqlite3.connect(PRODUCTDATABASE)
                cur = conn.cursor()
                user_mail = request.cookies.get("UserEmail")
                cur.execute("CREATE TABLE IF NOT EXISTS \'" + user_mail + "\' (\
				ProductID text, ProductName text, ProductBrand text, ProductModel text, ProductPrice text\
				ProductKeywords text, ProductDiscount text, ProductURL text, ProductImage text)")
                cur.execute("DELETE FROM \'" + user_mail + "\'")
                for q in range(0, i - 1):
                    # injecting database with sql with product
                    cur.execute("INSERT INTO \'" + user_mail + "\'('ProductID', 'ProductName', 'ProductBrand', 'ProductModel', \
					'ProductPrice', 'ProductKeywords', 'ProductDiscount', 'ProductURL', 'ProductImage') \
					VALUES (?,?,?,?,?,?,?,?,?)", (
                        product_id[q], name[q], brand[q], model[q], price[q], keywords[q], discount[q], url[q],
                        file_path[q],))
                    conn.commit()
            except:
                print("Error in editing the database")
                conn.rollback()
                conn.close()
            return redirect("/admin/Products", code=302)


@app.route("/admin/displayQuestions", methods=['GET'])
def adminDisplayQuestions():
    if request.method == "GET":
        return render_template("admin-table-questions.html")


@app.route("/admin/displayAnswers", methods=['GET'])
def adminDisplayAnswers():
    if request.method == "GET":
        return render_template("admin-table-answers.html")


@app.route("/admin/connect")
def connectionCode():
    return render_template("admin-connect.html")


@app.route("/admin/pricing")
def adminPricing():
    return render_template("admin-pricing-tables.html", pub_key=pub_key)


@app.route('/admin/thanks')
def thanks():
    return render_template('admin-thank-you.html')


@app.route("/admin/pay", methods=['GET', 'POST'])
def chargeUser():
    if request.method == 'GET':
        return render_template("admin-pay.html")


@app.route("/admin/profile", methods=['GET'])
def adminProfile():
    if request.method == "GET":
        return render_template("admin-profile.html")


@app.route("/admin/analytics", methods=['GET'])
def adminAnalytics():
    if request.method == "GET":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM Users WHERE ContactEmail=\"" + user_mail + "\"")
        mes = cur.fetchall()
        companyName = mes[0][4]
        conn.close()
        conn = sqlite3.connect(STATISTICSDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM \"" + companyName + "\"")
        stats = cur.fetchall()
        conn.close()
        return render_template("admin-analytics.html", data=stats)


@app.route("/admin/supportGeneral", methods=['GET'])
def adminGeneralSupport():
    if request.method == "GET":
        return render_template("admin-general-support.html")


@app.route("/admin/supportDocs", methods=['GET'])
def adminDocsSupport():
    if request.method == "GET":
        return render_template("admin-docs.html")


@app.route("/admin/supportSetup", methods=['GET'])
def adminSetupSupport():
    if request.method == "GET":
        return render_template("admin-getting-setup.html")


@app.route("/admin/supportIntergartion", methods=['GET'])
def adminIntergrationSupport():
    if request.method == "GET":
        return render_template("admin-intergation-tutorial.html")


@app.route("/admin/supportBilling", methods=['GET'])
def adminBillingSupport():
    if request.method == "GET":
        return render_template("admin-billing-support.html")


@app.route("/send/mail", methods=['GET', 'POST'])
def sendEmail():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        mailFirstname = request.form.get("sendingName", default="Error")
        mailUserEmail = request.form.get("sendingEmail", default="Error")
        mailUserMessage = request.form.get("sendMessage", default="Error")

        msg = Message(mailFirstname + " from " + mailUserEmail + " has sent you a message.",
                      sender=mailUserEmail,
                      recipients=["thesearchbase@gmail.com"])
        msg.body = mailFirstname + " said: " + mailUserMessage + " their email is: " + mailUserEmail
        mail.send(msg)
        return render_template("index.html")


@app.route("/send/mailtop", methods=['GET', 'POST'])
def sendMarketingEmail():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        userEmail = request.form.get("user_email", default="Error")
        msg = Message(userEmail + " Has sent you mail!",
                      sender=userEmail,
                      recipients=["thesearchbase@gmail.com"])
        msg.body = userEmail + " Has registerd their Interest for your product"
        mail.send(msg)
        return render_template("index.html")


# Route for the computer search

@app.route("/GetComputers", methods=['POST'])
def getcomputers():
    if request.method == 'POST':
        computerUse = request.form["compuse"]
        minBudget = request.form["minbudget"]
        maxBudget = request.form["maxbudget"]
        portable = request.form["portable"]
        battery = request.form["battery"]
        keyfeatures = request.form["keyfeatures"]
        conn = sqlite3.connect(COMPUTERDATABASE)
        cur = conn.cursor()
        print("Looking for: ", computerUse, " ", minBudget, " ", maxBudget, " ", portable, " ", battery, " ",
              keyfeatures)
        try:
            if (portable == "null"):
                print("Search without portable setting")
                cur.execute("SELECT * FROM computers WHERE (Use1=? OR Use2=?) \
                AND Price>=? AND Price<=? AND BatteryLife>=? \
                ", [computerUse, computerUse, minBudget, maxBudget, battery])
            else:
                print("Search for ", portable)
                cur.execute("SELECT * FROM computers WHERE (Use1=? OR Use2=?) \
                AND Price>=? AND Price<=? AND Type=? AND BatteryLife>=? \
                ", [computerUse, computerUse, minBudget, maxBudget, portable, battery])
            data = cur.fetchall()
        except:
            print("ERROR IN RETRIEVING COMPUTERS")
        finally:
            conn.close()
        # filter for keyfeatures
        if (keyfeatures != ""):
            print("before keyfeatures: ", data)
            print(type(keyfeatures))
            if (keyfeatures is not list):
                print("Convert keyfeatures to list")
                keyfeatures = [keyfeatures]
            print(type(keyfeatures))
            print(keyfeatures)
            for t in keyfeatures:
                for c in data:
                    print(len(data))
                    print("Checking :", c)
                    init = False
                    for i in c:
                        if i == t:
                            init = True
                    if init == False:
                        data.remove(c)
                        print(t, " ", c, "removed")
                for c in data:
                    print(len(data))
                    print("Checking :", c)
                    init = False
                    for i in c:
                        if i == t:
                            init = True
                    if init == False:
                        data.remove(c)
                        print(t, " ", c, "removed")
            print("after keyfeatures: ", data)
        if not data:
            return "We could not find Computers that matched your seach. Please try different filter options."
        datastring = ""
        for i in data:
            for c in i:
                datastring += str(c) + "|"
            datastring = datastring[:-1]
            datastring += ","
        print(datastring)
        return jsonify(datastring)


# Sitemap route

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# Terms and conditions page route
@app.route("/termsandconditions", methods=['GET'])
def termsPage():
    if request.method == "GET":
        return render_template("terms.html")


# Terms and conditions page route
@app.route("/privacy", methods=['GET'])
def PrivacyPage():
    if request.method == "GET":
        return render_template("privacy-policy.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
