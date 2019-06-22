from utilities import helpers
from models import Callback, db, Plan, Company
import stripe


def unsubscribe(company: Company) -> Callback:

    try:
        # If user has no sub. already
        if not company.SubID:
            return Callback(False, 'This account has no active subscription to unsubscribe')

        # Unsubscribe
        stripeSub = stripe.Subscription.retrieve(company.SubID)
        stripeSub.delete()
        company.SubID = None

        # Save db changes
        db.session.commit()

        return Callback(True, 'You have unsubscribe successfully!')

    except Exception as exc:
        helpers.logError("sub_services.unsubscribe(): SubID " + company.SubID + " / " + str(exc))
        db.session.rollback()
        return Callback(False, 'An error occurred while trying to unsubscribe')


def subscribe(company: Company, planID, trialDays=None, token=None, coupon='') -> Callback:

    # Get the Plan by ID
    plan_callback: Callback = getPlanByID(planID)
    if not plan_callback.Success:
        return Callback(False, 'Plan does not exist')

    # Validate Coupon
    if len(coupon.strip()) == 0: coupon = None
    if coupon:
        coupon_callback: Callback = isCouponValid(coupon.strip())
        if not coupon_callback.Success:
            return coupon_callback

    # Set the Plan
    plan: Plan = plan_callback.Data

    try:
        # Check user if already has a StripeID
        stripeID = company.StripeID
        if not stripeID:
            return Callback(False, "Sorry, your company doesn't have a Stripe ID to subscribe to a plan")

        customer = stripe.Customer.retrieve(stripeID)
        if token:
            customer.source = token
            customer.save()

        # Subscribe to the  plan
        subscription = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': plan.ID}],
            trial_period_days=trialDays,
            coupon=coupon
        )

        # Get all company's assistants for activation

        # If everything is OK, activate company's assistants
        assistants = company.Assistants

        if assistants != 0:
            for assistant in assistants:
                assistant.Active = True

        # Update user's StripeID & SubID
        company.StripeID = customer['id']
        company.SubID = subscription['id']

        # Save db changes
        db.session.commit()

        return Callback(True, 'Subscribed successfully', {'stripeID': customer['id'],
                                                      'subID': subscription['id'],
                                                      'planNickname': plan.Nickname})

    except Exception as exc:
        helpers.logError("sub_services.subscribe(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'An error occurred while subscribing with Stripe')



def getPlanByID(planID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.ID == planID).first()
        if not result: raise Exception

        return Callback(True, 'Plan found.', result)
    except Exception as exc:
        helpers.logError("sub_services.getPlanByID(): " + str(exc))
        return Callback(False, 'Could not find a plan with ID ' + planID)


def getPlanByNickname(nickname) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.Nickname == nickname).first()
        if not result: raise Exception

        return Callback(True, 'No message.',
                        result)
    except Exception as exc:
        helpers.logError("sub_services.getPlanByNickname(): " + str(exc))
        return Callback(False, 'Could not find a plan with ' + nickname + ' nickname')


def getStripePlan(planID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = stripe.Plan.retrieve(planID)
        if not result: raise Exception

        return Callback(True, 'No message.', result)
    except Exception as exc:
        helpers.logError("sub_services.getPlanByNickname(): " + str(exc))
        return Callback(False, "This plan doesn't exist! Make sure the plan ID is correct.")


def getStripePlanNicknameBySubID(SubID):
    try:
        # Get result and check if None then raise exception
        result = stripe.Subscription.retrieve(SubID)["items"]["data"][0]["plan"]["nickname"]
        if not result: raise Exception

        # Get subscription object from Stripe API

        # Return the subscription item's plan nickname e.g (Basic, Ultimate...)
        return Callback(True, 'No message.', result)

    except Exception as exc:
        helpers.logError("sub_services.getStripePlanNicknameBySubID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not find plan nickname form Stripe')


def isCouponValid(coupon) -> Callback:
    try:
        coupon = stripe.Coupon.retrieve(str(coupon))
        if not coupon['valid']:
            return Callback(False, "Coupon has expired.")
        return Callback(True, "Coupon is valid")
    except Exception as exc:
        helpers.logError("sub_services.isCouponValid(): " + str(exc))
        db.session.rollback()
        return Callback(False, "coupon is not valid.")