#/usr/bin/python3.5
import os
import config
from flask import Flask, redirect, request, render_template, session
from flask_api import status
from services import assistant_services, user_services
from models import db, Plan
from services.mail_services import mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, command
from sqlalchemy_utils import create_database, database_exists
from flask_apscheduler import APScheduler
from utilities import helpers


# Import all routers to register them as blueprints
from routes.admin.routers import dashboard_router, profile_router,  admin_api, settings_router,\
    solutions_router, analytics_router, sub_router, connection_router, userInput_router, users_router,\
    changePassword_router, bot_router, adminBasic_router,\
    assistantManager_router, assistant_router

from routes.public.routers import public_router, resetPassword_router

app = Flask(__name__, static_folder='static')
db.app = app


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
app.register_blueprint(bot_router)


# Code to ensure user is logged in
@app.before_request
def before_request():

    currentURL = str(request.url_rule)
    restrictedRoutes = ['/admin', 'admin/dashboard']

    # If the user try to visit one of the restricted routes without logging in he will be redirected
    if any(route in currentURL for route in restrictedRoutes):
        print("Security Check For Restricted Routes")
        if not session.get('Logged_in', False):
            return redirect('login')
        try:
            if request.view_args['assistantID']:
                assistantID = int(request.view_args['assistantID'])
                ownership_callback = assistant_services.checkOwnership(assistantID, session.get('CompanyID', None))
                if not ownership_callback.Success:
                    return helpers.hardRedirectWithMessage("login", ownership_callback.Message)
                role_callback = user_services.getRolePermissions(session.get('UserID', None))
                if not role_callback.Success:
                    return helpers.hardRedirectWithMessage("admin/dashboard", role_callback.Message)
                if not role_callback.Data.EditChatbots:
                    return helpers.hardRedirectWithMessage("admin/dashboard", "Your company owner has not allowed you access to this feature.")
        except:
            pass


# @manager.command
def seed():

    # Plans
    db.session.add(Plan(ID='plan_D3lp2yVtTotk2f', Nickname='basic', MaxSolutions=600, MaxBlocks=100, ActiveBotsCap=2,
                        InactiveBotsCap=3,
                        AdditionalUsersCap=5, ExtendedLogic=False, ImportDatabase=False, CompanyNameOnChatbot=False))

    db.session.add(
        Plan(ID='plan_D3lpeLZ3EV8IfA', Nickname='ultimate', MaxSolutions=5000, MaxBlocks=100, ActiveBotsCap=4,
             InactiveBotsCap=8,
             AdditionalUsersCap=10, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(
        Plan(ID='plan_D3lp9R7ombKmSO', Nickname='advanced', MaxSolutions=30000, MaxBlocks=100, ActiveBotsCap=10,
             InactiveBotsCap=30,
             AdditionalUsersCap=999, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(Plan(ID='plan_D48N4wxwAWEMOH', Nickname='debug', MaxSolutions=100, MaxBlocks=100, ActiveBotsCap=2,
                        InactiveBotsCap=2,
                        AdditionalUsersCap=3, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))
    db.session.commit()



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


# Server Setup
migrate_var = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
scheduler = APScheduler()

print("Run the server...")
if os.environ['FLASK_ENV'] == 'production':

    app.config.from_object('config.ProductionConfig')
    url = os.environ['SQLALCHEMY_DATABASE_URI']

    # Server Setup
    app.config['SECRET_KEY_DB'] = config.set_encrypt_key() # IMPORTANT!
    db.init_app(app)
    mail.init_app(app)
    app.app_context().push()

    if not database_exists(url):
        print('Create db tables')
        create_database(url)
        db.create_all()
        seed()

    # Run the app server
    if os.environ['DB_MIGRATION'] == 'yes':
        print('Database migration mode...')
        manager.run()
    else:
        print('Production mode running...')
        # app.run()

elif os.environ['FLASK_ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')

    # Server Setup
    print("Use Encryption:", app.config['USE_ENCRYPTION'])
    print("Secret DB Key:", app.config['SECRET_KEY_DB'])
    db.init_app(app)
    mail.init_app(app)
    app.app_context().push()

    print('Reinitialize the database...')
    db.drop_all()
    db.create_all()
    helpers.gen_dummy_data()

    scheduler.init_app(app)
    # scheduler.start()

    # Run the app server
    print('Development mode running...')
    # app.run(threaded = True)
else:
    print("Please set FLASK_ENV first to either 'production' or 'development' in .env file")
