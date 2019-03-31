import sqlalchemy.exc
from models import db, Callback, Newsletter
from utilities import helpers
import logging

def addNewsletterPerson(email):
    try:
        newNewsletter = Newsletter(Email=email)
        db.session.add(newNewsletter)

        db.session.commit()
        return Callback(True, email + ' has been registered for newsletters.')
    except Exception as exc:
        print("newsletter_service.addNewsletterPerson() Error: ", exc)
        logging.error("newsletter_service.addNewsletterPerson(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Couldnot register' + email+ ' for newsletters.')

def checkForNewsletter(email):
    try:
        result = db.session.query(Newsletter).filter(Newsletter.Email == email).first()
        print(result)
        if not result: raise Exception

        return Callback(True, email + ' is registered for newsletters')
    except Exception as exc:
        logging.error("newsletter_service.checkForNewsletter(): " + str(exc))
        db.session.rollback()
        return Callback(False, email + ' is not registered for newsletters')


def removeNewsletterPerson(email):
    try:
        db.session.query(Newsletter).filter(Newsletter.Email == email).delete()
        db.session.commit()
        return Callback(True, email + ' has been unsubscribed from newsletters.')

    except Exception as exc:
        print("removeNewsletterPerson() Error: ", exc)
        logging.error("newsletter_service.removeNewsletterPerson(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not unsubscribe' + email+ ' from newsletters.')


def getAll():
    try:
        result = db.session.query(Newsletter).all()

        return Callback(True, "Newsletters retrieved", result)
    except Exception as exc:
        print("newsletter_services.getAll ERROR: ", exc)
        logging.error("newsletter_service.getAll(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Error in getting newsletters: ")