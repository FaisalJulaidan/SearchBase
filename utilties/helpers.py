from bcrypt import hashpw, gensalt
from flask import request, redirect, url_for, session, render_template
from sqlalchemy import inspect
import stripe
import re

def hashPass(password, salt=gensalt()):
    hashed = hashpw(bytes(password, 'utf-8'), salt)
    return hashed

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


def render(template, **context):
    if session.get('Logged_in', False):
        return render_template(template, debug=0, assistants=session.get('UserAssistants', []), **context)
    return render_template(template, debug=0, **context)


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


def isValidEmail(email: str) -> bool:
    # Validate the email address using a regex.
    if not re.match("[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", email):
        return False
    return True

# Convert a SQLAlchemy object to a single dict
def getDictFromSQLAlchemy(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# Convert a SQLAlchemy list of objects to a list of dicts
def getListFromSQLAlchemy(SQLAlchemyResult):
    return list(map(getDictFromSQLAlchemy, SQLAlchemyResult))


