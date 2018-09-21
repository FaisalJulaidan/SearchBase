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
        return Callback(False,
                        'Company with ID ' + str(id) + ' does not exist')


def getAll() -> list:
    return db.session.query(Company)


def create(name, url, ownerEmail) -> Company or None:

    try:
        stripeCus = stripe.Customer.create(
            description="Customer for " + name + " company.",
            email=ownerEmail
        )
        newCompany = Company(Name=name, URL=url, StripeID=stripeCus['id'])
        db.session.add(newCompany)

    except stripe.error as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "An error occurred while creating a stripe customer for the new company.")
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "Couldn't create a company entity.")

    # Save
    db.session.commit()
    return Callback(True, "Company uas been created successfully.", newCompany)



def removeByName(name) -> bool:

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
    except Exception as exc:
        db.session.rollback()
        print(exc)
        return False
    db.session.commit()
    return True

def getByEmail(email) -> Callback:

    result = db.session.query(User).filter(User.Email == email).first()
    if not result: return Callback(False, 'Could not retrieve user\'s data')

    result = db.session.query(Company).filter(Company.ID == result.CompanyID).first()
    if not result: return Callback(False, 'Could not retrieve company\'s data.')
    
    return Callback(True, 'Company was successfully retrieved.', result)

def getByCompanyID(id) -> Callback:

    result = db.session.query(Company).filter(Company.ID == id).first()
    if not result: return Callback(False, 'Could not retrieve company\'s data.')
    
    return Callback(True, 'Company was successfully retrieved.', result)


def getByStripeID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Company).filter(Company.StripeID == id).first()
        if not result: raise Exception

        return Callback(True, "Got company successfully.", result)

    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not get the assistant by nickname.')