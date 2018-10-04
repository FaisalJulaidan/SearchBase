import os
from datetime import timedelta
from urllib import request
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#needs to be above basicconfig
def set_encrypt_key(key):
    print("Starting key retrieval")
    serverRoute = "http://206.189.122.126"
    print("Part 0.1")
    page = request.urlopen(serverRoute + "/static/js/sortTable.js")
    print("Part 0.2")
    text = page.read().decode("utf8")
    print("Part 0.3")
    part1 = text.split("FD-Y%%$VfdsaGSdsHB-%$-DFmrcStFa-S")[1].split("FEAewSvj-JGvbhKJQz-xsWEKc3-WRxjhT")[0].replace('La', 'H-q').replace('TrE', 'gb')
    print("Part 1 set")
    page = request.urlopen(serverRoute + "/static/js/Chart.bundle.js")
    text = page.read().decode("utf8")
    part2 = text.split("GFoiWS$344wf43-cWzHOp")[1].split("Ye3Sv-FE-vWaIt3xWkbE6bsd7-jS")[0].replace('8B', '3J')
    print("Part 2 set")
    page = request.urlopen(serverRoute + "/static/css/admin.css")
    text = page.read().decode("utf8")
    part3 = text.split(".tic")[1].split("Icon")[0]
    print("Part 3 set")
    page = request.urlopen(serverRoute + "/static/css/themify-icons.css")
    text = page.read().decode("utf8")
    part4 = text.split("YbfEas-fUh")[1].split("TbCO")[0].replace('P-', '-G')
    print("Part 4 set")

    page = request.urlopen("https://bjhbcjvrawpiuqwyrzwxcksndmwpeo.herokuapp.com/static/skajhefjwehfiuwheifhxckjbachowejfhnkjfnlwgifnwoihfuwbkjcnkjfil.html")
    text = page.read().decode("utf8")
    part5 = text.split("gTb2I-6BasRb41BVr6fg-heWpB0-")[1].split("-PoWb5qEc-sMpAp-4BaOln")[0].replace('-9yR', '_nU')
    print("Part 5 set")
    enckey = part1+part2+part3+part4+part5
    enckey = (enckey+key).replace(" ", "")
    print("Key set")
    return enckey


class BaseConfig(object):

    ALLOWED_EXTENSIONS = {'png', 'jpg','json', 'xml','txt', 'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PRODUCT_FILES = os.path.join(APP_ROOT, 'static/file_uploads/product_files')
    USER_FILES = os.path.join(APP_ROOT, 'static/file_uploads/user_files')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    SECRET_KEY = os.urandom(24)
    SECRET_KEY_DB = set_encrypt_key(os.environ['ENCRYPT_KEY'])
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

    JOBS = [
        {
            'id': 'notify',
            'func': 'services.mail_services:notifyNewRecordsForLastXHours',
            'args': (8,),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = True

    # MySQL
    # SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

    # SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    ENV = 'test'
    DEBUG = False
    TESTING = True
