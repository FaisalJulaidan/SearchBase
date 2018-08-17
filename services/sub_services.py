import stripe


from models import Callback, db, Role, Plan


def subscribe(email, planNickname, trialDays=None) -> Callback:

    plan: Plan = getPlanByNickname(planNickname)
    print(plan)
    if not plan:
        return Callback(False, 'Plan does not exist')

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

    return Callback(True, 'Subscribed successfully', {'stripeID': customer['id'], 'subID': sub['id']})


def getPlanByNickname(nickname) -> Plan or None:
    try:
        return Callback(True, 'No message.',
                        db.session.query(Plan).filter(Plan.Nickname == nickname).first())
    except Exception as e:
        return Callback(False, 'Could not find a plan with ' + nickname + ' nickname',
                        db.session.query(Plan).filter(Plan.Nickname == nickname).first())