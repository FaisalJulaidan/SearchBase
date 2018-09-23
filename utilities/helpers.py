from bcrypt import hashpw, gensalt
from flask import request, redirect, url_for, session, render_template, json
from sqlalchemy import inspect
import stripe
import re


def hashPass(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed



def redirectWithMessage(function, message):
    session["returnMessage"] = message
    return redirect(url_for("." + function))

def redirectWithMessageAndAssistantID(function, assistantID, message):
    session["returnMessage"] = message
    return redirect(url_for("." + function, assistantID=assistantID))

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