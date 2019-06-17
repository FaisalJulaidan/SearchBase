from flask import json, after_this_request, request
from models import db, Role, Company, Assistant, Plan, Conversation, Database, Candidate, Job, CRM,\
    OpenTimeSlot, AutoPilot, Appointment, Callback
from services import user_services, flow_services, auto_pilot_services, assistant_services, scheduler_services
from datetime import datetime, timedelta, time
from enum import Enum
from hashids import Hashids
from config import BaseConfig
from io import BytesIO
from itsdangerous import URLSafeTimedSerializer
from cryptography.fernet import Fernet
from sqlalchemy_utils import Currency
from jsonschema import validate
from utilities import json_schemas
from typing import List
from flask_jwt_extended import get_jwt_identity
from utilities import tasks
import enums, re, os, stripe, gzip, functools, logging, geoip2.webservice
import inspect

# will merge with the previous imports if the code is kept - batu


# GeoIP Client
geoIP = geoip2.webservice.Client(140914, 'cKrqAZ675SPb')

# Signer
verificationSigner = URLSafeTimedSerializer(os.environ['SECRET_KEY_TEMP'])

# Configure logging system
logging.basicConfig(filename='logs/errors.log',
                    level=logging.ERROR,
                    format='%(asctime)s -- %(message)s')

# Fernet for encryption
fernet = Fernet(os.environ['SECRET_KEY_TEMP'])


# ID Hasher
# IMPORTANT: don't you ever make changes to the hash values before consulting Faisal Julaidan
hashids = Hashids(salt=BaseConfig.HASH_IDS_SALT, min_length=5)
def encode_id(id):
    return hashids.encrypt(id)

def decode_id(id):
    return hashids.decrypt(id)

# Encryptors
def encrypt(value, isDict=False):
    if isDict: value=json.dumps(value)
    return fernet.encrypt(bytes((value.encode('utf-8'))))

def decrypt(token, isDict=False, isBtye=False):
    if not isBtye: token=bytes(token.encode('utf-8'))
    value = fernet.decrypt(token)
    if isDict: value=json.loads(value)
    return value


# Generates dummy data for testing
def gen_dummy_data():

    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com', StripeID='cus_00000000000000', SubID='sub_00000000000000'))
    db.session.add(Company(Name='Sabic', URL='ff.com', StripeID='cus_DbgKupMRLNYXly'))

    # Get Companies
    aramco: Company = Company.query.filter(Company.Name == "Aramco").first()
    sabic: Company = Company.query.filter(Company.Name == "Sabic").first()

    # Create and validate a flow for an assistant

    # job = scheduler_services.scheduler.add_job(func=scheduler_services.printSomething, trigger='interval', seconds=5, id="3559a1946b52419899e8841d4317d194", replace_existing=True)
    # scheduler_services.scheduler.start()

    # Create Assistants for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there",
                         TopBarText="Aramco Bot", SecondsUntilPopup=1,
                         Active=True, Company=aramco)



    flow = {
        "groups": [
            {
                "id": "tisd83f4",
                "name": "group 1",
                "description": "The best group",
                "blocks": [
                    {
                        "ID":"8EDEBiDHa",
                        "Type":"Question",
                        "StoreInDB":True,
                        "Skippable":False,
                        "SkipText":"Skip!",
                        "SkipAction":"End Chat",
                        "SkipBlockToGoID": None,
                        "DataType":"CandidateAvailability",
                        "Content":{
                            "text":"what?",
                            "answers":[
                                {
                                    "id":"WZXp26mdL",
                                    "text":"low",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 2
                                },
                                {
                                    "id":"godj9rom5",
                                    "text":"medium",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 5
                                },
                                {
                                    "id":"E6phkGY5u",
                                    "text":"high",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 8
                                }
                            ]
                        },
                    },
                    {
                        "ID": "834hf",
                        "DataType": enums.DataType.CandidateSkills.name,
                        "Type": enums.BlockType.UserInput.value,
                        "StoreInDB": True,
                        "Skippable": True,
                        "SkipText": "Skip!",
                        "SkipAction": enums.BlockAction.EndChat.value,
                        "SkipBlockToGoID": None,
                        "Content": {
                            "action": "Go To Next Block",
                            "text": "What's are your skills?",
                            "blockToGoID": "by_GnLY-f",
                            "afterMessage": "Your input is being processed...",
                            "keywords": ['python', 'sql', 'java']
                        }
                    },
                    # {
                    #     "ID":"by_GnLY-f",
                    #     "Type": enums.BlockType.Solutions.value,
                    #     "StoreInDB":False,
                    #     "Skippable":True,
                    #     "SkipText": "Skip!",
                    #     "SkipAction": enums.BlockAction.EndChat.value,
                    #     "SkipBlockToGoID": None,
                    #     "DataType":enums.DataType.NoType.name,
                    #     "Content": {
                    #         "showTop": 3,
                    #         "action": "End Chat",
                    #         "blockToGoID": None,
                    #         "afterMessage": "We will contact you with this candidate",
                    #         "databaseType": enums.DatabaseType.Candidates.value['enumName']
                    #     },
                    # },
                    # {
                    #     "ID": "gje6D",
                    #     "DataType": enums.DataType.CandidateEmail.name,
                    #     "Type": "User Input",
                    #     "StoreInDB": True,
                    #     "Skippable": False,
                    #     "Content": {
                    #         "action": "End Chat",
                    #         "text": "What's your email",
                    #         "blockToGoID": None,
                    #         "afterMessage": "Your email is in good hands :) Bye!"
                    #     }
                    # },
                    # {
                    #     "ID": "hkwt845",
                    #     "DataType": enums.DataType.CandidateSkills.name,
                    #     "Type": "File Upload",
                    #     "StoreInDB": True,
                    #     "Skippable": True,
                    #     "Content": {
                    #         "action": "Go To Next Block",
                    #         "text": "Upload CV1",
                    #         "blockToGoID": "gjdfl34",
                    #         "afterMessage": "File processed!",
                    #         "fileTypes": ["docx", "txt", "png", "xml", "doc", "pdf", "jpg"]
                    #     }
                    # },
                    # {
                    #     "ID": "gjdfl34",
                    #     "DataType": enums.DataType.CandidateSkills.value,
                    #     "Type": "File Upload",
                    #     "StoreInDB": True,
                    #     "Skippable": True,
                    #     "Content": {
                    #         "action": "End Chat",
                    #         "text": "Upload CV2",
                    #         "blockToGoID": None,
                    #         "afterMessage": "File processed!",
                    #         "fileTypes": ["docx", "txt", "png", "xml", "doc", "pdf", "jpg"]
                    #     }
                    # },
                ]
            }
        ]
    }
    flow_services.updateFlow(flow, reader_a)

    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco, LastNotificationDate=datetime.now(), NotifyEvery=5)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic, LastNotificationDate=datetime.now())
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic, LastNotificationDate=datetime.now())


    # Create Roles
    db.session.add(Role(Name="Owner", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= aramco, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    db.session.add(Role(Name="Owner", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= sabic, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))


    # Get Roles
    owner_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Owner").first()
    admin_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Admin").first()
    user_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "User").first()

    owner_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Owner").first()
    admin_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Admin").first()
    user_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "User").first()

    # Create Users
    user_services.create(firstname='Sylvester', surname='Stallone', email='aa@aa.com', password='123', phone='4344423',
                         company=aramco, role=owner_aramco, verified=True)
    user_services.create(firstname='Evg', surname='Test', email='evgeniy67@abv.bg', password='123', phone='4344423',
                         company=aramco, role=admin_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', phone='4344423', company=aramco,
                         role=admin_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', phone='4344423', company=aramco,
                         role=user_aramco, verified=True)

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='4344423', company=sabic,
                         role=owner_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', phone='4344423', company=sabic,
                         role=admin_sabic, verified=True)
    user_services.create(firstname='Faisal', surname='Julaidan', email='julaidan.faisal@gmail.com', password='123', phone='4344423', company=sabic,
                         role=user_sabic, verified=False)


    # Chatbot Sessions
    data = {
        "collectedData": [
            {
                "blockID": 1,
                "questionText": "What is your email?",
                "dataType": 'Email',
                "input": "faisal@gmail.com",
                "keywords": ['faisal', 'developer', 'email']
            },
            {
                "blockID": 2,
                "questionText": "How are you doing?",
                "dataType": 'No Type',
                "input": "I am fine thank you",
                "keywords": []
            },
            {
                "blockID": 3,
                "questionText": "When are you available?",
                "dataType": 'Availability',
                "input": "Only weekend days",
                "keywords": []
            },
            {
                "blockID": 4,
                "questionText": "What is your friend's email?",
                "dataType": "Email",
                "input": "friend@hotmail.com",
                "keywords": []
            }
        ],
        "selectedSolutions": None,
        "keywordsByDataType": {"Email": ["faisal@gmail.com", "friend@hotmail.com"],
                               "Availability": ["Only weekend days"],
                               "No Type": ["I am fine thank you"]}
    }
    conversation1 = Conversation(Data=data, DateTime=datetime.now(),
                      TimeSpent=55, SolutionsReturned=2, QuestionsAnswered=3,
                      UserType=enums.UserType.Candidate, Score= 1,
                      ApplicationStatus=enums.ApplicationStatus.Accepted, Assistant=reader_a)
    db.session.add(conversation1)
    db.session.add(Conversation(Data=data, DateTime=datetime.now(),
                                TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                UserType=enums.UserType.Client, Score= 0.05, Completed=False,
                                ApplicationStatus=enums.ApplicationStatus.Rejected, Assistant=reader_a))

    # add chatbot session in bulk
    for i in range(50):
        db.session.add(Conversation(Data=data, DateTime=datetime.now() - timedelta(days=i),
                                    TimeSpent=i+40, SolutionsReturned=i+3, QuestionsAnswered=i+4,
                                    UserType=enums.UserType.Candidate, Score= 0.45, Assistant=reader_a))


    db1: Database = Database(Name='db1', Type=enums.DatabaseType.Candidates, Company=aramco)
    db2: Database = Database(Name='db2', Type=enums.DatabaseType.Candidates, Company=aramco)

    db.session.add(db1)
    db.session.add(db2)

    db.session.add(addCandidate(db1, 'Faisal', 2000, "Software Engineer", "python, java, javascript, SQL",
                                5, "London"))

    db.session.add(addCandidate(db1, 'Mohammed', 4000, "Software Engineer", "python, SQL",
                                10, "Cardiff"))

    db.session.add(addCandidate(db2, 'Ahmed', 1500, "Web Developer", "html,css, javascript",
                                2, "Cardiff"))

    for i in list(range(120)):
        db.session.add(addCandidate(db1, 'Ahmed', 1500, "Web Developer", "html,css, javascript",
                                    2, "Cardiff"))

    # Add CRM conncetion for aramco company
    db.session.add(CRM(Type=enums.CRM.Adapt, Company=aramco, Auth={
        "domain": "PartnerDomain9",
        "username": "SD9USR8",
        "password": "P@55word",
        "profile": "CoreProfile",
        "locale": "en_GB",
        "timezone": "GMT",
        "dateFormat": 0,
        "timeFormat": 0}))

    # Create an AutoPilot for a Company
    auto_pilot_services.create('First Pilot',
                               "First pilot to automate the acceptance and rejection of candidates application",
                               aramco.ID)
    auto_pilot_services.create('Second Pilot', '', aramco.ID)
    reader_a.AutoPilot = auto_pilot_services.getByID(1,1).Data

    # Add Appointment
    a = Appointment(DateTime=datetime.now() + timedelta(days=5),
                    Conversation=conversation1, Assistant=reader_a)

    db.session.add(a)


    seed() # will save changes as well



def addCandidate(db, name, desiredSalary, jobTitle, skills, exp, location):
    return Candidate(Database=db,
                     CandidateName=name,
                     CandidateDesiredSalary=desiredSalary,
                     CandidateJobTitle=jobTitle,
                     CandidateSkills =skills,
                     CandidateYearsExperience = exp,
                     CandidateLocation = location,
                     Currency= Currency('USD'))



def seed():

    # Plans
    db.session.add(Plan(ID='plan_D3lp2yVtTotk2f', Nickname='basic', MaxSolutions=600, MaxBlocks=100, ActiveBotsCap=2,
                        InactiveBotsCap=3,
                        AdditionalUsersCap=5, ExtendedLogic=False, ImportDatabase=False, CompanyNameOnChatbot=False))

    db.session.add(
        Plan(ID='plan_D3lpeLZ3EV8IfA', Nickname='ultimate', MaxSolutions=5000, MaxBlocks=100, ActiveBotsCap=4,
             InactiveBotsCap=8,
             AdditionalUsersCap=10, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(
        Plan(ID='plan_D3lp9R7ombKmSO', Nickname='advanced', MaxSolutions=30000, MaxBlocks=100, ActiveBotsCap=10,
             InactiveBotsCap=30,
             AdditionalUsersCap=999, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(Plan(ID='plan_D48N4wxwAWEMOH', Nickname='debug', MaxSolutions=100, MaxBlocks=100, ActiveBotsCap=2,
                        InactiveBotsCap=2,
                        AdditionalUsersCap=3, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.commit()


def getPlanNickname(SubID=None):
    try:
        # Get subscription object from Stripe API
        subscription = stripe.Subscription.retrieve(SubID)

        # Debug
        # print(subscription)

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return subscription["items"]["data"][0]["plan"]["nickname"]

    except stripe.error.StripeError as e:
        return None


def isValidEmail(email: str) -> bool:
    # Validate the email address using a regex.
    if not re.match("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return False
    return True


# -------- SQLAlchemy Converters -------- #
"""Convert a SQLAlchemy object to a single dict """
def getDictFromSQLAlchemyObj(obj, excludedColumns: list = None) -> dict:

    dict = {} # Results
    if not obj: return dict

    # A nested for loop for joining two tables
    for attr in obj.__table__.columns:
        key = attr.name
        if key not in ['Password']:
            dict[key] = getattr(obj, key)
            if isinstance(dict[key], Enum): # Convert Enums
                dict[key] = dict[key].value

            if isinstance(dict[key], time): # Convert Times
                dict[key] = str(dict[key])

            if isinstance(dict[key], Currency): # Convert Currencies
                dict[key] = dict[key].code

            if key in [Job.JobStartDate.name, Job.JobEndDate.name] and dict[key]: # Convert Datetime only for Jobs
                dict[key] = '/'.join(map(str, [dict[key].year, dict[key].month, dict[key].day]))

            if key == Assistant.Flow.name and dict[key]: # Parse Flow !!
                flow_services.parseFlow(dict[key]) # pass by reference

    if hasattr(obj, "FilePath"):
        dict["FilePath"] = obj.FilePath
    return dict


"""Used when you want to only gather specific data from a table (columns)"""
"""Provide a list of keys (e.g ['id', 'name']) and the list of tuples"""
"""provided by sqlalchemy when querying for specific columns"""
"""this func will work for enums as well."""
def getDictFromLimitedQuery(columnsList, tupleList: List[tuple]):

    if not isinstance(tupleList, list):
        raise Exception("Provided list of tuples is empty. (Check data being returned from db)")

    # If the database returned an empty list, it's ok
    if not len(tupleList) > 0:
        return []

    # When tupleList is not empty, then the number of items in each tuple must match the number of items in columnsList
    if len(columnsList) != len(tupleList[0]) :
        raise Exception("List of indexes provided must match in length to the items in each of the tuples")

    d = []
    for item in tupleList:
        dict = {}
        for idx, i in enumerate(item):
            if isinstance(i, Enum):
                dict[columnsList[idx]] = i.value
            else:
                dict[columnsList[idx]] = i
        d.append(dict)
    return d



"""Convert a SQLAlchemy list of objects to a list of dicts"""
def getListFromSQLAlchemyList(SQLAlchemyList):
    return list(map(getDictFromSQLAlchemyObj, SQLAlchemyList))

# ---------------- #

def isStringsLengthGreaterThanZero(*args) -> bool:
    for arg in args:
        if len(arg.strip()) == 0:
            return False
    return True


def jsonResponse(success: bool, http_code: int, msg: str, data=None):
    return json.dumps({'success': success, 'code': http_code, 'msg': msg, 'data': data}), \
        http_code, {'ContentType': 'application/json'}


def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                'Content-Encoding' in response.headers):
                return response
            gzip_buffer = BytesIO()
            gzip_file = gzip.GzipFile(mode='wb',
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


# Check if the logged in user owns the accessed assistant for security
def validAssistant(func):
    def wrapper(assistantID):
        user = get_jwt_identity()['user']
        callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
        if not callback.Success:
            return jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data
        return func(assistant)
    wrapper.__name__ = func.__name__
    return wrapper

def findIndexOfKeyInArray(key, value, array):
    for item, idx in array:
        if item.key == value:
            return idx
    return False

#Helpful printer, so you can find out where a print if you forget about it and want to remove it
def HPrint(message):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    filenamearr = info.filename.split('\\')
    filename = filenamearr[len(filenamearr)-1]

    print(message + " - (%s, line %s)" % (filename, info.lineno))

# def csrf():
