from flask import Blueprint

from .account.profile import profile_router
profile_router: Blueprint = profile_router

from .account.users import users_router
users_router: Blueprint = users_router

from .account.changePassword import changePassword_router
changePassword_router: Blueprint = changePassword_router

from .assistant.settings import settings_router
settings_router: Blueprint = settings_router

from .assistant.solutions import solutions_router
solutions_router: Blueprint = solutions_router

from .subscription.sub import sub_router
sub_router: Blueprint = sub_router

from .assistant.assistant import assistant_router
assistant_router: Blueprint = assistant_router

from .assistant.analytics import analytics_router
analytics_router: Blueprint = analytics_router

from .assistant.connection import connection_router
connection_router: Blueprint = connection_router

from .assistant.chatbotSession import chatbotSession_router
chatbotSession_router: Blueprint = chatbotSession_router

from .assistant.flow import flow_router
flow_router: Blueprint = flow_router

from .account.users import users_router
users_router: Blueprint = users_router

from .account.profile import profile_router
profile_router: Blueprint = profile_router

from .assistant.bot import bot_router
bot_router: Blueprint = bot_router
