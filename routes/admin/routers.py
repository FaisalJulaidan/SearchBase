from flask import Blueprint

from .adminBasic.adminBasic import adminBasic_router
adminBasic_router: Blueprint = adminBasic_router

from .dashboard.dashboard import dashboard_router
dashboard_router: Blueprint = dashboard_router

from .account.profile import profile_router
profile_router: Blueprint = profile_router

from .account.users import users_router
users_router: Blueprint = users_router

from .account.changePassword import changePassword_router
changePassword_router: Blueprint = changePassword_router

from .admin_api import admin_api
admin_api: Blueprint = admin_api

from .assistant.settings import settings_router
settings_router: Blueprint = settings_router

from .assistant.products import products_router
products_router: Blueprint = products_router

from .subscription.sub import sub_router
sub_router: Blueprint = sub_router



from .assistant.analytics import analytics_router
analytics_router: Blueprint = analytics_router

from .assistant.connection import connection_router
connection_router: Blueprint = connection_router

from .assistant.userInput import userInput_router
userInput_router: Blueprint = userInput_router

from .account.users import users_router
users_router: Blueprint = users_router

from .account.profile import profile_router
profile_router: Blueprint = profile_router

from .assistant.answers import answers_router
answers_router: Blueprint = answers_router

from .assistant.bot import bot_router
bot_router: Blueprint = bot_router

from .tools.emojiConverter import emoji_router
emoji_router: Blueprint = emoji_router