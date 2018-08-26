from flask import Blueprint

from .public import public_router
public_router: Blueprint = public_router

from .public import resetPassword_router
resetPassword_router: Blueprint = resetPassword_router
