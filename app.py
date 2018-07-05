#!/usr/bin/python3
from flask_mail import Mail, Message
from flask import Flask, redirect, request, render_template, jsonify, send_from_directory, abort, escape, url_for, \
    make_response
from werkzeug.utils import secure_filename
from flask_api import status
from datetime import datetime
from bcrypt import hashpw, gensalt
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadData
from xml.dom import minidom
from json import dumps, loads, load, dump
import os
import sqlite3
import stripe
import string
import random

verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE = APP_ROOT + "/database.db"
PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'

stripe.api_key = secret_key

stripe_keys = {
    'secret_key': secret_key,
    'publishable_key': pub_key
}

# stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, static_folder='static')
mail = Mail(app)

ALLOWED_IMAGE_EXTENSION = {'png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG'}
ALLOWED_PRODUCT_FILE_EXTENSIONS = {'json', 'JSON', 'xml', 'xml'}

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='thesearchbase@gmail.com',
    MAIL_PASSWORD='pilbvnczzdgxkyzy'
)


def select_from_database_table(sql_statement, array_of_terms=None, all=False, database=DATABASE):
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




def get_last_row_from_table(table, database=DATABASE):
    data = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM " + table + " WHERE ROWID IN ( SELECT max( ROWID ) FROM " + table +" );").fetchone()

    except Exception as e:
        row = -1
    finally:
        if conn is not None:
            conn.close()
        return row;




def insert_into_database_table(sql_statement, tuple_of_terms, database=DATABASE):
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


def update_table(sql_statement, array_of_terms, database=DATABASE):
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


def delete_from_table(sql_statement, array_of_terms, database=DATABASE):
    msg = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
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


def allowed_product_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_PRODUCT_FILE_EXTENSIONS


def allowed_image_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_IMAGE_EXTENSION


# TODO just overall better validation

# code to ensure user is logged in
@app.before_request
def before_request():
    theurl = str(request.url_rule)
    if "admin" not in theurl or "admin/homepage" in theurl:
        print("Ignore before request for: ", theurl)
        return None
    email = request.cookies.get("UserEmail")
    print("USER EMAIL: " + str(email))
    if email is None:
        print("User not logged in")
        return render_template("login.html", msg="You are not logged in!")
    print("Before request checking: ", theurl, " ep: ", request.endpoint)
    if email == 'None' and request.endpoint != 'login':
        return render_template("login.html", msg="You are not logged in!")
    print("Before Request checks out")
    return None


# TODO jackassify it
@app.route("/demo/<route>", methods=['GET'])
def dynamic_popup(route):
    if request.method == "GET":
        url = "http://www.example.com/"
        company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [escape(route)])
        if company is None:
            abort(status.HTTP_404_NOT_FOUND)
        # elif "Debug" in company[4]:
        else:
            url = company[3]
            if "http" not in url:
                url = "https://" + url
        return render_template("dynamic-popup.html", route=route, url=url)


# drop down routes.
@app.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/features", methods=['GET'])
def features():
    if request.method == "GET":
        return render_template("features.html")


@app.route("/dataRetrieval", methods=['GET'])
def data_retrieval():
    if request.method == "GET":
        return render_template("retrieval.html")


@app.route("/dataCollection", methods=['GET'])
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
            email = email.lower()
            data = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
            if data is not None:
                password = data[6]
                if hash_password(password_to_check, password) == password:
                    verified = data[8]
                    print(verified == "True")
                    if verified == "True":
                        messages = dumps({"email": escape(email)})
                        return redirect(url_for(".admin_home", messages=messages))
                    else:
                        return render_template('errors/verification.html',
                                               data="Account not verified, please check your email and follow instructions")
                else:
                    return render_template('login.html', data="User name and password does not match!")
            else:
                return render_template('login.html', data="User doesn't exist!")


# TODO improve verification
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html", debug=app.debug)
    elif request.method == "POST":

        # # update company for with stripe details
        # update_table("UPDATE Companies SET SubscriptionID=?, StripeID=? WHERE Name=?",
        #              ['SubTest', new_customer['id'], companyName])

        # TODO this need to be removed in production
        # remove the Stripe customer when not in production to kepp Stripe clean when testing
        # if app.debug:
        #     new_customer.delete()

        # company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [companyName])
        # TODO check company for errors
        # companyID = company[0]

        email = request.form.get("email", default="Error").lower()

        fullname = request.form.get("fullname", default="Error")
        accessLevel = "Admin"
        password = request.form.get("password", default="Error")

        companyName = request.form.get("companyName", default="Error")
        companySize = request.form.get("companySize")
        companyPhoneNumber = request.form.get("phoneNumber")
        websiteURL = request.form.get("websiteURL", default="Error")


        if fullname == "Error" or accessLevel == "Error" or email == "Error" or password == "Error" \
                or companyName == "Error" or websiteURL == "Error":
            print("Invalid request")
            return render_template("signup.html", msg="Invalid request", debug=app.debug), status.HTTP_400_BAD_REQUEST


        else:
            user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
            print(user)
            if user is not None:
                print("Email is already in use!")
                return render_template("signup.html", msg="Email is already in use!", debug=app.debug), status.HTTP_400_BAD_REQUEST

            try:
                firstname = fullname.strip().split(" ")[0]
                surname = fullname.strip().split(" ")[1]

                #debug
                print(firstname)
                print(surname)

            except IndexError as e:
                abort(status.HTTP_400_BAD_REQUEST)
                # TODO handle much better


            # Create a Stripe customer for the new company.
            new_customer = stripe.Customer.create(
                email=email
            )
            print(new_customer)

            hashed_password = hash_password(password)

            verified = app.debug

            insertCompanyResponse = insert_into_database_table(
                "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (companyName,companySize, websiteURL, companyPhoneNumber))

            company = get_last_row_from_table("Companies")

            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified') VALUES (?,?,?,?,?,?,?,?);",
                (company[0], firstname, surname, accessLevel, email, hashed_password, new_customer['id'], str(verified)))


            if not app.debug:
                # TODO this needs improving
                msg = Message("Account verification",
                              sender="thesearchbase@gmail.com",
                              recipients=[email])

                payload = email + ";" + companyName
                link = "www.thesearchbase.com/account/verify/{}".format(verificationSigner.dumps(payload))
                msg.body = "You have registered with TheSearchBase.\n" \
                           "Please visit <a href='{}'>this link</a> to verify your account.".format(email, link)
                mail.send(msg)

                # sending the registration confirmation email to us
                msg = Message("A new company has signed up!",
                              sender="thesearchbase@gmail.com",
                              recipients=["thesearchbase@gmail.com"])
                msg.body = "Company name: {} has signed up the admin's details are. Name: {}, Email: {}, ".format(
                    companyName, fullname, email)
                mail.send(msg)

            return render_template('errors/verification.html',
                                   msg="Please check your email and follow instructions to verify account and get started.")




# Data retrieval functions
def get_company(email):
    user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
    # TODO check user for errors
    company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
    # TODO check company for errors
    return company


def get_assistants(email):
    user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
    # TODO check user for errors
    company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
    # TODO check company for errors
    assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]],
                                            True)
    # TODO check assistants for errors
    return assistants


def get_total_statistics(num, email):
    try:
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [get_company(email)[0]])
        statistics = select_from_database_table("SELECT * FROM Statistics WHERE AssistantID=?;", [assistant[0]])
        total = 0
        try:
            for c in statistics[num]:
                total += int(c)
        except:
            total = statistics[num]
    except:
        total = 0
    return total


# Admin pages
@app.route("/admin/homepage", methods=['GET'])
def admin_home():
    if request.method == "GET":
        sendEmail = False
        args = request.args
        if len(args) > 0:
            messages = args['messages']
            if messages is not None:
                email = loads(messages)['email']
                if email is None or email == "None":
                    return render_template("login.html", msg="You are not logged in!")
                sendEmail = True
            else:
                abort(status.HTTP_400_BAD_REQUEST)
        else:
            email = request.cookies.get("UserEmail")
        statistics = [get_total_statistics(3, email), get_total_statistics(5, email)]
        if sendEmail:
            assistants = get_assistants(email)
            # TODO check assistants for errors
            assistantIDs = []
            for assistant in assistants:
                assistantIDs.append(assistant[0])
            return render_template("admin/main.html", stats=statistics, email=email, assistantIDs=assistantIDs)
        else:
            return render("admin/main.html", stats=statistics)


@app.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        args = request.args
        if len(args) > 0:
            messages = args['messages']
            if messages is not None:
                email = loads(messages)['email']
                if email is None or email == "None":
                    email = request.cookies.get("UserEmail")
                sendEmail = True
            else:
                email = request.cookies.get("UserEmail")
        else:
            email = request.cookies.get("UserEmail")
        user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
        # TODO check database output for errors
        company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
        return render_template("admin/profile.html", user=user, email=email, company=company)

    elif request.method == "POST":
        curEmail = request.cookies.get("UserEmail")
        names = request.form.get("names", default="Error")
        newEmail = request.form.get("email", default="error").lower()
        companyName = request.form.get("companyName", default="Error")
        companyURL = request.form.get("companyURL", default="error").lower()
        if names != "Error" and newEmail != "error" and companyURL != "error" and companyName != "Error":
            names = names.split(" ")
            name1 = names[0]
            name2 = names[1]
            updateUser = update_table("UPDATE Users SET Firstname=?, Surname=?, Email=? WHERE Email=?;", [name1,name2,newEmail,curEmail])
            companyID = select_from_database_table("SELECT CompanyID FROM Users WHERE Email=?;", [newEmail])
            updateCompany = update_table("UPDATE Companies SET Name=?, URL=? WHERE ID=?;", [companyName,companyURL,companyID[0]])
            messages = dumps({"email": escape(newEmail)})
            return redirect(url_for(".profilePage", messages=messages))
        print("Error in updating Company or Profile Data")
        return redirect("/admin/profile", code=302)


@app.route("/popupsettings", methods=['GET'])
def get_pop_settings():
    if request.method == "GET":
        url = request.form.get("URL", default="Error")
        print(url)
        if url != "Error":
            if "127.0.0.1:5000" in url or "thesearchbase.com" in url:
                # its on test route
                companyName = url.split("/")[len(url.split("/")) - 1]
                print(companyName)
                companyID = select_from_database_table("SELECT ID FROM Companies WHERE Name=?", [companyName], True)
                print(companyID)
            else:
                # its on client route
                companyID = select_from_database_table("SELECT ID FROM Companies WHERE URL=?", [url], True)
            secsUntilPop = select_from_database_table("SELECT SecondsUntilPopup FROM Assistants WHERE CompanyID=?",
                                                      [companyID[0][0]], True)
            datastring = secsUntilPop[0][0]
            print(datastring)
            return jsonify(datastring)


@app.route("/admin/assistant/create", methods=['GET', 'POST'])
def admin_assistant_create():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        if assistants is None or len(assistants) < 4:
            return render("admin/create-assistant.html", autopop="Off")
        elif "Error" in assistants:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            abort(status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            nickname = request.form.get("nickname", default="Error")
            message = request.form.get("welcome-message", default="Error")
            autopopup = request.form.get("switch-autopop", default="off")
            popuptime = request.form.get("timeto-autopop", default="Error")

            if message is "Error" or nickname is "Error" or (popuptime is "Error" and autopopup is not "off"):
                abort(status.HTTP_400_BAD_REQUEST)
            else:
                if autopopup == "off":
                    secondsUntilPopup = "Off"
                else:
                    secondsUntilPopup = popuptime
                createAssistant = insert_into_database_table(
                    "INSERT INTO Assistants (CompanyID, Message, SecondsUntilPopup, Nickname) VALUES (?,?,?,?);",
                    (company[0], message, secondsUntilPopup, nickname))

                if "Error" in createAssistant:
                    abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    assistant = select_from_database_table(
                        "SELECT ID FROM Assistants WHERE CompanyID=? AND Nickname=?",
                        [company[0], nickname])
                    if assistant is None or "Error" in assistant:
                        if "UNIQUE" in assistant:
                            # TODO handle this better
                            abort(status.HTTP_409_CONFLICT)
                        else:
                            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return redirect("/admin/assistant/{}/settings".format(assistant[0]))


@app.route("/admin/assistant/<assistantID>/settings", methods=['GET', 'POST'])
def admin_assistant_edit(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
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
                message = assistant[3]
                autoPop = assistant[4]
                nickname = assistant[5]

                return render("admin/edit-assistant.html", autopop=autoPop, message=message, id=assistantID,
                              nickname=nickname)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None:
                abort(status.HTTP_400_BAD_REQUEST)
            elif "Error" in assistant:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                nickname = request.form.get("nickname", default="Error")
                message = request.form.get("welcome-message", default="Error")
                popuptime = request.form.get("timeto-autopop", default="Error")
                autopopup = request.form.get("switch-autopop", default="off")

                if message is "Error" or nickname is "Error" or (popuptime is "Error" and autopopup is not "off"):
                    abort(status.HTTP_400_BAD_REQUEST)
                else:
                    if autopopup == "off":
                        secondsUntilPopup = "Off"
                    else:
                        secondsUntilPopup = popuptime
                    updateAssistant = update_table(
                        "UPDATE Assistants SET Message=?, SecondsUntilPopup=?, Nickname=? WHERE ID=? AND CompanyID=?",
                        [message, secondsUntilPopup, nickname, assistantID, company[0]])

                    if "Error" in updateAssistant:
                        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return redirect("/admin/assistant/{}/settings".format(assistantID))


# TODO rewrite
@app.route("/admin/assistant/<assistantID>/questions", methods=['GET', 'POST'])
def admin_questions(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
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
                questionsTuple = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                            [assistant[0]], True)
                # TODO check questionstuple for errors
                message = assistant[3]

                questions = []
                for i in range(0, len(questionsTuple)):
                    question = [questionsTuple[i][2] + ";" + questionsTuple[i][3]]
                    questions.append(tuple(question))
                return render("admin/questions.html", data=questions, message=message, id=assistantID)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
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
                currentQuestions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                              [assistantID], True)
                # TODO check currentQuestions for errors

                updatedQuestions = []
                noq = request.form.get("noq-hidden", default="Error")
                for i in range(1, int(noq) + 1):
                    question = request.form.get("question" + str(i), default="Error")
                    if question != "Error":
                        updatedQuestions.append(question)
                    else:
                        return render_template("admin/questions.html",
                                               data=currentQuestions), status.HTTP_400_BAD_REQUEST

                i = -1
                if (len(updatedQuestions) + 1 < len(currentQuestions) + 1):
                    for b in range(len(updatedQuestions) + 1, len(currentQuestions) + 1):
                        questionID = currentQuestions[i][0]
                        question = currentQuestions[i][2]

                        # print("DELETING: ", question)
                        deleteQuestion = delete_from_table("DELETE FROM Questions WHERE AssistantID=? AND Question=?;",
                                                           [assistantID, escape(question)])
                        # TODO check deleteQuestion for errors
                        deleteAnswers = delete_from_table(DATABASE, "DELETE FROM Answers WHERE QuestionID=?;",
                                                          [questionID])
                        # TODO check deleteAnswers for errors
                for q in updatedQuestions:
                    i += 1
                    qType = request.form.get("qType" + str(i))
                    if i >= len(currentQuestions):
                        insertQuestion = insert_into_database_table(
                            "INSERT INTO Questions ('AssistantID', 'Question', 'Type')"
                            "VALUES (?,?,?);", (assistantID, q, qType))
                        # TODO check insertQuestion for errors
                    else:
                        updateQuestion = update_table("UPDATE Questions SET Question=?, Type=? WHERE Question=?;",
                                                      [escape(q), qType, currentQuestions[i][2]])
                        # TODO check updateQuestion for errors

                return redirect("/admin/assistant/{}/questions".format(assistantID))


# TODO rewrite
@app.route("/admin/assistant/<assistantID>/answers", methods=['GET', 'POST'])
def admin_answers(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
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
                questionsTuple = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                            [assistantID], True)
                # TODO check questionstuple for errors
                questions = []
                for i in range(0, len(questionsTuple)):
                    questions.append(questionsTuple[i][2] + ";" + questionsTuple[i][3])

                allAnswers = {}
                for i in range(0, len(questions)):
                    answersTuple = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;",
                                                              [questionsTuple[i][0]], True)
                    # TODO Check answerstuple for errors
                    answers = []
                    for j in range(0, len(answersTuple)):
                        answers.append(answersTuple[j][2] + ";" + answersTuple[j][3] + ";" + answersTuple[j][5])

                    allAnswers[questions[i]] = answers

                # remove userInfoRetrieval questions
                # number = 0
                # maxNumber = len(questions)
                # while (number < maxNumber):
                #    if (len(questions) > 0):
                #        if (number >= len(questions)):
                #            break
                #        else:
                #            if (questions[number].split(";")[1] == "userInfoRetrieval"):
                #                allAnswers[questions[number]] = None
                #                questions.remove(questions[number])
                #                number -= 1
                #                maxNumber -= 1
                #                if number < 0:
                #                    number = 0
                #            else:
                #                number += 1
                #    else:
                #        break

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
                return render("admin/answers.html", msg=questionsAndAnswers, id=assistantID)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
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
                selected_question = request.form.get("question", default="Error")  # question_text;question_type
                # TODO check selected_question for errors

                question = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=? AND Question=?;",
                                                      [assistantID, selected_question.split(";")[0]])
                # TODO Check question for errors
                questionID = question[0]
                currentAnswers = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;", [questionID])
                # TODO check currentAnswers for errors
                if (currentAnswers is not None):
                    delete_from_table("DELETE FROM Answers WHERE QuestionID=?;", [questionID])
                    # TODO check delete from table for errors

                noa = 1
                for key in request.form:
                    if "pname" in key:
                        noa += 1

                for i in range(1, noa):
                    answer = request.form.get("pname" + str(i), default="Error")
                    # TODO check answer for errors
                    # keyword = request.form.get("keywords" + str(i), default="Error")
                    keyword = request.form.getlist("keywords" + str(i))
                    keyword = ','.join(keyword)
                    # TODO check keywords for errors
                    # print(request.form.getlist("keywords" + str(i)))
                    action = request.form.get("action" + str(i), default="None")
                    # TODO check action for errors
                    insertAnswer = insert_into_database_table(
                        "INSERT INTO Answers (QuestionID, Answer, Keyword, Action) VALUES (?,?,?,?);",
                        (questionID, answer, keyword, action))
                    # TODO check insertAnswer

                return redirect("/admin/assistant/{}/answers".format(assistantID)+"?res="+str(noa)+"")


@app.route("/admin/assistant/<assistantID>/products", methods=['GET', 'POST'])
def admin_products(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
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
                products = select_from_database_table(
                    "SELECT ProductID, Name, Brand, Model, Price, Keywords, Discount, URL "
                    "FROM Products WHERE AssistantID=?;", [assistantID], True)
                # TODO check products for errors
                return render("admin/products.html", data=products, id=assistantID)
    elif request.method == 'POST':
        email = request.cookies.get("UserEmail")
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
                currentProducts = select_from_database_table("SELECT * FROM Products WHERE AssistantID=?;",
                                                             [assistantID], True)
                if "Error" in currentProducts:
                    # TODO handle errors with currentProducts
                    abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Retrieving current products: " + currentProducts)
                elif currentProducts is not None and currentProducts != []:
                    deleteCurrentProducts = delete_from_table("DELETE FROM Products WHERE AssistantID=?;",
                                                              [assistantID])
                    if "Error" in deleteCurrentProducts:
                        # TODO handle errors with deleteCurrentProducts
                        abort(status.HTTP_500_INTERNAL_SERVER_ERROR,
                              "Deleting current products: " + deleteCurrentProducts)
                    else:
                        pass

                nop = 1
                for key in request.form:
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

                    insertProduct = insert_into_database_table(
                        "INSERT INTO Products (AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) "
                        "VALUES (?,?,?,?,?,?,?,?,?);", (
                            assistantID, id, name, brand, model, price,
                            keywords, discount, url))
                    # TODO try to recover by re-adding old data if insertProduct fails
                return redirect("/admin/assistant/{}/products".format(assistantID))


# TODO improve
@app.route("/admin/assistant/<assistantID>/products/file", methods=['POST'])
def admin_products_file_upload(assistantID):
    if request.method == "POST":
        msg = ""
        if 'productFile' not in request.files:
            msg = "Error no file given."
        else:
            email = request.cookies.get("UserEmail")
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


# TODO improve
@app.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?", [assistantID,
                                                                                                           company[0]])
            if assistant is None:
                abort(status.HTTP_404_NOT_FOUND)
            elif "Error" in assistant:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                       [assistantID], True)
                data = []
                dataTuple = tuple(["Null"])
                for i in range(0, len(questions)):
                    question = questions[i]
                    questionID = question[0]
                    userInput = select_from_database_table("SELECT * FROM UserInput WHERE QuestionID=?", [questionID],
                                                           True)
                    # TODO check userInput for errors
                    inputTuple = ()
                    for inputData in userInput:
                        input = inputData[3]
                        inputDate = inputData[2]
                        if len(inputTuple) == 0:
                            inputTuple = tuple([inputDate])
                        elif inputTuple[0] != inputDate:
                            dataTuple = dataTuple + inputTuple
                            data.append(dataTuple)
                            dataTuple = tuple(["Null"])
                            inputTuple = tuple([inputDate])
                        inputTuple = inputTuple + tuple([input])
                    if len(userInput) > 0:
                        dataTuple = dataTuple + inputTuple
                        data.append(dataTuple)
                        dataTuple = tuple(["Null"])
                return render("admin/data-storage.html", data=data)


@app.route("/admin/templates", methods=['GET', 'POST'])
def admin_templates():
    if request.method == "GET":
        return render("admin/convo-template.html")
    elif request.method == "POST":
        abort(status.HTTP_501_NOT_IMPLEMENTED)


@app.route("/admin/connect", methods=['GET'])
def admin_connect():
    return render("admin/connect.html")


@app.route("/admin/pricing", methods=['GET'])
def admin_pricing():
    return render("admin/pricing-tables.html", pub_key=pub_key)


@app.route('/admin/thanks', methods=['GET'])
def admin_thanks():
    return render('admin/thank-you.html')


@app.route("/admin/pay/<planID>", methods=['GET', 'POST'])
def admin_pay(planID):

    # if request.method == 'GET':
    #     return render("admin/pay.html")

    if request.method == 'POST':

        # abort(status.HTTP_501_NOT_IMPLEMENTED)
        email = request.cookies.get("UserEmail")
        company = get_company(email)


        if company is None or "Error" in company:
            # TODO handle this better, as it's payments so is very important we don't charge the customer etc
            return redirect("/login")


        else:
            token = request.form.get("stripeToken", default="Error")
            print(token)
            print(planID)
            if token is "Error":
                # TODO improve this
                abort(status.HTTP_400_BAD_REQUEST)
            else:

                user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
                try:
                    subscription = stripe.Subscription.create(
                        customer=user[7],
                        source=token,
                        items=[
                            {
                                "plan": planID,
                            },
                        ]
                    )
                    # if everything is ok
                    # TODO activate assistants

                except Exception as e:
                    print(e)
                    # TODO check subscription for errors https://stripe.com/docs/api#errors
                    # TODO this is important todo properly

                print("You have successfully subscribed!")
                return render("admin/pricing-tables.html", msg="You have successfully subscribed!")

                # TODO surround with try except and catch any errors
                # customer = stripe.Customer.create(
                #     source=token,
                #     email=email,
                #     description=company[1]
                # )
                #
                # updateCompany = update_table("UPDATE Companies SET StripeID=? WHERE ID=?", [customer['id'], company[0]])
                #
                # planID = select_from_database_table("SELECT * FROM Plans WHERE ID=?", [], True)
                #

                # if "Error" in updateCompany:
                #     # TODO handle this better
                #     customer.delete()
                # else:
                #     planID = ""
                #     subscription = company[4].lower()
                #     if subscription == "basic":
                #         planID = "plan_D3lp2yVtTotk2f"
                #     elif subscription == "advanced":
                #         planID = "plan_D3lp9R7ombKmSO"
                #     elif subscription == "ultimate":
                #         planID = "plan_D3lpeLZ3EV8IfA"
                #     elif subscription == "debug":
                #         planID = "plan_D48N4wxwAWEMOH"
                #     elif subscription == "trial":
                #         abort(status.HTTP_501_NOT_IMPLEMENTED)
                #     else:
                #         abort(status.HTTP_500_INTERNAL_SERVER_ERROR)





# Stripe Webhooks
#This will not work anymore since the StripeID column is moved from Companies table to the Users table.
@app.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhook_subscription_cancelled():
    if request.method == "POST":
        event_json = request.get_json(force=True)
        customerID = event_json['data']['object']['customer']
        print(customerID)
        company = select_from_database_table("SELECT * FROM Companies WHERE StripeID=?", [customerID])
        # TODO check company for errors
        assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?", [company[0]], True)
        for assistant in assistants:
            updateAssistant = update_table("UPDATE Assistants SET Active=? WHERE ID=?", ["False", assistant[0]])
            # TODO check update assistant for errors
        return '', status.HTTP_200_OK


# TODO implement this
@app.route("/admin/analytics", methods=['GET'])
def admin_analytics():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        # TODO check assistants for errors
        assistantIndex = 0  # TODO change this
        assistantID = assistants[assistantIndex][0]
        stats = select_from_database_table(
            "SELECT Date, Opened, QuestionsAnswered, ProductsReturned FROM Statistics WHERE AssistantID=?",
            [assistantID], True)
        return render("admin/analytics.html", data=stats)


# Method for the users
@app.route("/admin/users", methods=['GET'])
def admin_users():
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        # todo check company
        companyID = company[0]

        userLevel = select_from_database_table("SELECT AccessLevel FROM Users WHERE Email=?", [email])[0]
        if userLevel is None:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO better handle
        elif "Error" in userLevel:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO better handle this
        else:
            if userLevel != "Admin":
                return redirect("/admin/homepage")
            else:
                # TODO improve this
                users = select_from_database_table("SELECT * FROM Users WHERE CompanyID=?", [companyID], True)
                return render("admin/users.html", users=users)


@app.route("/admin/users/add", methods=['POST'])
def admin_add_users():
    if request.method == "POST":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        # todo check company
        companyID = company[0]
        fullname = request.form.get("fullname", default="Error")
        accessLevel = request.form.get("accessLevel", default="Error")
        newEmail = request.form.get("email", default="Error")
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        # Generates a random password

        if fullname == "Error" or accessLevel == "Error" or newEmail == "Error":
            print("Invalid request")
            abort(status.HTTP_400_BAD_REQUEST)
        else:
            newEmail = newEmail.lower()
            try:
                firstname = fullname.split(" ")[0]
                surname = fullname.split(" ")[1]
            except IndexError as e:
                abort(status.HTTP_400_BAD_REQUEST)
                # TODO handle much better
            hashed_password = hash_password(password)

            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
                (companyID, firstname, surname, accessLevel, newEmail, hashed_password, "True"))
            if "added" not in insertUserResponse:
                if "UNIQUE constraint" in insertUserResponse:
                    abort(status.HTTP_409_CONFLICT)
                else:
                    abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # TODO handle this better
            else:
                if not app.debug:
                    # sending email to the new user.
                    # TODO this needs improving
                    msg = Message("Account verification, {} {}".format(firstname, surname),
                                  sender="thesearchbase@gmail.com",
                                  recipients=[email])
                    link = "www.thesearchbase.com/account/changepassword"
                    msg.body = "You have been registered with TheSearchBase by an Admin at your company. \n" \
                               "If you feel this is a mistake please contact {}. \n" \
                               "Your temporary password is: {}\n" \
                               "Please visit <a href='{}'>this link</a> to set password for account.".format(email,
                                                                                                             password,
                                                                                                             link)
                    mail.send(msg)

                return redirect("/admin/users")


# Method for the billing
@app.route("/admin/billing", methods=['GET'])
def admin_billing():
    if request.method == "GET":
        return render("admin/billing.html")


@app.route("/admin/support/general", methods=['GET'])
def admin_general_support():
    if request.method == "GET":
        return render("admin/support/general.html")


@app.route("/admin/support/docs", methods=['GET'])
def admin_support_docs():
    if request.method == "GET":
        return render("admin/support/docs.html")


@app.route("/admin/support/setup", methods=['GET'])
def admin_support_setup():
    if request.method == "GET":
        return render("admin/support/getting-setup.html")


@app.route("/admin/support/integration", methods=['GET'])
def admin_support_integration():
    if request.method == "GET":
        return render("admin/support/integration.html")


@app.route("/admin/support/billing", methods=['GET'])
def admin_support_billing():
    if request.method == "GET":
        return render("admin/support/billing.html")


@app.route("/admin/emoji-converter", methods=['GET'])
def admin_emoji():
    if request.method == "GET":
        return render("admin/emoji.html")


@app.route("/chatbot/<route>", methods=['GET', 'POST'])
def chatbot(route):
    if request.method == "GET":
        company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [escape(route)])

        if company is None:
            abort(status.HTTP_400_BAD_REQUEST, "This company does't exist")

        # for debugging
        print(escape(route))
        print(company)

        # TODO check company for errors
        assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]], True)

        # for debugging
        print(assistants)


        # TODO check assistant for errors
        assistantIndex = 0  # TODO implement this properly
        assistantID = assistants[assistantIndex][0]

        assistantActive = assistants[assistantIndex][5]

        if assistantActive != "True":
            abort(status.HTTP_404_NOT_FOUND, "Assistant not active.")
        else:
            questionsTuple = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                        [assistantID], True)
            # TODO check questionstuple for errors
            questions = []
            for i in range(0, len(questionsTuple)):
                questions.append(questionsTuple[i][2] + ";" + questionsTuple[i][3])

            allAnswers = {}
            for i in range(0, len(questions)):
                answersTuple = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;",
                                                          [questionsTuple[i][0]], True)
                print(answersTuple)
                # TODO Check answerstuple for errors
                answers = []
                for j in range(0, len(answersTuple)):
                    answers.append(answersTuple[j][2] + ";" + answersTuple[j][3] + ";" + answersTuple[j][5])

                allAnswers[questions[i]] = answers

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

            message = assistants[assistantIndex][3]
            # MONTHLY UPDATE
            date = datetime.now().strftime("%Y-%m")
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, 0, 0))
                # TODO check newStats for errors
            else:
                updatedStats = update_table("UPDATE Statistics SET Opened=? WHERE AssistantID=? AND Date=?;",
                                            [currentStats[3] + 1, assistantID, date])

            # WEEKLY UPDATE
            dateParts = datetime.now().strftime("%Y-%m-%d").split("-")
            date = datetime.now().strftime("%Y") + ";" + str(datetime.date(datetime.now()).isocalendar()[1])
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, 0, 0))
                # TODO check newStats for errors
            else:
                updatedStats = update_table("UPDATE Statistics SET Opened=? WHERE AssistantID=? AND Date=?;",
                                            [currentStats[3] + 1, assistantID, date])
            print(questionsAndAnswers)

            return render_template("dynamic-chatbot.html", data=questionsAndAnswers, user="chatbot/" + route,
                                   message=message)
    elif request.method == "POST":
        company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [escape(route)])
        # TODO check company for errors
        assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]], True)
        # TODO check assistant for errors
        assistantIndex = 0  # TODO implement this properly
        assistantID = assistants[assistantIndex][0]

        questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?", [assistantID], True)
        # TODO check questions for errors

        products = select_from_database_table("SELECT * FROM Products WHERE AssistantID=?;", [assistantID], True)
        # TODO check products for errors

        collectedInformation = request.form.get("collectedInformation").split("||")
        date = datetime.now().strftime("%d-%m-%Y")
        for i in range(0, len(collectedInformation)):
            questionIndex = int(collectedInformation[i].split(";")[0]) - 1
            input = collectedInformation[i].split(";")[1]
            questionID = int(questions[questionIndex][0])
            insertInput = insert_into_database_table("INSERT INTO UserInput (QuestionID, Date, Input) VALUES (?,?,?)",
                                                     (questionID, date, input))
            # TODO check insertInput for errors

        # TODO work out wtf this is actually doing
        nok = request.form.get("numberOfKeywords", default="Error")
        if nok is "Error":
            abort(status.HTTP_501_NOT_IMPLEMENTED, "Number of keywords invalid")
        else:
            keywords = []
            budget = []

            # TODO work out this
            for i in range(1, int(nok) + 1):
                keyword = request.form.get("keyword" + str(i), default="Error")
                if keyword is not "Error":
                    if "-" in keyword:
                        budget = keyword.split("-")
                    else:
                        keywords.append(keyword)
                else:
                    abort(status.HTTP_400_BAD_REQUEST)

            keywordsmatch = []
            i = -1
            for product in products:
                keywordsmatch.append(0)
                i += 1
                productKeywords = product[7].split(",")
                for keyword in keywords:
                    for productKeyword in productKeywords:
                        if productKeyword == keyword:
                            keywordsmatch[i] += 1

            exitAtLength = 0
            while (True):
                for i in range(0, len(keywordsmatch) - 1):
                    if (keywordsmatch[i] < keywordsmatch.pop(i + 1)):
                        keywordsmatch.insert(i, keywordsmatch.pop(i + 1))
                        products.insert(i, products.pop(i + 1))
                        exitAtLength = 0
                        break
                exitAtLength += 1
                if exitAtLength == 5:
                    break
            subtract = 0
            for i in range(0, len(keywordsmatch)):
                if (keywordsmatch[i] == 0):
                    products.pop(i - subtract)
                    subtract += 1
            if budget:
                DD = Del()
                dl = len(products) - 1
                i = 0
                while (i <= dl):
                    product = products[i]
                    itemprice = product[6].translate(DD)
                    if ((int(itemprice) < int(budget[0])) or (int(itemprice) > int(budget[1]))):
                        products.pop(i)
                        i -= 1
                        dl -= 1
                    i += 1

            while (len(products) > 9):
                products.pop()
            if products is None or products == []:
                return "We could not find anything that matched your search criteria. Please try different filter options."

            # UPDATE MONTHLY
            date = datetime.now().strftime("%Y-%m")
            questionsAnswered = request.form.get("questionsAnswered", default="Error")
            # TODO check questionsAnswered for errors
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, questionsAnswered, len(products)))
                # TODO check newStats for errors
            else:
                currentQuestionAnswerd = currentStats[4]
                currentProductsReturned = currentStats[5]
                questionsAnswered = int(questionsAnswered) + int(currentQuestionAnswerd)
                productsReturned = len(products) + int(currentProductsReturned)
                updatedStats = update_table(
                    "UPDATE Statistics SET QuestionsAnswered=?, ProductsReturned=? WHERE AssistantID=? AND Date=?;",
                    [questionsAnswered, productsReturned, assistantID, date])
                # TODO check updatedStats for errors

            # UPDATE WEEKLY
            date = datetime.now().strftime("%Y") + ";" + str(datetime.date(datetime.now()).isocalendar()[1])
            questionsAnswered = request.form.get("questionsAnswered", default="Error")
            # TODO check questionsAnswered for errors
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, questionsAnswered, len(products)))
                # TODO check newStats for errors
            else:
                currentQuestionAnswerd = currentStats[4]
                currentProductsReturned = currentStats[5]
                questionsAnswered = int(questionsAnswered) + int(currentQuestionAnswerd)
                productsReturned = len(products) + int(currentProductsReturned)
                updatedStats = update_table(
                    "UPDATE Statistics SET QuestionsAnswered=?, ProductsReturned=? WHERE AssistantID=? AND Date=?;",
                    [questionsAnswered, productsReturned, assistantID, date])
                # TODO check updatedStats for errors

            datastring = ""
            for product in products:
                for i in range(2, len(product)):
                    datastring += str(product[i]) + "|||"
                datastring = datastring[:-3]
                datastring += "&&&"
            print(datastring)
            return jsonify(datastring)


@app.route("/account/verify/<payload>", methods=['GET'])
def verify_account(payload):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        if email is None or email is "None":
            data = ""
            try:
                data = verificationSigner.loads(payload)
                try:
                    email = data.split(";")[0]
                    companyName = data.split(";")[1]

                    company = get_company(email)
                    # TODO check company
                    if company is None:
                        # TODO handle better
                        print("Verification failed due to invalid payload.")
                        abort(status.HTTP_400_BAD_REQUEST)
                    elif "Error" in company:
                        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        if company[1] != companyName:
                            # TODO handle this
                            abort(status.HTTP_400_BAD_REQUEST, "Company data doesn't match")
                        else:
                            updateUser = update_table("UPDATE Users SET Verified=? WHERE Email=?;", ["True", email])
                            # TODO check updateUser

                            user = select_from_database_table("SELECT * FROM Users WHERE Email=?", [email])
                            # TODO check user

                            # sending registration confirmation email to the user.
                            msg = Message("Thank you for registering, {} {}".format(user[2], user[3]),
                                          sender="thesearchbase@gmail.com",
                                          recipients=[email])
                            msg.body = "We appreciate you registering with TheSearchBase. A whole new world of possibilities is ahead of you."
                            mail.send(msg)

                            return redirect("/login")

                except IndexError:
                    # TODO handle better
                    print("Verification failed due to invalid payload.")
                    abort(status.HTTP_400_BAD_REQUEST)
            except BadSignature as e:
                encodedData = e.payload
                if encodedData is None:
                    msg = "Verification failed due to payload containing no data."
                    print(msg)
                    abort(status.HTTP_400_BAD_REQUEST, msg)
                else:
                    msg = ""
                    try:
                        verificationSigner.load_payload(encodedData)
                        msg = "Verification failed, bad signature"
                    except:
                        msg = "Verification failed"
                    finally:
                        print(msg)
                        abort(status.HTTP_400_BAD_REQUEST, msg)
        else:
            return redirect("/admin/homepage")


@app.route("/account/resetpassword", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("/accounts/resetpassword.html")
    else:
        abort(status.HTTP_501_NOT_IMPLEMENTED)

        # email = request.form.get("email", default="Error")
        # # TODO check this
        #
        # user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
        # # TODO check user
        #
        # if user is None:
        #     # TODO hadnle this better
        #     abort(status.HTTP_400_BAD_REQUEST, "User doesn't exist")
        # elif "Error" in user:
        #     # TODO handle this better
        #     abort(status.HTTP_500_INTERNAL_SERVER_ERROR, user)
        # else:
        #     company = get_company(email)
        #     if company is None or "Error" in company:
        #         # TODO handle this better
        #         abort(status.HTTP_500_INTERNAL_SERVER_ERROR, company)
        #     else:
        #         password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        #         # Generates a random password
        #
        #         updateUser = update_table("UPDATE Users SET Password=?, Verified=? WHERE Email=?;",
        #                                   [hash_password(password), "False"])
        #         # TODO check updateUser for errors
        #
        #         # TODO this needs improving
        #         msg = Message("Password reset",
        #                       sender="thesearchbase@gmail.com",
        #                       recipients=[email])
        #
        #         payload = email + ";" + company[1]
        #         link = "www.thesearchbase.com/account/verify/{}".format(verificationSigner.dumps(payload))
        #         msg.body = "Your password has been reset as per your request.\n" \
        #                    "Please visit <a href='{}'>this link</a> to verify your account.".format(email, link)
        #         mail.send(msg)
        #
        #         return


@app.route("/account/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("/accounts/changepassword.html")
    else:
        email = request.form.get("email", default="Error")
        currentPassword = request.form.get("currentPassword", default="Error")
        newPassword = request.form.get("newPassword", defaul="Error")
        # TODO check these

        user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
        # TODO check user
        if user[7] == "True":
            password = user[6]
            if hash_password(currentPassword, password) == password:
                hashedNewPassword = hash_password(newPassword)
                updatePassword = "UPDATE Users SET Password=? WHERE Email=?;", [hashedNewPassword, email]
                # TODO check updatePassword

                return render_template("/accounts/changepassword.html", "Success")
            else:
                return render_template("/accounts/changepassword.html", "Email and password don't match!")
        else:
            return render_template('errors/verification.html',
                                   msg="Account not verified, please check your email and follow instructions")


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
        abort(status.HTTP_501_NOT_IMPLEMENTED, "Affiliate program coming soon")
        # return render_template("affiliate.html")


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
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(e):
    return render('errors/400.html', error=e), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    return render('errors/404.html'), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def unsupported_media(e):
    return render('errors/415.html', error=e), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(418)
def im_a_teapot(e):
    return render('errors/418.html', error=e), 418


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render('errors/500.html', error=e), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(status.HTTP_501_NOT_IMPLEMENTED)
def not_implemented(e):
    return render('errors/501.html', error=e), status.HTTP_501_NOT_IMPLEMENTED


# Used to passthrough variables without repeating it in each method call
# IE assistant information
def render(template, **context):
    email = request.cookies.get("UserEmail")
    if email is not None:
        assistants = get_assistants(email)
        if assistants is not None:
            if "Error" in assistants:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

        assistantDetails = []
        for assistant in assistants:
            assistantDetails.append((assistant[0], assistant[5]))

        return render_template(template, debug=app.debug, assistantDetails=assistantDetails, **context)
    else:
        print("Render function redirects to login")
        return render_template("login.html", msg="You are not logged in!")


class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


if __name__ == "__main__":
    app.run(debug=True)
conn = None
try:
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    devseed = open(APP_ROOT + '/sql/devseed.sql', 'r').read()
    create_db = open(APP_ROOT + '/sql/createdb.sql', 'r').read()
    if app.debug:
        cur.executescript(create_db)
        cur.executescript(devseed)
        conn.commit()
        print("Applied devseed file")
    elif not os.path.exists(DATABASE):
        cur.executescript(create_db)
        conn.commit()
        print("Created database structure")
    cur.close()
except Exception as e:
    conn.rollback()
    print(e)
    exit(1)
finally:
    if conn is not None:
        conn.close()

# Janky way to seed password
if app.debug:
    hash = hash_password("test")
    update_table("UPDATE Users SET Password=? WHERE ID=?", [hash, 1])
