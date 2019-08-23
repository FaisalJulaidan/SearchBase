from flask_jwt_extended import get_jwt_identity
from models import Assistant, Callback, Company
from services import assistant_services, company_services
from utilities import helpers


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
    def wrapper():
        print('Access Assistants decorator executed')
        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data
        print('Access Assistants: ', company.AccessAssistants)
        if company.AccessAssistants:
            return func()
        else:
            return helpers.jsonResponse(False, 401, "Assistants not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows Assistant access (not used anywhere yet)
def AccessCampaignsRequired(func):
    def wrapper():
        print('Access Campaigns decorator executed')
        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data
        print('Access Campaigns: ', company.AccessCampaigns)
        if company.AccessAssistants:
            return func()
        else:
            return helpers.jsonResponse(False, 401, "Campaigns not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows appointment access
def AccessAppointmentsRequired(func):
    def wrapper():
        print('Access appointments decorator executed')
        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data
        print('Access Appointments: ', company.AccessAppointments)
        if company.AccessAppointments:
            return func()
        else:
            return helpers.jsonResponse(False, 401, "Appointments not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows autopilot access
def AccessAutoPilotRequired(func):
    def wrapper():
        print('Access autopilot decorator executed')
        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data
        print('Access Autopilot: ', company.AccessAutoPilot)
        if company.AccessAutoPilot:
            return func()
        else:
            return helpers.jsonResponse(False, 401, "Autopilot not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper


# Check if the plan allows database access
def AccessDatabasesRequired(func):
    def wrapper():
        print('Access database decorator executed')
        user = get_jwt_identity()['user']
        callback: Callback = company_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 404, "Not found.", None)

        company: Company = callback.Data
        print('Access Databases: ', company.AccessDatabases)
        if company.AccessDatabases:
            return func()
        else:
            return helpers.jsonResponse(False, 401, "Databases not included in plan", None)

    wrapper.__name__ = func.__name__
    return wrapper

