from flask import render_template,redirect, session
from services import auth_services, assistant_services, user_services
from models import Callback, User
from utilties import helpers


def render(template, **context):
    if session.get('Logged_in', False):
        callback: Callback = user_services.getByID(session['userID'])
        if callback.Success:
            # Get all assistants
            assistants: Callback = assistant_services.getAll(session['companyID']).Data

            # If there are assistants then convert them to a list of dict. Otherwise return empty list[].
            if assistants: assistants = helpers.getListFromSQLAlchemyList(assistants)
            else: assistants = []
            user: User = callback.Data
            return render_template(template,
                                   assistants=assistants,
                                   **context)
        else:
            raise ValueError('Can not render a template')
    else:
        raise ValueError('Can not render a template')
