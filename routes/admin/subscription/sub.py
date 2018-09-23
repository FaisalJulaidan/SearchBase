
from flask import Blueprint, request, session
from services import admin_services, sub_services, user_services, company_services
from utilities import helpers
import stripe
from models import db, Callback, User, Company


sub_router: Blueprint = Blueprint('sub_router', __name__ ,template_folder="../../templates")

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'
encryption = None

stripe_keys = {
    'secret_key': secret_key,
    'publishable_key': pub_key
}

stripe.api_key = secret_key




@sub_router.route("/admin/pricing", methods=['GET'])
def admin_pricing():
    return admin_services.render("admin/pricing-tables.html", pub_key=pub_key)


@sub_router.route("/admin/subscribe/<planID>", methods=['GET', 'POST'])
def admin_pay(planID):
    if request.method == 'GET':

        stripePlan_callback: Callback = sub_services.getStripePlan(planID)
        if not stripePlan_callback.Success:
            helpers.redirectWithMessage('admin_pricing', 'This plan does not exist! Make sure the plan ID '
                                        + planID + ' is correct.')

        print(stripePlan_callback.Data)
        return admin_services.render("admin/sub.html", plan=stripePlan_callback.Data)

    if request.method == 'POST':

        if not session.get('Logged_in', False):
            helpers.redirectWithMessage("login", "You must login first!")


        # Get the user who is logged in.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred. Try again please!")
        user: User = callback.Data

        stripePlan_callback: Callback = sub_services.getStripePlan(planID)
        print(stripePlan_callback.Success)
        if not stripePlan_callback.Success:
            return helpers.jsonResponse(False, 404, "This plan doesn't exist!", None)


        # Get Stripe from passed data. That's include the generated token using JavaScript
        data = request.get_json(silent=True)
        token = data['token']['id']
        coupon = data['coupon']

        print(">>>>>>>>>>>")
        print(token)
        print(coupon)

        if token is "Error" or not token:
            return helpers.jsonResponse(False, 404, "No token provided to complete the payment!", None)

        sub_callback: Callback = sub_services.subscribe(user.Company,planID=planID, token=token, coupon=coupon)
        if not sub_callback.Success:
            return helpers.jsonResponse(False, 404, sub_callback.Message)

        # Set Plan session for logged in user
        session['UserPlan'] = sub_callback.Data['planNickname']
        print("You have successfully subscribed!")
        return helpers.jsonResponse(True, 200, "You have successfully subscribed!", {"url": "admin/pricing-tables.html"})


@sub_router.route("/admin/adjustments", methods=['GET'])
def admin_pricing_adjust():
    return admin_services.render("admin/pricing-adjustments.html")


@sub_router.route("/admin/unsubscribe", methods=['POST'])
def unsubscribe():
    if request.method == 'POST':

        if not session.get('Logged_in', False):
            helpers.redirectWithMessage("login", "You must login first!")

        # Get the user who is logged in.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred. Try again please!")
        user: User = callback.Data

        unsubscribe_callback: Callback = sub_services.unsubscribe(user.Company)

        if not unsubscribe_callback.Success:
            return helpers.jsonResponse(False, 400, unsubscribe_callback.Message)

        # Reaching to this point means unsubscribe successfully
        # Clear plan session
        session.pop('UserPlan')

        print(unsubscribe_callback.Message)
        return helpers.jsonResponse(True, 200, unsubscribe_callback.Message)


# Stripe Webhooks
@sub_router.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhooks_subscription_cancelled():
    if request.method == "POST":
        try:
            print("STRIPE TRIGGER FOR UNSUBSCRIPTION...")
            event_json = request.get_json(force=True)
            customerID = event_json['data']['object']['customer']

            print("Webhooks: Customer ID")
            print(customerID)

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

            print("Company with " + customerID + " has been unsubscribed successfully")
            return helpers.jsonResponse(True, 200, "Company with " + customerID + " has been unsubscribed successfully")

        except Exception as e:
            return helpers.jsonResponse(False, 400, "Sorry, error occurred with Webhooks...")



