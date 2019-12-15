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

from routes.admin.marketplace.marketplace import marketplace_router
marketplace_router: Blueprint = marketplace_router

from .account.users import users_router
users_router: Blueprint = users_router

from .campaign.campaign import campaign_router
campaign_router: Blueprint = campaign_router

from .database.database import database_router
database_router: Blueprint = database_router

from .account.options import options_router
options_router: Blueprint = options_router

from .auto_pilot.auto_pilot import auto_pilot_router
auto_Pilot_router: Blueprint = auto_pilot_router

from .auto_pilot.crm_auto_pilot import crm_auto_pilot_router
crm_auto_pilot_router: Blueprint = crm_auto_pilot_router

from .appointment.appointment import appointment_router
appointment_router: Blueprint = appointment_router

from .webhook.webhook import webhook_router
webhook_router: Blueprint = webhook_router
