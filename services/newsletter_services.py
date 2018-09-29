import sqlalchemy.exc
from models import db, Callback, Newsletter
from utilities import helpers

def addNewsletterPerson(email):
    try:
        newNewsletter = Newsletter(Email=email)
        db.session.add(newNewsletter)
    except Exception as e:
        db.session.rollback()
        print("addNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot register' + email+ ' for newsletters.')
    
    db.session.commit()
    return Callback(True, email + ' has been registered for newsletters.')

def checkForNewsletter(email):
    try:
        result = db.session.query(Newsletter).filter(Newsletter.Email == email).first()
        print(result)
        if not result: raise Exception
    except Exception as e:
        return Callback(False, email + ' is not registered for newsletters')

    return Callback(True, email + ' is registered for newsletters')

def removeNewsletterPerson(email):
    try:
        db.session.query(Newsletter).filter(Newsletter.Email == email).delete()
    except Exception as e:
        db.session.rollback()
        print("removeNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot unsubsribe' + email+ ' from newsletters.')
    
    db.session.commit()
    return Callback(True, email + ' has been unsubsribed from newsletters.')

def getAll():
    try:
        result = db.session.query(Newsletter).all()
    except Exception as e:
        print("newsletter_services.getAll ERROR: ", e)
        return Callback(False, "Error in getting newsletters: ")

    return Callback(True, "Newsletters retrieved", result)