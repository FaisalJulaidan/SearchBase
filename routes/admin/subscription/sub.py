
from flask import Blueprint, request, redirect, abort, render_template, session, jsonify
from flask_api import status
from services import admin_services, sub_services, user_services, assistant_services
from utilties import helpers
import stripe
from models import Callback, User


sub_router: Blueprint = Blueprint('sub_router', __name__ ,template_folder="../../templates")

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'
encryption = None

stripe.api_key = secret_key

stripe_keys = {
    'secret_key': secret_key,
    'publishable_key': pub_key
}


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

        # Get Stripe from passed data. That's include the generated token using JavaScript
        data = request.get_json(silent=True)
        token = data['token']['id']
        coupon = data['coupon']

        print(">>>>>>>>>>>")
        print(token)
        print(coupon)

        if token is "Error":
            return jsonify(error="No token provided to complete the payment!")

        sub_callback: Callback = sub_services.subscribe(email=session.get('userEmail', 'Invalid Email'),
                                                        planID=planID, token=token, coupon=coupon)

        if not sub_callback.Success:
            return jsonify(error=sub_callback.Message)

        # Reaching to this point means no errors and subscription is successful

        # session['UserPlan']['Nickname'] = getPlanNickname(subscription['id'])
        # if getPlanNickname(user['SubID']) is None:
        #     session['UserPlan']['Settings'] = NoPlan
        # elif "Basic" in getPlanNickname(user['SubID']):
        #     session['UserPlan']['Settings'] = BasicPlan
        # elif "Advanced" in getPlanNickname(user['SubID']):
        #     session['UserPlan']['Settings'] = AdvancedPlan
        # elif "Ultimate" in getPlanNickname(user['SubID']):
        #     session['UserPlan']['Settings'] = UltimatePlan
        # print("Plan changed to: ", session.get('UserPlan')['Settings'])

        # Set Plan session for logged in user
        session['userPlan'] = sub_callback.Data['planNickname']
        print("You have successfully subscribed!")

        return jsonify(success="You have successfully subscribed!", url="admin/pricing-tables.html")


@sub_router.route("/admin/unsubscribe", methods=['POST'])
def unsubscribe():
    if request.method == 'POST':

        if not session.get('Logged_in', False):
            helpers.redirectWithMessage("login", "You must login first!")

        unsubscribe_callback: Callback = sub_services.unsubscribe(session.get('userEmail', 'InvalidEmail'))

        if not unsubscribe_callback.Success:
            return jsonify(error=unsubscribe_callback.Message)

        # Reaching to this point means unsubscribe successfully
        # Clear plan session
        session.pop('UserPlan')

        print(unsubscribe_callback.Message)
        return jsonify(success=unsubscribe_callback.Message)


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

            # user = select_from_database_table("SELECT * FROM Users WHERE StripeID=?", [customerID])
            user = query_db("SELECT * FROM Users WHERE StripeID=?", [customerID], one=True)
            print(user)

            if user:

                update_table("UPDATE Users SET SubID=? WHERE StripeID=?;",
                             [None, customerID])

                # TODO check company for errors
                assistants = select_from_database_table("SELECT * FROM Assistants WHERE CompanyID=?", ['CompanyID'])

                # Check if user has assistants to deactivate first
                if len(assistants) > 0:
                    for assistant in assistants:
                        updateAssistant = update_table("UPDATE Assistants SET Active=? WHERE ID=?",
                                                       ["False", assistant[0]])
                        # TODO check update assistant for errors

                return "Assistants for " + user['Email'] \
                       + " account has been deactivated due to subscription cancellation"

            else:
                return "Webhooks Message: No User to unsubscribe"

        except Exception as e:
            abort(status.HTTP_400_BAD_REQUEST, "Webhook error")



