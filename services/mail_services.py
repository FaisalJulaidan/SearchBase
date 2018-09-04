import sqlalchemy.exc

from flask import Flask, render_template, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import Callback
from threading import Thread
from time import sleep  
import string
import random


verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')
mail = Mail()

def sendVerificationEmail(email, companyName, fullname) -> Callback:
    try:

        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)

        send_email((email), 'Account verification', 
               '/emails/verification.html', link = link)

        # sending the registration confirmation email to us - needs template
        #msg = Message("A new company has signed up!",
        #              sender="thesearchbase@gmail.com",
        #              recipients=["thesearchbase@gmail.com"])
        #msg.html = "<p>Company name: " + companyName + " has signed up. <br>The admin's details are: <br>Name: " \
        #           + fullname + " <br>Email: " + email + ".</p>"
        #mail.send(msg)

    except Exception as e:
        print("sendVerificationEmail() Error: ", e)
        return Callback(False, 'Could not send a verification email to ' + email)

    return Callback(True, 'Verification email sent successfully to ' + email)

def sendPasswordResetEmail(email, companyID):
    try:
              
        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
        
        send_email((email), 'Password reset', 
               '/emails/reset-password.html', link = link)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)
    
    return Callback(True, 'Password reset email sent successfully to ' + email)

def addedNewUserEmail(adminEmail, targetEmail):
    try:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        link = "http://206.189.122.126/admin/changepassword"

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
        #for i in range(*delay int*, -1, -1):
        #    sleep(1)

        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[to], sender="thesearchbase@gmail.com")
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr