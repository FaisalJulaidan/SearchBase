#/usr/bin/python3.5
from flask import Flask, redirect, request, render_template, session
from datetime import datetime
from services import assistant_services, user_services
import os
from models import db, Role, Company, Assistant, Plan, Statistics, Answer, ValidationType, Block, BlockType, Solution, ChatbotSession
from services.mail_services import mail
from utilities import helpers


# Import all routers to register them as blueprints
from routes.admin.routers import dashboard_router, profile_router,  admin_api, settings_router,\
    solutions_router, analytics_router, sub_router, connection_router, userInput_router, users_router,\
    changePassword_router, answers_router, bot_router, emoji_router, adminBasic_router,\
    assistantManager_router, assistant_router

from routes.public.routers import public_router, resetPassword_router
from services import user_services, mail_services

app = Flask(__name__, static_folder='static')

# Register Routes:
app.register_blueprint(adminBasic_router)
app.register_blueprint(assistantManager_router)
app.register_blueprint(assistant_router)
app.register_blueprint(dashboard_router)
app.register_blueprint(public_router)
app.register_blueprint(resetPassword_router)
app.register_blueprint(profile_router)
app.register_blueprint(admin_api)
app.register_blueprint(sub_router)
app.register_blueprint(settings_router)
app.register_blueprint(solutions_router)
app.register_blueprint(analytics_router)
app.register_blueprint(connection_router)
app.register_blueprint(userInput_router)
app.register_blueprint(changePassword_router)
app.register_blueprint(users_router)
app.register_blueprint(answers_router)
app.register_blueprint(bot_router)
app.register_blueprint(emoji_router)


# Code to ensure user is logged in
@app.before_request
def before_request():

    currentURL = str(request.url_rule)
    restrictedRoutes = ['/admin', 'admin/dashboard']

    # If the user try to visit one of the restricted routes without logging in he will be redirected
    if any(route in currentURL for route in restrictedRoutes) and not session.get('Logged_in', False):
        return redirect('login')


# Generates dummy data for testing
def gen_dummy_data():

    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com', StripeID='cus_00000000000000', SubID='sub_00000000000000'))
    db.session.add(Company(Name='Sabic', URL='ff.com', StripeID='cus_DbgKupMRLNYXly'))

    # Get Companies
    aramco = Company.query.filter(Company.Name == "Aramco").first()
    sabic = Company.query.filter(Company.Name == "Sabic").first()

    # Create Assistatns for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=aramco)
    helper_a = Assistant(Name="Helper", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", SecondsUntilPopup=1, Active=True, Company=sabic)

    # Create Blocks
    db.session.add(Block(Type=BlockType.Question, Order=1, StoreInDB=True, Assistant=reader_a, Content={
        "answers": [
          {
            "action": "Go To Next Block",
            "text": "Yes",
            "timesClicked": 0,
            "keywords": [
              "smoker",
              "sad"
            ],
            "blockToGoId": None,
            "afterMessage": ''
          },
          {
            "action": "Go To Next Block",
            "text": "No",
            "timesClicked": 0,
            "keywords": [
              "smoker",
              "sad"
            ],
            "blockToGoId": None,
            "afterMessage": ''

          }
        ],
        "id": 2,
        "order": 2,
        "text": "Do you smoke?",
      }))
    db.session.add(Block(Type=BlockType.UserInput, Order=2, StoreInDB=True, Assistant=reader_a, Content={
        "action": "Go To Next Block",
        "text": "What's your email?",
        "blockToGoID": None,
        "storeInDB": True,
        "validation": "Email",
        "afterMessage": 'Your input is being processed...'

    }))
    db.session.add(Block(Type=BlockType.FileUpload, Order=3, StoreInDB=True, Assistant=reader_a, Content={
        "action": "Go To Next Block",
        "fileTypes": [
        "doc",
        "pdf"
        ],
        "text": "Upload your CV",
        "blockToGoID": None,
        "afterMessage": 'File is being uploaded...'
    }))

    db.session.add(Block(Type=BlockType.Solutions, Order=4, StoreInDB=True, Assistant=reader_a, Content={
        "showTop": 5,
        "afterMessage": 'DONE!!!!',
    }))

    # Create Roles
    db.session.add(Role(Name="Owner", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= aramco, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    db.session.add(Role(Name="Owner", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= sabic, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    # Get Roles
    owner_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Owner").first()
    admin_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Admin").first()
    user_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "User").first()

    owner_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Owner").first()
    admin_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Admin").first()
    user_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "User").first()

    # Create Users
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

    # Plans
    db.session.add(Plan(ID='plan_D3lp2yVtTotk2f', Nickname='basic', MaxSolutions=600, MaxBlocks=20, ActiveBotsCap=2, InactiveBotsCap=3,
                        AdditionalUsersCap=5, ExtendedLogic=False, ImportDatabase=False, CompanyNameOnChatbot=False))

    db.session.add(
        Plan(ID='plan_D3lpeLZ3EV8IfA', Nickname='ultimate', MaxSolutions=5000, MaxBlocks=20, ActiveBotsCap=4, InactiveBotsCap=8,
             AdditionalUsersCap=10, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(
        Plan(ID='plan_D3lp9R7ombKmSO', Nickname='advanced', MaxSolutions=30000, MaxBlocks=20, ActiveBotsCap=10, InactiveBotsCap=30,
             AdditionalUsersCap=999, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))
    
    db.session.add(Plan(ID='plan_D48N4wxwAWEMOH', Nickname='debug', MaxSolutions=100, MaxBlocks=30,  ActiveBotsCap=2, InactiveBotsCap=2,
                        AdditionalUsersCap=3, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(Solution(SolutionID='D48N4wxwAWEMOH', MajorTitle='Big Title 1', SecondaryTitle="Small Title 1",
                            ShortDescription="A job at my little town",  Money="£56000", Keywords="smoker,duck",
                            URL="http://google.com", Assistant=reader_a, TimesReturned=2))

    db.session.add(Solution(SolutionID='asd8213AWEMOH', MajorTitle='Big Title 2', SecondaryTitle="Small Title 2",
                            ShortDescription="A town at my little job",  Money="£56000", Keywords="dog,sad",
                            URL="http://google.com", Assistant=reader_a, TimesReturned=10))

    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,18), SolutionsReturned=40, QuestionsAnswered=25, TimeSpent=120, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,16), SolutionsReturned=55, QuestionsAnswered=25, TimeSpent=120, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,16), SolutionsReturned=12, QuestionsAnswered=28, TimeSpent=127, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,15), SolutionsReturned=64, QuestionsAnswered=45, TimeSpent=300, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,6), SolutionsReturned=11, QuestionsAnswered=12, TimeSpent=50, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,5), SolutionsReturned=636, QuestionsAnswered=5, TimeSpent=23, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 9,1), SolutionsReturned=84, QuestionsAnswered=22, TimeSpent=67, Assistant=reader_a))
    db.session.add(ChatbotSession(Data={'f':3}, DateTime=datetime(2018, 7,1), SolutionsReturned=123, QuestionsAnswered=17, TimeSpent=80, Assistant=reader_a))

    # Save all changes
    db.session.commit()


@app.route("/admin/cancellation/confirmation", methods=['GET'])
def admin_plan_confirmation():
    return render("admin/cancellation_confirmation.html")


@app.route('/admin/thanks', methods=['GET'])
def admin_thanks():
    return render('admin/thank-you.html')


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


if __name__ == "__main__":

    print("Run the server...")
    if os.environ['FLASK_ENV'] == 'production':
        app.config.from_object('config.BaseConfig')

        db.init_app(app)
        mail.init_app(app)
        app.app_context().push()

        print('Production mode running...')
        # Run the app server
        app.run()

    elif os.environ['FLASK_ENV'] == 'development' :
        app.config.from_object('config.DevelopmentConfig')

        db.init_app(app)
        mail.init_app(app)
        app.app_context().push()

        print('Reinitialize the database...')
        db.drop_all()
        db.create_all()
        gen_dummy_data()
        print('Development mode running...')

        # Run the app server
        app.run()
    else:
        print("Please set FLASK_ENV first to either 'production' or 'development' \r\n "
              "ex. in Windows >set FLASK_ENV=development, in Linux/Mac >export FLASK_ENV=development \r\n"
              "then run the server >python app.py")


