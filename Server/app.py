# /usr/bin/python3.5

from gevent import monkey

monkey.patch_all()

import os, datetime, time
from flask import Flask, render_template, request
from flask_api import status
from flask_babel import Babel
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils import create_database, database_exists
import config
from models import db, Callback
# Import all routers to register them as blueprints
from routes.admin.routers import account_router, analytics_router, sub_router, \
    conversation_router, users_router, flow_router, assistant_router, \
    database_router, options_router, marketplace_router, auto_pilot_router, appointment_router, webhook_router, \
    campaign_router, crm_auto_pilot_router
from routes.public.routers import public_router, reset_password_router, chatbot_router, auth_router
from routes.staff.routers import staff_router
from services import scheduler_services, url_services
from services.auth_services import jwt
from services.mail_services import mail
from utilities import helpers, tasks, dummy_data


# from utilities.helpers import limiter
app = Flask(__name__, static_folder='static')

# Register Routes:
app.register_blueprint(assistant_router, url_prefix='/api')
app.register_blueprint(flow_router, url_prefix='/api')
app.register_blueprint(marketplace_router, url_prefix='/api')
app.register_blueprint(public_router)
app.register_blueprint(reset_password_router, url_prefix='/api')
app.register_blueprint(account_router, url_prefix='/api')
app.register_blueprint(sub_router)
app.register_blueprint(analytics_router, url_prefix='/api')
app.register_blueprint(conversation_router, url_prefix='/api')
app.register_blueprint(users_router, url_prefix='/api')
app.register_blueprint(chatbot_router, url_prefix='/api')
app.register_blueprint(auth_router, url_prefix='/api')
app.register_blueprint(campaign_router, url_prefix='/api')
app.register_blueprint(database_router, url_prefix='/api')
app.register_blueprint(auto_pilot_router, url_prefix='/api')
app.register_blueprint(crm_auto_pilot_router, url_prefix='/api')
app.register_blueprint(options_router, url_prefix='/api')
app.register_blueprint(appointment_router, url_prefix='/api')
app.register_blueprint(webhook_router, url_prefix='/api')
app.register_blueprint(staff_router, url_prefix='/api/staff')


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers["X-Frame-Options"] = "DENY"
    return response


# 404 Error Handler
@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/404.html', error=e.description), status.HTTP_404_NOT_FOUND
    except:
        print("Error without description")
        return render_template('errors/404.html'), status.HTTP_404_NOT_FOUND


# Requests limiter initialisation:
# limiter.init_app(app)
# limiter.enabled = os.environ['FLASK_ENV'] != 'development'

# Custom limiter exceeded error response
@app.errorhandler(429)
def ratelimit_handler(e):
    return helpers.jsonResponse(False, 429, "ratelimit exceeded %s" % e.description, None)


@marketplace_router.route("/bullhorn_callback", methods=['GET', 'POST', 'PUT'])
def test_crm_123():
    print("got something here", request)
    return request


# Server Setup
migrate_var = Migrate(app, db)
manager = Manager(app)
babel = Babel(app)
manager.add_command('db', MigrateCommand)
app.jinja_env.add_extension('jinja2.ext.do')  # Add 'do' extension to Jinja engine


# will be used for migration purposes
@manager.command
def run_tasks(functionName):
    getattr(tasks, functionName)()


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
        helpers.seed()

    # Start scheduled tasks
    if not os.environ.get("scheduler_lock"):
        scheduler_services.scheduler.start()
        os.environ["scheduler_lock"] = "True"

    print('Production mode running...')

elif os.environ['FLASK_ENV'] == 'development':
    # Server Setup
    app.config.from_object('config.DevelopmentConfig')
    config.BaseConfig.USE_ENCRYPTION = False

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    app.app_context().push()

    url = os.environ['SQLALCHEMY_DATABASE_URI']  # get database URL
    if os.environ['REFRESH_DB_IN_DEV'] == 'yes':
        print('Reinitialize the database...')
        db.drop_all()
        db.create_all()
        dummy_data.generate()

    # Start scheduled tasks
    if not os.environ.get("scheduler_lock"):
        # scheduler_services.scheduler.start()
        os.environ["scheduler_lock"] = "True"

    print('Development mode running...')

else:
    raise Exception("Please set FLASK_ENV first to either 'production', 'development', or 'staging' in .env file")

# Run the migration if in .env, MIGRATION = yes
if os.environ['MIGRATION'] == 'yes':
    print('Migration mode running...')
    manager.run()
