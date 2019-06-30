import functools
import gzip
import inspect
import logging
import os
import re
import traceback
from datetime import time
from enum import Enum
from io import BytesIO
from typing import List

import geoip2.webservice
import stripe
from cryptography.fernet import Fernet
from flask import json, after_this_request, request
from flask_jwt_extended import get_jwt_identity
from forex_python.converter import CurrencyRates
from hashids import Hashids
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy_utils import Currency

from config import BaseConfig
from models import db, Assistant, Job, Callback, Role
from services import flow_services, assistant_services
from utilities.enums import Period

# ======== Global Variables ======== #

# GeoIP Client
geoIP = geoip2.webservice.Client(140914, os.environ['GEOIP_KEY'])

# Signer
verificationSigner = URLSafeTimedSerializer(os.environ['TEMP_SECRET_KEY'])

# Configure logging system
if os.environ['FLASK_ENV'] == 'development':
    logging.basicConfig(filename='Server/logs/errors.log',
                        level=logging.ERROR,
                        format='%(asctime)s -- %(message)s')
elif os.environ['FLASK_ENV'] in ['production', 'staging']:
    logging.basicConfig(filename='logs/errors.log',
                        level=logging.ERROR,
                        format='%(asctime)s -- %(message)s')

# Fernet for encryption
fernet = Fernet(os.environ['TEMP_SECRET_KEY'])

# Currency converter by forex-python
currencyConverter = CurrencyRates()


# ======== Helper Functions ======== #

# Get domain based on current environment
def getDomain():
    if os.environ['FLASK_ENV'] == 'development':
        return 'localhost:3000'
    elif os.environ['FLASK_ENV'] == 'staging':
        return 'http://staging.thesearchbase.com'
    elif os.environ['FLASK_ENV'] == 'production':
        return 'http://thesearchbase.com'
    return None


def logError(exception):
    if os.environ['FLASK_ENV'] == 'development':
        print(exception)
        # print(traceback.format_exc())
    logging.error(traceback.format_exc() + exception + "\n \n")


# ID Hasher
# IMPORTANT: don't you ever make changes to the hash values before consulting Faisal Julaidan
hashids = Hashids(salt=BaseConfig.HASH_IDS_SALT, min_length=5)
def encodeID(id):
    return hashids.encrypt(id)


def decodeID(id):
    return hashids.decrypt(id)


# Encryptors
def encrypt(value, isDict=False):
    if isDict: value = json.dumps(value)
    return fernet.encrypt(bytes((value.encode('utf-8'))))


def decrypt(token, isDict=False, isBtye=False):
    if not isBtye: token = bytes(token.encode('utf-8'))
    value = fernet.decrypt(token)
    if isDict: value = json.loads(value)
    return value


def seed():
    # Create universal Roles
    db.session.add(Role(Name="Staff", EditChatbots=True, AddUsers=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Owner", EditChatbots=True, AddUsers=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
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


# Note: Hourly is not supported because it varies and number of working hours is required
def convertSalaryPeriod(salary, fromPeriod: Period, toPeriod: Period):

    if fromPeriod == Period.Annually:
        if toPeriod == Period.Monthly:
            return salary / 12
        elif toPeriod == Period.Weekly:
            return salary / 52.1429
        else:
            return salary

    elif fromPeriod == Period.Monthly:
        if toPeriod == Period.Annually:
            return salary * 12
        elif toPeriod == Period.Weekly:
            return salary / 4
        else:
            return salary

    elif fromPeriod == Period.Weekly:
        if toPeriod == Period.Annually:
            return salary * 52.1429
        elif toPeriod == Period.Monthly:
            return salary * 4.33
        else:
            return salary

    else:
        raise Exception("helpers.convertSalaryPeriod(): Not supported Period")


# -------- SQLAlchemy Converters -------- #
"""Convert a SQLAlchemy object to a single dict """
def getDictFromSQLAlchemyObj(obj) -> dict:
    dict = {}  # Results
    if not obj: return dict

    # A nested for loop for joining two tables
    for attr in obj.__table__.columns:
        key = attr.name
        if key not in ['Password', 'Auth']:
            dict[key] = getattr(obj, key)
            if isinstance(dict[key], Enum):  # Convert Enums
                dict[key] = dict[key].value

            if isinstance(dict[key], time):  # Convert Times
                dict[key] = str(dict[key])

            if isinstance(dict[key], Currency):  # Convert Currencies
                dict[key] = dict[key].code

            if key in [Job.JobStartDate.name, Job.JobEndDate.name] and dict[key]:  # Convert Datetime only for Jobs
                dict[key] = '/'.join(map(str, [dict[key].year, dict[key].month, dict[key].day]))

            if key == Assistant.Flow.name and dict[key]:  # Parse Flow !!
                flow_services.parseFlow(dict[key])  # pass by reference

    if hasattr(obj, "FilePath"):
        dict["FilePath"] = obj.FilePath
    return dict

"""Convert a SQLAlchemy list of objects to a list of dicts"""
def getListFromSQLAlchemyList(SQLAlchemyList):
    return list(map(getDictFromSQLAlchemyObj, SQLAlchemyList))

"""Used when you want to only gather specific data from a table (columns)"""
"""Provide a list of keys (e.g ['id', 'name']) and the list of tuples"""
"""provided by sqlalchemy when querying for specific columns"""
"""this func will work for enums as well."""

# For a list of SQLAlchemy objects
def getListFromLimitedQuery(columnsList, tupleList: List[tuple]) -> list:
    if not isinstance(tupleList, list):
        raise Exception("Provided list of tuples is empty. (Check data being returned from db)")

    # If the database returned an empty list, it's ok
    if not len(tupleList) > 0:
        return []

    # When tupleList is not empty, then the number of items in each tuple must match the number of items in columnsList
    if len(columnsList) != len(tupleList[0]):
        raise Exception("List of indexes provided must match in length to the items in each of the tuples")

    d = []
    for tuple in tupleList:
        d.append(getDictFromLimitedQuery(columnsList, tuple))
    return d


# For a list of SQLAlchemy objects
def getDictFromLimitedQuery(columnsList, tuple) -> dict:

    # When tupleList is not empty, then the number of items in each tuple must match the number of items in columnsList
    if len(columnsList) != len(tuple):
        raise Exception("List of indexes provided must match in length to the items in each of the tuples")

    dict = {}
    for idx, v in enumerate(tuple):
        key = columnsList[idx]
        if isinstance(v, Enum): # Convert Enum
            dict[key] = v.value

        elif isinstance(v, time): # Convert Times
            dict[key] = str(v)

        elif isinstance(v, Currency): # Convert Currencies
            dict[key] = v.code

        elif key in [Job.JobStartDate.name, Job.JobEndDate.name] and v: # Convert Datetime only for Jobs
            dict[key] = '/'.join(map(str, [v.year, v.month, v.day]))

        elif key in ['Flow', 'AssistantFlow'] and v: # Parse Flow
            dict[key] = flow_services.parseFlow(v)

        else:
            dict[key] = v
    return dict


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


# example: objectListContains(myList, lambda x: x.n == 3)  # True if any element has .n==3
def objectListContains(list, filter):
    for x in list:
        if filter(x):
            return x
    return False


def getListValue(list, idx, default=None):
    try:
        return list[idx]
    except IndexError:
        return default


# Helpful printer, so you can find out where a print if you forget about it and want to remove it
def HPrint(message):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    filenamearr = info.filename.split('\\')
    filename = filenamearr[len(filenamearr) - 1]

    print(message + " - (%s, line %s)" % (filename, info.lineno))

# def csrf():
