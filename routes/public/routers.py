from flask import Blueprint

from .public import public_router
public_router: Blueprint = public_router

from .reset_password import  reset_password_router
resetPassword_router: Blueprint = reset_password_router

from .chatbot import chatbot_router
chatbot_router: Blueprint = chatbot_router

from .auth import auth_router
auth_router: Blueprint = auth_router

from .appointment import appointment_router
appointment_router: Blueprint = appointment_router