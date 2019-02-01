#/usr/bin/python3.5
import os
import config
from flask import Flask, render_template
from flask_api import status
from models import db, User
from services.mail_services import mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, command
from sqlalchemy_utils import create_database, database_exists
from flask_apscheduler import APScheduler
from services.jwt_auth_services import jwt
from utilities import helpers
import pandas
import re
# Import all routers to register them as blueprints
from routes.admin.routers import profile_router, settings_router,\
    solutions_router, analytics_router, sub_router, connection_router, chatbotSession_router, users_router,\
    changePassword_router, bot_router, flow_router, assistant_router

from routes.public.routers import public_router, resetPassword_router, chatbot_router, auth_router

app = Flask(__name__, static_folder='static')
db.app = app


# Register Routes:
app.register_blueprint(assistant_router, url_prefix='/api')
app.register_blueprint(flow_router, url_prefix='/api')
app.register_blueprint(public_router)
app.register_blueprint(resetPassword_router)
app.register_blueprint(profile_router, url_prefix='/api')
app.register_blueprint(sub_router)
app.register_blueprint(settings_router)
app.register_blueprint(solutions_router, url_prefix='/api')
app.register_blueprint(analytics_router, url_prefix='/api')
app.register_blueprint(connection_router, url_prefix='/api')
app.register_blueprint(chatbotSession_router, url_prefix='/api')
app.register_blueprint(changePassword_router)
app.register_blueprint(users_router)
app.register_blueprint(bot_router)
app.register_blueprint(chatbot_router)
app.register_blueprint(auth_router, url_prefix='/api')


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
jwt.init_app(app)

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
        helpers.seed()

    scheduler.init_app(app)
    scheduler.start()

    # Run the app server
    if os.environ['DB_MIGRATION'] == 'yes':
        print('Database migration mode...')
        manager.run()
    else:
        print('Production mode running...')

elif os.environ['FLASK_ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
    config.BaseConfig.USE_ENCRYPTION = False
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
    scheduler.start()

    # # Test with data analysis using Pandas library
    # df = pandas.read_sql_query("SELECT * FROM User", db.get_engine(app))
    # keywords = ['Hadi', 'name', 'Ali', 4]
    # df['result'] = df['Firstname'] + " " + df['Surname'] + " " + df['Email'] + " " + df['PhoneNumber']
    # df['count'] = df.result.str.count('h', flags=re.IGNORECASE)
    # df.loc[df.RoleID >=3, ['count']] += 5
    #
    # print(df)
    # print(df.nlargest(2, 'count').to_json(orient='records'))
    #
    # # Run the app server
    # print('Development mode running...')

else:
    print("Please set FLASK_ENV first to either 'production' or 'development' in .env file")
