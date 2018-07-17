#!/usr/bin/python3
from flask_mail import Mail, Message
from flask import Flask, redirect, request, render_template, jsonify, send_from_directory, abort, escape, url_for, \
    make_response, g, session
from werkzeug.utils import secure_filename
from contextlib import closing
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
from urllib.request import urlopen

app = Flask(__name__, static_folder='static')
app.config.from_object('config.DevelopmentConfig')


verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE = APP_ROOT + "/database.db"
PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'

stripe.api_key = secret_key

stripe_keys = {
    'secret_key': secret_key,
    'publishable_key': pub_key
}

# stripe.api_key = stripe_keys['secret_key']




app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='thesearchbase@gmail.com',
    MAIL_PASSWORD='pilbvnczzdgxkyzy'
)

mail = Mail(app)


ALLOWED_IMAGE_EXTENSION = {'png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG'}
ALLOWED_PRODUCT_FILE_EXTENSIONS = {'json', 'JSON', 'xml', 'xml'}






def hash_password(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


def allowed_product_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_PRODUCT_FILE_EXTENSIONS


def allowed_image_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_IMAGE_EXTENSION



# TODO jackassify it
@app.route("/demo/<route><botID>", methods=['GET'])
def dynamic_popup(route, botID):
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
        return render_template("dynamic-popup.html", route=route, botID=botID, url=url)


# drop down routes.
@app.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        userID = query_db("SELECT * FROM Users WHERE ID=?;", [1], one=True)['ID']
        print(userID)
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
        msg = checkForMessage()
        return render_template("login.html", msg=msg)

    elif request.method == "POST":

        email = request.form.get("email", default="Error")
        password_to_check = request.form.get("password", default="Error")


        if email == "Error" or password_to_check == "Error":
            print("Invalid request: Email or password not received!")
            return redirectWithMessage("login", "Email or password not received!")

        else:
            email = email.lower()
            user = query_db("SELECT * FROM Users WHERE Email=?;", [email], one=True)

            # If user exists
            if user is not None:
                password = user['Password']
                if hash_password(password_to_check, password) == password:

                    verified = user['Verified']
                    print(verified == "True")

                    # If credentials are correct and users' account is verified
                    if verified == "True":

                        messages = dumps({"email": escape(email)})

                        # Set the session for the logged in user
                        session['User'] = user
                        session['Logged_in'] = True

                        # Store user assistants if they exist, in the session
                        assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?;",
                                            [user['CompanyID']])
                        if len(assistants) > 0:
                            session['UserAssistants'] =  assistants

                        # Test session specific values
                        print(session)
                        print(session.get('User')['Email'])
                        return redirect(url_for(".admin_home", messages=messages))

                    else:
                        return render_template('errors/verification.html',
                                               data="Account not verified, please check your email and follow instructions")
                else:
                    return redirectWithMessage("login", "User name and password does not match!")
            else:
                return redirectWithMessage("login", "User not found!")


@app.route('/logout')
def logout():

    # Will clear out the session.
    session.pop('User', None)
    session.pop('UserAssistants', None)
    session.pop('Logged_in', False)

    return redirect(url_for('login'))



# code to ensure user is logged in
@app.before_request
def before_request():

    theurl = str(request.url_rule)
    print(theurl)
    restrictedRoutes = ['/admin', 'admin/homepage']
    # If the user try to visit one of the restricted routes without logging in he will be redirected
    if any(route in theurl for route in restrictedRoutes) and not session.get('Logged_in', False):
        return redirectWithMessage("login", "You are not logged in!")




# Used to passthrough variables without repeating it in each method call
# IE assistant information
def render(template, **context):

    if session.get('Logged_in', False):
        return render_template(template, debug=app.debug, assistants=session.get('UserAssistants', []), **context)
    return render_template(template, debug=app.debug, **context)


def redirectWithMessage(function, message):
    messages = dumps({"msg": escape(message)})
    return redirect(url_for("."+function, messages=messages))

def checkForMessage():
    args = request.args
    msg=" "
    if len(args) > 0:
        messages = args['messages']
        if messages is not None:
            msg = loads(messages)['msg']
            if msg is None or msg == "None":
                msg = " "
    return msg

# TODO improve verification
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        msg = checkForMessage()
        return render_template("signup.html", debug=app.debug, msg=msg)
    elif request.method == "POST":


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
            return redirectWithMessage("signup", "Error in getting all input information")


        else:
            user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
            print(user)
            if user is not None:
                print("Email is already in use!")
                return redirectWithMessage("signup", "Email is already in use!")

            try:
                firstname = fullname.strip().split(" ")[0]
                surname = fullname.strip().split(" ")[1]

                #debug
                print(firstname)
                print(surname)

            except IndexError as e:
                return redirectWithMessage("signup", "Error in handling names")


            # Create a Stripe customer for the new company.
            new_customer = stripe.Customer.create(
                email=email
            )

            # debug
            print(new_customer)

            hashed_password = hash_password(password)
            verified = "False"

            # Create a company record for the new user
            insertCompanyResponse = insert_into_database_table(
                "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (companyName,companySize, websiteURL, companyPhoneNumber))

            company = get_last_row_from_table("Companies")

            # Create a user account and link it with the new created company record above
            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified') VALUES (?,?,?,?,?,?,?,?);",
                (company[0], firstname, surname, accessLevel, email, hashed_password, new_customer['id'], str(verified)))



            try:

                # Subscribe to the Basic plan with a trial of 14 days
                stripe.Subscription.create(
                customer=new_customer['id'],
                items=[{'plan': 'plan_D3lp2yVtTotk2f'}],
                trial_period_days=14,
                )



            except Exception as e:
                print(e)
                return redirectWithMessage("signup", "An error occurred and could not subscribe. Account has been created.")
                # TODO check subscription for errors https://stripe.com/docs/api#errors


            if not app.debug:
                # TODO this needs improving
                msg = Message("Account verification",
                              sender="thesearchbase@gmail.com",
                              recipients=[email])

                payload = email + ";" + companyName
                link = "https://www.thesearchbase.com/account/verify/"+verificationSigner.dumps(payload)
                msg.html = "<img src='https://thesearchbase.com/static/email_images/password_reset.png' style='width:500px;height:228px;'> <br /><p>You have registered with TheSearchBase!</p> <br>Please visit \
                            <a href='"+link+"'>this link</a> to verify your account."
                with app.open_resource("static\\email_images\\verify_email.png") as fp:
                    msg.attach("verify_email.png","image/png", fp.read())
                mail.send(msg)

                # sending the registration confirmation email to us
                msg = Message("A new company has signed up!",
                              sender="thesearchbase@gmail.com",
                              recipients=["thesearchbase@gmail.com"])
                msg.html = "<p>Company name: "+companyName+" has signed up. <br>The admin's details are: <br>Name: "+fullname+" <br>Email: "+email+".</p>"
                mail.send(msg)

            return render_template('errors/verification.html',
                                   msg="Please check your email and follow instructions to verify account and get started.")





# Data retrieval functions
def get_company(email):
    user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
    if user is not None and user is not "None" and user is not "Error":

        company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
        if company is not None and company is not "None" and company is not "Error":
            return company
        else:
            print("Error with finding company")
            return "Error"
    else:
        print("Error with finding user")
        return "Error"


def get_assistants(email):
    user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
    if user is not None and user is not "None" and user is not "Error":
        company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
        if company is not None and company is not "None" and company is not "Error":
            assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]], True)
            if assistants is not None and assistants is not "None" and assistants is not "Error":
                return assistants
            else:
                print("Error with finding assistants")
                return "Error"
        else:
            print("Error with finding company")
            return "Error"
    else:
        print("Error with finding user")
        return "Error"


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
                    return redirectWithMessage("login", "Please log in first!")
                sendEmail = True
            else:
                return redirectWithMessage("login", "Error in finding user!")
        else:
            email = request.cookies.get("UserEmail")
        statistics = [get_total_statistics(3, email), get_total_statistics(5, email)]
        if sendEmail:
            assistants = get_assistants(email)
            if assistants == "Error":
                return render_template("admin/main.html", stats=statistics, email=email, assistantIDs=[])
            assistantIDs = []
            for assistant in assistants:
                assistantIDs.append(assistant[0])
            return render("admin/main.html", stats=statistics, email=email, assistantIDs=assistantIDs)
        else:
            return render("admin/main.html", stats=statistics)

#data for the user which to be displayed on every admin page
@app.route("/admin/getAdminPagesData", methods=['POST'])
def adminPagesData():
    if request.method == "POST":
        email = request.cookies.get("UserEmail")
        user = select_from_database_table("SELECT Firstname FROM Users WHERE Email=?;", [email])[0]
        print(user)
        return user

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
        print(email)
        user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
        print(user)
        if user is None or user is "None" or user is "Error":
            user="Error in finding user"
        print(user)
        company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user[1]])
        if company is None or company is "None" or company is "Error":
            company="Error in finding company"
        print(company)
        print(email)
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
            return redirectWithMessage("profilePage", newEmail)
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
        msg = checkForMessage()
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        if assistants is None or "Error" in assistants:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error in getting your assistants!")
        return render("admin/create-assistant.html", autopop="Off", msg=msg)
    elif request.method == "POST":
        email = request.cookies.get("UserEmail")
        assistants = get_assistants(email)
        # Return the user to the page if has reached the limit of assistants
        if type(assistants) is type([]) and assistants:
            if len(assistants) >= 4:
                return redirectWithMessage("admin_assistant_create", "You have reached the limit of 3 chat bots")
        company = get_company(email)
        if company is None or "Error" in company:
            return redirectWithMessage("admin_assistant_create", "Error in getting company")
        else:
            nickname = request.form.get("nickname", default="Error")
            message = request.form.get("welcome-message", default="Error")
            autopopup = request.form.get("switch-autopop", default="off")
            popuptime = request.form.get("timeto-autopop", default="Error")

            if message is "Error" or nickname is "Error" or (popuptime is "Error" and autopopup is not "off"):
                return redirectWithMessage("admin_assistant_create", "Error in getting input information")
            else:
                if autopopup == "off":
                    secondsUntilPopup = "Off"
                else:
                    secondsUntilPopup = popuptime

                # Insert the new assistant to db
                newAssistant = insert_db("Assistants", ('CompanyID', 'Message', 'SecondsUntilPopup', 'Nickname'),
                                         (company[0], message, secondsUntilPopup, nickname))

                # Update the session to have the new added assistant
                session['UserAssistants'].append(newAssistant)
                session.modified = True


                if "Error" in newAssistant:
                    return redirectWithMessage("admin_assistant_create", "There was an error in creating your assistant")

                else:
                     return redirect("/admin/assistant/{}/settings".format(newAssistant['ID']))


@app.route("/admin/assistant/delete/<assistantID>", methods=['GET', 'POST'])
def admin_assistant_delete(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        userCompanyID = select_from_database_table("SELECT CompanyID FROM Users WHERE Email=?", [email])
        assistantCompanyID = select_from_database_table("SELECT CompanyID FROM Assistants WHERE ID=?", [assistantID])
        print(userCompanyID[0], "   ", assistantCompanyID[0])

        #Check if the user is from the company that owns the assistant
        if userCompanyID[0] == assistantCompanyID[0]:
            deleteAssistant = delete_from_table("DELETE FROM Assistants WHERE ID=?;",[assistantID])
            print(deleteAssistant)
            if deleteAssistant == "Record successfully deleted.":

                # Update user assistants list stored in the session
                assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?;",
                                      [session.get('User')['CompanyID']])
                if len(assistants) > 0:
                    session['UserAssistants'] = assistants
                else:
                    session['UserAssistants'] = []

                return redirect("/admin/homepage")
            else:
                return redirect("/admin/assistant/"+str(assistantID)+"/settings")
        else:
            return redirect("/admin/homepage")


@app.route("/admin/assistant/<assistantID>/settings", methods=['GET', 'POST'])
def admin_assistant_edit(assistantID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error in getting company")
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None or "Error" in assistant:
                abort(status.HTTP_404_NOT_FOUND, "Error in getting assistant")
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
                #dataTuple = tuple(["Null"])
                for i in range(0, len(questions)):
                    question = questions[i]
                    questionID = question[0]
                    userInput = select_from_database_table("SELECT * FROM UserInput WHERE QuestionID=?", [questionID],
                                                           True)
                    if(userInput != [] and userInput != None):
                        for record in userInput:
                            data.append(record)
                    ## TODO check userInput for errors
                    #inputTuple = ()
                    #for inputData in userInput:
                    #    input = inputData[3]
                    #    inputDate = inputData[2]
                    #    if len(inputTuple) == 0:
                    #        inputTuple = tuple([inputDate])
                    #    elif inputTuple[0] != inputDate:
                    #        dataTuple = dataTuple + inputTuple
                    #        data.append(dataTuple)
                    #        dataTuple = tuple(["Null"])
                    #        inputTuple = tuple([inputDate])
                    #    inputTuple = inputTuple + tuple([input])
                    #if len(userInput) > 0:
                    #    dataTuple = dataTuple + inputTuple
                    #    data.append(dataTuple)
                    #    dataTuple = tuple(["Null"])
                print(data)
                return render("admin/data-storage.html", data=data)


@app.route("/admin/assistant/<assistantID>/connect", methods=['GET'])
def admin_connect(assistantID):
    companyID = select_from_database_table("SELECT CompanyID FROM Assistants WHERE ID=?;", [assistantID])
    company = select_from_database_table("SELECT Name FROM Companies WHERE ID=?;", [companyID[0]])
    return render("admin/connect.html", company=company[0], assistantID=assistantID)


@app.route("/admin/templates", methods=['GET', 'POST'])
def admin_templates():
    if request.method == "GET":
        return render("admin/convo-template.html")
    elif request.method == "POST":
        abort(status.HTTP_501_NOT_IMPLEMENTED)



@app.route("/admin/pricing", methods=['GET'])
def admin_pricing():
    return render("admin/pricing-tables.html", pub_key=pub_key)

@app.route("/admin/adjustments", methods=['GET'])
def admin_pricing_adjust():
    return render("admin/pricing-adjustments.html")


@app.route('/admin/thanks', methods=['GET'])
def admin_thanks():
    return render('admin/thank-you.html')




def is_coupon_valid(coupon="Error"):
    try:
        stripe.Coupon.retrieve(coupon)
        return True
    except stripe.error.StripeError as e:
        print("coupon is not valid")
        return False




@app.route("/admin/check-out/<planID>", methods=['GET', 'POST'])
def admin_pay(planID):

    if request.method == 'GET':

        try:
            plan = stripe.Plan.retrieve(planID)
        except stripe.error.InvalidRequestError as e:
            abort(status.HTTP_400_BAD_REQUEST, "This plan does't exist! Make sure the plan ID is correct.")

        print(plan)
        return render("admin/check-out.html", plan=plan)


    if request.method == 'POST':

        # abort(status.HTTP_501_NOT_IMPLEMENTED)
        email = request.cookies.get("UserEmail")
        company = get_company(email)

        # Get the plan opject from Stripe API
        try:
            plan = stripe.Plan.retrieve(planID)
        except stripe.error.InvalidRequestError as e:
            abort(status.HTTP_400_BAD_REQUEST, "This plan does't exist! Make sure the plan ID is correct.")


        # Check of a company is logged in TODO we should use sessions later
        if company is None or "Error" in company:
            return redirectWithMessage("login", "Please log in first!")


        # Validate the given coupon.
        coupon = request.form.get("coupon", default="Error")
        if coupon == "" or coupon is None or coupon == "Error":
            print("make no use of coupons")
            # If coupon is not provided set it to None as Stripe API require.
            coupon = "None"


        if not (is_coupon_valid(coupon)):
            return render("admin/check-out.html", error="The coupon used is not valid")


        # Get Stripe token generated using JavaScript in the client-side
        token = request.form.get("tokenId", default="Error")
        print(">>>> The token: "+ token)
        if token is "Error":
            # TODO improve this
            abort(status.HTTP_400_BAD_REQUEST)


        # If no errors occurred, subscribe the user to plan.
        else:
            # Get the user by email
            user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
            try:
                subscription = stripe.Subscription.create(
                    customer=user[7],
                    source=token,
                    coupon=coupon,
                    items=[
                        {
                            "plan": planID,
                        },
                    ]
                )

                # if everything is ok activate assistants
                update_table("UPDATE Assistants SET Active=? WHERE CompanyID=?", ["True", user[1]])


            except Exception as e:
                print(e)
                abort(status.HTTP_400_BAD_REQUEST, "An error occurred and could not subscribe.")
                # TODO check subscription for errors https://stripe.com/docs/api#errors



            print("You have successfully subscribed!")
            return render("admin/pricing-tables.html", msg="You have successfully subscribed!")


@app.route("/admin/check-out/checkPromoCode", methods=['POST'])
def checkPromoCode():
    if request.method == 'POST':

        # abort(status.HTTP_501_NOT_IMPLEMENTED)
        email = request.cookies.get("UserEmail")
        company = get_company(email)

        if company is None or "Error" in company:
            # TODO handle this better, as it's payments so is very important we don't charge the customer etc
            return redirectWithMessage("login", "Please log in first!")

        else:

            # TODO: check the promoCode from user then response with yes or no with json
            promoCode = str(request.data, 'utf-8')
            if promoCode == 'abc':
                return jsonify(isValid=True)
            else:
                return jsonify(isValid=False)



@app.route("/admin/unsubscribe", methods=['POST'])
def unsubscribe():

    if request.method == 'POST':
        email = request.cookies.get("UserEmail")
        company = get_company(email)

        # Check of a company is logged in TODO we should use sessions later
        if company is None or "Error" in company:
            return redirect("/login")

        # Get company Stripe subscription ID
        user = select_from_database_table("SELECT * FROM Users WHERE CompanyID=?", [company[0]])
        subID = user[9]


        if subID is None or subID == "" or subID == "null" :
            abort(status.HTTP_404_NOT_FOUND, "This account has no active subscriptions ")

        try:
            sub = stripe.Subscription.retrieve(subID)
            sub.delete()
        except Exception as e:
            abort(status.HTTP_400_BAD_REQUEST, "An error occurred while trying to unsubscribe")


# Stripe Webhooks
@app.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhook_subscription_cancelled():
    if request.method == "POST":
        try:

            event_json = request.get_json(force=True)
            customerID = event_json['data']['object']['customer']
            print(customerID)

            user = select_from_database_table("SELECT * FROM Users WHERE StripeID=?", [customerID])
            # TODO check company for errors
            assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?", [user[1]], True)

            # Check if user has assistants to deactivate first
            if len(assistants) > 0:
                for assistant in assistants:

                    updateAssistant = update_table("UPDATE Assistants SET Active=? WHERE ID=?", ["False", assistant[0]])
                    # TODO check update assistant for errors

        except Exception as e:
            abort(status.HTTP_400_BAD_REQUEST, "Error in Webhook event")


        return "Assistants for " + user[5] + " account has been deactivated due to subscription cancellation", status.HTTP_200_OK



# TODO implement this
@app.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics(assistantID):
    if request.method == "GET":
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
        if userLevel is None or "Error" in userLevel or userLevel == "User":
            return redirect("/admin/homepage")
        else:
            # TODO improve this
            users = select_from_database_table("SELECT * FROM Users WHERE CompanyID=?", [companyID], True)
            return render("admin/users.html", users=users, email=email)

@app.route("/admin/users/add", methods=['POST'])
def admin_users_add():
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
            print("A textbox has not been filled")
            #TODO pass in feedback message
            return redirect("/admin/users", code=302)
        else:
            newEmail = newEmail.lower()
            user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [newEmail])
            print(user)
            if user is not None:
                print("Email is already in use!")
                #TODO Return feedback message
                return redirect("/admin/users", code=302)
            try:
                firstname = fullname.split(" ")[0]
                surname = fullname.split(" ")[1]
            except IndexError as e:
                print("Error in splitting")
                #TODO pass in feedback message
                redirect("/admin/users", code=302)
            hashed_password = hash_password(password)

            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
                (companyID, firstname, surname, accessLevel, newEmail, hashed_password, "True"))
            if "added" not in insertUserResponse:
                print("Error in insert operation")
                #TODO pass in feedback message
                redirect("/admin/users", code=302)
            else:
                #if not app.debug:

                # sending email to the new user.
                # TODO this needs improving
                link = "https://www.thesearchbase.com/admin/changepassword"
                msg = Message("Account verification, "+firstname+" "+surname,
                              sender="thesearchbase@gmail.com",
                              recipients=[newEmail])
                msg.html = "<p>You have been registered with TheSearchBase by an Admin at your company.<br> \
                            If you feel this is a mistake please contact "+email+".<br> \
                            Your temporary password is: "+password+".<br>\
                            Please visit <a href='"+link+"'>this link</a> to set password for your account.<p>"
                mail.send(msg)
                #TODO return feedbackmessage
                return redirect("/admin/users")

@app.route("/admin/users/modify", methods=["POST"])
def admin_users_modify():
    if request.method == "POST":
        email = request.cookies.get("UserEmail")
        userID = request.form.get("userID", default="Error")
        newAccess = request.form.get("accessLevel", default="Error")
        if userID != "Error" and newAccess != "Error":
            updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE ID=?;", [newAccess, userID])
            if newAccess == "Owner":
                updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE Email=?;", ["Admin", email])
                #TODO return feedbackmessage
                return redirect("/admin/users", code=302)
        #TODO return feedbackmessage
        return redirect("/admin/users", code=302)

@app.route("/admin/users/delete/<userID>", methods=["GET"])
def admin_users_delete(userID):
    if request.method == "GET":
        email = request.cookies.get("UserEmail")
        company = get_company(email)
        # todo check company
        companyID = company[0]

        requestingUser = select_from_database_table("SELECT * FROM Users WHERE Email=?", [email])
        targetUser = select_from_database_table("SELECT CompanyID FROM Users WHERE ID=?", [userID])[0]
        if requestingUser[4] == "User" or requestingUser[1] != targetUser:
            #TODO send feedback message
            return redirect("/admin/homepage", code=302)
        delete_from_table("DELETE FROM Users WHERE ID=?;", [userID])
        return redirect("/admin/users", code=302)


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


@app.route("/chatbot/<companyName>/<assistantID>", methods=['GET', 'POST'])
def chatbot(companyName, assistantID):
    if request.method == "GET":
        company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [escape(companyName)])

        # for debugging
        print(escape(companyName))
        print(company)

        if company is None:
            abort(status.HTTP_400_BAD_REQUEST, "This company does't exist")

        # TODO check company for errors
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=?;", [assistantID])

        if assistant is None:
            abort(status.HTTP_400_BAD_REQUEST, "This Assistant does't exist")

        # for debugging
        print(assistant)


        # TODO check assistant for errors
        # assistantIndex = 0  # TODO implement this properly
        # assistantID = assistant[assistantIndex][0]

        # is assistant active ? True/False
        assistantActive = assistant[6]

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

            message = assistant[3]
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

            return render_template("dynamic-chatbot.html", data=questionsAndAnswers, user="chatbot/" + companyName + "/" + assistantID,
                                   message=message)
    elif request.method == "POST":


        company = select_from_database_table("SELECT * FROM Companies WHERE Name=?;", [escape(companyName)], True)

        if company is None:
            abort(status.HTTP_400_BAD_REQUEST, "This company does't exist")


        # TODO check company for errors
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]], True)

        if assistant is None:
            abort(status.HTTP_400_BAD_REQUEST, "This Assistant does't exist")

        # TODO check assistant for errors
        # assistantIndex = 0  # TODO implement this properly

        questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?", [assistantID], True)
        # TODO check questions for errors
        print(questions)
        products = select_from_database_table("SELECT * FROM Products WHERE AssistantID=?;", [assistantID], True)
        # TODO check products for errors

        lastSessionID = select_from_database_table("SELECT * FROM UserInput", [])
        if lastSessionID is None or not lastSessionID:
            lastSessionID = 1
        else:
            lastSessionID = lastSessionID[len(lastSessionID)-1][4] + 1

        collectedInformation = request.form.get("collectedInformation").split("||")
        date = datetime.now().strftime("%d-%m-%Y")
        for i in range(0, len(collectedInformation)):
            questionIndex = int(collectedInformation[i].split(";")[0]) - 1
            input = collectedInformation[i].split(";")[1]
            questionID = int(questions[questionIndex][0])
            for question in questions:
                if question[0] == questionID:
                    questionName = question[2]
            for question in questions:
                if question[0] == questionID:
                    questionName = question[2]
            insertInput = insert_into_database_table("INSERT INTO UserInput (QuestionID, Date, Input, SessionID, QuestionString) VALUES (?,?,?,?,?)", (questionID, date, input, lastSessionID, questionName))
            # TODO check insertInput for errors

        #lastSessionID = select_from_database_table("SELECT TOP(1) * FROM UserInput ORDER BY ID DESC", [], True)[0]
        #TODO needs improving

        fileUploads = request.form.get("fileUploads", default="Error");
        if "Error" not in fileUploads:
            fileUploads = fileUploads.split("||");
            for i in range(0, len(fileUploads)):
                file = urlopen(fileUploads[i].split(":::")[0])
                filename = fileUploads[i].split(":::")[2]
                print(date,"-----", lastSessionID, "------", fileUploads[i].split(":::")[1], "------", filename)
                filename = date + '_' + str(lastSessionID) + '_' + fileUploads[i].split(":::")[1] + '_' + filename
                #filename = secure_filename(filename)

                #if file and allowed_file(filename):
                if file:
                    open(os.path.join(USER_FILES, filename), 'wb').write(file.read())
                    savePath = "static"+os.path.join(USER_FILES, filename).split("static")[len(os.path.join(USER_FILES, filename).split("static")) - 1]
                    for question in questions:
                        if question[0] == questionID:
                            questionName = question[2]
                    for question in questions:
                        if question[0] == questionID:
                            questionName = question[2]
                    insertInput = insert_into_database_table("INSERT INTO UserInput (QuestionID, Date, Input, SessionID, QuestionString) VALUES (?,?,?,?,?)", (fileUploads[i].split(":::")[1], date, fileUploads[i].split(":::")[2]+";"+savePath, lastSessionID, questionName))

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
                        msg.body = "<img src='https://thesearchbase.com/static/email_images/welcome.png' style='width:500px;height:228px;'> <br /> We appreciate you registering with TheSearchBase. A whole new world of possibilities is ahead of you."
                        with app.open_resource("static\\email_images\\welcome.png") as fp:
                            msg.attach("welcome.png","image/png", fp.read())
                        mail.send(msg)

                        return redirectWithMessage("login", "Thank you for verifying.")

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


@app.route("/account/resetpassword", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("/accounts/resetpassword.html")
    else:
         email = request.form.get("email", default="Error")
         # TODO check this

         user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
         # TODO check user

         if user is None or "Error" in user:
             return redirectWithMessage("login", "Error in finding user!")
         else:
             company = get_company(email)
             if company is None or "Error" in company:
                 return redirectWithMessage("login", "Error in finding company!")
             else:
                 # TODO this needs improving
                 msg = Message("Password reset",
                               sender="thesearchbase@gmail.com",
                               recipients=[email])

                 payload = email + ";" + company[1]
                 link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
                 msg.html ="<img src='https://thesearchbase.com/static/email_images/password_reset.png' style='width:500px;height:228px;'><br /><p>Your password has been reset as per your request.<br/ >Please visit <a href='"+link+"'>this link</a> to verify your account.</p>"
                 with app.open_resource("static\\email_images\\password_reset.png") as fp:
                     msg.attach("password_reset.png","image/png", fp.read())
                 mail.send(msg)

                 return redirect("/errors/verification_password.html", code=302)

@app.route("/account/resetpassword/<payload>", methods=['GET', 'POST'])
def reset_password_verify(payload):
    if request.method == "GET":
        data = ""
        try:
            print(payload)
            data = verificationSigner.loads(payload)
            print(data)
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
                        # Everything checks out
                        return render_template("/accounts/resetpasswordset.html", email=email, payload=payload)

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
        email = request.form.get("email", default="Error")
        password = request.form.get("password", default="Error")
        hashedNewPassword = hash_password(password)
        updatePassword = update_table("UPDATE Users SET Password=? WHERE Email=?;", [hashedNewPassword, email])
        return redirectWithMessage("login", "Password has been changed.")


@app.route("/admin/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("/accounts/changepassword.html")
    else:
        email = request.cookies.get("UserEmail")
        currentPassword = request.form.get("currentPassword", default="Error")
        newPassword = request.form.get("newPassword", default="Error")
        # TODO check these

        user = select_from_database_table("SELECT * FROM Users WHERE Email=?;", [email])
        # TODO check user
        print(currentPassword, "   ", newPassword)
        if user[8] == "True":
            password = user[6]
            if hash_password(currentPassword, password) == password:
                hashedNewPassword = hash_password(newPassword)
                updatePassword = update_table("UPDATE Users SET Password=? WHERE Email=?;", [hashedNewPassword, email])
                # TODO check updatePassword
                print(updatePassword)
                return render_template("/accounts/changepassword.html", msg="Password has been successfully changed.")
            else:
                return render_template("/accounts/changepassword.html", msg="Old password is incorrect!")
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
    return query_db("SELECT * FROM " + table + " WHERE ROWID IN ( SELECT max( ROWID ) FROM " + table +" );", one=True)





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


# ====\ Database (Connection & Initialisation) /====

# Connects to the specific database.
def connect_db():
    print("Connect to DB")
    return sqlite3.connect(DATABASE)


# Initializes the database with test data while in debug mode.
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(APP_ROOT + '/sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        if app.debug:
            with app.open_resource(APP_ROOT + '/sql/devseed.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                # Create and store a hashed password for "test" user
                hash = hash_password("test")
                update_table("UPDATE Users SET Password=? WHERE ID=?", [hash, 1])
            db.commit()

    print("Database Initialized")


# facilitate querying data from the database.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def insert_db(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    row = query_db("SELECT * FROM " + table + " WHERE ID=?", [cur.lastrowid], one=True)
    cur.close()
    return row



# Get connection when no requests e.g Pyton REPL.
def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db


@app.before_request
def before_request():
    print("Before Request")
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    # Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()
        print("Connection Closed")





## Error Handlers ##
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(e):
    print("Error Handler:" + e.description)
    return render_template('errors/400.html', error=e.description), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    print("Error Handler:" + e.description)
    return render_template('errors/404.html', error= e.description), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def unsupported_media(e):
    print("Error Handler:" + e.description)
    return render_template('errors/415.html', error=e.description), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(418)
def im_a_teapot(e):
    print("Error Handler:" + e.description)
    return render_template('errors/418.html', error=e.description), 418


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    print("Error Handler for:" + e.description)
    return render_template('errors/500.html', error=e.description), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(status.HTTP_501_NOT_IMPLEMENTED)
def not_implemented(e):
    print("Error Handler:" + e.description)
    return render_template('errors/501.html', error=e.description), status.HTTP_501_NOT_IMPLEMENTED



class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


if __name__ == "__main__":
    print("TEST TEST TEST")
    app.run(debug=True)

# Create the schema
init_db()
