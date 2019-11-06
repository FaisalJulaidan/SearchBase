from utilities import helpers, enums
from models import Callback, db, Company
from services import company_services
import os
import stripe
        
def handleStripeWebhook(req) -> Callback:
    try:
        stripe_sig = req.headers.get("STRIPE_SIGNATURE")
        event = stripe.Event.construct_from(req.json, stripe_sig, stripe.api_key)
        if event.type == 'checkout.session.completed':
            customer: Callback = company_services.getByStripeID(event['data']['object']['customer']) 
            plan = event['data']['object']['display_items'][0]['plan']['id']
            planEnum: enums.Plan = enums.Plan.get_plan(plan)

            if not customer.Success:
                raise Exception("No customer found with given ID")
            
            if not planEnum:
                raise Exception("Trying to subscribe with invalid plan ID")

            customer.Data.Plan = planEnum.name
            customer.Data.Active = 1

            db.session.commit()

            return Callback(True, 'No Message')
            # if customer doesnt exist
        elif event.type == 'customer.subscription.deleted': 
            customer: Callback = company_services.getByStripeID(event['data']['object']['customer']) 

            if not customer.Success:
                raise Exception("No customer found with given ID")

            customer.Plan = None

            db.session.commit()
            # Until we figure out a wa

            return Callback(True, 'No Message') #tell stripe webhook was handled succesfully
        elif event.type == 'customer.subscription.created':
            return Callback(True, 'No Message') #tell stripe webhook was handled succesfully
            
    except stripe.error.SignatureVerificationError as e:
        return Callback(False, 'No Message')
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
            success_url='{}/success-payment?session_id={CHECKOUT_SESSION_ID}'.format(helpers.getDomain(3000)),
            cancel_url='{}/order-plan'.format(helpers.getDomain(3000)),
        )

        return Callback(True, 'Checkout URL Succesfully created', session['id'])    
    except helpers.requestException as e:
        helpers.logError("sub_services.generateCheckoutURL(): " + str(e))
        return Callback(False, str(e), None)
    except Exception as e:
        helpers.logError("sub_services.generateCheckoutURL(): " + str(e))
        return Callback(False, "Failed to generate checkout URL", None)

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