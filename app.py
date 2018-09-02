#/usr/bin/python3.5
from flask import Flask, redirect, request, render_template, jsonify, abort, escape, \
    g, session
from werkzeug.utils import secure_filename
from flask_api import status
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadData
from xml.dom import minidom
import os
import sqlite3
import stripe
from urllib.request import urlopen
from cryptography.fernet import Fernet
import urllib.request

from models import db, Role, Company, Assistant, Plan, Statistics, Question, Answer, QuestionType, QuestionAction,\
    QuestionFU, QuestionUI, QuestionPA, UserInputValidation
from services.mail_services import mail

# Import all routers to register them as blueprints
from routes.admin.routers import dashboard_router, profile_router,  admin_api, settings_router,\
    products_router, questions_router, analytics_router, sub_router, connection_router, userInput_router, users_router,\
    changePassword_router, answers_router, bot_router, emoji_router

from routes.public.routers import public_router, resetPassword_router
from services import user_services, mail_services

app = Flask(__name__, static_folder='static')

app.register_blueprint(dashboard_router)
app.register_blueprint(public_router)
app.register_blueprint(resetPassword_router)
app.register_blueprint(profile_router)
app.register_blueprint(admin_api)
app.register_blueprint(sub_router)
app.register_blueprint(settings_router)
app.register_blueprint(products_router)
app.register_blueprint(questions_router)
app.register_blueprint(analytics_router)
app.register_blueprint(connection_router)
app.register_blueprint(userInput_router)
app.register_blueprint(changePassword_router)
app.register_blueprint(users_router)
app.register_blueprint(answers_router)
app.register_blueprint(bot_router)
app.register_blueprint(emoji_router)


# code to ensure user is logged in
@app.before_request
def before_request():

    currentURL = str(request.url_rule)
    restrictedRoutes = ['/admin', 'admin/dashboard']

    # If the user try to visit one of the restricted routes without logging in he will be redirected
    if any(route in currentURL for route in restrictedRoutes) and not session.get('Logged_in', False):
        return redirect('login')

    #if on admin route
    # if any(route in theurl for route in restrictedRoutes):
    #     Check user permissions as user type
        # if not session['Permissions']["EditChatbots"] and "/admin/assistant" in theurl:
        #     return redirect("/admin/dashboard", code=302)
        # if not session['Permissions']["EditUsers"] and "/admin/users" in theurl:
        #     return redirect("/admin/dashboard", code=302)
        # if not session['Permissions']["AccessBilling"] and "/admin/assistant/" in theurl:
        #     return redirect("/admin/dashboard", code=302)

        #Check user plan permissions
        # print("PLAN:", session.get('UserPlan', []))

#################################
#      THIS IS TO BE ABLE       #
#     TO DEBUG FROM PYCHARM     #
#    IN PRODUCTION THIS CODE    #
#      WILL BE REMOVED          #
#################################

# app.config.from_object('config.DevelopmentConfig')
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
#
#
# db.init_app(app)
# mail.init_app(app)
# app.app_context().push()
#
# db.drop_all()
# db.create_all()


# Generates dummy data for testing
def genDummyData():

    # Companies creation
    db.session.add(Company(Name='Aramco', Size=12, PhoneNumber='4344423', URL='ff.com'))
    db.session.add(Company(Name='Sabic', Size=12, PhoneNumber='4344423', URL='ff.com'))

    aramco = Company.query.filter(Company.Name == "Aramco").first()
    sabic = Company.query.filter(Company.Name == "Sabic").first()

    # Assistants creation for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=aramco)
    helper_a = Assistant(Name="Helper", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=sabic)


    # Questions for Aramco
    question_UI = Question(Text="What's your email?", Type=QuestionType.UserInput, Order=1,
                                     StoreInDB=True, Assistant=reader_a)
    question_PA: Question = Question(Text="Do you smoke?", Type=QuestionType.PredefinedAnswers, Order=2,
                                     StoreInDB=True, Assistant=reader_a)
    question_FU: Question = Question(Text="Upload your CV", Type=QuestionType.FileUpload, Order=3,
                                     StoreInDB=True, Assistant=reader_a)
    # Questions Associations
    questionUI = QuestionUI(Question=question_UI, Validation=UserInputValidation.Email,
                            Action=QuestionAction.GoToNextQuestion, QuestionToGo=question_PA )

    questionPA = QuestionPA(Question=question_PA)
    answer1 = Answer(QuestionPA=questionPA, Text="Yes", Keywords="smoker,sad", TimesClicked=1,
                     Action=QuestionAction.GoToSpecificQuestion, QuestionToGo=question_FU)
    answer2 = Answer(QuestionPA=questionPA, Text="No", Keywords="smoker,sad", TimesClicked=1,
                     Action=QuestionAction.ShowSolutions, QuestionToGo=None)

    questionFU = QuestionFU(Question=question_FU, TypesAllowed="gif,pdf",
                            Action=QuestionAction.ShowSolutions, QuestionToGo=None)

    db.session.add(questionUI)
    db.session.add(questionPA)
    db.session.add(answer1)
    db.session.add(answer2)
    db.session.add(questionFU)



    db.session.add(Role(Name="Owner", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= aramco, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    db.session.add(Role(Name="Owner", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= sabic, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    owner_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Owner").first()
    admin_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Admin").first()
    user_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "User").first()

    owner_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Owner").first()
    admin_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Admin").first()
    user_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "User").first()

    user_services.create(firstname='Ahmad', surname='Hadi', email='aa@aa.com', password='123',
                         company=aramco, role=owner_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', company=aramco,
                         role=admin_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', company=aramco,
                         role=user_aramco, verified=True)

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', company=sabic,
                         role=owner_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', company=sabic,
                         role=admin_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e6@e.com', password='123', company=sabic,
                         role=user_sabic, verified=True)

    db.session.add(Plan(ID='plan_D3lp2yVtTotk2f', Nickname='basic'))
    db.session.add(Plan(ID='plan_D3lpeLZ3EV8IfA', Nickname='ultimate'))
    db.session.add(Plan(ID='plan_D3lp9R7ombKmSO', Nickname='advanced'))
    db.session.add(Plan(ID='plan_D48N4wxwAWEMOH', Nickname='debug'))

    db.session.commit()

#################################


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

# mail = Mail(app)



NoPlan = {"MaxProducts":0, "ActiveBotsCap":0, "InactiveBotsCap":0, "AdditionalUsersCap":0, "ExtendedLogic":False, "ImportDatabase":False, "CompanyNameonChatbot": False}
BasicPlan = {"MaxProducts":600, "ActiveBotsCap":2, "InactiveBotsCap":3, "AdditionalUsersCap":5, "ExtendedLogic":False, "ImportDatabase":False, "CompanyNameonChatbot": False}
AdvancedPlan = {"MaxProducts":5000, "ActiveBotsCap":4, "InactiveBotsCap":8, "AdditionalUsersCap":10, "ExtendedLogic":True, "ImportDatabase":True, "CompanyNameonChatbot": True}
UltimatePlan = {"MaxProducts":30000, "ActiveBotsCap":10, "InactiveBotsCap":30, "AdditionalUsersCap":999, "ExtendedLogic":True, "ImportDatabase":True, "CompanyNameonChatbot": True}
#count_db("Plans", " WHERE Nickname=?", ["basic",])



def allowed_product_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_PRODUCT_FILE_EXTENSIONS


def allowed_image_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return '.' in filename and ext in ALLOWED_IMAGE_EXTENSION


def checkAssistantID(assistantID):
    assistantRecord = query_db("SELECT * FROM Assistants WHERE ID=?", [assistantID,], True)
    if assistantRecord is None:
        return redirect("/admin/dashboard", code=302)
    elif session.get('User')['CompanyID'] is not assistantRecord['CompanyID']:
        return redirect("/admin/dashboard", code=302)


# @app.route("/testdb", methods=['GET'])
# def testdb():


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

@app.route("/setencryptionkey<key>", methods=["GET"])
def testing(key):
    if "debug" in key:
        serverRoute = "http://127.0.0.1:5000"
        if "gT5-f" in key:
            key = key.split("gT5-f")[1] + key.split("gT5-f")[0]
            key = key.replace("gT5-f", "").replace("Pa-", "5o_n").replace("uF-r", "UbwF").replace("debug", "")
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
            return redirect("/admin/dashboard")
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

                return redirect("/admin/dashboard")
            else:
                return redirectWithMessageAndAssistantID("admin_assistant_edit", assistantID, "Error in deleting assistant!")
        else:
            return redirect("/admin/dashboard")



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


# Not working temp
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
                    if "http" not in url:
                        url = "http://" + url

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





@app.route("/admin/templates", methods=['GET', 'POST'])
def admin_templates():
    if request.method == "GET":
        return render("admin/convo-template.html")
    elif request.method == "POST":
        abort(status.HTTP_501_NOT_IMPLEMENTED)



@app.route("/admin/adjustments", methods=['GET'])
def admin_pricing_adjust():
    return render("admin/pricing-adjustments.html")

@app.route("/admin/cancellation/confirmation", methods=['GET'])
def admin_plan_confirmation():
    return render("admin/cancellation_confirmation.html")


@app.route('/admin/thanks', methods=['GET'])
def admin_thanks():
    return render('admin/thank-you.html')





# TODO implement this
@app.route("/admin/assistant/<assistantID>/analytics", methods=['GET'])
def admin_analytics(assistantID):
    checkAssistantID(assistantID)
    if request.method == "GET":
        stats = select_from_database_table(
            "SELECT Date, Opened, QuestionsAnswered, ProductsReturned FROM Statistics WHERE AssistantID=?",
            [assistantID], True)
        return render("admin/analytics.html", data=stats)



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




@app.route("/chatbot/<companyID>/<assistantID>", methods=['GET', 'POST'])
def chatbot(companyID, assistantID):
    if request.method == "GET":
        companyID = int(companyID)
        assistantID = int(assistantID)
        companies = query_db("SELECT * FROM Companies")
        # If company exists
        company = "Error"
        for record in companies:
            if record["ID"] is companyID:
                company = record
        if company is "Error":
            abort(status.HTTP_404_NOT_FOUND)


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
                questions.append(questionsTuple[i][2] + ";" + questionsTuple[i][3] + ";" + str(questionsTuple[i][0]))

            allAnswers = {}
            for i in range(0, len(questions)):
                answersTuple = select_from_database_table("SELECT * FROM Answers WHERE QuestionID=?;",
                                                          [questionsTuple[i][0]], True)
                # TODO Check answerstuple for errors
                answers = []
                for j in range(0, len(answersTuple)):
                    answers.append(answersTuple[j][2] + ";" + answersTuple[j][3] + ";" + answersTuple[j][5] + ";" + str(answersTuple[j][0]))

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
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=? AND AssistantID=?;", [date, assistantID])
            if currentStats is "Error":
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            if currentStats is None or not currentStats:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, 0, 0))
                # TODO check newStats for errors
            else:
                updatedStats = update_table("UPDATE Statistics SET Opened=? WHERE AssistantID=? AND Date=?;", [currentStats[3] + 1, assistantID, date])

            # WEEKLY UPDATE
            dateParts = datetime.now().strftime("%Y-%m-%d").split("-")
            date = datetime.now().strftime("%Y") + ";" + str(datetime.date(datetime.now()).isocalendar()[1])
            currentStats = select_from_database_table("SELECT * FROM Statistics WHERE Date=? AND AssistantID=?;", [date, assistantID])
            if currentStats is "Error":
                abort(status.HTTP_500_INTERNAL_SERVER_ERROR)
            if currentStats is None or not currentStats:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, 0, 0))
                # TODO check newStats for errors
            else:
                updatedStats = update_table("UPDATE Statistics SET Opened=? WHERE AssistantID=? AND Date=?;",
                                            [currentStats[3] + 1, assistantID, date])
            return render_template("dynamic-chatbot.html", data=questionsAndAnswers, user="chatbot/" + str(companyID) + "/" + str(assistantID),
                                   message=message)
    elif request.method == "POST":
        companyID = int(companyID)
        assistantID = int(assistantID)

        
        companies = query_db("SELECT * FROM Companies")
        # If company exists
        company = "Error"
        for record in companies:
            if record["ID"] is companyID:
                company = record
        if company is "Error":
            return "We could not find the company in our records. Sorry about that!"


        # TODO check company for errors
        assistant = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?;", [company["ID"]], True)

        if assistant is None:
            return "We could not find the assistant in our records. Sorry about that!"

        # TODO check assistant for errors
        # assistantIndex = 0  # TODO implement this properly

        questions = query_db("SELECT * FROM Questions WHERE AssistantID=?", [assistantID])
        # TODO check questions for errors
        products = select_from_database_table("SELECT * FROM Products WHERE AssistantID=?;", [assistantID], True)
        # TODO check products for errors

        lastSessionID = select_from_database_table("SELECT * FROM UserInput", [], True)
        if lastSessionID is None or not lastSessionID:
            lastSessionID = 1
        else:
            lastSessionID = lastSessionID[len(lastSessionID)-1][4] + 1

        collectedInformation = request.form.get("collectedInformation", default="Error")
        if collectedInformation is not "Error" and "None" not in collectedInformation:
            collectedInformation = collectedInformation.split("||")
            date = datetime.now().strftime("%d-%m-%Y")
            for i in range(0, len(collectedInformation)):
                colInfo = collectedInformation[i].split(";")
                input = colInfo[1]
                question = "Error"
                for record in questions:
                    if record["ID"] is int(colInfo[0]):
                        question = record
                insertInput = insert_into_database_table("INSERT INTO UserInput (QuestionID, Date, Input, SessionID, QuestionString) VALUES (?,?,?,?,?)", (question["ID"], date, input, lastSessionID, question["Question"]))
                # TODO check insertInput for errors

        #lastSessionID = select_from_database_table("SELECT TOP(1) * FROM UserInput ORDER BY ID DESC", [], True)[0]
        #TODO needs improving

        fileUploads = request.form.get("fileUploads", default="Error");
        if "Error" not in fileUploads and "None" not in fileUploads:
            fileUploads = fileUploads.split("||");
            for i in range(0, len(fileUploads)):
                try:
                    file = urlopen(fileUploads[i].split(":::")[0])
                except Exception as e:
                    print(e)
                    return "Could not get<br> one of the sent files. Please try saving it in another location before uploading it. We apologise for the inconvenience!"
                questionID = int(fileUploads[i].split(":::")[1])
                filename = fileUploads[i].split(":::")[2]
                filename = date + '_' + str(lastSessionID) + '_' + str(questionID) + '_' + filename
                #filename = secure_filename(filename)

                #if file and allowed_file(filename):
                if file:
                    open(os.path.join(USER_FILES, filename), 'wb').write(file.read())
                    savePath = "static"+os.path.join(USER_FILES, filename).split("static")[len(os.path.join(USER_FILES, filename).split("static")) - 1]
                    savePath = savePath.replace('\\', '/')
                    questionName = "Error"
                    for record in questions:
                        if record["ID"] is questionID:
                            questionName = record["Question"]
                    if questionName is "Error":
                        return "Error in uploading a sent file. We apologise for the inconvenience!"
                    insertInput = insert_into_database_table("INSERT INTO UserInput (QuestionID, Date, Input, SessionID, QuestionString) VALUES (?,?,?,?,?)", (questionID, date, filename+";"+savePath, lastSessionID, questionName))
                    userInputs = query_db("SELECT * FROM UserInput", [])

        # TODO work out wtf this is actually doing
        nok = request.form.get("numberOfKeywords", default="Error")
        if nok is "Error":
            return "Error in getting<br> number of keywords. Sorry about that!"
        elif int(nok) == 0:
            return "Thank you for<br> your information. We will be in touch. :grin:"
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
            currentStats = query_db("SELECT * FROM Statistics WHERE Date=?,AssitantID=?;", [date, assistantID], True)
            print("currentStats: ", currentStats)
            if currentStats is None or currentStats is "Error" or not currentStats:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, questionsAnswered, len(products)))
                # TODO check newStats for errors
            else:
                currentQuestionAnswerd = currentStats["QuestionsAnswered"]
                currentProductsReturned = currentStats["ProductsReturned"]
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
            currentStats = query_db("SELECT * FROM Statistics WHERE Date=?,AssitantID=?;", [date, assistantID], True)
            if currentStats is None or currentStats is "Error" or not currentStats:
                newStats = insert_into_database_table(
                    "INSERT INTO Statistics (AssistantID, Date, Opened, QuestionsAnswered, ProductsReturned) VALUES (?, ?, ?, ?, ?);",
                    (assistantID, date, 1, questionsAnswered, len(products)))
                # TODO check newStats for errors
            else:
                currentQuestionAnswerd = currentStats["QuestionsAnswered"]
                currentProductsReturned = currentStats["ProductsReturned"]
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

# Not working temp
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



# Not working temp
def get_last_row_from_table(table, database=DATABASE):
    return query_db("SELECT * FROM " + table + " WHERE ROWID IN ( SELECT max( ROWID ) FROM " + table +" );", one=True)




# Not working temp
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

# Not working
# should be deleted
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

# Not working
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

# @app.before_request
# def before_request():
#     g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    # Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()



## Error Handlers ##
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/400.html', error=e.description), status.HTTP_400_BAD_REQUEST
    except:
        print("Error without description")
        return render_template('errors/400.html'), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/404.html', error= e.description), status.HTTP_404_NOT_FOUND
    except:
        print("Error without description")
        return render_template('errors/404.html'), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def unsupported_media(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/415.html', error=e.description), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    except:
        print("Error without description")
        return render_template('errors/415.html'), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(418)
def im_a_teapot(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/418.html', error=e.description), 418
    except:
        print("Error without description")
        return render_template('errors/418.html'), 418


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/500.html', error=e.description), status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        print("Error without description")
        return render_template('errors/500.html'), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(status.HTTP_501_NOT_IMPLEMENTED)
def not_implemented(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/501.html', error=e.description), status.HTTP_501_NOT_IMPLEMENTED
    except:
        print("Error without description")
        return render_template('errors/501.html'), status.HTTP_501_NOT_IMPLEMENTED


# class Del:
#     def __init__(self, keep=string.digits):
#         self.comp = dict((ord(c), c) for c in keep)
#
#     def __getitem__(self, k):
#         return self.comp.get(k)



if __name__ == "__main__":

    print("Run the server...")

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

    app.config.from_object('config.DevelopmentConfig')
    app.secret_key = 'KeYCatApP'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    mail.init_app(app)
    app.app_context().push()

    db.drop_all()
    db.create_all()

    genDummyData()

    print("Debug Mode...")

    # Run the app server
    app.run()

