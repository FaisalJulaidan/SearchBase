from flask import Blueprint

from .account.account import account_router
profile_router: Blueprint = account_router

from .account.users import users_router
users_router: Blueprint = users_router

from .subscription.sub import sub_router
sub_router: Blueprint = sub_router

from .assistant.assistant import assistant_router
assistant_router: Blueprint = assistant_router

from .assistant.analytics import analytics_router
analytics_router: Blueprint = analytics_router

from .assistant.conversation import conversation_router
conversation_router: Blueprint = conversation_router

from .assistant.flow import flow_router
flow_router: Blueprint = flow_router

from routes.admin.crm.crm import crm_router
crm_router: Blueprint = crm_router

from .account.users import users_router
users_router: Blueprint = users_router

from .database.database import database_router
database_router: Blueprint = database_router

from .account.options import options_router
options_router: Blueprint = options_router

from .auto_pilot.auto_pilot import auto_pilot_router
auto_Pilot_router: Blueprint = auto_pilot_router

from .appointment.appointment import appointment_router
appointment_router: Blueprint = appointment_router
