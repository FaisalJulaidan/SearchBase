import sqlalchemy.exc

from flask import Flask, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import Callback
import string
import random
#from celery import Celery


verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')
mail = Mail()

def sendVerificationEmail(email, companyName, fullname) -> Callback:
    try:
        print(1)
        msg = Message("Account verification",
                      sender="thesearchbase@gmail.com",
                      recipients=[email])
        print(2)
        payload = email + ";" + companyName
        print(3)
        link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)
        print(4)
        msg.html = render_template('/emails/verification.html', link = link)
        print(5)
        mail.send(msg)
        print(6)

        # sending the registration confirmation email to us
        msg = Message("A new company has signed up!",
                      sender="thesearchbase@gmail.com",
                      recipients=["thesearchbase@gmail.com"])
        msg.html = "<p>Company name: " + companyName + " has signed up. <br>The admin's details are: <br>Name: " \
                   + fullname + " <br>Email: " + email + ".</p>"
        mail.send(msg)
        print(7)
    except Exception as e:
        print("sendVerificationEmail() Error: ", e)
        return Callback(False, 'Could not send a verification email to ' + email)

    return Callback(True, 'Verification email sent successfully to ' + email)

def sendPasswordResetEmail(email, companyID):
    try:
        msg = Message("Password reset",
                    sender="thesearchbase@gmail.com",
                    recipients=[email])
              
        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
        msg.html = "Hi"
        #msg.html = render_template('/emails/reset-password.html', link = link) error with '/emails/reset-password.html' missing?
        mail.send(msg)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)
    
    return Callback(True, 'Password reset email sent successfully to ' + email)

def addedNewUserEmail(adminEmail, targetEmail):
    try:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        link = "http://206.189.122.126/admin/changepassword"

        msg = Message("You have been added to TheSearchBase",
                        sender="thesearchbase@gmail.com",
                        recipients=[targetEmail])

        msg.html = render_template('/emails/account_invitation.html', password=password, adminEmail=adminEmail)

        mail.send(msg)

    except:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)
    
    return Callback(True, 'Email sent successfully to ' + targetEmail)