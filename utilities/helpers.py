from flask import json, after_this_request, request
from models import db, Role, Company, Assistant, Plan, Block, ChatbotSession, BlockGroup
from services import user_services
from datetime import datetime, timedelta
from sqlalchemy import inspect
from hashids import Hashids
from config import BaseConfig
import stripe
import re
from io import BytesIO
import gzip
import functools
import enums


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
    reader_a = Assistant(Name="Reader", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)
    reader_a_blocksGroup = BlockGroup(Name="Group One", Description="This is Group one", Assistant=reader_a)
    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)

    ## Create Blocks
    #db.session.add(Block(Type=BlockType.Question, Order=1, StoreInDB=True, Skippable=False,
    # Group=reader_a_blocksGroup, Content={
    #    "answers": [
    #      {
    #        "action": "Go To Next Block",
    #        "text": "Yes",
    #        "timesClicked": 0,
    #        "keywords": [
    #          "smoker",
    #          "sad"
    #        ],
    #        "blockToGoId": 0,
    #        "afterMessage": 'Yesss!!'
    #      },
    #      {
    #        "action": "Go To Next Block",
    #        "text": "No",
    #        "timesClicked": 0,
    #        "keywords": [
    #          "smoker",
    #          "sad"
    #        ],
    #        "blockToGoId": 1,
    #        "afterMessage": 'NOOOO!!'

    #      }
    #    ],
    #    "text": "Do you smoke?",
    #  }))

    db.session.add(Block(Type=enums.BlockType.UserInput, Order=1, StoreInDB=True, Skippable=True,
                         Group=reader_a_blocksGroup, DataType=enums.DataType.Email, Content={
        "action": "Go To Next Block",
        "text": "What's your email?",
        "blockToGoID": None,
        "afterMessage": 'Your input is being processed...'
    }))

    db.session.add(Block(Type=enums.BlockType.UserInput, Order=2, StoreInDB=True, Skippable=False,
                         Group=reader_a_blocksGroup, DataType=enums.DataType.Name, Content={
        "action": "Go To Next Block",
        "text": "Give me some input",
        "blockToGoID": None,
        "afterMessage": 'Your input is being processed...'
    }))

    # db.session.add(Block(Type=enums.BlockType.FileUpload, Order=2, StoreInDB=True, Skippable=True,
    #                      DataType=enums.DataType.Resume, Group=reader_a_blocksGroup, Content={
    #    "action": "Go To Next Block",
    #    "fileTypes": [
    #    "doc",
    #    "pdf",
    #    "docx",
    #    ],
    #    "text": "Upload your CV",
    #    "blockToGoID": None,
    #    "afterMessage": 'File is being uploaded...'
    # }))

    # db.session.add(Block(Type=enums.BlockType.FileUpload, Order=2, StoreInDB=True,
    #                      DataType=enums.DataType.Resume, Group=reader_a_blocksGroup, Content={
    #         "action": "Go To Next Block",
    #         "fileTypes": [
    #             "doc",
    #             "pdf",
    #             "docx",
    #         ],
    #         "text": "Upload your CV 2",
    #         "blockToGoID": None,
    #         "afterMessage": 'File is being uploaded...'
    #     }))


    # db.session.add(Block(Type=enums.BlockType.Solutions, Order=4, StoreInDB=True, DataType=enums.DataType.NoType,
    #                      Group=reader_a_blocksGroup, Content={
    #     "showTop": 5,
    #     "afterMessage": 'DONE!!!!',
    #     "action": "End Chat",
    #     "blockToGoID": 0
    # }))

    # Create Roles
    db.session.add(Role(Name="Owner", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= aramco, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= aramco, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    db.session.add(Role(Name="Owner", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Admin", Company= sabic, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= sabic, EditChatbots=False, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    # does not work currently
    # db.session.add(Solution(Name="TestSolution", Content="",
    #                         RequiredFilters=None, DisplayTitles=None,
    #                         Type="RDB XML File Export", WebLink=None, IDReference=None, automaticSolutionAlerts=False, AssistantID=1))

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
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', phone='4344423', company=aramco,
                         role=admin_aramco, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', phone='4344423', company=aramco,
                         role=user_aramco, verified=True)

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='4344423', company=sabic,
                         role=owner_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', phone='4344423', company=sabic,
                         role=admin_sabic, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e6@e.com', password='123', phone='4344423', company=sabic,
                         role=user_sabic, verified=True)


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
        ]
    }

    db.session.add(ChatbotSession(Data=data, FilePath=None, DateTime=datetime.now(),
                                  TimeSpent=55, SolutionsReturned=2, QuestionsAnswered=3,
                                  UserType=enums.UserType.Candidate, Assistant=reader_a))

    db.session.add(ChatbotSession(Data=data, FilePath=None, DateTime=datetime.now() - timedelta(days=10),
                                  TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                  UserType=enums.UserType.Client,Assistant=reader_a))

    # add chatbot session in bulk
    for i in range(50):
        db.session.add(ChatbotSession(Data=data, FilePath=None, DateTime=datetime.now() - timedelta(days=i),
                                      TimeSpent=i+40, SolutionsReturned=i+3, QuestionsAnswered=i+4,
                                      UserType=enums.UserType.Candidate, Assistant=reader_a))


    # will save changes as well
    seed()

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
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs if c.key not in ("Password")}


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
    # print("success: ", success)
    # print("http_code: ", http_code)
    # print("msg: ", msg)
    # print("data: ", data)
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
