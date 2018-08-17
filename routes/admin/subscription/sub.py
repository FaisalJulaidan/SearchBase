
from flask import Blueprint, request, redirect

sub_router: Blueprint = Blueprint('sub_router', __name__ ,template_folder="../../templates")


def is_coupon_valid(coupon="Error"):
    try:
        print(coupon)
        stripe.Coupon.retrieve(coupon)
        return True
    except stripe.error.StripeError as e:
        print("coupon is not valid")
        return False


def getPlanNickname(SubID=None):
    try:
        # Get subscription object from Stripe API
        subscription = stripe.Subscription.retrieve(SubID)

        # Debug
        print(subscription)

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return subscription["items"]["data"][0]["plan"]["nickname"]

    except stripe.error.StripeError as e:
        return None


@sub_router.route("/admin/check-out/<planID>", methods=['GET', 'POST'])
def admin_pay(planID):
    if request.method == 'GET':

        try:
            plan = stripe.Plan.retrieve(planID)
        except stripe.error.InvalidRequestError as e:
            abort(status.HTTP_400_BAD_REQUEST, "This plan doesn't exist! Make sure the plan ID is correct.")

        # print(plan)
        return render("admin/check-out.html", plan=plan)

    if request.method == 'POST':

        if not session.get('Logged_in', False):
            redirectWithMessage("login", "You must login first!")

        # Get Stripe from data. That's includ the generated token using JavaScript
        data = request.get_json(silent=True)
        # print(data)
        token = data['token']['id']
        coupon = data['coupon']

        if token is "Error":
            # TODO improve this
            return jsonify(error="No token provided to complete the payment!")

        # Get the plan opject from Stripe API
        try:
            plan = stripe.Plan.retrieve(planID)
        except stripe.error.StripeError as e:
            return jsonify(error="This plan does't exist! Make sure the plan ID is correct.")

        # Validate the given coupon.
        if coupon == "" or coupon is None or coupon == "Error":
            # If coupon is not provided set it to None as Stripe API require.
            coupon = None
            print("make no use of coupons")

        elif not (is_coupon_valid(coupon)):
            print("The coupon used is not valid")
            return jsonify(error="The coupon used is not valid")

        # If no errors occurred, subscribe the user to plan.

        # Get the user by email
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == session.get('User')['Email']:
                user = record
        if "Error" in user:
            return jsonify(error="An error occurred and could not subscribe.")

        try:
            subscription = stripe.Subscription.create(
                customer=user['StripeID'],
                source=token,
                coupon=coupon,
                items=[
                    {
                        "plan": planID,
                    },
                ]
            )

            # print(subscription)

            # if everything is ok activate assistants
            update_table("UPDATE Assistants SET Active=? WHERE CompanyID=?", ("True", user['CompanyID']))
            update_table("UPDATE Users SET SubID=? WHERE ID=?", (subscription['id'], user['ID']))

            # Resit the session
            session['UserPlan']['Nickname'] = getPlanNickname(subscription['id'])
            if getPlanNickname(user['SubID']) is None:
                session['UserPlan']['Settings'] = NoPlan
            elif "Basic" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = BasicPlan
            elif "Advanced" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = AdvancedPlan
            elif "Ultimate" in getPlanNickname(user['SubID']):
                session['UserPlan']['Settings'] = UltimatePlan
            print("Plan changed to: ", session.get('UserPlan')['Settings'])

        # TODO check subscription for errors https://stripe.com/docs/api#errors
        except Exception as e:
            print(e)
            return jsonify(error="An error occurred and could not subscribe.")

        # Reaching to point means no errors and subscription is successful
        print("You have successfully subscribed!")
        return jsonify(success="You have successfully subscribed!", url="admin/pricing-tables.html")


@sub_router.route("/admin/check-out/checkPromoCode", methods=['POST'])
def checkPromoCode():
    if request.method == 'POST':

        if not session.get('Logged_in', False):
            redirectWithMessage("login", "You must login first!")
        else:

            # TODO: check the promoCode from user then response with yes or no with json
            promoCode = str(request.data, 'utf-8')
            print(">>>>>>>>>>>>>>>>")
            print(promoCode)
            if promoCode == 'abc':
                return jsonify(isValid=True)
            else:
                return jsonify(isValid=False)


@sub_router.route("/admin/unsubscribe", methods=['POST'])
def unsubscribe():
    if request.method == 'POST':

        # if not session.get('Logged_in', False):
        #     redirectWithMessage("login", "You must login first!")

        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        print(session.get('User')['Email'])
        for record in users:
            if record["Email"] == session.get('User')['Email']:
                user = record
        if "Error" in user:
            return jsonify(error="This user does't exist. Please login again!")
        if user['SubID'] is None:
            print("This account has no active subscriptions ")
            return jsonify(error="This account has no active subscription")

        try:
            # Unsubscribe
            sub = stripe.Subscription.retrieve(user['SubID'])
            print(sub)
            sub.delete()

            # TODO why query_db does not work with update?
            # query_db('UPDATE Users SET SubID=? WHERE ID=?;', (None,  session.get('User')['ID']))
            update_table("UPDATE Users SET SubID=? WHERE ID=?;",
                         [None, session.get('User')['ID']])
            # Reset session
            session['UserPlan'] = NoPlan

            print("You have unsubscribed successfully!")
            return jsonify(msg="You have unsubscribed successfully!")

        except Exception as e:
            print("An error occurred while trying to unsubscribe")
            return jsonify(error="An error occurred while trying to unsubscribe")


# Stripe Webhooks
@sub_router.route("/api/stripe/subscription-cancelled", methods=["POST"])
def webhook_subscription_cancelled():
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



