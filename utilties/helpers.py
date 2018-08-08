from bcrypt import hashpw, gensalt
from flask import request,redirect,url_for

def hash_password(password, salt=gensalt()):
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
