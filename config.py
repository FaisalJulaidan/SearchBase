import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):


    ALLOWED_EXTENSIONS = {'png', 'jpg','json', 'xml','txt', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    SECRET_KEY = os.urandom(24)
    SECRET_KEY_DB = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    CSRF_SESSION_KEY = os.urandom(24)
    SESSION_TYPE = 'filesystem'
    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'thesearchbase@gmail.com'
    MAIL_PASSWORD = 'pilbvnczzdgxkyzy'
    MAIL_SUPPRESS_SEND = False
    USE_ENCRYPTION = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Production.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Lithium3@localhost/MySQLProduction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = True

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Development.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/MySQLDevelopment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    ENV = 'test'
    DEBUG = False
    TESTING = True
