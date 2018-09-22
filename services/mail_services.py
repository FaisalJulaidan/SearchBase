import sqlalchemy.exc

from flask import Flask, render_template, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import Callback
from threading import Thread
from time import sleep  


verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')
mail = Mail()

def sendVerificationEmail(email, companyName, fullname) -> Callback:
    try:

        payload = email + ";" + companyName
        link = "http://127.0.0.1:5000/account/verify/" + verificationSigner.dumps(payload)

        send_email((email), 'Account verification', 
               '/emails/verification.html', link = link)

    except Exception as e:
        print("sendVerificationEmail() Error: ", e)
        return Callback(False, 'Could not send a verification email to ' + email)

    return Callback(True, 'Verification email sent successfully to ' + email)

def sendNewUserHasRegistered(name, email, companyName, tel):
    try:

        send_email(("thesearchbase@gmail.com"), companyName+' has signed up', 
               '/emails/company_signup.html', name = name, email=email, companyName=companyName, tel=tel)

    except Exception as e:
        print("sendNewUserHasRegistered() Error: ", e)
        return Callback(False, 'Could not send a signed up email')

    return Callback(True, 'Signed up email sent successfully')

def sendPasswordResetEmail(email, companyID):
    try:
              
        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
        
        send_email((email), 'Password reset', 
               '/emails/reset_password.html', link = link)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)
    
    return Callback(True, 'Password reset email sent successfully to ' + email)

def addedNewUserEmail(adminEmail, targetEmail, password):
    try:
        link = "https://www.thesearchbase.com/admin/changepassword"

        send_email((targetEmail), 'You have been added to TheSearchBase', 
               'emails/account_invitation.html', password=password, adminEmail=adminEmail)

    except:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)
    
    return Callback(True, 'Email sent successfully to ' + targetEmail)

#mailing
def send_async_email(app, msg):
    with app.app_context():
        #uncomment bellow to add delay
        #for i in range(*seconds int*, -1, -1):
        #    sleep(1)

        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[to], sender="thesearchbase@gmail.com")
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr