import functools
import gzip
from io import BytesIO
from flask import after_this_request, request
from flask_jwt_extended import get_jwt_identity
from models import Assistant, Callback, Company
from services import assistant_services, company_services
from utilities import helpers


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
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)
        assistant: Assistant = callback.Data
        return func(assistant)

    wrapper.__name__ = func.__name__
    return wrapper


def validOwner(type, *args):
    def wrap(func):
        def wrapper():
            jwt = get_jwt_identity()['user']
            Owns = helpers.owns()
            valid = Owns.getOwner(type, jwt, *args)
            if valid != True:
                return valid
            return func()
        wrapper.__name__ = func.__name__
        return wrapper
    wrap.__name__ = type #needs to change
    return wrap


# Check if the plan allows Assistant access
def AccessAssistantsRequired(func):
    def wrapper(*args, **kwargs):

        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data

        if company.AccessAssistants:
            return func(*args, **kwargs)
        else:
            return helpers.jsonResponse(False, 401, "Assistants not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows Assistant access (not used anywhere yet)
def AccessCampaignsRequired(func):
    def wrapper(*args, **kwargs):

        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data

        if company.AccessCampaigns:
            return func(*args, **kwargs)
        else:
            return helpers.jsonResponse(False, 401, "Campaigns not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows appointment access
def AccessAppointmentsRequired(func):
    def wrapper(*args, **kwargs):

        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data

        if company.AccessAppointments:
            return func(*args, **kwargs)
        else:
            return helpers.jsonResponse(False, 401, "Appointments not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows autopilot access
def AccessAutoPilotRequired(func):
    def wrapper(*args, **kwargs):

        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data

        if company.AccessAutoPilot:
            return func(*args, **kwargs)
        else:
            return helpers.jsonResponse(False, 401, "Autopilot not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows database access
def AccessDatabasesRequired(func):
    def wrapper(*args, **kwargs):

        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data

        if company.AccessDatabases:
            return func(*args,**kwargs)
        else:
            return helpers.jsonResponse(False, 401, "Databases not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper
