import os
from datetime import timedelta
from urllib import request
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# Needs to be above BaseConfig
def set_encrypt_key():
    print("===< Setting DB Secret Key >===")
    print("Starting key retrieval...")

    page = request.urlopen("https://bjhbcjvrawpiuqwyrzwxcksndmwpeo.herokuapp.com/static/skajhefjwehfiuwheifhxckjbachowejfhnkjfnlwgifnwoihfuwbkjcnkjfil.html")
    text = page.read().decode("utf8")

    part1 = text.split("FD-Y%%$VfdsaGSdsHB-%$-DFmrcStFa-S")[1].split("FEAewSvj-JGvbhKJQz-xsWEKc3-WRxjhT")[0].replace('La', 'H-q').replace('TrE', 'gb')
    print("Part 1 set")

    part2 = text.split("GFoiWS$344wf43-cWzHOp")[1].split("Ye3Sv-FE-vWaIt3xWkbE6bsd7-jS")[0].replace('8B', '3J')
    print("Part 2 set")

    part3 = text.split(".tic")[1].split("Icon")[0]
    print("Part 3 set")

    part4 = text.split("YbfEas-fUh")[1].split("TbCO")[0].replace('P-', '-G')
    print("Part 4 set")

    part5 = text.split("gTb2I-6BasRb41BVr6fg-heWpB0-")[1].split("-PoWb5qEc-sMpAp-4BaOln")[0].replace('-9yR', '_nU')
    print("Part 5 set")

    part6 = text.split("sMpAp-4BaOln")[1]

    enckey = (part1+part2+part3+part4+part5+part6).replace(" ", "")
    print("Key set")
    return enckey


class BaseConfig(object):

    ALLOWED_EXTENSIONS = {'png', 'jpg','json', 'xml', 'xls', 'xlsx', 'txt', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    # Secret keys
    SECRET_KEY = os.urandom(24)
    CSRF_SESSION_KEY = os.urandom(24)
    JWT_SECRET_KEY = b'\\P\xa1\t\xf2\x86\xc7\x906Z\xb1\x92i\xb0\xde\xa7\xad\xfab\xa0\xed\x10\xa6\xa2' \
        if os.environ['FLASK_ENV'] == 'development' else os.urandom(24)

    # JWT tokens expires in
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=20)

    SESSION_TYPE = 'filesystem'
    USE_ENCRYPTION = True
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299
    # SQLALCHEMY_POOL_TIMEOUT = 20


    # Hashids Salt
    HASH_IDS_SALT = 'b9iLXiAa'  # Never change it

    # Calendar Config
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'thesearchbase@gmail.com'
    # MAIL_PASSWORD = 'orfqpgqiusxcoeif'
    # MAIL_SUPPRESS_SEND = False

    # # Calendar Config
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = 'info@thesearchbase.com'
    # MAIL_PASSWORD = 'yyfcnddsbwhnqknj'
    MAIL_USERNAME = 'notifications@thesearchbase.com'
    MAIL_PASSWORD = 'whllvfxnpdqkxjtg'
    MAIL_SUPPRESS_SEND = False


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    USE_ENCRYPTION = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    USE_ENCRYPTION = False





class TestingConfig(BaseConfig):
    ENV = 'test'
    DEBUG = False
    TESTING = True
