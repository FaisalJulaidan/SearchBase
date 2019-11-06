import os
import stripe
from flask import Blueprint, request, session
from services import admin_services, sub_services, user_services, company_services
from utilities import helpers
from models import db, Callback, User, Company


sub_router: Blueprint = Blueprint('sub_router', __name__, template_folder="../../templates")

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY_TEST'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY_TEST']
} if os.environ['STRIPE_IS_TESTING'] == "yes" else {
  'secret_key': os.environ['STRIPE_SECRET_KEY_LIVE'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY_LIVE']
}

stripe.api_key = stripe_keys['secret_key']



@sub_router.route("/admin/pricing", methods=['GET'])
def admin_pricing():
    currentPlan = session.get('UserPlan')
    return admin_services.render("admin/pricing-tables.html", stripe_pubKey=stripe_keys['publishable_key'], currentPlan=currentPlan)


@sub_router.route("/admin/adjustments", methods=['GET'])
def admin_pricing_adjust():
    return admin_services.render("admin/pricing-adjustments.html")



# Stripe Webhooks
@sub_router.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhooks_subscription_cancelled():
    if request.method == "POST":
        try:
            event_json = request.get_json(force=True)
            customerID = event_json['data']['object']['customer']

            # Get the admin user who is logged in and wants to create a new user.
            callback: Callback = company_services.getByStripeID(customerID)
            if not callback.Success:
                return helpers.jsonResponse(False, 400, "Sorry, this customer doesn't exist in the system")
            company: Company = callback.Data

            company.SubID = None
            db.session.commit()

            # Deactivate assistants
            assistants = company.Assistants
            if len(assistants) > 0:
                for assistant in assistants:
                    assistant.Active = False

            return helpers.jsonResponse(True, 200, "Company with " + customerID + " has been unsubscribed successfully")

        except Exception as e:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred with Webhooks...")



