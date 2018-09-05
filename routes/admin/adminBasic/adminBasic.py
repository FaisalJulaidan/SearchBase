from services import admin_services
from flask import Blueprint, request

adminBasic_router: Blueprint = Blueprint('adminBasic_router', __name__ ,template_folder="../../templates")

#Support pages
@adminBasic_router.route("/admin/support/general", methods=['GET'])
def admin_general_support():
    if request.method == "GET":
        return admin_services.render("admin/support/general.html")


@adminBasic_router.route("/admin/support/docs", methods=['GET'])
def admin_support_docs():
    if request.method == "GET":
        return admin_services.render("admin/support/docs.html")


@adminBasic_router.route("/admin/support/setup", methods=['GET'])
def admin_support_setup():
    if request.method == "GET":
        return admin_services.render("admin/support/getting-setup.html")


@adminBasic_router.route("/admin/support/integration", methods=['GET'])
def admin_support_integration():
    if request.method == "GET":
        return admin_services.render("admin/support/integration.html")


@adminBasic_router.route("/admin/support/billing", methods=['GET'])
def admin_support_billing():
    if request.method == "GET":
        return admin_services.render("admin/support/billing.html")

#Billing
@adminBasic_router.route("/admin/adjustments", methods=['GET'])
def admin_pricing_adjust():
    return admin_services.render("admin/pricing-adjustments.html")