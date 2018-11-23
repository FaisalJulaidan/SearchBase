from flask import Blueprint

from .public import public_router
public_router: Blueprint = public_router

from .resetPassword import  resetPassword_router
resetPassword_router: Blueprint = resetPassword_router

from .chatbot import chatbot_router
chatbot_router: Blueprint = chatbot_router

from .auth import auth_router
auth_router: Blueprint = auth_router
