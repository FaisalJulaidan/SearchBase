from flask import Blueprint

from .dashboard.dashboard import dashboard_router
dashboard_router: Blueprint = dashboard_router

from .profile.profile import profile_router
profile_router: Blueprint = profile_router

from .admin_api import admin_api
admin_api: Blueprint = admin_api

from .assistant.settings import settings_router
settings_router: Blueprint = settings_router
