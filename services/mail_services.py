import sqlalchemy.exc

from flask import Flask, render_template, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import Callback, db, Newsletter
from threading import Thread
from time import sleep
from services import user_services, assistant_services, analytics_services, newsletter_services



verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')
mail = Mail()

def sendVerificationEmail(email, companyName) -> Callback:
    try:

        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)

        send_email((email), 'Account verification', 
               '/emails/verification.html', link = link)

    except Exception as e:
        print("sendVerificationEmail() Error: ", e)
        return Callback(False, 'Could not send a verification email to ' + email)

    return Callback(True, 'Verification email is on its way to ' + email)

def sendNewUserHasRegistered(name, email, companyName, tel):
    try:

        send_email(("thesearchbase@gmail.com"), companyName+' has signed up', 
               '/emails/company_signup.html', name = name, email=email, companyName=companyName, tel=tel)

    except Exception as e:
        print("sendNewUserHasRegistered() Error: ", e)
        return Callback(False, 'Could not send a signed up email')

    return Callback(True, 'Signed up email is on its way')

def sendPasswordResetEmail(email, companyID):
    try:
              
        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
        
        send_email((email), 'Password reset', 
               '/emails/reset_password.html', link = link)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)
    
    return Callback(True, 'Password reset email is on its way to ' + email)

def addedNewUserEmail(adminEmail, targetEmail, password):
    try:
        link = "https://www.thesearchbase.com/admin/changepassword"

        send_email((targetEmail), 'You have been added to TheSearchBase', 
               'emails/account_invitation.html', password=password, adminEmail=adminEmail)

    except:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)
    
    return Callback(True, 'Email sent is on its way to ' + targetEmail)

#NOTIFICATIONS
def notifyNewRecordsForLastXHours(hours):
    try:
        print("0")
        newsletters_callback : Callback = newsletter_services.getAll()
        if not newsletters_callback.Success: raise Exception("newsletters_callback: ", newsletters_callback.Message)

        for record in newsletters_callback.Data:
            print("1")
            user_callback : Callback = user_services.getByEmail(record.Email)
            if not user_callback.Success: raise Exception("user_callback: ", user_callback.Message)
            print("2")

            assistants_callback : Callback = assistant_services.getAll(user_callback.Data.CompanyID)
            if not assistants_callback.Success: raise Exception("assistants_callback: ", assistants_callback.Message)
            print("3")

            for assistant in assistants_callback.Data:
                print("4")
                records_callback : Callback = analytics_services.getAllRecordsByAssistantIDInTheLast(hours, assistant.ID)
                if not records_callback.Success: raise Exception("records_callback: ", records_callback.Message)
                print("5")

                print(records_callback.Data)
                if not records_callback.Data: continue
                print("6")

                sendRecords_callback : Callback = sendNewRecordsNotification(record.Email, {"assistantName": assistant.Name, "data": records_callback.Data, "assistantID": assistant.ID})
                if not sendRecords_callback.Success: raise Exception("sendRecords_callback: ", sendRecords_callback.Message)
                print("7")

    except Exception as e:
        print("mail_services.notifyNewRecordsForLastXHours() ERROR: ", e)

def sendNewRecordsNotification(reciever, data):
    try:
        send_email((reciever), 'Your new data', 
               'emails/user_notification.html', data=data)

    except Exception as e:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + reciever)
    
    return Callback(True, 'Email sent and it\'s on its way to ' + reciever)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


#SEND CODE
# @async
def send_async_email(app, msg):
    with app.app_context():
        print('====> sending async')
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    # app = current_app._get_current_object()
    msg = Message(subject, recipients=[to], sender="thesearchbase@gmail.com")
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[mail.app, msg])
    thr.start()
    # send_async_email(app, msg)