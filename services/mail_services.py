import sqlalchemy.exc

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

from models import Callback

mail = Mail()
verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')


def sendVerificationEmail(email, companyName, fullname) -> Callback:

    try:
        msg = Message("Account verification",
                      sender="thesearchbase@gmail.com",
                      recipients=[email])
        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)
        msg.html = "<img src='https://thesearchbase.com/static/email_images/verify_email.png'><br /><h4>Hi,</h4>" \
                   " <p>Thank you for registering with TheSearchbase.</p> <br />  There is just one small step left, visit \
                    <a href='" + link + "'> this link </a> to verify your account. \
                            In case the link above doesn't work you can click on the link below. <br /> <br /> " + link + " <br />  <br /> \
                            We look forward to you, using our platform. <br /> <br />\
                            Regards, <br /> TheSearchBase Team <br />\
                            <img src='https://thesearchbase.com/static/email_images/footer_image.png'>"
        mail.send(msg)

        # sending the registration confirmation email to us
        msg = Message("A new company has signed up!",
                      sender="thesearchbase@gmail.com",
                      recipients=["thesearchbase@gmail.com"])
        msg.html = "<p>Company name: " + companyName + " has signed up. <br>The admin's details are: <br>Name: " \
                   + fullname + " <br>Email: " + email + ".</p>"
        mail.send(msg)
    except Exception as e:
        return Callback(False, 'Error in sending verification email to ' + email)

    return Callback(True, 'Verification email sent successfully to ' + email)
