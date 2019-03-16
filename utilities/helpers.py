from flask import json, after_this_request, request
from models import db, Role, Company, Assistant, Plan, ChatbotSession, Database, Candidate
from services import user_services
from datetime import datetime, timedelta
from enum import Enum
from hashids import Hashids
from config import BaseConfig
import stripe
import re
from io import BytesIO
import gzip
import functools
import enums
from itsdangerous import URLSafeTimedSerializer
import logging

# Signer
verificationSigner = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)

# Configure logging system
logging.basicConfig(filename='errors.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# logging.error("Error example")

# ID Hasher
# IMPORTANT: don't you ever make changes to the hash values before consulting Faisal Julaidan
hashids = Hashids(salt=BaseConfig.HASH_IDS_SALT, min_length=5)
def encrypt_id(id):
    return hashids.encrypt(id)


def decrypt_id(id):
    return hashids.decrypt(id)



# Generates dummy data for testing
def gen_dummy_data():

    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com', StripeID='cus_00000000000000', SubID='sub_00000000000000'))
    db.session.add(Company(Name='Sabic', URL='ff.com', StripeID='cus_DbgKupMRLNYXly'))

    # Get Companies
    aramco = Company.query.filter(Company.Name == "Aramco").first()
    sabic = Company.query.filter(Company.Name == "Sabic").first()

    # Create Assistants for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there",
                         TopBarText="Aramco Bot", SecondsUntilPopup=1,
                         Active=True, Company=aramco,
                         Flow= {
                             "groups": [
                                 {
                                     "id": "tisd83f4",
                                     "name": "group 1",
                                     "description": "The best group",
                                     "blocks": [
                                         {
                                             "ID": "834hf",
                                             "DataType": enums.DataType.DesiredSalary.value,
                                             "Type": "User Input",
                                             "StoreInDB": True,
                                             "Skippable": False,
                                             "Content": {
                                                 "action": "Go To Next Block",
                                                 "text": "What's salary are you offering",
                                                 "blockToGoID": "by_GnLY-f",
                                                 "afterMessage": "Your input is being processed..."
                                             }
                                         },
                                         {
                                            "ID":"by_GnLY-f",
                                            "Type":"Solutions",
                                            "StoreInDB":False,
                                            "Skippable":False,
                                            "DataType":{
                                                "name":"No Type",
                                                "userTypes":[],
                                                "validation":"Ignore"
                                            },
                                             "Content":{
                                                 "showTop":3,
                                                 "action":"Go To Next Block",
                                                 "blockToGoID":"gje6D",
                                                 "afterMessage":"Here are you solutions",
                                                 "databaseType":"Candidates"
                                             },
                                         },
                                         {
                                             "ID": "gje6D",
                                             "DataType": enums.DataType.Email.value,
                                             "Type": "User Input",
                                             "StoreInDB": True,
                                             "Skippable": False,
                                             "Content": {
                                                 "action": "End Chat",
                                                 "text": "What's your email",
                                                 "blockToGoID": None,
                                                 "afterMessage": "Your email is in good hands :) Bye!"
                                             }
                                         },
                                     ]
                                 }
                             ]
                         })
    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)


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
        'selectedSolutions': None
    }

    db.session.add(ChatbotSession(Data=data, DateTime=datetime.now(),
                                  TimeSpent=55, SolutionsReturned=2, QuestionsAnswered=3,
                                  UserType=enums.UserType.JobSeeker, Assistant=reader_a))

    db.session.add(ChatbotSession(Data=data, DateTime=datetime.now() - timedelta(days=10),
                                  TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                  UserType=enums.UserType.CandidateSeeker, Assistant=reader_a))

    # add chatbot session in bulk
    for i in range(50):
        db.session.add(ChatbotSession(Data=data, DateTime=datetime.now() - timedelta(days=i),
                                      TimeSpent=i+40, SolutionsReturned=i+3, QuestionsAnswered=i+4,
                                      UserType=enums.UserType.JobSeeker, Assistant=reader_a))


    db1: Database = Database(Name='db1', Type=enums.DatabaseType.Candidates, Company=aramco)
    db2: Database = Database(Name='db2', Type=enums.DatabaseType.Candidates, Company=aramco)

    db.session.add(db1)
    db.session.add(db2)

    db.session.add(addCandidate(db1, 'Faisal', 2000, "Software Engineer", "python, java, javascript, SQL",
                                5, "London","contract", 30))

    db.session.add(addCandidate(db1, 'Mohammed', 4000, "Software Engineer", "python, SQL",
                                10, "Cardiff","Contract", 50))

    db.session.add(addCandidate(db2, 'Ahmed', 1500, "Web Developer", "html,css, javascript",
                                2, "Cardiff","Contract", 20))

    seed() # will save changes as well


def addCandidate(db, name, ds, dp, cs, ye, pl, pe, ehr):
    return Candidate(Database=db, Name=name,
                     DesiredSalary=ds,
                     DesiredPosition=dp,
                     CandidateSkills =cs,
                     YearsExp = ye,
                     PreferredLocation = pl,
                     PreferredEmploymentType = pe,
                     DesiredPayRate = ehr)




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


# Convert a SQLAlchemy object to a single dict
def getDictFromSQLAlchemyObj(obj):
    d = {}
    for attr in obj.__table__.columns:
        key = attr.name
        if not key == 'Password':
            d[key] = getattr(obj, key)
            if isinstance(d[attr.name], Enum):
                d[key] = d[key].value
            if key == 'Currency' and d[key]:
                d[key] = d[key].code
            if key == 'StartDate' and d[key]:
                d[key] = '/'.join(map(str, [d[key].year, d[key].month, d[key].day]))
    if hasattr(obj, "FilePath"):
        d["FilePath"] = obj.FilePath
    return d


# Convert a SQLAlchemy list of objects to a list of dicts
def getListFromSQLAlchemyList(SQLAlchemyList):
    return list(map(getDictFromSQLAlchemyObj, SQLAlchemyList))


def mergeRolesToUserLists(users: list, roles: list):
    for user in users:
        if 'Role' not in user:
            for role in roles:
                if user['RoleID'] == role['ID']:
                    user['Role']= role
                    break
                else:
                    user['Role']= None
    return users


def isStringsLengthGreaterThanZero(*args):
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
