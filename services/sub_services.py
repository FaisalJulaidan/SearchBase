from flask import jsonify
import stripe


from models import Callback, db, Role, Plan, User
from services import assistant_services, user_services


def unsubscribe(email) -> Callback:

    # Get the user by email
    callback: Callback = user_services.getByEmail(email)
    if not callback.Success:
        return jsonify(error='Could not find the logged in user to unsubscribe.')

    # Set the User from the callback
    user: User = callback.Data

    try:
        # If user has no sub. already
        if not user.SubID:
            Callback(False, 'This account has no active subscription to unsubscribe')

        # Unsubscribe
        stripeSub = stripe.Subscription.retrieve(user.SubID)
        stripeSub.delete()
        user.SubID = None

        # Save db changes
        db.session.commit()

        return Callback(True, 'You have unsubscribe successfully!')

    except Exception as e:
        return Callback(False, 'An error occurred while trying to unsubscribe')


def subscribe(email, planID, trialDays=None, token=None, coupon=None) -> Callback:

    # Get the Plan by ID
    plan_callback: Callback = getPlanByID(planID)
    if not plan_callback.Success:
        return Callback(False, 'Plan does not exist')

    # Validate Coupon
    if coupon and not isCouponValid(coupon):
        return Callback(False, 'Coupon is not valid!')

    # Get the user by email
    callback: Callback = user_services.getByEmail(email)
    if not callback.Success:
        print('Could not find the logged in user.')
        return Callback(False, 'Could not find the logged in user to subscribe.')

    # Set the User and Plan
    user: User = callback.Data
    plan: Plan = plan_callback.Data

    try:
        # Check user if already has a StripeID
        if user.StripeID:
            customer = {'id': user.StripeID}

        # If not, then create a new Stripe customer
        else:

            customer = stripe.Customer.create(
                email=email
            )

        # Subscribe to the  plan
        subscription = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': plan.ID}],
            trial_period_days=trialDays,
            token=token,
            coupon=coupon
        )

        # Get all company's assistants for activation
        assistants_callback = assistant_services.getAll(user.CompanyID)
        if not assistants_callback.Success:
            # unsubscribe before return the error
            unsubscribe(email)
            return Callback(False, "Issue while dealing with user's assistants.")

        # If everything is OK, activate company's assistants
        assistants = assistants_callback.Data
        if assistants != 0:
            for assistant in assistants:
                assistant.Active = True


        # Update user's StripeID & SubID
        user.StripeID = customer['id']
        user.SubID = subscription['id']

        # Save db changes
        db.session.commit()


    except Exception as e:
        return Callback(False, 'An error occurred while subscribing with Stripe')

    return Callback(True, 'Subscribed successfully', {'stripeID': customer['id'],
                                                      'subID': subscription['id'],
                                                      'planNickname': plan.Nickname})


def getPlanByID(planID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.ID == planID).first()
        if not result: raise Exception

        return Callback(True, 'Plan found.',
                        result)
    except Exception as e:
        return Callback(False, 'Could not find a plan with ID ' + planID)


def getPlanByNickname(nickname) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.Nickname == nickname).first()
        if not result: raise Exception

        return Callback(True, 'No message.',
                        result)
    except Exception as e:
        return Callback(False, 'Could not find a plan with ' + nickname + ' nickname')


def getStripePlan(planID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = stripe.Plan.retrieve(planID)
        if not result: raise Exception

        return Callback(True, 'No message.', result)
    except Exception as e:
        return Callback(False, "This plan doesn't exist! Make sure the plan ID is correct.")


def getStripePlanNicknameBySubID(SubID):
    try:
        # Get result and check if None then raise exception
        result = stripe.Subscription.retrieve(SubID)["items"]["data"][0]["plan"]["nickname"]
        if not result: raise Exception

        # Get subscription object from Stripe API

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return Callback(True, 'No message.', result)

    except Exception as e:
        return Callback(False, 'Could not find plan nickname form Stripe')


def isCouponValid(coupon):
    try:
        stripe.Coupon.retrieve(str(coupon))
        return True
    except stripe.error.StripeError as e:
        print("coupon is not valid")
        return False
