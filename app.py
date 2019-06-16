#/usr/bin/python3.5
import os
import config
from flask import Flask, render_template, request
from flask_api import status
from models import db, Callback, Assistant
from services.mail_services import mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import create_database, database_exists
from services.auth_services import jwt
from utilities import helpers, tasks, dummy_data
from flask_babel import Babel
from services import scheduler_services, mail_services, assistant_services
from datetime import datetime
# Import all routers to register them as blueprints
from routes.admin.routers import profile_router, analytics_router, sub_router, \
    conversation_router, users_router, flow_router, assistant_router,\
    database_router, options_router, crm_router, auto_pilot_router
from routes.public.routers import public_router, reset_password_router, chatbot_router, auth_router, appointment_router

app = Flask(__name__, static_folder='static')

# Register Routes:
app.register_blueprint(assistant_router, url_prefix='/api')
app.register_blueprint(flow_router, url_prefix='/api')
app.register_blueprint(crm_router, url_prefix='/api')
app.register_blueprint(public_router)
app.register_blueprint(reset_password_router, url_prefix='/api')
app.register_blueprint(profile_router, url_prefix='/api')
app.register_blueprint(sub_router)
app.register_blueprint(analytics_router, url_prefix='/api')
app.register_blueprint(conversation_router, url_prefix='/api')
app.register_blueprint(users_router, url_prefix='/api')
app.register_blueprint(chatbot_router, url_prefix='/api')
app.register_blueprint(auth_router, url_prefix='/api')
app.register_blueprint(database_router, url_prefix='/api')
app.register_blueprint(auto_pilot_router, url_prefix='/api')
app.register_blueprint(options_router, url_prefix='/api')
app.register_blueprint(appointment_router, url_prefix='/api')


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    return response


# 404 Error Handler
@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/404.html', error= e.description), status.HTTP_404_NOT_FOUND
    except:
        print("Error without description")
        return render_template('errors/404.html'), status.HTTP_404_NOT_FOUND


@crm_router.route("/bullhorn_callback", methods=['GET', 'POST', 'PUT'])
def test_crm_123():
    print("got something here", request)
    return request


# Server Setup
db.app = app
migrate_var = Migrate(app, db)
manager = Manager(app)
babel = Babel(app)
# scheduler = APScheduler()
manager.add_command('db', MigrateCommand)


# will be used for migration purposes
@manager.command
def run_tasks():
    tasks.migrate_flow()


print("Run the server...")
if os.environ['FLASK_ENV'] in ['production', 'staging']:
    # Server Setup
    app.config.from_object('config.ProductionConfig')
    url = os.environ['SQLALCHEMY_DATABASE_URI']

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    app.app_context().push()

    if not database_exists(url):
        print('Create db tables')
        create_database(url)
        db.create_all()

    # Check if staging what to do
    # scheduler.start()

    print('Production mode running...')

elif os.environ['FLASK_ENV'] == 'development':

    # Server Setup
    app.config.from_object('config.DevelopmentConfig')
    config.BaseConfig.USE_ENCRYPTION = False

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    url = os.environ['SQLALCHEMY_DATABASE_URI']  # get database URL
    if os.environ['REFRESH_DB_IN_DEV'] == 'yes':
        print('Reinitialize the database...')
        db.drop_all()
        db.create_all()
        dummy_data.generate()

    # payload = str(5) + ";" + str(1) + ";" + str(1) + ";"  + "Faisal Jul"
    # mail_services.send_email(
    #     "Julaidan.faisal@gmail.com",
    #     'Appointment',
    #     '/emails/appointment_letter.html',
    #     companyName="Company Name",
    #     logoPath="f",
    #     userName="Faisal Jula",
    #     appointmentLink=helpers.getDomain() + "/appointments_picker/" + \
    #                     helpers.verificationSigner.dumps(payload, salt='appointment-key')
    # )

    # a = datetime.strptime("2019-12-14 16:08", "%Y-%m-%d %H:%M")
    # print(a)

    print('Development mode running...')

else:
    raise Exception("Please set FLASK_ENV first to either 'production', 'development', or 'staging' in .env file")

# Run the migration if in .env, MIGRATION = yes
if os.environ['MIGRATION'] == 'yes':
    print('Migration mode running...')
    manager.run()