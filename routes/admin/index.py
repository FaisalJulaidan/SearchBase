from flask import Blueprint

from .homepage.homepage import homepage_router
homepage_router: Blueprint = homepage_router

from .profile.profile import profile_router
profile_router: Blueprint = profile_router



from .admin_api import admin_api
admin_api: Blueprint = admin_api
