import sqlalchemy.exc

from .db_services import _safeCommit
from models import db, Callback, Company, User, Role
from flask import session
import stripe


def getByID(id) -> Company or None:
    try:
        if id:
            # Get result and check if None then raise exception
            result = db.session.query(Company).get(id)
            if not result: raise Exception

            return Callback(True,
                            'Company with ID ' + str(id) + ' was successfully retrieved',
                            result)
        else:
            raise Exception
    except Exception as exc:
        db.session.rollback()
        return Callback(False,
                        'Company with ID ' + str(id) + ' does not exist')

    # finally:
       # db.session.close()


def getAll() -> list:
    try:
        return db.session.query(Company)
    except:
        db.session.rollback()
        return None
    # finally:
       # db.session.close()



def create(name, url, ownerEmail) -> Company or None:

    try:
        stripeCus = stripe.Customer.create(
            description="Customer for " + name + " company.",
            email=ownerEmail
        )
        newCompany = Company(Name=name, URL=url, StripeID=stripeCus['id'])
        db.session.add(newCompany)

        db.session.commit()
        return Callback(True, "Company uas been created successfully.", newCompany)

    except stripe.error as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "An error occurred while creating a stripe customer for the new company.")
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "Couldn't create a company entity.")
    # finally:
       # db.session.close()
    # Save



def removeByName(name) -> bool:

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
        db.session.commit()
        return True
    except Exception as exc:
        db.session.rollback()
        print(exc)
        return False
    # finally:
       # db.session.close()

def getByEmail(email) -> Callback:
    try:
        result = db.session.query(User).filter(User.Email == email).first()
        if not result: return Callback(False, 'Could not retrieve user\'s data')

        result = db.session.query(Company).filter(Company.ID == result.CompanyID).first()
        if not result: return Callback(False, 'Could not retrieve company\'s data.')

        return Callback(True, 'Company was successfully retrieved.', result)
    except Exception as exc:
        print("company_services.getByEmail() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Company could not be retrieved')
    # finally:
       # db.session.close()

def getByCompanyID(id) -> Callback:
    try:
        result = db.session.query(Company).filter(Company.ID == id).first()
        if not result: return Callback(False, 'Could not retrieve company\'s data.')

        return Callback(True, 'Company was successfully retrieved.', result)
    except Exception as exc:
        db.session.rollback()
        print("company_services.getByCompanyID() ERROR: ", exc)
        return Callback(False, 'Company could not be retrieved')
    # finally:
       # db.session.close()


def getByStripeID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Company).filter(Company.StripeID == id).first()
        if not result: raise Exception

        return Callback(True, "Got company successfully.", result)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')
    # finally:
       # db.session.close()
