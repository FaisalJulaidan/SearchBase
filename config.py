import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'theNewDB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENV = 'production'
    DEBUG = False
    TESTING = False

    ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG',
                          'json', 'JSON', 'xml', 'xml',
                          'txt', 'pdf', 'doc', 'docx'}
    UPLOAD_FOLDER = '/static/file_uploads/user_files'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')

    SECRET_KEY = os.urandom(24)
    CSRF_SESSION_KEY = os.urandom(24)

    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'thesearchbase@gmail.com'
    MAIL_PASSWORD = 'pilbvnczzdgxkyzy'
    MAIL_SUPPRESS_SEND = False



class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    ENV = 'development'
    DEBUG = False
    TESTING = True
