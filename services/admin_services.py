from flask import render_template
from services import auth_services, assistant_services, user_services
from models import Callback, User


def render(template, **context):
    if auth_services.isLogged():
        callback: Callback = user_services.getUserFromSession()
        if callback.Success:
            user: User = callback.Data
            return render_template(template,
                                   assistants=assistant_services.getAll(user.CompanyID),
                                   **context)
        else:
            raise ValueError('Can not render a template')
    else:
        raise ValueError('Can not render a template')

