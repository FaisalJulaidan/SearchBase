from flask import Blueprint

from .dashboard.dashboard import dashboard_router
dashboard_router: Blueprint = dashboard_router

from .profile.profile import profile_router
profile_router: Blueprint = profile_router

from .admin_api import admin_api
admin_api: Blueprint = admin_api

from .assistant.settings import settings_router
settings_router: Blueprint = settings_router

from .assistant.products import products_router
products_router: Blueprint = products_router

from .subscription.sub import sub_router
sub_router: Blueprint = sub_router

from .assistant.questions import questions_router
questions_router: Blueprint = questions_router

from .assistant.analytics import analytics_router
analytics_router: Blueprint = analytics_router

from .assistant.connection import connection_router
connection_router: Blueprint = connection_router

from .assistant.userInput import userInput_router
userInput_router: Blueprint = userInput_router
