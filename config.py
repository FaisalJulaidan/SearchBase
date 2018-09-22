import os
from models import useEncryption

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'theNewDB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENV = 'production'
    DEBUG = False
    TESTING = False

    ALLOWED_EXTENSIONS = {'png', 'jpg','json', 'xml','txt', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')

    SECRET_KEY = os.urandom(24)
    CSRF_SESSION_KEY = os.urandom(24)
    SESSION_TYPE = 'filesystem'
    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'thesearchbase@gmail.com'
    MAIL_PASSWORD = 'pilbvnczzdgxkyzy'
    MAIL_SUPPRESS_SEND = False
    useEncryption = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    ENV = 'development'
    DEBUG = False
    TESTING = True
