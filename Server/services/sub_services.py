from utilities import helpers
from models import Callback, db, Company
from services import company_services
import os
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

        
def handleStripeWebhook(req) -> Callback:
    # Plan structure
    #  Assitants | Campaign | AutoPilot | DB | Appointments
    #  1.0.0.0.0 - means only access to assistants 
    
    plans = {"plan_D3lp2yVtTotk2f": "1.0.0.1.0", "plan_D3lp9R7ombKmSO": "1.1.0.1.1", "plan_D3lpeLZ3EV8IfA": "1.1.1.1.1"} if os.environ['STRIPE_IS_TESTING'] == 'yes' \
      else {"plan_G7Sth78cbr8Pgl": "1.0.0.1.0", "plan_G7SuTtSoBxJ7aS": "1.1.0.1.1", "plan_G7SuT5aJA1OFJU": "1.1.1.1.1"}# testing env

    try:
        event = stripe.Event.construct_from(req, stripe.api_key)
        if event.type == 'checkout.session.completed':
            customer: Callback = company_services.getByStripeID(event['data']['object']['customer']) 
            plan = plans[event['data']['object']['display_items'][0]['plan']['id']].split(".")

            if not customer.Success:
                raise Exception("No customer found with given ID")

            customer.Data.AccessAssistants = int(plan[0])
            customer.Data.AccessCampaigns = int(plan[1])
            customer.Data.AccessAutoPilot = int(plan[2])
            customer.Data.AccessDatabases = int(plan[3])
            customer.Data.AccessAppointments = int(plan[4])

            db.session.commit()

            return Callback(True, 'No Message')
            # if customer doesnt exist
        elif event.type == 'customer.subscription.deleted': 
            customer: Callback = company_services.getByStripeID(event['data']['object']['customer']) 

            if not customer.Success:
                raise Exception("No customer found with given ID")

            customer.Data.AccessAssistants = 0
            customer.Data.AccessCampaigns = 0
            customer.Data.AccessAutoPilot = 0
            customer.Data.AccessDatabases = 0
            customer.Data.AccessAppointments = 0

            db.session.commit()
            # Until we figure out a wa

            return Callback(True, 'No Message') #tell stripe webhook was handled succesfully
        elif event.type == 'customer.subscription.created':
            return Callback(True, 'No Message') #tell stripe webhook was handled succesfully
            

    except Exception as e:
        helpers.logError("sub_services.handleStripeWebhook(): " + str(e))
        return Callback(False, 'No Message')

def generateCheckoutURL(req) -> Callback:
    try:
        resp: dict = helpers.validateRequest(req, {"plan": {"type": str, "required": True}, "companyID": {"type": int, "required": False}})
        company: Callback = company_services.getByCompanyID(resp['inputs']['companyID'])

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            subscription_data={
                'items': [{
                  'plan': resp['inputs']['plan'],
                }],
            },
            customer=company.Data.StripeID,
            success_url='https://www.thesearchbase.com/success-payment?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://www.thesearchbase.com/order-plan',
        )
        print(session['id'])

        return Callback(True, 'Checkout URL Succesfully created', session['id'])    
    except helpers.requestException as e:
        helpers.logError("sub_services.generateCheckoutURL(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("sub_services.generateCheckoutURL(): " + str(e))
        return Callback(False, "Failed to generate checkout URL", None)


#
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