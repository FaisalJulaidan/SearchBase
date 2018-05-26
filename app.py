#!/usr/bin/python3
import os
import sqlite3
import stripe
from flask_mail import Mail, Message
from werkzeug import secure_filename
from flask import Flask, redirect, request, render_template, jsonify, send_from_directory, abort, escape
from flask_api import status
from datetime import datetime
import string
from bcrypt import hashpw, gensalt
import json
from xml.dom import minidom

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

COMPUTERDATABASE = APP_ROOT + "/computers.db"
USERINPUTDATABASE = APP_ROOT + "/userInput.db"

DATABASE = APP_ROOT + "/database.db"

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

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='thesearchbase@gmail.com',
    MAIL_PASSWORD='pilbvnczzdgxkyzy'
)


# code to ensure user is logged in
@app.before_request
def before_request():
    theurl = str(request.url_rule)
    if "admin" not in theurl:
        print("Ignore before request for: ", theurl)
        return None
    email = request.cookies.get("UserEmail")
    print("USER EMAIL: " + str(email))
    if email is None:
        print("User not logged in")
        return redirect("/login")
    print("Before request checking: ", theurl, " ep: ", request.endpoint)
    if email == 'None' and request.endpoint != 'login':
        return render_template("login.html", msg="Please log in first!")
    print("Before Request checks out")
    return None


def select_from_database_table(database, sql_statement, array_of_terms=None, all=False):
    data = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        if (all):
            data = cur.fetchall()
        else:
            data = cur.fetchone()
    except sqlite3.ProgrammingError as e:
        print("Error in select statement," + str(e))
    except sqlite3.OperationalError as e:
        print("Error in select operation," + str(e))
    finally:
        if (conn is not None):
            conn.close()
        return data


def insert_into_database_table(database, sql_statement, tuple_of_terms):
    msg = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, tuple_of_terms)
        conn.commit()
        msg = "Record successfully added."
    except sqlite3.ProgrammingError as e:
        msg = "Error in insert statement: " + str(e)
    except sqlite3.OperationalError as e:
        msg = "Error in insert operation: " + str(e)
    except Exception as e:
        msg = "Error in insert operation: " + str(e)
    finally:
        if conn is not None:
            conn.rollback()
            conn.close()
        print(msg)
        return msg


def update_table(database, sql_statement, array_of_terms):
    msg = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        conn.commit()
        msg = "Record successfully updated."
    except sqlite3.ProgrammingError as e:
        msg = "Error in update statement" + str(e)
    except sqlite3.OperationalError as e:
        msg = "Error in update operation" + str(e)
    finally:
        if conn is not None:
            conn.rollback()
            conn.close()
        print(msg)
        return msg


def delete_from_table(database, sql_statement, array_of_terms):
    msg = "Error"
    conn = None
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
        msg = "Error in delete statement" + str(e)
    except sqlite3.OperationalError as e:
        msg = "Error in delete operation" + str(e)
    finally:
        if conn is not None:
            conn.rollback()
            conn.close()
        print(msg)
        return msg


def hash_password(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


# TODO jackassify it
@app.route("/demo/<route>", methods=['GET'])
def dynamic_popup(route):
    if request.method == "GET":
        url = "http://www.example.com/"
        company = select_from_database_table(DATABASE, "SELECT * FROM Company WHERE Name=?", [escape(route)])
        if (company is not None and "Debug" in company[4]):
            url = company[3]
            if "http" not in url:
                url = "http://" + url
        return render_template("dynamic-popup.html", msg=route, url=url)


# drop down routes.
@app.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/features", methods=['GET'])
def features():
    if request.method == "GET":
        return render_template("features.html")


@app.route("/data/retrieval", methods=['GET'])
def data_retrieval():
    if request.method == "GET":
        return render_template("retrieval.html")


@app.route("/data/collection", methods=['GET'])
def data_collection():
    if request.method == "GET":
        return render_template("collection.html")


@app.route("/pricing", methods=['GET'])
def pricing():
    if request.method == "GET":
        return render_template("pricing.html")


@app.route("/about", methods=['GET'])
def about():
    if request.method == "GET":
        return render_template("about.html")


@app.route("/contact", methods=['GET'])
def contactpage():
    if request.method == "GET":
        return render_template("contact.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email", default="Error")
        password_to_check = request.form.get("password", default="Error")
        if email == "Error" or password_to_check == "Error":
            print("Invalid request: Email or password not received!")
            return render_template('login.html', data="Email or password not received!"), status.HTTP_400_BAD_REQUEST
        else:
            data = select_from_database_table(DATABASE, "SELECT * FROM Users WHERE Email=?", [email])
            if data is not None:
                password = data[6]
                print(password_to_check)
                if hash_password(password_to_check, password) == password:
                    user = data[2] + " " + data[3]
                    return render_template("admin/admin-main.html", msg=email, user=user)
                else:
                    return render_template('login.html', data="User name and password does not match!")
            else:
                return render_template('login.html', data="User doesn't exist!")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html", debug=app.debug)
    elif request.method == "POST":
        print(request.form)
        companyName = request.form.get("companyName", default="Error")
        companySize = request.form.get("companySize")
        subscription = request.form.get("subscription", default="Error")
        websiteURL = request.form.get("websiteURL", default="Error")

        if companyName == "Error" or subscription == "Error" or websiteURL == "Error":
            print("Invalid request")
            render_template("signup.html", msg="Invalid request", debug=app.debug), status.HTTP_400_BAD_REQUEST

        insertCompanyResponse = insert_into_database_table(DATABASE,
                                                           "INSERT INTO Company ('Name', 'Size', 'URL', 'Subscription') VALUES (?,?,?,?)",
                                                           (companyName, companySize, websiteURL, subscription))
        if "added" not in insertCompanyResponse:
            if "UNIQUE constraint" in insertCompanyResponse:
                return render_template("signup.html", msg=companyName + " already has an account.", debug=app.debug)
            else:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            companyID = select_from_database_table(DATABASE, "SELECT * FROM Company WHERE Name=?", [companyName])[0]
            fullname = request.form.get("fullname", default="Error")
            accessLevel = "Admin"
            email = request.form.get("email", default="Error")
            password = request.form.get("password", default="Error")
            if fullname == "Error" or accessLevel == "Error" or email == "Error" or password == "Error":
                print("Invalid request")
                render_template("signup.html", msg="Invalid request", debug=app.debug), status.HTTP_400_BAD_REQUEST
            else:
                firstname = fullname.split(" ")[0]
                surname = fullname.split(" ")[1]
                hashed_password = hash_password(password)

                insertUserResponse = insert_into_database_table(DATABASE,
                                                                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password') VALUES (?,?,?,?,?,?)",
                                                                (companyID, firstname, surname, accessLevel, email,
                                                                 hashed_password))
                if "added" not in insertUserResponse:
                    if "UNIQUE constraint" in insertUserResponse:
                        delete_from_table(DATABASE, "DELETE FROM Company WHERE Name=?", [companyName])
                        return render_template("signup.html", msg=email + " already in use.", debug=app.debug)
                    else:
                        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    if not app.debug:
                        # sending registration confirmation email to the user.
                        msg = Message("Thank you for registering, {} {}".format(firstname, surname),
                                      sender="thesearchbase@gmail.com",
                                      recipients=[email])
                        msg.body = "We appreciate you registering with TheSearchBase. A whole new world of possibilities is ahead of you."
                        mail.send(msg)

                        # sending the registration confirmation email to us
                        msg = Message("A new company has signed up!",
                                      sender="thesearchbase@gmail.com",
                                      recipients=["thesearchbase@gmail.com"])
                        msg.body = "Company name: {} has signed up the admin's details are. Name: {}, Email: {}, ".format(
                            companyName, fullname, email)
                        mail.send(msg)
                    return redirect("/login")


# Admin pages
@app.route("/admin/homepage", methods=['GET'])
def admin_home():
    if request.method == "GET":
        return render_template("admin/admin-main.html")


@app.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        user = select_from_database_table(DATABASE, "SELECT * FROM Users WHERE Email=?", [email])
        # TODO check database output for errors
        companyName = select_from_database_table(DATABASE, "SELECT * FROM Company WHERE ID=?", [user[1]])
        return render_template("admin/admin-profile.html", user=user, companyName=companyName[1])
    elif request.method == "POST":
        abort(status.HTTP_501_NOT_IMPLEMENTED)


def get_assistants(email):
    user = select_from_database_table(DATABASE, "SELECT * FROM Users WHERE Email=?", [email])
    # TODO check user for errors
    company = select_from_database_table(DATABASE, "SELECT * FROM Company WHERE ID=?", [user[1]])
    # TODO check company for errors
    assistants = select_from_database_table(DATABASE, "SELECT * FROM Assistant WHERE CompanyID=?", [company[0]],
                                            True)
    # TODO check assistants for errors
    return assistants


@app.route("/admin/questions", methods=['GET', 'POST'])
def admin_questions():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        # TODO check assistants for errors
        assistantIndex = 0  # TODO change this
        questionsTuple = select_from_database_table(DATABASE, "SELECT * FROM Questions WHERE AssistantID=?",
                                                    [assistants[assistantIndex][0]], True)
        # TODO check questionstuple for errors
        questions = []
        for i in range(0, len(questionsTuple)):
            questions.append(questionsTuple[i][2])

        allAnswers = {}
        for i in range(0, len(questions)):
            answersTuple = select_from_database_table(DATABASE, "SELECT * FROM Answers WHERE QuestionID=?",
                                                      [questionsTuple[i][0]], True)
            # TODO Check answerstuple for errors
            answers = []
            for j in range(0, len(answersTuple)):
                answers.append(answersTuple[j][2] + ";" + answersTuple[j][3])

            allAnswers[
                questions[i]] = answers  # dictionary, Key: index of question in question array, value: array of answers

        number = 0
        maxNumber = len(questions)
        while (number < maxNumber):
            if (len(questions) > 0):
                print(number, " ", maxNumber)
                try:
                    print(questions[number])
                except:
                    break
                if (questions[number].split(";")[1] == "userInfoRetrieval"):
                    questions.remove(questions[number])
                    allAnswers[questions[number]] = None
                    number -= 1
                    maxNumber -= 1
                    if number < 0:
                        number = 0
                else:
                    number += 1
            else:
                break

        questionsAndAnswers = []
        for i in range(0, len(questions)):
            question = []
            question.append(questions[i])
            merge = tuple(question)
            answers = allAnswers[questions[i]]
            for j in range(0, len(answers)):
                answer = []
                answer.append(answers[j])
                merge = merge + tuple(answer)
            questionsAndAnswers.append(merge)
        return render_template("admin/admin-form-add-question.html", data=questionsAndAnswers)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        assistantIndex = 0  # TODO change this
        currentQuestions = select_from_database_table(DATABASE, "SELECT * FROM Questions WHERE AssistantID=?",
                                                      [assistants[assistantIndex][0]], True)
        # TODO check currentQuestions for errors

        updatedQuestions = []
        noq = request.form.get("noq-hidden", default="Error")
        for i in range(1, (noq + 1)):
            question = request.form.get("question" + str(i), default="Error")
            if question != "Error":
                updatedQuestions.append(question)
            else:
                return render_template("admin/admin-form-add-question.html", data=currentQuestions), status.HTTP_400_BAD_REQUEST


        # TODO implement this, need to work out how to store the retrieved answers
        abort(status.HTTP_501_NOT_IMPLEMENTED)


@app.route("/admin/answers", methods=['GET', 'POST'])
def admin_answers():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        # TODO check assistants for errors
        assistantIndex = 0  # TODO change this
        questionsTuple = select_from_database_table(DATABASE, "SELECT * FROM Questions WHERE AssistantID=?",
                                               [assistants[assistantIndex][0]], True)
        # TODO check questionstuple for errors
        questions = []
        for i in range (0, len(questionsTuple)):
            questions.append(questionsTuple[i][2])

        allAnswers = {}
        for i in range(0, len(questions)):
            answersTuple = select_from_database_table(DATABASE, "SELECT * FROM Answers WHERE QuestionID=?",
                                                 [questionsTuple[i][0]], True)
            # TODO Check answerstuple for errors
            answers = []
            for j in range(0, len(answersTuple)):
                answers.append(answersTuple[j][2] + ";" + answersTuple[j][3])

            allAnswers[questions[i]] = answers #dictionary, Key: index of question in question array, value: array of answers

        number = 0
        maxNumber = len(questions)
        while (number < maxNumber):
            if (len(questions) > 0):
                print(number, " ", maxNumber)
                try:
                    print(questions[number])
                except:
                    break
                if (questions[number].split(";")[1] == "userInfoRetrieval"):
                    questions.remove(questions[number])
                    allAnswers[questions[number]] = None
                    number -= 1
                    maxNumber -= 1
                    if number < 0:
                        number = 0
                else:
                    number += 1
            else:
                break

        questionsAndAnswers = []
        for i in range(0, len(questions)):
            question = []
            question.append(questions[i])
            merge = tuple(question)
            answers = allAnswers[questions[i]]
            for j in range(0, len(answers)):
                answer = []
                answer.append(answers[j])
                merge = merge + tuple(answer)
            questionsAndAnswers.append(merge)
        print(questionsAndAnswers)
        return render_template("admin/admin-form-add-answer.html", msg=questionsAndAnswers)
    elif request.method == "POST":
        #TODO not even looked at yet
        abort(status.HTTP_501_NOT_IMPLEMENTED)


@app.route("/admin/products", methods=['GET', 'POST'])
def admin_products():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        # TODO check assistants for errors
        assistantIndex = 0  # TODO change this
        products = select_from_database_table(DATABASE, "SELECT * FROM Products WHERE AssistantID=?",
                                              [assistants[assistantIndex][0]], True)
        # TODO check products for errors
        return render_template("admin/admin-form-add-product.html", data=products)
    elif request.method == 'POST':
        # TODO implement this
        abort(status.HTTP_501_NOT_IMPLEMENTED)


@app.route("/admin/templates", methods=['GET', 'POST'])
def admin_templates():
    if request.method == "GET":
        return render_template("admin/admin-convo-template.html")
    elif request.method == "POST":
        abort(status.HTTP_501_NOT_IMPLEMENTED)


@app.route("/admin/connect")
def admin_connect():
    return render_template("admin/admin-connect.html")


@app.route("/admin/pricing")
def admin_pricing():
    return render_template("admin/admin-pricing-tables.html", pub_key=pub_key)


@app.route('/admin/thanks')
def admin_thanks():
    return render_template('admin/admin-thank-you.html')


@app.route("/admin/pay", methods=['GET', 'POST'])
def admin_pay():
    if request.method == 'GET':
        return render_template("admin/admin-pay.html")


@app.route("/admin/analytics", methods=['GET'])
def admin_analytics():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        user = select_from_database_table(DATABASE, "SELECT * FROM Users WHERE Email=?", [email])
        # TODO check user for errors
        company = select_from_database_table(DATABASE, "SELECT * FROM Company WHERE ID=?", [user[1]])
        # TODO check company for errors
        assistants = select_from_database_table(DATABASE, "SELECT * FROM Assistant WHERE CompanyID=?", [company[0]],
                                                True)
        # TODO check assistants for errors
        assistantIndex = 0  # TODO change this
        stats = select_from_database_table(DATABASE, "SELECT * FROM Statistics WHERE AssistantID=?",
                                           [assistants[assistantIndex][2]], True)
        return render_template("admin/admin-analytics.html", data=stats)


@app.route("/admin/support/general", methods=['GET'])
def admin_general_support():
    if request.method == "GET":
        return render_template("admin/admin-general-support.html")


@app.route("/admin/support/docs", methods=['GET'])
def admin_support_docs():
    if request.method == "GET":
        return render_template("admin/admin-docs.html")


@app.route("/admin/support/setup", methods=['GET'])
def admin_support_setup():
    if request.method == "GET":
        return render_template("admin/admin-getting-setup.html")


@app.route("/admin/support/intergration", methods=['GET'])
def admin_support_intergration():
    if request.method == "GET":
        return render_template("admin/admin-intergration-tutorial.html")


@app.route("/admin/support/billing", methods=['GET'])
def admin_support_billing():
    if request.method == "GET":
        return render_template("admin/admin-billing-support.html")


@app.route("/emoji-converter", methods=['GET'])
def admin_emoji():
    if request.method == "GET":
        return render_template("admin/admin-emoji.html")


# Sitemap route
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# Terms and conditions page route
@app.route("/termsandconditions", methods=['GET'])
def terms_and_conditions():
    if request.method == "GET":
        return render_template("terms.html")


@app.route("/privacy", methods=['GET'])
def privacy():
    if request.method == "GET":
        return render_template("privacy-policy.html")


# Affiliate page route
@app.route("/affiliate", methods=['GET'])
def affiliate():
    if request.method == "GET":
        abort(404)
        # return render_template("affiliate.html")


### Redirects ###
@app.route("/Admin/<route>", methods=["GET"])
def redirect_admin(route):
    if request.method == "GET":
        return redirect("/admin/" + route)


@app.route("/admin/Questions", methods=['GET'])
def redirect_admin_questions():
    if request.method == "GET":
        return redirect("/admin/questions")


@app.route("/admin/Answers", methods=['GET'])
def redirect_admin_answers():
    if request.method == "GET":
        return redirect("/admin/answers")


@app.route("/admin/Products", methods=['GET'])
def redirect_admin_products():
    if request.method == "GET":
        return redirect("/admin/products")


@app.route("/admin/Templates", methods=['GET'])
def redirect_admin_templates():
    if request.method == "GET":
        return redirect("/admin/templates")


@app.route("/admin/Support/<route>", methods=["GET"])
def redirect_admin_support(route):
    if request.method == "GET":
        return redirect("/admin/support/" + route)


@app.route("/admin/supportGeneral", methods=['GET'])
def redirect_admin_general_support():
    if request.method == "GET":
        return redirect("/admin/support/general")


@app.route("/admin/supportDocs", methods=['GET'])
def redirect_admin_support_docs():
    if request.method == "GET":
        return redirect("/admin/support/docs")


@app.route("/admin/supportSetup", methods=['GET'])
def redirect_admin_support_setup():
    if request.method == "GET":
        return redirect("/admin/support/setup")


@app.route("/admin/supportIntergartion", methods=['GET'])
def redirect_admin_support_intergration():
    if request.method == "GET":
        return redirect("/admin/support/intergration")


@app.route("/admin/supportBilling", methods=['GET'])
def redirect_admin_support_billing():
    if request.method == "GET":
        return redirect("/admin/support/billing")


@app.route("/Data/<route>", methods=['GET'])
def redirect_data_route(route):
    if request.method == "GET":
        return redirect("/data/" + route)


@app.route("/dataRetrival", methods=['GET'])
def redirect_data_retrieval():
    if request.method == "GET":
        return redirect("/data/retrieval")


@app.route("/dataCollection", methods=['GET'])
def redirect_data_collection():
    if request.method == "GET":
        return redirect("/data/collection")



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


## Error Handlers ##
@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    return render_template('errors/404.html', error=e), status.HTTP_404_NOT_FOUND


@app.errorhandler(418)
def im_a_teapot(e):
    return render_template('errors/418.html', error=e), 418


@app.route("/teapot", methods=["GET"])
def teapot():
    abort(418)

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('errors/500.html', error=e, debug=app.debug), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(status.HTTP_501_NOT_IMPLEMENTED)
def not_implemented(e):
    return render_template('errors/501.html', error=e, debug=app.debug), status.HTTP_501_NOT_IMPLEMENTED


if __name__ == "__main__":
    app.run(debug=True)


########################## OLD CODE ##########################
def adminAddQuestion():
    if request.method == "POST":
        questions = []
        noq = request.form.get("noq-hidden", default="Error")
        for i in range(1, (noq + 1)):
            if (request.form.get("question" + str(i)) != None):
                questions.append(request.form.get("question" + str(i)))

        ##OLD CODE
        # conn = sqlite3.connect(USERPREFERENCES)
        # cur = conn.cursor()
        # cur.execute("UPDATE \""+user_mail+"\" SET PricingQuestion = " + request.form.get("pricing-question"))
        # conn.commit()
        # conn.close()

        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
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
            qType = request.form.get("qType" + str(i))
            try:
                print(tempData[i][0] != None)  # IMPORTANT DO NOT REMOVE
                print("UPDATING: ", tempData[i][0], " TO ", q + ";" + qType)
                cur.execute(
                    "UPDATE \"" + user_mail + "\" SET Question = \"" + q + ";" + qType + "\" WHERE Question = \"" +
                    tempData[i][0] + "\"")
            except:
                print("INSERTING NEW: ", q + ";" + qType)
                cur.execute("INSERT INTO \'" + user_mail + "\'('Question') VALUES (?)", (q + ";" + qType,))
        conn.commit()
        conn.close()
        return redirect("/admin/Questions", code=302)


##OLD CODE
def adminAnswers():
    if request.method == "GET":
        conn = sqlite3.connect(QUESTIONDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        mes = cur.fetchall()
        n = 0
        maxN = len(mes)
        while (n < maxN):
            if (len(mes) > 0):
                print(n, "   ", maxN)
                try:
                    print(mes[n])
                except:
                    break
                if (mes[n][0].split(";")[1] == "userInfoRetrieval"):
                    mes.remove(mes[n])
                    n -= 1
                    maxN -= 1
                    if n < 0:
                        n = 0
                else:
                    n += 1
            else:
                break
        conn.close()
        return render_template("admin/admin-form-add-answer.html", msg=mes)
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
                        if data == [(None,)] or data == [("",)] or data == []:
                            answers.append(request.form.get("pname" + str(i)) + ";" + request.form.get(
                                "keywords" + str(i)) + ";../static/img/core-img/android-icon-72x72.png")
                        else:
                            print(data)
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


def adminAddProduct():
    if request.method == "GET":
        conn = sqlite3.connect(PRODUCTDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        mes = cur.fetchall()
        conn.close()
        return render_template("admin/admin-form-add-product.html", data=mes)
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


# Route for the data storage
@app.route("/admin/userinput", methods=['GET', 'POST'])
def adminDataStorage():
    if request.method == "GET":
        conn = sqlite3.connect(USERINPUTDATABASE)
        cur = conn.cursor()
        user_mail = request.cookies.get("UserEmail")
        cur.execute("SELECT * FROM \"" + user_mail + "\"")
        data = cur.fetchall()
        return render_template("admin/admin-data-storage.html", data=data)
    if request.method == "POST":
        return redirect("/admin/userinput", code=302)


##OLD CODE
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
                        msg = productIntoDatabase(email, data[i]["ProductID"], data[i]["ProductName"],
                                                  data[i]["ProductBrand"], data[i]["ProductModel"],
                                                  data[i]["ProductPrice"], data[i]["ProductKeywords"],
                                                  data[i]["ProductDiscount"], data[i]["ProductURL"],
                                                  data[i]["ProductImage"])
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
                                msg = productIntoDatabase(email, id, name, brand, model, price, keywords, discount, url,
                                                          image)
                            except IndexError:
                                msg = productIntoDatabase(email, id, name, brand, model, price, keywords, discount, url)
                        except IndexError:
                            msg = "Invalid xml file"
                            print(msg)
                else:
                    msg = "File not implemented yet"
                    pass
                os.remove(PRODUCT_FILES + "/" + productFile.filename)
            else:
                msg = "Error not allowed that type of file."
        return msg


def productIntoDatabase(email, id="", name="", brand="", model="", price="", keywords="", discount="", url="",
                        image=""):
    msg = insert_into_database_table(PRODUCTDATABASE,
                                     "INSERT INTO \"" + email + "\" (ProductID, ProductName, ProductBrand, ProductModel, ProductPrice, ProductKeywords, ProductDiscount, ProductURL, ProductImage) VALUES (?,?,?,?,?,?,?,?,?)",
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


@app.route("/chatbot/<route>", methods=['GET', 'POST'])
def dynamicChatbot(route):
    if request.method == "GET":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users;")
        cns = cur.fetchall()
        conn.close()
        for record in cns:
            if route == record[4]:
                conn = sqlite3.connect(QUESTIONDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + record[7] + "\"")
                data = cur.fetchall()
                conn.close()
                date = datetime.now().strftime("%Y-%m")
                if (not app.debug):
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
                return render_template("dynamic-chatbot.html", data=data, user="chatbot/" + route)
        return redirect("/pagenotfound", code=302)
    if request.method == "POST":
        conn = sqlite3.connect(USERDATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users;")
        cns = cur.fetchall()
        for record in cns:
            if route == record[4]:
                # print(1)
                conn = sqlite3.connect(PRODUCTDATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM \"" + record[7] + "\"")
                data = cur.fetchall()
                conn.close()
                keywords = []
                budget = []
                # print(2)
                collectedInformation = request.form.get("collectedInformation").split("||")
                date = datetime.now().strftime("%d-%m-%Y")
                conn = sqlite3.connect(USERINPUTDATABASE)
                cur = conn.cursor()
                i = 0
                b = 0
                # print(data)
                try:
                    cur.execute("INSERT INTO \"" + record[7] + "\" ('Date', 'Question1Info', 'Question2Info', 'Question3Info', 'Question4Info', 'Question5Info', \
                    'Question6Info', 'Question7Info', 'Question8Info', 'Question9Info', 'Question10Info', 'Question11Info', 'Question12Info', 'Question13Info', 'Question14Info', \
                    'Question15Info' ) VALUES ('" + date + "', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')")
                    for c in range(0, 15):
                        print(c + 1, "   ", collectedInformation[c - b].split(";")[0])
                        if (collectedInformation[c - b].split(";")[0] == str(c + 1)):
                            # print(collectedInformation[c - b].split(";")[1])
                            cur.execute("UPDATE \"" + record[7] + "\" SET Question" + str(c + 1) + "Info = \"" + str(
                                collectedInformation[c - b].split(";")[
                                    1]) + "\" WHERE DataID = (SELECT MAX(DataID) FROM \"" + record[7] + "\")")
                        else:
                            b += 1
                            cur.execute("UPDATE \"" + record[7] + "\" SET Question" + str(
                                c + 1) + "Info = \"\" WHERE DataID = (SELECT MAX(DataID) FROM \"" + record[7] + "\")")
                        i = c
                    conn.commit()
                    conn.close()
                except:
                    for c in range(i + 1, 15):
                        cur.execute("UPDATE \"" + record[7] + "\" SET Question" + str(
                            c + 1) + "Info = \"\" WHERE DataID = (SELECT MAX(DataID) FROM \"" + record[7] + "\")")
                    conn.commit()
                    conn.close()
                    # print(data)
                for i in range(1, int(request.form.get("numberOfKeywords")) + 1):
                    if "-" in request.form.get("keyword" + str(i)):
                        budget = request.form.get("keyword" + str(i)).split("-")
                    else:
                        keywords.append(request.form.get("keyword" + str(i)))
                keywordsmatch = []
                # print(data)
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
                # print(data)
                for p in range(0, len(keywordsmatch)):
                    if (keywordsmatch[p] == 0):
                        data.pop(p - substract)
                        substract += 1
                if budget:
                    DD = Del()
                    dl = len(data) - 1
                    i = 0
                    while (i <= dl):
                        item = data[i]
                        itemprice = item[4].translate(DD)
                        if ((int(itemprice) < int(budget[0])) or (int(itemprice) > int(budget[1]))):
                            data.pop(i)
                            i -= 1
                            dl -= 1
                        i += 1
                while (len(data) > 9):
                    data.pop()
                if not data:
                    return "We could not find anything that matched your search criteria. Please try different filter options."
                datastring = ""
                # print(data)
                for i in data:
                    for c in i:
                        datastring += str(c) + "|||"
                    datastring = datastring[:-3]
                    datastring += "&&&"
                conn.close()
                # print(data)
                if (not app.debug):
                    date = datetime.now().strftime("%Y-%m")
                    conn = sqlite3.connect(STATISTICSDATABASE)
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM \"" + route + "\" WHERE Date=?;", [date])
                    stats = cur.fetchall()
                    questionsAnswered = request.form["questionsAnswered"]
                    if not stats:
                        cur.execute("INSERT INTO \"" + route + "\" ('Date', 'AssistantOpened', 'QuestionsAnswered', 'ProductsReturned')\
                                        VALUES (?,?,?,?)", (date, "0", questionsAnswered, len(data)))
                    else:
                        cur.execute("UPDATE \"" + route + "\" SET ProductsReturned = \"" + str(
                            int(stats[0][3]) + len(data)) + "\" WHERE Date = \"" + date + "\"")
                        cur.execute("UPDATE \"" + route + "\" SET QuestionsAnswered = \"" + str(
                            int(stats[0][2]) + int(questionsAnswered)) + "\" WHERE Date = \"" + date + "\"")
                    conn.commit()
                    cur.execute("SELECT * FROM \"" + route + "\" WHERE Date=?;", [date])
                    stats = cur.fetchall()
                    conn.close()
                # print(datastring)
                return jsonify(datastring)


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_EXTENSIONS


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
