import re

from bcrypt import hashpw, gensalt
from flask import request,redirect,url_for

def hashPass(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


def checkForMessage():
    args = request.args
    msg=" "
    if len(args) > 0:
        msg = args['messages']
    return msg


def redirectWithMessageAndAssistantID(function, assistantID, message):
    return redirect(url_for("." + function, assistantID=assistantID, message=message))


def checkForMessageWhenAssistantID():
        try:
            message = request.args["message"]
        except:
            message = " "
        return message


def redirectWithMessage(function, message):
    return redirect(url_for("."+function, messages=message))


def checkForMessage():
    args = request.args
    msg=" "
    if len(args) > 0:
        msg = args['messages']
    return msg


def hash_password(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


def isValidEmail(email: str) -> bool:
    """Validate the email address using a regex."""
    if not re.match("[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", email):
        return False
    return True