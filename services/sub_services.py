import sqlalchemy.exc
import stripe


from models import Callback, db, Role, Plan


def subscribe(email, planNickname, trialDays=None) -> Callback:

    plan: Plan = getPlanByNickname(planNickname)
    if not Plan:
        Callback(False, 'Plan does not exist')

    try:
        # Create a Stripe customer for the new company.
        customer = stripe.Customer.create(
            email=email
        )

        # Subscribe to the Basic plan with a trial of 14 days
        sub = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': plan.ID}],
            trial_period_days=trialDays,
        )

        # debug
        # print(customer)
        # print(sub)

    except Exception as e:
        return Callback(False, 'An error occurred while subscribing with Stripe')

    return Callback(True, 'Subscribed successfully!')


def getPlanByNickname(nickname) -> Plan or None:
    return db.session.query(Plan).filter(Plan.Nickname).first()