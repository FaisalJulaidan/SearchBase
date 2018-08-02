#/usr/bin/python3.5
from flask import Flask, redirect, request, render_template, jsonify, send_from_directory, abort, escape, url_for, \
    make_response, g, session, json
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from contextlib import closing
from flask_api import status
from datetime import datetime, timedelta
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
from cryptography.fernet import Fernet
import urllib.request

app = Flask(__name__, static_folder='static')


## -----
# Only one should be commented in
# For Production
#app.config.from_object('config.BaseConfig')
 
# For Development
app.config.from_object('config.DevelopmentConfig')
## -----

verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE = APP_ROOT + "/database.db"
PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'
encryption = None

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

NoPlan = {"MaxProducts":0, "ActiveBotsCap":0, "InactiveBotsCap":0, "AdditionalUsersCap":0, "ExtendedLogic":False, "ImportDatabase":False, "CompanyNameonChatbot": False}
BasicPlan = {"MaxProducts":600, "ActiveBotsCap":2, "InactiveBotsCap":3, "AdditionalUsersCap":5, "ExtendedLogic":False, "ImportDatabase":False, "CompanyNameonChatbot": False}
AdvancedPlan = {"MaxProducts":5000, "ActiveBotsCap":4, "InactiveBotsCap":8, "AdditionalUsersCap":10, "ExtendedLogic":True, "ImportDatabase":True, "CompanyNameonChatbot": True}
UltimatePlan = {"MaxProducts":30000, "ActiveBotsCap":10, "InactiveBotsCap":30, "AdditionalUsersCap":999, "ExtendedLogic":True, "ImportDatabase":True, "CompanyNameonChatbot": True}
#count_db("Plans", " WHERE Nickname=?", ["basic",])

def hash_password(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


def allowed_product_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_PRODUCT_FILE_EXTENSIONS


def allowed_image_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_IMAGE_EXTENSION


# code to ensure user is logged in
@app.before_request
def before_request():
    print(encryption)
    theurl = str(request.url_rule)
    restrictedRoutes = ['/admin', 'admin/homepage']
    # If the user try to visit one of the restricted routes without logging in he will be redirected
    if any(route in theurl for route in restrictedRoutes) and not session.get('Logged_in', False):
        return redirectWithMessage("login", "Please log in first")
    #if on admin route
    if any(route in theurl for route in restrictedRoutes):
        #Check user permissions as user type
        if not session['Permissions']["EditChatbots"] and "/admin/assistant" in theurl:
            return redirect("/admin/homepage", code=302)
        if not session['Permissions']["EditUsers"] and "/admin/users" in theurl:
            return redirect("/admin/homepage", code=302)
        if not session['Permissions']["AccessBilling"] and "/admin/assistant/" in theurl:
            return redirect("/admin/homepage", code=302)

        #Check user plan permissions
        print("PLAN:", session.get('UserPlan', []))
    

def checkAssistantID(assistantID):
    assistantRecord = query_db("SELECT * FROM Assistants WHERE ID=?", [assistantID,], True)
    if assistantRecord is None:
        return redirect("/admin/homepage", code=302)
    elif session.get('User')['CompanyID'] is not assistantRecord['CompanyID']:
        return redirect("/admin/homepage", code=302)


# TODO jackassify it
@app.route("/demo/<route><botID>", methods=['GET'])
def dynamic_popup(route, botID):
    if request.method == "GET":
        url = "http://www.example.com/"
        companies = query_db("SELECT * FROM Companies")
        # If company exists
        for record in companies:
            if record["Name"] == escape[route]:
                company = record
            else:
                abort(status.HTTP_404_NOT_FOUND)
        url = company["URL"]
        if "http" not in url:
            url = "https://" + url
        return render_template("dynamic-popup.html", route=route, botID=botID, url=url)


# drop down routes.
@app.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        # query_db("UPDATE Users SET SubID=? WHERE ID=?;", ('dfg', 1))
        # update_table("UPDATE Users SET SubID=? WHERE ID=?;",
        #              ['ddd', 1])
        return render_template("index.html")

@app.route("/setencryptionkey<key>", methods=["GET"])
def testing(key):
    if app.debug:
        serverRoute = "http://127.0.0.1:5000"
        if "gT5-f" in key:
            key = key.split("gT5-f")[1] + key.split("gT5-f")[0]
            key = key.replace("gT5-f", "").replace("Pa-", "5o_n").replace("uF-r", "UbwF")
    else:
        serverRoute = "https://www.thesearchbase.com"
    page = urllib.request.urlopen(serverRoute + "/static/js/sortTable.js")
    text = page.read().decode("utf8")
    part1 = text.split("FD-Y%%$VfdsaGSdsHB-%$-DFmrcStFa-S")[1].split("FEAewSvj-JGvbhKJQz-xsWEKc3-WRxjhT")[0].replace('La', 'H-q').replace('TrE', 'gb')
    page = urllib.request.urlopen(serverRoute + "/static/js/Chart.bundle.js")
    text = page.read().decode("utf8")
    part2 = text.split("GFoiWS$344wf43-cWzHOp")[1].split("Ye3Sv-FE-vWaIt3xWkbE6bsd7-jS")[0].replace('8B', '3J')
    page = urllib.request.urlopen(serverRoute + "/static/css/admin.css")
    text = page.read().decode("utf8")
    part3 = text.split(".tic")[1].split("Icon")[0]
    page = urllib.request.urlopen(serverRoute + "/static/css/themify-icons.css")
    text = page.read().decode("utf8")
    part4 = text.split("YbfEas-fUh")[1].split("TbCO")[0].replace('P-', '-G')
    if not app.debug:
        page = urllib.request.urlopen("https://bjhbcjvrawpiuqwyrzwxcksndmwpeo.herokuapp.com/static/skajhefjwehfiuwheifhxckjbachowejfhnkjfnlwgifnwoihfuwbkjcnkjfil.html")
        text = page.read().decode("utf8")
        part5 = text.split("gTb2I-6BasRb41BVr6fg-heWpB0-")[1].split("-PoWb5qEc-sMpAp-4BaOln")[0].replace('-9yR', '_nU')
    else:
        part5 = ""
    enckey = part1+part2+part3+part4+part5
    enckey = ((enckey+key).replace(" ", "")).encode()
    global encryption
    encryption = Fernet(enckey)
    print(encryption)
    return "Done"


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
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)

        email = request.form.get("email", default="Error")
        password_to_check = request.form.get("password", default="Error")


        if email == "Error" or password_to_check == "Error":
            print("Invalid request: Email or password not received!")
            return redirectWithMessage("login", "You entered an incorrect username or password.")

        else:
            email = email.lower()
            users = query_db("SELECT * FROM Users")
            # If user exists
            for user in users:
                if user["Email"] == email:
                    password = user['Password']
                    if hash_password(password_to_check, password) == password:

                        verified = user['Verified']

                        # If credentials are correct and users' account is verified
                        if verified == "True":

                            messages = dumps({"email": escape(email)})

                            # Set the session for the logged in user
                            session['User'] = user
                            session['Logged_in'] = True

                            # Store user assistants if they exist, in the session
                            assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?;",
                                                [user['CompanyID']])

                            #Store users access permisions
                            session['UserAssistants'] =  assistants
                            permissionsDic = {}
                            permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]
                            if "Owner" in session.get('User')['AccessLevel']:
                                permissions = permissions["AdminPermissions"].split(";")
                                for perm in permissions:
                                    if perm:
                                        permissionsDic[perm.split(":")[0]] = True
                            else:
                                permissions = permissions[session.get('User')['AccessLevel']+"Permissions"].split(";")
                                for perm in permissions:
                                    if perm:
                                        if "True" in perm.split(":")[1]:
                                            permBool = True
                                        else:
                                            permBool = False
                                        permissionsDic[perm.split(":")[0]] = permBool
                            session['Permissions'] = dict(permissionsDic)

                            # Set user plan e.g. (Basic, Ultimate...)
                            session['UserPlan'] = {}
                            session['UserPlan']['Nickname'] =  getPlanNickname(user['SubID'])
                            if getPlanNickname(user['SubID']) is None:
                                session['UserPlan']['Settings'] = NoPlan
                            elif "Basic" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = BasicPlan
                            elif "Advanced" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = AdvancedPlan
                            elif "Ultimate" in getPlanNickname(user['SubID']):
                                session['UserPlan']['Settings'] = UltimatePlan

                            # Test session specific values
                            print(session)

                            return redirect("/admin/homepage", code=302)

                        else:
                            return redirectWithMessage("login", "Please verify your account before you log in.")
            return redirectWithMessage("login", "You entered an incorrect username or password.")


@app.route('/logout')
def logout():

    # Will clear out the session.
    session.pop('User', None)
    session.pop('UserAssistants', None)
    session.pop('Logged_in', False)

    return redirect(url_for('login'))

def getPlanNickname(SubID=None):
    try:
        # Get subscription object from Stripe API
        subscription = stripe.Subscription.retrieve(SubID)

        # Debug
        print(subscription)

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return subscription["items"]["data"][0]["plan"]["nickname"]

    except stripe.error.StripeError as e:
        return None




# Used to passthrough variables without repeating it in each method call
# IE assistant information
def render(template, **context):

    if session.get('Logged_in', False):
        return render_template(template, debug=app.debug, assistants=session.get('UserAssistants', []), **context)
    return render_template(template, debug=app.debug, **context)

def redirectWithMessage(function, message):
    return redirect(url_for("."+function, messages=message))

def checkForMessage():
    args = request.args
    msg=" "
    if len(args) > 0:
        msg = args['messages']
    return msg

def redirectWithMessageAndAssistantID(function, assistantID, message):
    return redirect(url_for("." + function, assistantID=assistantID, message=message))

def checkForMessageWhenAssistantID():
        try:
            message = request.args["message"]
        except:
            message = " "
        return message

# TODO improve verification
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        msg = checkForMessage()
        return render_template("signup.html", debug=app.debug, msg=msg)
    elif request.method == "POST":


        email = request.form.get("email", default="Error").lower()

        fullname = request.form.get("fullname", default="Error")
        accessLevel = "Owner"
        password = request.form.get("password", default="Error")

        companyName = request.form.get("companyName", default="Error")
        companySize = request.form.get("companySize", default="0")
        companyPhoneNumber = request.form.get("phoneNumber", default="Error")
        websiteURL = request.form.get("websiteURL", default="Error")


        if fullname == "Error" or accessLevel == "Error" or email == "Error" or password == "Error" \
                or companyName == "Error" or websiteURL == "Error":
            print("Invalid request")
            return redirectWithMessage("signup", "Error in getting all input information")


        else:
            users = query_db("SELECT * FROM Users")
            # If user exists
            for user in users:
                if user["Email"] == email:
                    print("Email is already in use!")
                    return redirectWithMessage("signup", "Email already in use.")
            try:
                firstname = fullname.strip().split(" ")[0]
                surname = fullname.strip().split(" ")[1]

                #debug
                print(firstname)
                print(surname)

            except IndexError as e:
                return redirectWithMessage("signup", "Error in handling names")

            newUser = None
            newCompany = None
            newCustomer = None

            # Create a Stripe customer for the new company.
            newCustomer = stripe.Customer.create(
                email=email
            )

            # debug
            # print(newCustomer)

            hashed_password = hash_password(password)
            if app.debug:
                verified = "True"
            else:
                verified = "False"



            # Create a company record for the new user
            #ENCRYPTION
            insertCompanyResponse = insert_into_database_table(
                "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (encryptVar(companyName), encryptVar(companySize), encryptVar(websiteURL), encryptVar(companyPhoneNumber)))
            #insertCompanyResponse = insert_into_database_table(
             #   "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (companyName, companySize, websiteURL, companyPhoneNumber))

            newCompany = get_last_row_from_table("Companies")
            # print(newCompany)
            
            createUserSettings = insert_into_database_table("INSERT INTO UserSettings('CompanyID') VALUES (?);", (newCompany['ID'],))
            #TODO validate insertCompanyResponse and createUserSettings

            try:

                # Subscribe to the Basic plan with a trial of 14 days
                sub = stripe.Subscription.create(
                customer=newCustomer['id'],
                items=[{'plan': 'plan_D3lp2yVtTotk2f'}],
                trial_period_days=14,
                )


                print(sub['items']['data'][0]['plan']['nickname'])
                # print(sub)

                # Create a user account and link it with the new created company record above
                #ENCRYPTION
                newUser = insert_db("Users", ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified', 'SubID'),
                            (newCompany['ID'], encryptVar(firstname), encryptVar(surname), accessLevel, encryptVar(email), hashed_password, newCustomer['id'],
                            str(verified), sub['id'])
                            )
                #newUser = insert_db("Users", ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified', 'SubID'),
                 #           (newCompany['ID'], firstname, surname, accessLevel, email, hashed_password, newCustomer['id'],
                  #          str(verified), sub['id'])
                   #         )



            except Exception as e:
                # Clear out when exception
                if newUser is not None:
                    query_db("DELETE FROM Users WHERE ID=?", [newUser['ID']])
                    print("Delete new user")

                if newCompany is not None:
                    query_db("DELETE FROM Companies WHERE ID=?", [newCompany['ID']])
                    print("Delete new company")

                print("Delete new user' stripe account")
                if newCustomer is not None:
                    cus = stripe.Customer.retrieve(newCustomer['id'])
                    cus.delete()

                print(e)
                return redirectWithMessage("signup", "An error occurred and could not subscribe. Please try again!.")
                # TODO check subscription for errors https://stripe.com/docs/api#errors


            if not app.debug:
                # TODO this needs improving
                msg = Message("Account verification",
                                sender="thesearchbase@gmail.com",
                                recipients=[email])
                payload = email + ";" + companyName
                link = "https://www.thesearchbase.com/account/verify/"+verificationSigner.dumps(payload)
                msg.html = "<img src='https://thesearchbase.com/static/email_images/verify_email.png'><br /><h4>Hi,</h4> <p>Thank you for registering with TheSearchbase.</p> <br />  There is just one small step left, visit \
                            <a href='"+link+"'> this link </a> to verify your account. \
                            In case the link above doesn't work you can click on the link below. <br /> <br /> " + link + " <br />  <br /> \
                            We look forward to you, using our platform. <br /> <br />\
                            Regards, <br /> TheSearchBase Team <br />\
                            <img src='https://thesearchbase.com/static/email_images/footer_image.png'>"
                mail.send(msg)

                # sending the registration confirmation email to us
                msg = Message("A new company has signed up!",
                                sender="thesearchbase@gmail.com",
                                recipients=["thesearchbase@gmail.com"])
                msg.html = "<p>Company name: "+companyName+" has signed up. <br>The admin's details are: <br>Name: "+fullname+" <br>Email: "+email+".</p>"
                mail.send(msg)

            return render_template('errors/verification.html', msg="Please check your email and follow instructions to verify account and get started.")



# Data retrieval functions
def get_company(email):
    users = query_db("SELECT * FROM Users")
    # If user exists
    for user in users:
        if user["Email"] == email:
            company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user["CompanyID"]])
            if company is not None and company is not "None" and company is not "Error":
                return company
            else:
                print("Error with finding company")
                return "Error"
    print("Error with finding user")
    return "Error"


def get_assistants(email):
    users = query_db("SELECT * FROM Users")
    # If user exists
    for user in users:
        if user["Email"] == email:
            company = select_from_database_table("SELECT * FROM Companies WHERE ID=?;", [user["CompanyID"]])
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
        email = session.get('User')['Email'] 
        statistics = [get_total_statistics(3, email), get_total_statistics(5, email)]
        if sendEmail:
            assistants = get_assistants(email)
            if assistants == "Error":
                return render_template("admin/main.html", stats=statistics, assistantIDs=[])
            assistantIDs = []
            for assistant in assistants:
                assistantIDs.append(assistant[0])
            return render("admin/main.html", stats=statistics, assistantIDs=assistantIDs)
        else:
            return render("admin/main.html", stats=statistics)

#data for the user which to be displayed on every admin page
@app.route("/admin/getadminpagesdata", methods=['POST'])
def adminPagesData():
    if request.method == "POST":
        email = session.get('User')['Email']
        users = query_db("SELECT * FROM Users")
        # If user exists
        for user in users:
            if user["Email"] == email:
                returnString = ""
                permissions = ""
                for key,value in session['Permissions'].items():
                    permissions+= key + ":" + str(value) + ";"
                planSettings = ""
                for key,value in session['UserPlan']['Settings'].items():
                    planSettings += key + ":" + str(value) + ";"
                return user["Firstname"] + "&&&" + permissions + "&&&" + planSettings
        return "wait...Who are you?"



#data for the user which to be displayed on every admin page
@app.route("/admin/userData", methods=['GET'])
def getUserData():
    if request.method == "GET":
        userDict = {
            "id": session['User']['ID'],
            "email": session['User']['Email'],
            "firstname": session['User']['Firstname'],
            "surname": session['User']['Surname'],
            "stripeID": session['User']['StripeID'],
            "subID": session['User']['SubID'],

        }
        return jsonify(userDict)



@app.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        message = checkForMessage()
        email = session.get('User')['Email']
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == email:
                user = record
        if "Error" in user:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error in finding user!")
        company = query_db("SELECT * FROM Companies WHERE ID=?;", [user["CompanyID"]])
        if company is None or company is "None" or company is "Error":
            company="Error in finding company"
        print(company)
        print(user)
        print(email)
        return render_template("admin/profile.html", user=user, email=email, company=company[0], message=message)

    elif request.method == "POST":
        curEmail = session.get('User')['Email']
        names = request.form.get("names", default="Error")
        newEmail = request.form.get("email", default="error").lower()
        companyName = request.form.get("companyName", default="Error")
        companyURL = request.form.get("companyURL", default="error").lower()
        if names != "Error" and newEmail != "error" and companyURL != "error" and companyName != "Error":
            names = names.split(" ")
            name1 = names[0]
            name2 = names[1]
            users = query_db("SELECT * FROM Users")
            # If user exists
            for user in users:
                if user["Email"] == curEmail:
                    #TODO check if they worked
                    #ENCRYPTION
                    updateUser = update_table("UPDATE Users SET Firstname=?, Surname=?, Email=? WHERE ID=?;", [encryptVar(name1),encryptVar(name2),encryptVar(newEmail),user["ID"]])
                    #updateUser = update_table("UPDATE Users SET Firstname=?, Surname=?, Email=? WHERE ID=?;", [name1,name2,newEmail,user["ID"]])
                    companyID = select_from_database_table("SELECT CompanyID FROM Users WHERE ID=?;", [user["ID"]])
                    updateCompany = update_table("UPDATE Companies SET Name=?, URL=? WHERE ID=?;", [encryptVar(companyName),encryptVar(companyURL),companyID[0]])
                    #updateCompany = update_table("UPDATE Companies SET Name=?, URL=? WHERE ID=?;", [companyName,companyURL,companyID[0]])
                    users = query_db("SELECT * FROM Users")
                    user = "Error"
                    for record in users:
                        if record["Email"] == newEmail:
                            user = record
                    if "Error" in user:
                        print("Error in updating Company or Profile Data")
                        return redirect("/admin/profile", code=302)
                    session['User'] = user
                    return redirect("/admin/profile", code=302)
        print("Error in updating Company or Profile Data")
        return redirect("/admin/profile", code=302)


@app.route("/admin/profile/delete", methods=['GET'])
def profile_delete():
    if request.method == "GET":
        email = session.get('User')['Email']
        company = query_db("SELECT * FROM Companies WHERE ID=?", [session.get('User')['CompanyID']], True)
        if company is None:
            return redirectWithMessage("profilePage", "Error in finding company!")
        payload = email + ";" + str(company["ID"])
        payload = verificationSigner.dumps(payload)
        msg = Message("Account deletion verification",
                                sender="thesearchbase@gmail.com",
                                recipients=[email])
        link = "https://www.thesearchbase.com/account/delete/verify/"+verificationSigner.dumps(payload)
        msg.html = "<img src='https://thesearchbase.com/static/email_images/verify_email.png'><br /><h4>Hi,</h4> <p>You haver requested that we delete your account.</p> <br /> \
                    To complete the process please follow <a href='"+link+"'> this link </a> . <br /> \
                    If you have not requested this then please change your password as soon as possible.<br />  <br /> \
                    Thank you for using our platform. <br /> <br />\
                    Regards, <br /> TheSearchBase Team <br />\
                    <img src='https://thesearchbase.com/static/email_images/footer_image.png'>"
        mail.send(msg)
        return redirectWithMessage("profilePage", "We have sent you a confirmation email through which to delete your account.")


@app.route("/account/delete/verify/<payload>", methods=['GET'])
def profile_delete_verify():
    if request.method == "GET":
        data = verificationSigner.loads(payload)
        email = data.split(";")[0]
        companyID = data.split(";")[1]
        users = query_db("SELECT * FROM Users")
        userCheck = False
        for user in users:
            if user["Email"] is email and user["CompanyID"] is companyID:
                userCheck = True
        if not userCheck:
            return redirectWithMessage("login", "User does not check out. Account deletion aborted!")
        deleteUser = delete_from_table("DELETE FROM Users WHERE Email=?, CompanyID=?;",[email, companyID])

        # sending the registration confirmation email to us
        msg = Message("User has deleted their account!",
                        sender="thesearchbase@gmail.com",
                        recipients=["thesearchbase@gmail.com"])
        msg.html = "<p>User: "+email+" has deleted their account. Company ID is " + str(companyID) + ".</p>"
        mail.send(msg)

        if deleteUser == "Record successfully deleted.":
            return redirectWithMessage("login", "Account has been deleted")
        else:
            return redirectWithMessage("login", "Error in deleting account")


@app.route("/admin/company/delete", methods=['GET'])
def company_delete():
    if request.method == "GET":
        email = session.get('User')['Email']
        company = query_db("SELECT * FROM Companies WHERE ID=?", [session.get('User')['CompanyID']], True)
        if company is None:
            return redirectWithMessage("profilePage", "Error in finding company!")
        if session.get('User')['AccessLevel'] is not "Owner":
            return redirectWithMessage("profilePage", "Only 'Owner' type account can delete company!")
        payload = email + ";" + str(company["ID"])
        payload = verificationSigner.dumps(payload)
        msg = Message("Company deletion vefication",
                                sender="thesearchbase@gmail.com",
                                recipients=[email])
        link = "https://www.thesearchbase.com/company/delete/verify/"+verificationSigner.dumps(payload)
        msg.html = "<img src='https://thesearchbase.com/static/email_images/verify_email.png'><br /><h4>Hi,</h4> <p>You haver requested that we delete your company.</p> <br /> \
                    Please do mind that deleting the company will also delete all accounts associated with it! <br />  \
                    To complete the process please follow <a href='"+link+"'> this link </a> . <br /> \
                    If you have not requested this then please change your password as soon as possible.<br />  <br /> \
                    Thank you for using our platform. <br /> <br />\
                    Regards, <br /> TheSearchBase Team <br />\
                    <img src='https://thesearchbase.com/static/email_images/footer_image.png'>"
        mail.send(msg)
        return redirectWithMessage("profilePage", "We have sent you a confirmation email through which to delete your company.")


@app.route("/company/delete/verify/<payload>", methods=['GET'])
def company_delete_verify():
    if request.method == "GET":
        data = verificationSigner.loads(payload)
        email = data.split(";")[0]
        companyID = data.split(";")[1]
        users = query_db("SELECT * FROM Users")
        userCheck = False
        for user in users:
            if user["Email"] is email and user["CompanyID"] is companyID and user["AccessLevel"] is "Owner":
                userCheck = True
        if not userCheck:
            return redirectWithMessage("login", "User does not check out. Company deletion aborted!")

        deleteUser = delete_from_table("DELETE FROM Users WHERE CompanyID=?;",[companyID])
        deleteCompany = delete_from_table("DELETE FROM Companies WHERE ID=?;",[companyID])

        # sending the registration confirmation email to us
        msg = Message("User has deleted their account!",
                        sender="thesearchbase@gmail.com",
                        recipients=["thesearchbase@gmail.com"])
        msg.html = "<p>Company has deleted their records. Company ID was " + str(companyID) + ".</p>"
        mail.send(msg)

        if deleteUser == "Record successfully deleted.":
            return redirectWithMessage("login", "Company has been deleted")
        else:
            return redirectWithMessage("login", "Error in deleting account")


@app.route("/getpopupsettings/<assistantID>", methods=['GET'])
def get_pop_settings(assistantID):
    if request.method == "GET":
        url = request.form.get("URL", default="Error")
        if url != "Error":
            assistant = query_db("SELECT * FROM Assistants WHERE ID=?", [assistantID], True)
            if session['UserPlan']['Settings']['CompanyNameonChatbot']:
                assistantLabel = query_db("SELECT * FROM Companies WHERE ID=?", [assistant["CompanyID"]], True)["Name"]
            else:
                assistantLabel = "TheSearchBase"
            datastring = assistant["SecondsUntilPopup"] + "&&&" + assistantLabel
            return jsonify(datastring)
        return "Off"


@app.route("/admin/assistant/create", methods=['GET', 'POST'])
def admin_assistant_create():
    if request.method == "GET":
        msg = checkForMessage()
        email = session.get('User')['Email']
        assistants = get_assistants(email)
        if assistants is None or "Error" in assistants:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error in getting your assistants!")
        return render("admin/create-assistant.html", autopop="Off", msg=msg)
    elif request.method == "POST":
        email = session.get('User')['Email']
        assistants = get_assistants(email)
        # Return the user to the page if has reached the limit of assistants
        if type(assistants) is type([]) and assistants:
            chatbotCap = session['UserPlan']['Settings']['ActiveBotsCap'] + session['UserPlan']['Settings']['InactiveBotsCap']
            print(chatbotCap, " ", len(assistants))
            if len(assistants) >= chatbotCap:
                return redirectWithMessage("admin_assistant_create", "You have reached the limit of "+str(chatbotCap)+" assistants")
        #Check max number of active bots
        numberOfActiveBots = count_db("Assistants", " WHERE CompanyID=? AND Active=?", [session.get('User')['CompanyID'], "True"])
        print(session.get('UserPlan')['Settings'])
        if numberOfActiveBots >= session.get('UserPlan')['Settings']['ActiveBotsCap']:
            return redirectWithMessage("admin_assistant_create", "You have already reached the maximum amount of Active Assistants. Please deactivate one to proceed.")
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
    checkAssistantID(assistantID)
    if request.method == "GET":
        email = session.get('User')['Email']
        users = query_db("SELECT * FROM Users")
        userCompanyID = "Error" 
        # If user exists
        for user in users:
            if user["Email"] == email:
                userCompanyID = user["CompanyID"]
        if userCompanyID == "Error":
            return redirect("/admin/homepage")
        assistantCompanyID = select_from_database_table("SELECT CompanyID FROM Assistants WHERE ID=?", [assistantID])

        #Check if the user is from the company that owns the assistant
        if userCompanyID == assistantCompanyID[0]:
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
                return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in deleting assistant!")
        else:
            return redirect("/admin/homepage")


@app.route("/admin/assistant/<assistantID>/settings", methods=['GET', 'POST'])
def admin_assistant_edit(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        msg = checkForMessageWhenAssistantID()
        email = session.get('User')['Email']
        assistant = query_db("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?", [assistantID, session.get('User')['CompanyID']], True)
        if assistant is None or "Error" in assistant:
            abort(status.HTTP_404_NOT_FOUND, "Error in getting assistant")
        else:
            message = assistant["Message"]
            autoPop = assistant["SecondsUntilPopup"]
            nickname = assistant["Nickname"]
            active = assistant["Active"]

            return render("admin/edit-assistant.html", autopop=autoPop, message=message, id=assistantID,
                            nickname=nickname, active=active, msg=msg)

    elif request.method == "POST":
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting the company's records!")
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None or "Error" in assistant:
                return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting the assistant's records!")
            else:
                nickname = request.form.get("nickname", default="Error")
                message = request.form.get("welcome-message", default="Error")
                popuptime = request.form.get("timeto-autopop", default="Error")
                autopopup = request.form.get("switch-autopop", default="off")

                if message is "Error" or nickname is "Error" or (popuptime is "Error" and autopopup is not "off"):
                    return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in getting your inputs!")
                else:
                    if autopopup == "off":
                        secondsUntilPopup = "Off"
                    else:
                        secondsUntilPopup = popuptime
                    updateAssistant = update_table(
                        "UPDATE Assistants SET Message=?, SecondsUntilPopup=?, Nickname=? WHERE ID=? AND CompanyID=?",
                        [message, secondsUntilPopup, nickname, assistantID, company[0]])

                    if "Error" in updateAssistant:
                        return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in updating assistant!")
                    else:
                        return redirect("/admin/assistant/{}/settings".format(assistantID))


@app.route("/admin/assistant/active/<turnto>/<assistantID>", methods=['GET'])
def admin_turn_assistant(turnto, assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        #Check if plan restrictions are ok with the assistant
        assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?", [session.get('User')['CompanyID']])
        numberOfProducts = 0
        maxNOP = session.get('UserPlan')['Settings']['MaxProducts']
        for record in assistants:
            numberOfProducts += count_db("Products", " WHERE AssistantID=?", [record["ID"],])
        if numberOfProducts > maxNOP:
            return redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP)+ ". In order to activate an assistant you will have to reduce the number of products you currently have: "+str(numberOfProducts)+".")
        
        if turnto == "True":
            #Check max number of active bots
            numberOfActiveBots = count_db("Assistants", " WHERE CompanyID=? AND Active=?", [session.get('User')['CompanyID'], "True"])
            if numberOfActiveBots >= session['UserPlan']['Settings']['ActiveBotsCap']:
                return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "You have already reached the maximum amount of Active Assistants. Please deactivate one to proceed.")

            message="activated."
        else:
            #Check max number of inactive bots
            numberOfActiveBots = count_db("Assistants", " WHERE CompanyID=? AND Active=?", [session.get('User')['CompanyID'], "False"])
            if numberOfActiveBots >= session['UserPlan']['Settings']['InactiveBotsCap']:
                return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "You have already reached the maximum amount of Inactive Assistants. If you wish to deactivate this bot please delete or activate an inactivate assistant")

            message="deactivated."

        updateBot = update_table("UPDATE Assistants SET Active=? WHERE ID=?;", [turnto, assistantID])
        return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Assistant has been "+message)

# TODO rewrite
@app.route("/admin/assistant/<assistantID>/questions", methods=['GET', 'POST'])
def admin_questions(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        message = checkForMessageWhenAssistantID()
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
                questionsTuple = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                            [assistant[0]], True)
                # TODO check questionstuple for errors

                questions = []
                for i in range(0, len(questionsTuple)):
                    question = [questionsTuple[i][2] + ";" + questionsTuple[i][3]]
                    questions.append(tuple(question))
                return render("admin/questions.html", data=questions, message=message, id=assistantID)
    elif request.method == "POST":
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting company's records!")
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None or "Error" in assistant:
                return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting assitant's records!")
            else:
                currentQuestions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                              [assistantID], True)
                if currentQuestions is None or "Error" in currentQuestions:
                    return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting old questions!")

                updatedQuestions = []
                noq = request.form.get("noq-hidden", default="Error")
                for i in range(1, int(noq) + 1):
                    question = request.form.get("question" + str(i), default="Error")
                    if question != "Error":
                        updatedQuestions.append(question)
                    else:
                        return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in getting new questions!")

                i = -1
                if (len(updatedQuestions) + 1 < len(currentQuestions) + 1):
                    for b in range(len(updatedQuestions) + 1, len(currentQuestions) + 1):
                        questionID = currentQuestions[i][0]
                        question = currentQuestions[i][2]

                        deleteQuestion = delete_from_table("DELETE FROM Questions WHERE AssistantID=? AND Question=?;", [assistantID, escape(question)])
                        if deleteQuestion is None or "Error" in deleteQuestion:
                            return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 1 Error in updating questions!")

                        deleteAnswers = delete_from_table(DATABASE, "DELETE FROM Answers WHERE QuestionID=?;", [questionID])
                        if deleteAnswers is None or "Error" in deleteAnswers:
                            return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Error in removing deleted question's answers!")
                for q in updatedQuestions:
                    i += 1
                    qType = request.form.get("qType" + str(i))
                    if i >= len(currentQuestions):
                        insertQuestion = insert_into_database_table(
                            "INSERT INTO Questions ('AssistantID', 'Question', 'Type')"
                            "VALUES (?,?,?);", (assistantID, q, qType))
                        if insertQuestion is None or "Error" in insertQuestion:
                            return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 2 Error in updating questions!")
                    else:
                        updateQuestion = update_table("UPDATE Questions SET Question=?, Type=? WHERE Question=?;", [escape(q), qType, currentQuestions[i][2]])
                        if updateQuestion is None or "Error" in updateQuestion:
                             return redirectWithMessageAndAssistantID("admin_questions", assistantID, "Position 3 Error in updating questions!")

                return redirect("/admin/assistant/{}/questions".format(assistantID))


# TODO rewrite
@app.route("/admin/assistant/<assistantID>/answers", methods=['GET', 'POST'])
def admin_answers(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        message = checkForMessageWhenAssistantID()
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?", [assistantID, company[0]])
            if assistant is None:
                abort(status.HTTP_404_NOT_FOUND)
            elif "Error" in assistant:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                questionsTuple = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;", [assistantID], True)
                # TODO check questionstuple for errors
                questions = []
                for i in range(0, len(questionsTuple)):
                    questions.append(questionsTuple[i][2] + ";" + questionsTuple[i][3])

                allAnswers = {}
                for i in range(0, len(questions)):
                    answersTuple = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;", [questionsTuple[i][0]], True)
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
                return render("admin/answers.html", msg=questionsAndAnswers, id=assistantID, message=message)
    elif request.method == "POST":
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting company's records!")
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])
            if assistant is None or "Error" in assistant:
                return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting assistant's records!")
            else:
                selected_question = request.form.get("question", default="Error")  # question_text;question_type
                if "Error" in selected_question:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting selected question!")

                question = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=? AND Question=?;",
                                                      [assistantID, selected_question.split(";")[0]])
                if question is None or "Error" in question:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting question's records")

                questionID = question[0]
                currentAnswers = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;", [questionID])
                if currentAnswers is None or "Error" in currentAnswers:
                    return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting old answers!")
                if (currentAnswers is not None):
                    deleteOldQuestions = delete_from_table("DELETE FROM Answers WHERE QuestionID=?;", [questionID])
                    if deleteOldQuestions is None or "Error" in deleteOldQuestions:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in deleting old answers!")

                noa = 1
                for key in request.form:
                    if "pname" in key:
                        noa += 1

                for i in range(1, noa):
                    answer = request.form.get("pname" + str(i), default="Error")
                    try:
                        keyword = request.form.getlist("keywords" + str(i))
                    except:
                        keyword = "Error"
                    keyword = ','.join(keyword)
                    action = request.form.get("action" + str(i), default="None")
                    if action != "Next Question by Order" and not session['UserPlan']['Settings']['ExtendedLogic']:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID, "It appears you tried to access extended logic without having access to it. Action aborted!")
                    if "Error" in answer or "Error" in keyword or "Error" in action:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in getting your input.")
                    insertAnswer = insert_into_database_table(
                        "INSERT INTO Answers (QuestionID, Answer, Keyword, Action) VALUES (?,?,?,?);",
                        (questionID, answer, keyword, action))
                    if insertAnswer is None or "Error" in insertAnswer:
                        return redirectWithMessageAndAssistantID("admin_answers", assistantID, "Error in updating answers!")

                return redirect("/admin/assistant/{}/answers".format(assistantID)+"?res="+str(noa)+"")


@app.route("/admin/assistant/<assistantID>/products", methods=['GET', 'POST'])
def admin_products(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
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
                products = select_from_database_table(
                    "SELECT ProductID, Name, Brand, Model, Price, Keywords, Discount, URL "
                    "FROM Products WHERE AssistantID=?;", [assistantID], True)
                # TODO check products for errors
                return render("admin/products.html", data=products, id=assistantID)
    elif request.method == 'POST':
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?",
                                                   [assistantID, company[0]])

            #get all company assistants (needed for totalproducts check)
            assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?", [company[0]])

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

                    #see if they have reached the limit
                    numberOfProducts = 0
                    maxNOP = session['UserPlan']['Settings']['MaxProducts']
                    for record in assistants:
                        numberOfProducts += count_db("Products", " WHERE AssistantID=?", [record["ID"],])
                    if numberOfProducts > maxNOP:
                        return redirectWithMessageAndAssistantID("admin_products", assistantID, "You have reached the maximum amount of solutions you can have: " + str(maxNOP)+ ". Solutions after " + name + " have not been added.")

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


# TODO improve
@app.route("/admin/assistant/<assistantID>/userinput", methods=["GET"])
def admin_user_input(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        email = session.get('User')['Email']
        company = get_company(email)
        if company is None or "Error" in company:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO handle this better
        else:
            assistant = select_from_database_table("SELECT * FROM Assistants WHERE ID=? AND CompanyID=?", [assistantID,
                                                                                                           company[0]])
            if assistant is None or "Error" in assistant:
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?;",
                                                       [assistantID], True)
                data = []
                #dataTuple = tuple(["Null"])
                for i in range(0, len(questions)):
                    question = questions[i]
                    questionID = question[0]
                    userInput = select_from_database_table("SELECT * FROM UserInput WHERE QuestionID=?", [questionID], True)
                    if(userInput != [] and userInput != None):
                        for record in userInput:
                            data.append(record)
                print(data)
                return render("admin/data-storage.html", data=data)


@app.route("/admin/assistant/<assistantID>/connect", methods=['GET'])
def admin_connect(assistantID):
    checkAssistantID(assistantID)
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

@app.route("/admin/cancellation/confirmation", methods=['GET'])
def admin_plan_confirmation():
    return render("admin/cancellation_confirmation.html")


@app.route('/admin/thanks', methods=['GET'])
def admin_thanks():
    return render('admin/thank-you.html')




def is_coupon_valid(coupon="Error"):
    try:
        print(coupon)
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
            abort(status.HTTP_400_BAD_REQUEST, "This plan doesn't exist! Make sure the plan ID is correct.")

        # print(plan)
        return render("admin/check-out.html", plan=plan)


    if request.method == 'POST':


        if not session.get('Logged_in', False):
            redirectWithMessage("login", "You must login first!")

        # Get Stripe from data. That's includ the generated token using JavaScript
        data = request.get_json(silent=True)
        # print(data)
        token = data['token']['id']
        coupon = data['coupon']

        if token is "Error":
            # TODO improve this
            return jsonify(error="No token provided to complete the payment!")



        # Get the plan opject from Stripe API
        try:
            plan = stripe.Plan.retrieve(planID)
        except stripe.error.StripeError as e:
            return jsonify(error="This plan does't exist! Make sure the plan ID is correct.")


        # Validate the given coupon.
        if coupon == "" or coupon is None or coupon == "Error":
            # If coupon is not provided set it to None as Stripe API require.
            coupon = None
            print("make no use of coupons")

        elif not (is_coupon_valid(coupon)):
            print("The coupon used is not valid")
            return jsonify(error="The coupon used is not valid")


    # If no errors occurred, subscribe the user to plan.

        # Get the user by email
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == session.get('User')['Email']:
                user = record
        if "Error" in user:
            return jsonify(error="An error occurred and could not subscribe.")

        try:
            subscription = stripe.Subscription.create(
                customer=user['StripeID'],
                source=token,
                coupon=coupon,
                items=[
                    {
                        "plan": planID,
                    },
                ]
            )

            # print(subscription)

            # if everything is ok activate assistants
            update_table("UPDATE Assistants SET Active=? WHERE CompanyID=?", ("True", user['CompanyID']))
            update_table("UPDATE Users SET SubID=? WHERE ID=?", (subscription['id'], user['ID']))

            # Resit the session
            session['UserPlan']['Nickname'] =  getPlanNickname(subscription['id'])
            if getPlanNickname(user['SubID']) is None:
                session['UserPlan']['Settings'] = NoPlan
            elif "Basic" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = BasicPlan
            elif "Advanced" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = AdvancedPlan
            elif "Ultimate" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = UltimatePlan

        # TODO check subscription for errors https://stripe.com/docs/api#errors
        except Exception as e:
            print(e)
            return jsonify(error="An error occurred and could not subscribe.")

        # Reaching to point means no errors and subscription is successful
        print("You have successfully subscribed!")
        return jsonify(success="You have successfully subscribed!", url= "admin/pricing-tables.html")


@app.route("/admin/check-out/checkPromoCode", methods=['POST'])
def checkPromoCode():
    if request.method == 'POST':

        if not session.get('Logged_in', False):
            redirectWithMessage("login", "You must login first!")
        else:

            # TODO: check the promoCode from user then response with yes or no with json
            promoCode = str(request.data, 'utf-8')
            print(">>>>>>>>>>>>>>>>")
            print(promoCode)
            if promoCode == 'abc':
                return jsonify(isValid=True)
            else:
                return jsonify(isValid=False)



@app.route("/admin/unsubscribe", methods=['POST'])
def unsubscribe():

    if request.method == 'POST':

        # if not session.get('Logged_in', False):
        #     redirectWithMessage("login", "You must login first!")
        
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        print(session.get('User')['Email'])
        for record in users:
            if record["Email"] == session.get('User')['Email']:
                user = record
        if "Error" in user:
            return jsonify(error="This user does't exist. Please login again!")
        if user['SubID'] is None:
            print("This account has no active subscriptions ")
            return jsonify(error="This account has no active subscription")

        try:
            # Unsubscribe
            sub = stripe.Subscription.retrieve(user['SubID'])
            print(sub)
            sub.delete()

            # TODO why query_db does not work with update?
            # query_db('UPDATE Users SET SubID=? WHERE ID=?;', (None,  session.get('User')['ID']))
            update_table("UPDATE Users SET SubID=? WHERE ID=?;",
                         [None, session.get('User')['ID']])
            # Reset session
            session['UserPlan'] = NoPlan

            print("You have unsubscribed successfully!")
            return jsonify(msg="You have unsubscribed successfully!")

        except Exception as e:
            print("An error occurred while trying to unsubscribe")
            return jsonify(error="An error occurred while trying to unsubscribe")




# Stripe Webhooks
@app.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhook_subscription_cancelled():
    if request.method == "POST":
        try:
            print("STRIPE TRIGGER FOR UNSUBSCRIPTION...")
            event_json = request.get_json(force=True)
            # event_json = json.loads(request.body)
            customerID = event_json['data']['object']['customer']
            print("CUSTOMER ID")
            print(customerID)


            user = select_from_database_table("SELECT * FROM Users WHERE StripeID=?", [customerID])
            print(user)

            if not user:
                print("NOT USER")

            update_table("UPDATE Users SET SubID=? WHERE StripeID=?;",
                         [None, customerID])


            # TODO check company for errors
            assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?", [user[1]], True)

            # Check if user has assistants to deactivate first
            if len(assistants) > 0:
                for assistant in assistants:

                    updateAssistant = update_table("UPDATE Assistants SET Active=? WHERE ID=?", ["False", assistant[0]])
                    # TODO check update assistant for errors


        except Exception as e:
            abort(status.HTTP_400_BAD_REQUEST, "Webhook error")


        return "Assistants for " + user[5] + " account has been deactivated due to subscription cancellation", status.HTTP_200_OK



# TODO implement this
@app.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        stats = select_from_database_table(
            "SELECT Date, Opened, QuestionsAnswered, ProductsReturned FROM Statistics WHERE AssistantID=?",
            [assistantID], True)
        return render("admin/analytics.html", data=stats)


# Method for the users
@app.route("/admin/users", methods=['GET'])
def admin_users():
    if request.method == "GET":
        message = checkForMessage()
        email = session.get('User')['Email']
        companyID = session.get('User')['CompanyID']

        userSettings = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [companyID])

        users = select_from_database_table("SELECT * FROM Users WHERE CompanyID=?", [companyID], True)
        return render("admin/users.html", users=users, email=email, userSettings=userSettings, message=message)

@app.route("/admin/users/add", methods=['POST'])
def admin_users_add():
    if request.method == "POST":
        numberOfCompanyUsers = count_db("Users", " WHERE CompanyID=?", [session.get('User')['CompanyID'],])
        if numberOfCompanyUsers >= session['UserPlan']['Settings']['AdditionalUsersCap'] + 1:
            return redirectWithMessage("admin_users", "You have reached the max amount of additional Users - " + str(session['UserPlan']['Settings']['AdditionalUsersCap'])+".")
        email = session.get('User')['Email']
        companyID = session.get('User')['CompanyID']
        fullname = request.form.get("fullname", default="Error")
        accessLevel = request.form.get("accessLevel", default="Error")
        newEmail = request.form.get("email", default="Error")
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        # Generates a random password

        if fullname == "Error" or accessLevel == "Error" or newEmail == "Error":
            return redirectWithMessage("admin_users", "Error in retrieving all textbox inputs.")
        else:
            newEmail = newEmail.lower()
            users = query_db("SELECT * FROM Users")
            # If user exists
            for record in users:
                if record["Email"] == newEmail:
                    return redirectWithMessage("admin_users", "Email is already in use!")
            try:
                firstname = fullname.split(" ")[0]
                surname = fullname.split(" ")[1]
            except IndexError as e:
                return redirectWithMessage("admin_users", "Error in retrieving both names.")
            hashed_password = hash_password(password)

            #ENCRYPTION
            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
                (companyID, encryptVar(firstname), encryptVar(surname), accessLevel, encryptVar(newEmail), hashed_password, "False"))
            #insertUserResponse = insert_into_database_table(
             #   "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
              #  (companyID, firstname, surname, accessLevel, newEmail, hashed_password, "True"))
            if "added" not in insertUserResponse:
                return redirectWithMessage("admin_users", "Error in adding user to our records.")
            else:
                #if not app.debug:

                # sending email to the new user.
                # TODO this needs improving
                link = "https://www.thesearchbase.com/admin/changepassword"
                msg = Message("Account verification, "+firstname+" "+surname,
                              sender="thesearchbase@gmail.com",
                              recipients=[newEmail])
                msg.html = "<h4>Hi, <h4> <br /> <p>You have been registered with TheSearchBase by an admin at your company.<br> \
                            To get access to the platform, we have generated a temporary password for you to access the platform.</p> <br /> \
                            <h4>Your temporary password is: "+password+".<h4><br />\
                            Please visit <a href='"+link+"'>this link</a> to sign in and to set the password for your account.<p><br /> If you feel this is a mistake please contact "+email+". <br /> <br / > Regards, TheSearchBase Team"
                mail.send(msg)
                return redirectWithMessage("admin_users", "User has been added. A temporary password has been emailed to them.")

@app.route("/admin/users/modify", methods=["POST"])
def admin_users_modify():
    if request.method == "POST":
        email = session.get('User')['Email']
        userID = request.form.get("userID", default="Error")
        newAccess = request.form.get("accessLevel", default="Error")
        if userID != "Error" and newAccess != "Error":
            updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE ID=?;", [newAccess, userID])
            if newAccess == "Owner":
                users = query_db("SELECT * FROM Users")
                recordID = "Error"
                # If user exists
                for record in users:
                    if record["Email"] == session.get('User')['Email']:
                        recordID = record["ID"]
                if "Error" in recordID:
                    return redirectWithMessage("admin_users", "Error in finding user.")
                updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE ID=?;", ["Admin", recordID])
                return redirectWithMessage("admin_users", "User has been modified.")
        return redirectWithMessage("admin_users", "Error in retrieving all textbox inputs.")

@app.route("/admin/users/delete/<userID>", methods=["GET"])
def admin_users_delete(userID):
    if request.method == "GET":
        email = session.get('User')['Email']
        companyID = session.get('User')['CompanyID']
        
        users = query_db("SELECT * FROM Users")
        requestingUser = "Error"
        # If user exists
        for user in users:
            if user["Email"] == email:
                requestingUser = user
        if "Error" in requestingUser:
            return redirectWithMessage("admin_users", "Error in finding user.")
        targetUser = select_from_database_table("SELECT CompanyID FROM Users WHERE ID=?", [userID])[0]
        #Check that users are from the same company and operating user isnt 'User'
        if requestingUser["AccessLevel"] == "User" or requestingUser["CompanyID"] != targetUser:
            #TODO send feedback message
            return redirect("/admin/homepage", code=302)
        delete_from_table("DELETE FROM Users WHERE ID=?;", [userID])
        return redirectWithMessage("admin_users", "User has been deleted.")


@app.route("/admin/users/permissions", methods=["POST"])
def admin_users_permissions():
    if request.method == "POST":
        adminPermissions = ""
        userPermissions = ""
        
        permissionTypes = ["EditChatbots", "EditUsers", "AccessBilling"]
        #try to get admin permissions
        for i in range(0,3):
            permission = request.form.get("AdminPermission" + str(i+1), default="Error")
            #look for Trues
            if "Error" not in permission:
                for pType in permissionTypes:
                    if pType in permission:
                        adminPermissions += (pType + ":True;")
                        permissionTypes.remove(pType)
        #look for Falses
        for pType in permissionTypes:
            adminPermissions += (pType + ":False;")

        permissionTypes = ["EditChatbots", "EditUsers", "AccessBilling"]
        #try to get user permissions
        for i in range(0,3):
            permission = request.form.get("UserPermission" + str(i+1), default="Error")
            #look for Trues
            if "Error" not in permission:
                for pType in permissionTypes:
                    if pType in permission:
                        userPermissions += (pType + ":True;")
                        permissionTypes.remove(pType)
        #look for Falses
        for pType in permissionTypes:
            userPermissions += (pType + ":False;")

        #update table
        #updatePermissions = query_db("UPDATE UserSettings SET AdminPermissions=?,UserPermissions=? WHERE CompanyID=?;", [adminPermissions, userPermissions, session.get('User')['CompanyID']])
        updatePermissions = update_table("UPDATE UserSettings SET AdminPermissions=?,UserPermissions=? WHERE CompanyID=?;", [adminPermissions, userPermissions, session.get('User')['CompanyID']])

        #update current user's permisions
        permissionsDic = {}
        permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]
        if "Owner" in session.get('User')['AccessLevel']:
            permissions = permissions["AdminPermissions"].split(";")
            for perm in permissions:
                if perm:
                    permissionsDic[perm.split(":")[0]] = True
        else:
            permissions = permissions[session.get('User')['AccessLevel']+"Permissions"].split(";")
            for perm in permissions:
                if perm:
                    if "True" in perm.split(":")[1]:
                        permBool = True
                    else:
                        permBool = False
                    permissionsDic[perm.split(":")[0]] = permBool
        session['Permissions'] = dict(permissionsDic)

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
        companies = query_db("SELECT * FROM Companies")
        # If company exists
        company = "Error"
        for record in companies:
            if record["Name"] == companyName:
                company = record
        if company is "Error":
            abort(status.HTTP_404_NOT_FOUND)


        if company is None:
            abort(status.HTTP_400_BAD_REQUEST, "This company does't exist")

        # TODO check company for errors
        assistant = query_db("SELECT * FROM Assistants WHERE ID=?;", [assistantID], True)

        if assistant is None or assistant is "Error":
            abort(status.HTTP_400_BAD_REQUEST, "This Assistant does't exist")



        # TODO check assistant for errors
        # assistantIndex = 0  # TODO implement this properly
        # assistantID = assistant[assistantIndex][0]

        # is assistant active ? True/False
        assistantActive = assistant["Active"]

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

            message = assistant["Message"]
            # MONTHLY UPDATE
            date = datetime.now().strftime("%Y-%m")
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None or "Error" in currentStats or not currentStats:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, 0, 0))
                # TODO check newStats for errors
            else:
                updatedStats = update_table("UPDATE Statistics SET Opened=? WHERE AssistantID=? AND Date=?;", [currentStats[3] + 1, assistantID, date])

            # WEEKLY UPDATE
            dateParts = datetime.now().strftime("%Y-%m-%d").split("-")
            date = datetime.now().strftime("%Y") + ";" + str(datetime.date(datetime.now()).isocalendar()[1])
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=?;", [date])
            if currentStats is None or "Error" in currentStats or not currentStats:
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

        
        companies = query_db("SELECT * FROM Companies")
        # If company exists
        for record in companies:
            if record["Name"] == escape(companyName):
                company = record
            else:
                return "We could not find the company in our records. Sorry about that!"


        # TODO check company for errors
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company[0]], True)

        if assistant is None:
            return "We could not find the assistant in our records. Sorry about that!"

        # TODO check assistant for errors
        # assistantIndex = 0  # TODO implement this properly

        questions = select_from_database_table("SELECT * FROM Questions WHERE AssistantID=?", [assistantID], True)
        # TODO check questions for errors
        print(questions)
        products = select_from_database_table("SELECT * FROM Products WHERE AssistantID=?;", [assistantID], True)
        # TODO check products for errors

        lastSessionID = select_from_database_table("SELECT * FROM UserInput", [], True)
        if lastSessionID is None or not lastSessionID:
            lastSessionID = 1
        else:
            lastSessionID = lastSessionID[len(lastSessionID)-1][4] + 1

        collectedInformation = request.form.get("collectedInformation").split("||")
        date = datetime.now().strftime("%d-%m-%Y")
        for i in range(0, len(collectedInformation)):
            colInfo = collectedInformation[i].split(";")
            input = colInfo[1]
            questionIndex = int(colInfo[0]) - 1
            questionID = int(questions[questionIndex][0])
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
                    savePath = savePath.replace('\\', '/')
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
            return "Error in getting number of keywords. Sorry about that!"
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
                        keywordList = keyword.split(",")
                        for ii in range(0, len(keywordList)):
                            keywords.append(keywordList[ii])
                else:
                    return "Error in getting keywords. Sorry about that!"

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
                        users = query_db("SELECT * FROM Users")
                        requestingUser = "Error"
                        # If user exists
                        for user in users:
                            if user["Email"] == email:
                                requestingUser = user
                        if "Error" in requestingUser:
                            abort(status.HTTP_400_BAD_REQUEST, "User not found!")
                        updateUser = update_table("UPDATE Users SET Verified=? WHERE ID=?;", ["True", requestingUser["ID"]])
                        # TODO check updateUser
                        
                        users = query_db("SELECT * FROM Users")
                        # If user exists
                        user = "Error"
                        for record in users:
                            if record["Email"] == email:
                                user = record
                        if "Error" in user:
                            abort(status.HTTP_400_BAD_REQUEST, "Target user not found!")

                        # sending registration confirmation email to the user.
                        msg = Message("Thank you for registering, {} {}".format(user["Firstname"], user["Surname"]),
                                      sender="thesearchbase@gmail.com",
                                      recipients=[email])
                        msg.html = "<img src='https://thesearchbase.com/static/email_images/welcome.png' style='width:500px;height:228px;'><br /> \
                                   <h4>Hi,</h4> <p>Thank you for registering with TheSearchBase!</p> \
                                   <p>A whole new world of possibilities is ahead of you, we strive to be a platform that aims to make chat bot technology available to everyone. \
                                   If you would like to know more about our start up story, check our <a href=https://www.thesearchbase.com/about> Story <a/> and see what we're all about. </p> \
                                   <p>More Importantly, we would like you to use our platform and tell us what you think. If you could share your ideas or suggestions with our team, we would be very happy to collect your feedback</p> \
                                   <p>As a final message, we would like to say, we thoroughly hope you enjoy using our platform and hope to see your chat bot revolutionise your company or idea.</p><br /> <p> Happy chatboting, </p><p>TheSearchbase Team</p> \
                                   <img src='https://thesearchbase.com/static/email_images/footer_image.png' style='width:500px;height:228px;'>"
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
         users = query_db("SELECT * FROM Users")
         user = "Error"
         # If user exists
         for record in users:
             if record["Email"] == email:
                 user = record
         if "Error" in user:
             return redirectWithMessage("login", "Error in finding user!")
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
             msg.html ="<img src='https://thesearchbase.com/static/email_images/password_reset.png' style='width:500px;height:228px;'> <h4> Hi, </h4><p>We have been informed you would like to reset your password. \
                        Please visit <a href='"+link+"'>this link</a> to verify your account and to set your new password.</p> <br /> <br /> \
                        <p>If you have received this by mistake, please let our team know and kindly delete this email</p><br /> Regards, <br /> TheSearchBase Team \
                        <img src='https://thesearchbase.com/static/email_images/footer_image.png' style='width:500px;height:228px;'>"
             mail.send(msg)
 
             return redirectWithMessage("login", "Password reset email has been sent")

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
                        return render_template("/accounts/set_resetpassword.html", email=email, payload=payload)

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
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == email:
                user = record
        if "Error" in user:
            return redirectWithMessage("login", "Error in finding user!")
        updatePassword = update_table("UPDATE Users SET Password=? WHERE ID=?;", [hashedNewPassword, user["ID"]])
        return redirectWithMessage("login", "Password has been changed.")


@app.route("/admin/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("/accounts/changepassword.html")
    else:
        email = session.get('User')['Email']
        currentPassword = request.form.get("currentPassword", default="Error")
        newPassword = request.form.get("newPassword", default="Error")
        # TODO check these
        
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == email:
                user = record
        if "Error" in user:
            return render_template("/accounts/changepassword.html", msg="User not found!")
        # TODO check user
        if user["Verified"] == "True":
            password = user["Password"]
            if hash_password(currentPassword, password) == password:
                hashedNewPassword = hash_password(newPassword)
                updatePassword = update_table("UPDATE Users SET Password=? WHERE ID=?;", [hashedNewPassword, user["ID"]])
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

def select_from_database_table(sql_statement, array_of_terms=None, multi=False, database=DATABASE):
    data = "Error"
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        data = cur.fetchall()
        if not multi:
            data = data[0]
    except sqlite3.ProgrammingError as e:
        print("Error in select statement," + str(e))
    except sqlite3.OperationalError as e:
        print("Error in select operation," + str(e))
    finally:
        if (conn is not None):
            conn.close()
        if "SELECT" in sql_statement:
            returnArray = []
            arrayPos = 0
            for record in data:
                tempVar = ""
                if type(record) == list or type(record) == tuple:
                    returnArray.append([])
                    for value in record:
                        if type(value) == bytes:
                            try:
                                tempVar = encryption.decrypt(value).decode()
                            except:
                                print("Could not decode value. Assuming hashed record!")
                        else:
                            tempVar = value
                        returnArray[arrayPos].append(tempVar)
                else:
                    if type(record) == bytes:
                        try:
                            tempVar = encryption.decrypt(record).decode()
                        except:
                            print("Could not decode value. Assuming hashed record!")
                    else:
                        tempVar = record
                    returnArray.append(tempVar)
                arrayPos+=1
            #remove empty []
            for records in returnArray:
                if not records:
                    returnArray.remove(records)
            data = returnArray
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
    return sqlite3.connect(DATABASE)


# Initializes the database with test data while in debug mode.
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(APP_ROOT + '/sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("Database Initialized...")

        if app.debug:
            with app.open_resource(APP_ROOT + '/sql/devseed.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                # Create and store a hashed password for "test" user
                hash = hash_password("test")
                update_table("UPDATE Users SET Password=? WHERE ID=?", [hash, 1])
            db.commit()
            print("Test Data Inserted...")

    print("Database Initialized")


# facilitate querying data from the database.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    if "SELECT" in query:
        for record in rv:
            for key, value in record.items():
                if type(value) == bytes and "Password" not in key:
                    record[key] = encryption.decrypt(value).decode()
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


def count_db(table, condition="", args=()):
    cur = g.db.execute("SELECT count(*) FROM "+table+" "+condition, args)
    return cur.fetchall()[0][0]


#encryption function to save typing
def encryptVar(var):
    return encryption.encrypt(var.encode())

# Get connection when no requests e.g Pyton REPL.
def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    # Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()



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


# class Del:
#     def __init__(self, keep=string.digits):
#         self.comp = dict((ord(c), c) for c in keep)
#
#     def __getitem__(self, k):
#         return self.comp.get(k)


if __name__ == "__main__":

    print("Run the server...")
    print(app.debug)

    # Create the schema only in development mode
    if app.debug:
        init_db()

    # Print app configuration
    print(app.config)
    # Run the app server
    app.run()



