import sqlalchemy.exc
from models import db, Callback, Newsletter
from utilties import helpers

def addNewsletterPerson(email):
    try:
        newNewsletter = Newsletter(Email=email)
        db.session.add(newNewsletter)
    except Exception as e:
        db.session.rollback()
        print("addNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot register' + email+ ' for newsletters.')

    return Callback(True, email + ' has been registered for newsletters.')

def removeNewsletterPerson(email):
    try:
        db.session.query(Newsletter).filter(Newsletter.Email == email).delete()
    except Exception as e:
        db.session.rollback()
        print("removeNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot unsubsribe' + email+ ' from newsletters.')

    return Callback(True, email + ' has been unsubsribed from newsletters.')