import sqlalchemy.exc

from flask import Flask
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import Callback
import string
import random

mail = Mail()
verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')

# Mail Config
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = 465,
MAIL_USE_SSL = True,
MAIL_USERNAME = 'thesearchbase@gmail.com',
MAIL_PASSWORD = 'pilbvnczzdgxkyzy'


def sendVerificationEmail(email, companyName, fullname) -> Callback:

    try:
        msg = Message("Account verification",
                      sender="thesearchbase@gmail.com",
                      recipients=[email])
        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)
        # need to add the links to the email, right now its just a page.
        msg.html = render_template('/emails/verification.html', link)
        mail.send(msg)

        # sending the registration confirmation email to us
        msg = Message("A new company has signed up!",
                      sender="thesearchbase@gmail.com",
                      recipients=["thesearchbase@gmail.com"])
        msg.html = "<p>Company name: " + companyName + " has signed up. <br>The admin's details are: <br>Name: " \
                   + fullname + " <br>Email: " + email + ".</p>"
        mail.send(msg)
    except Exception as e:
        return Callback(False, 'Could not send a verification email to ' + email)

    return Callback(True, 'Verification email sent successfully to ' + email)





def sendPasswordResetEmail(email, companyID):
    try:
        msg = Message("Password reset",
                    sender="thesearchbase@gmail.com",
                    recipients=[email])
              
        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/account/resetpassword/" + verificationSigner.dumps(payload)
        # msg.html
        render_template('/emails/reset-password.html', link)
        mail.send(msg)

    except Exception as e:
        print("sendPasswordResetEmail() Error: ", e)
        return Callback(False, 'Could not send a password reset email to ' + email)
    
    return Callback(True, 'Password reset email sent successfully to ' + email)

def addedNewUserEmail(adminEmail, targetEmail):
    try:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        link = "https://www.thesearchbase.com/admin/changepassword"

        msg = Message("You have been added to TheSearchBase",
                        sender="thesearchbase@gmail.com",
                        recipients=[targetEmail])

        msg.html = "<h4>Hi, <h4> <br /> <p>You have been registered with TheSearchBase by an admin at your company.<br /> \
                    To get access to the platform, we have generated a temporary password for you to access the platform.</p> <br /> \
                    <h4>Your temporary password is: "+password+".<h4><br />\
                    Please visit <a href='"+link+"'>this link</a> to sign in. To change your password you can use the same link or go to Account Details -> Profile on the left menu.<p><br /> \
                    If you feel this is a mistake please contact "+adminEmail+". <br /> <br /> Regards, <br />TheSearchBase Team"

        mail.send(msg)

    except:
        print("addedNewUserEmail() Error: ", e)
        return Callback(False, 'Could not send email to ' + targetEmail)
    
    return Callback(True, 'Password reset email sent successfully to ' + targetEmail)