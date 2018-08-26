from flask import render_template,redirect, session
from services import auth_services, assistant_services, user_services
from models import Callback, User, Company
from utilties import helpers


def render(template, **context):
    if session.get('Logged_in', False):
        callback: Callback = user_services.getByID(session['UserID'])
        if callback.Success:
            # Get all assistants
            assistants: Callback = assistant_services.getAll(session['CompanyID']).Data

            # If there are assistants then convert them to a list of dict. Otherwise return empty list[].
            if assistants: assistants = helpers.getListFromSQLAlchemyList(assistants)
            else: assistants = []
            user: User = callback.Data
            return render_template(template,
                                   assistants=assistants,
                                   **context)
        else:
            return helpers.redirectWithMessage("login", "Could not find user. Please relog.")
    else:
        return helpers.redirectWithMessage("login", "Please log in first.")

def convertForJinja(toConvert, convertType):
    try:
        if type(toConvert) is convertType:
            result = [helpers.getDictFromSQLAlchemyObj(toConvert)]
        else:
            result = helpers.getListFromSQLAlchemyList(toConvert)
        return Callback(True, 'Data converted', result)
    except Exception as exc:
        print("convertForJinja() Error: ", exc)
        return Callback(False, 'Data could not be converted')