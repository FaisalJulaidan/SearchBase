#/usr/bin/python3.5
import os
import config
from flask import Flask, render_template
from flask_api import status
from models import db
from services.mail_services import mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import create_database, database_exists, drop_database
from flask_apscheduler import APScheduler
from services.auth_services import jwt
from utilities import helpers, tasks
from flask_babel import Babel
from services.CRM import CRM_base
import enums
# Import all routers to register them as blueprints
from routes.admin.routers import profile_router, analytics_router, sub_router,\
    connection_router, chatbotSession_router, users_router, flow_router, assistant_router,\
    database_router, options_router

from routes.public.routers import public_router, resetPassword_router, chatbot_router, auth_router

app = Flask(__name__, static_folder='static')


# Register Routes:
app.register_blueprint(assistant_router, url_prefix='/api')
app.register_blueprint(flow_router, url_prefix='/api')
app.register_blueprint(public_router)
app.register_blueprint(resetPassword_router, url_prefix='/api')
app.register_blueprint(profile_router, url_prefix='/api')
app.register_blueprint(sub_router)
app.register_blueprint(analytics_router, url_prefix='/api')
app.register_blueprint(connection_router, url_prefix='/api')
app.register_blueprint(chatbotSession_router, url_prefix='/api')
app.register_blueprint(users_router, url_prefix='/api')
app.register_blueprint(chatbot_router, url_prefix='/api')
app.register_blueprint(auth_router, url_prefix='/api')
app.register_blueprint(database_router, url_prefix='/api')
app.register_blueprint(options_router, url_prefix='/api')


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
db.app = app
migrate_var = Migrate(app, db)
manager = Manager(app)
babel = Babel(app)
scheduler = APScheduler()
manager.add_command('db', MigrateCommand)


# will be used for migration purposes
@manager.command
def run_tasks():
    tasks.migrate_flow()


print("Run the server...")
if os.environ['FLASK_ENV'] == 'production':
    # Server Setup
    app.config.from_object('config.ProductionConfig')
    url = os.environ['SQLALCHEMY_DATABASE_URI']

    app.config['SECRET_KEY_DB'] = config.set_encrypt_key()  # IMPORTANT!
    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    app.app_context().push()

    if not database_exists(url):
        print('Create db tables')
        create_database(url)
        db.create_all()
        helpers.seed()

    scheduler.start()
    print('Production mode running...')

elif os.environ['FLASK_ENV'] == 'development':
    # Server Setup
    app.config.from_object('config.DevelopmentConfig')
    config.BaseConfig.USE_ENCRYPTION = False
    config.BaseConfig.USE_ENCRYPTION = False

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)

    url = os.environ['SQLALCHEMY_DATABASE_URI'] # get database URL
    if os.environ['REFRESH_DB_IN_DEV'] == 'yes':
        print('Reinitialize the database...')
        # drop_database(url)
        # create_database(url)
        db.drop_all()
        db.create_all()
        helpers.gen_dummy_data()

    scheduler.start()
    print('Development mode running...')
    # CRM_base.insertCandidate("PartnerDomain9", "SD9USR7", "P@55word", enums.CRM.Adapt)


else:
    print("Please set FLASK_ENV first to either 'production' or 'development' in .env file")


# Run the migration if in .env, MIGRATION = ues
if os.environ['MIGRATION'] == 'yes':
    print('Migration mode running...')
    manager.run()