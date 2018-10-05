import sqlalchemy.exc
from models import db, Callback, Newsletter
from utilities import helpers

def addNewsletterPerson(email):
    try:
        newNewsletter = Newsletter(Email=email)
        db.session.add(newNewsletter)

        db.session.commit()
        return Callback(True, email + ' has been registered for newsletters.')
    except Exception as e:
        db.session.rollback()
        print("addNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot register' + email+ ' for newsletters.')

    # finally:
    #     db.session.close()

def checkForNewsletter(email):
    try:
        result = db.session.query(Newsletter).filter(Newsletter.Email == email).first()
        print(result)
        if not result: raise Exception

        return Callback(True, email + ' is registered for newsletters')
    except Exception as e:
        db.session.rollback()
        print("newsletter_services.checkForNewsletter() ERROR: ", e)
        return Callback(False, email + ' is not registered for newsletters')

    # finally:
    #     db.session.close()

def removeNewsletterPerson(email):
    try:
        db.session.query(Newsletter).filter(Newsletter.Email == email).delete()

        db.session.commit()
        return Callback(True, email + ' has been unsubsribed from newsletters.')
    except Exception as e:
        db.session.rollback()
        print("removeNewsletterPerson() Error: ", e)
        return Callback(False, 'Couldnot unsubsribe' + email+ ' from newsletters.')

    # finally:
    #     db.session.close()

def getAll():
    try:
        result = db.session.query(Newsletter).all()

        return Callback(True, "Newsletters retrieved", result)
    except Exception as e:
        print("newsletter_services.getAll ERROR: ", e)
        db.session.rollback()
        return Callback(False, "Error in getting newsletters: ")

    # finally:
    #     db.session.close()
