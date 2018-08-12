from bcrypt import hashpw, gensalt
from flask import request, redirect, url_for
import json


def hashPass(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed


def checkForMessage():
    args = request.args
    msg = " "
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
    return redirect(url_for("." + function, messages=message))


def checkForMessage():
    args = request.args
    msg = " "
    if len(args) > 0:
        msg = args['messages']
    return msg


def getPlanNickname(SubID=None):
    try:
        # Get subscription object from Stripe API
        subscription = stripe.Subscription.retrieve(SubID)

        # Debug
        print(subscription)

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return subscription["items"]["data"][0]["plan"]["nickname"]

    except stripe.error.StripeError as e:
        return None

# todo: add this to db
UserPlans = {
    "NoPlan": {
        "MaxProducts": 0,
        "ActiveBotsCap": 0,
        "InactiveBotsCap": 0,
        "AdditionalUsersCap": 0,
        "ExtendedLogic": False,
        "ImportDatabase": False,
        "CompanyNameonChatbot": False
    },
    "BasicPlan": {
        "MaxProducts": 600,
        "ActiveBotsCap": 2,
        "InactiveBotsCap": 3,
        "AdditionalUsersCap": 5,
        "ExtendedLogic": False,
        "ImportDatabase": False,
        "CompanyNameonChatbot": False
    },
    "AdvancedPlan": {
        "MaxProducts": 5000,
        "ActiveBotsCap": 4,
        "InactiveBotsCap": 8,
        "AdditionalUsersCap": 10,
        "ExtendedLogic": True,
        "ImportDatabase": True,
        "CompanyNameonChatbot": True
    },
    "UltimatePlan": {
        "MaxProducts": 30000,
        "ActiveBotsCap": 10,
        "InactiveBotsCap": 30,
        "AdditionalUsersCap": 999,
        "ExtendedLogic": True,
        "ImportDatabase": True,
        "CompanyNameonChatbot": True
    }
}


def toJSON(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    convert['DATETIME'] = ''
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        x = convert.keys()
        print(c.type)
        if str(c.type) == "DATETIME" and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    print(d)
    return json.dumps(d)


def isValidEmail(email: str) -> bool:
    """Validate the email address using a regex."""
    if not re.match("[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", email):
        return False
    return True