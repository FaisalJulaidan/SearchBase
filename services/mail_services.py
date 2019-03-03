from datetime import datetime
from threading import Thread

from flask import render_template, current_app
from flask_mail import Mail, Message

from models import Callback
from services import user_services, assistant_services, analytics_services
from utilities import helpers

mail = Mail()


def timer_tick():
    now = datetime.now()

    session1 = [now.replace(hour=0, minute=0, second=0, microsecond=0),
                now.replace(hour=3, minute=59, second=59, microsecond=999999)]
    session2 = [now.replace(hour=4, minute=0, second=0, microsecond=0),
                now.replace(hour=7, minute=59, second=59, microsecond=999999)]
    session3 = [now.replace(hour=8, minute=0, second=0, microsecond=0),
                now.replace(hour=11, minute=59, second=59, microsecond=999999)]
    session4 = [now.replace(hour=12, minute=0, second=0, microsecond=0),
                now.replace(hour=15, minute=59, second=59, microsecond=999999)]
    session5 = [now.replace(hour=16, minute=0, second=0, microsecond=0),
                now.replace(hour=19, minute=59, second=59, microsecond=999999)]
    session6 = [now.replace(hour=20, minute=0, second=0, microsecond=0),
                now.replace(hour=23, minute=59, second=59, microsecond=999999)]
    sessions = [session1, session2, session3, session4, session5, session6]

    sub4 = {"interval": 4, "sessions": [session1, session2, session3, session4, session5, session6]}
    sub8 = {"interval": 8, "sessions": [session1, session3, session5]}
    sub12 = {"interval": 12, "sessions": [session2, session5]}
    sub24 = {"interval": 24, "sessions": [session3]}
    subs = [sub4, sub8, sub12, sub24]

    for session in sessions:
        if session[0] < now < session[1]:
            print(session[0], " > ", now, " > ", session[1])
            for sub in subs:
                if session in sub["sessions"]:
                    notifyNewRecordsForLastXHours(sub["interval"])


def sendVerificationEmail(email, companyName) -> Callback:
    try:

        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" +\
               helpers.verificationSigner.dumps(payload, salt='email-confirm-key')

        send_email((email), 'Account verification',
                   '/emails/verification.html', link=link)

        return Callback(True, 'Verification email is on its way to ' + email)

    except Exception as e:
        print("sendVerificationEmail() Error: ", e)
        return Callback(False, 'Could not send a verification email to ' + email)


def sendPasswordResetEmail(email, companyID):
    try:

        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/reset_password/" +\
               helpers.verificationSigner.dumps(payload, salt='reset-pass-key')

        send_email((email), 'Password reset',
                   '/emails/reset_password.html', link=link)

        return Callback(True, 'Password reset email is on its way to ' + email)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)


def sendNewUserHasRegistered(name, email, companyName, tel):
    try:

        send_email(("thesearchbase@gmail.com"), companyName + ' has signed up',
                   '/emails/company_signup.html', name=name, email=email, companyName=companyName, tel=tel)

        return Callback(True, 'Signed up email is on its way')

    except Exception as e:
        print("sendNewUserHasRegistered() Error: ", e)
        return Callback(False, 'Could not send a signed up email')


def addedNewUserEmail(adminEmail, targetEmail, password):
    try:
        link = "https://www.thesearchbase.com/admin/changepassword"

        send_email((targetEmail), 'You have been added to TheSearchBase',
                   'emails/account_invitation.html', password=password, adminEmail=adminEmail)

        return Callback(True, 'Email sent is on its way to ' + targetEmail)

    except Exception as e:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)


def sendSolutionAlert(record, solutions):
    try:
        targetEmail = record["email"]
        userData = record["record"]
        print("DATA: ", solutions)

        send_email((targetEmail), 'You have new job matches',
                   'emails/solution_alert.html', userData=userData, solutions=solutions)

        return Callback(True, 'Email sent is on its way to ' + targetEmail)

    except Exception as e:
        print("mail_services.sendSolutionAlert ERROR: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)


# NOTIFICATIONS
def notifyNewRecordsForLastXHours(hours):
    try:
        userSettings_callback: Callback = user_services.getAllUserSettings()
        if not userSettings_callback.Success: raise Exception("userSettings_callback: ", userSettings_callback.Message)

        for record in userSettings_callback.Data:
            if not record.UserInputNotifications:
                continue

            user_callback: Callback = user_services.getByID(record.ID)
            if not user_callback.Success: raise Exception("user_callback: ", user_callback.Message)

            assistants_callback: Callback = assistant_services.getAll(user_callback.Data.CompanyID)
            if not assistants_callback.Success: raise Exception("assistants_callback: ", assistants_callback.Message)

            information = []

            for assistant in assistants_callback.Data:
                if not assistant.MailEnabled or not hours == assistant.MailPeriod:
                    continue

                records_callback: Callback = analytics_services.getAllRecordsByAssistantIDInTheLast(hours, assistant.ID)
                if not records_callback.Success:
                    raise Exception("records_callback: ", records_callback.Message)

                if not records_callback.Data:
                    continue

                information.append(
                    {"assistantName": assistant.Name, "data": records_callback.Data, "assistantID": assistant.ID})

            if not information:
                continue

            sendRecords_callback: Callback = sendNewRecordsNotification(user_callback.Data.Email, information)
            if not sendRecords_callback.Success: raise Exception("sendRecords_callback: ", sendRecords_callback.Message)

    except Exception as e:
        print("mail_services.notifyNewRecordsForLastXHours() ERROR: ", e)


def sendNewRecordsNotification(reciever, data):
    try:
        send_email((reciever), 'Your new data',
                   'emails/user_notification.html', data=data)

        return Callback(True, 'Email sent and it\'s on its way to ' + reciever)

    except Exception as e:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + reciever)


# def async(f):
#    def wrapper(*args, **kwargs):
#        thr = Thread(target=f, args=args, kwargs=kwargs)
#        thr.start()
#    return wrapper


# SEND CODE
# @async
def send_async_email(app, msg):
    with app.app_context():
        print('====> sending async')
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    try:
        app = current_app._get_current_object()
        msg = Message(subject, recipients=[to], sender="thesearchbase@gmail.com")
        msg.html = render_template(template, **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
    except Exception as e:
        print("mail_services.send_email() ERROR / TEMPLATE ERROR: ", e)
    # send_async_email(app, msg)
