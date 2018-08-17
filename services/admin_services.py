from flask import render_template,redirect, session
from services import auth_services, assistant_services, user_services
from models import Callback, User


def render(template, **context):
    if session.get('Logged_in', False):
        callback: Callback = user_services.getByID(session['userID'])
        if callback.Success:
            user: User = callback.Data
            return render_template(template,
                                   assistants=assistant_services.getAll(user.CompanyID),
                                   **context)
        else:
            raise ValueError('Can not render a template')
    else:
        raise ValueError('Can not render a template')
