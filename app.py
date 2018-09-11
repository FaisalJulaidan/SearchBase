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
#from celery import Celery

from models import db, Role, Company, Assistant, Plan, Statistics, Question, Answer, QuestionType, QuestionAction,\
    QuestionFU, QuestionUI, QuestionPA, UserInputValidation
from services.mail_services import mail
#, celery

# Import all routers to register them as blueprints
from routes.admin.routers import dashboard_router, profile_router,  admin_api, settings_router,\
    products_router, questions_router, analytics_router, sub_router, connection_router, userInput_router, users_router,\
    changePassword_router, answers_router, bot_router, emoji_router, adminBasic_router, assistantManager_router

from routes.public.routers import public_router, resetPassword_router
from services import user_services, mail_services

app = Flask(__name__, static_folder='static')

app.register_blueprint(adminBasic_router)
app.register_blueprint(assistantManager_router)
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


# Generates dummy data for testing
def genDummyData():

    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com'))
    db.session.add(Company(Name='Sabic', URL='ff.com'))

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

    user_services.create(firstname='Ahmad', surname='Hadi', email='aa@aa.com', password='123', phone='4344423',
                         company=aramco, role=owner_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', phone='4344423', company=aramco,
                         role=admin_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', phone='4344423', company=aramco,
                         role=user_aramco, verified=True)

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='4344423', company=sabic,
                         role=owner_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', phone='4344423', company=sabic,
                         role=admin_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e6@e.com', password='123', phone='4344423', company=sabic,
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

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=465,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME='thesearchbase@gmail.com',
#     MAIL_PASSWORD='pilbvnczzdgxkyzy'
# )

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

