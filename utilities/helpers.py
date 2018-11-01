from flask import redirect, url_for, session, render_template, json
from models import db, Role, Company, Assistant, Plan, Block, BlockType, Solution, ChatbotSession
from services import assistant_services, user_services
from datetime import datetime
from sqlalchemy import inspect
from hashids import Hashids
from config import BaseConfig
import stripe
import re

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

    # Create Assistatns for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)
    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)

    ## Create Blocks
    #db.session.add(Block(Type=BlockType.Question, Order=1, StoreInDB=True, Assistant=reader_a, Content={
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
    db.session.add(Block(Type=BlockType.UserInput, Order=2, StoreInDB=True, Assistant=reader_a, Content={
        "action": "Go To Next Block",
        "text": "What's your email?",
        "blockToGoID": None,
        "storeInDB": True,
        "validation": "Email",
        "afterMessage": 'Your input is being processed...'
    }))

    #db.session.add(Block(Type=BlockType.FileUpload, Order=3, StoreInDB=True, Assistant=reader_a, Content={
    #    "action": "Go To Next Block",
    #    "fileTypes": [
    #    "doc",
    #    "pdf"
    #    ],
    #    "text": "Upload your CV",
    #    "blockToGoID": None,
    #    "afterMessage": 'File is being uploaded...'
    #}))

    #db.session.add(Block(Type=BlockType.Solutions, Order=4, StoreInDB=True, Assistant=reader_a, Content={
    #    "showTop": 5,
    #    "afterMessage": 'DONE!!!!',
    #    "action": "End Chat",
    #    "blockToGoID": 0
    #}))

    db.session.add(Block(Type=BlockType.Solutions, Order=4, StoreInDB=True, Assistant=reader_a, Content={
        "showTop": 5,
        "afterMessage": 'DONE!!!!',
        "action": "End Chat",
        "blockToGoID": 0
    }))

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
    user_services.create(firstname='Ahmad', surname='Hadi', email='aa@aa.com', password='123', phone='4344423',
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

    # Plans
    db.session.add(Plan(ID='plan_D3lp2yVtTotk2f', Nickname='basic', MaxSolutions=600, MaxBlocks=20, ActiveBotsCap=2, InactiveBotsCap=3,
                        AdditionalUsersCap=5, ExtendedLogic=False, ImportDatabase=False, CompanyNameOnChatbot=False))

    db.session.add(
        Plan(ID='plan_D3lpeLZ3EV8IfA', Nickname='ultimate', MaxSolutions=5000, MaxBlocks=20, ActiveBotsCap=4, InactiveBotsCap=8,
             AdditionalUsersCap=10, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(
        Plan(ID='plan_D3lp9R7ombKmSO', Nickname='advanced', MaxSolutions=30000, MaxBlocks=20, ActiveBotsCap=10, InactiveBotsCap=30,
             AdditionalUsersCap=999, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    db.session.add(Plan(ID='plan_D48N4wxwAWEMOH', Nickname='debug', MaxSolutions=100, MaxBlocks=30,  ActiveBotsCap=2, InactiveBotsCap=2,
                        AdditionalUsersCap=3, ExtendedLogic=True, ImportDatabase=True, CompanyNameOnChatbot=True))

    # Save all changes
    db.session.commit()


def hardRedirectWithMessage(route, message):
    session["returnMessage"] = message
    return redirect(route)


def redirectWithMessage(route, message):
    session["returnMessage"] = message
    if "/" in route:
        return redirect(route)
    else:
        return redirect(url_for("." + route))


def redirectWithMessageAndAssistantID(route, assistantID, message):
    session["returnMessage"] = message
    return redirect(url_for("." + route, assistantID=assistantID))
    if "/" in route:
        return redirect(route)
    else:
        return redirect(url_for("." + route, assistantID=assistantID))

def checkForMessage():
    message = session.get('returnMessage', "")
    if message:
        session["returnMessage"] = ""
    return message


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
    return json.dumps({'success': success, 'code': http_code, 'msg': msg, 'data': data}),\
            http_code, {'ContentType': 'application/json'}
