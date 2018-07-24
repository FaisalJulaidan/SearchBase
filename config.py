import os


class BaseConfig(object):

    DEBUG = False
    TESTING = False

    ALLOWED_IMAGE_EXTENSION = {'png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG'}
    ALLOWED_PRODUCT_FILE_EXTENSIONS = {'json', 'JSON', 'xml', 'xml'}

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')

    SECRET_KEY = os.urandom(24)
    CSRF_SESSION_KEY = os.urandom(24)


    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'thesearchbase@gmail.com',
    MAIL_PASSWORD = 'pilbvnczzdgxkyzy'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True