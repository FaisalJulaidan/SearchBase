from models import db, Callback, Company, User, Role
import stripe
import logging


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
        logging.error("company_service.create() Stripe Issue: " + str(exc))
        return Callback(False, "An error occurred while creating a stripe customer for the new company.")
    except Exception as exc:
        print(exc)
        logging.error("company_service.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't create a company entity.")



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
        logging.error("company_service.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False,
                        'Company with ID ' + str(id) + ' does not exist')


def getAll() -> list or None:
    try:
        return db.session.query(Company)
    except Exception as exc:
        logging.error("company_service.getAll(): " + str(exc))
        db.session.rollback()
        return None



def removeByName(name) -> bool:

    try:
        db.session.query(Company).filter(Company.Name == name).delete()
        db.session.commit()
        return True
    except Exception as exc:
        print(exc)
        logging.error("company_service.removeByName(): " + str(exc))
        db.session.rollback()
        return False


def getByEmail(email) -> Callback:
    try:
        result = db.session.query(User).filter(User.Email == email).first()
        if not result: return Callback(False, 'Could not retrieve user\'s data')

        result = db.session.query(Company).filter(Company.ID == result.CompanyID).first()
        if not result: return Callback(False, 'Could not retrieve company\'s data.')

        return Callback(True, 'Company was successfully retrieved.', result)
    except Exception as exc:
        print("company_services.getByEmail() ERROR: ", exc)
        logging.error("company_service.getByEmail(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Company could not be retrieved')


def getByCompanyID(id) -> Callback:
    try:
        result = db.session.query(Company).filter(Company.ID == id).first()
        if not result: return Callback(False, 'Could not retrieve company\'s data.')

        return Callback(True, 'Company was successfully retrieved.', result)
    except Exception as exc:
        print("company_services.getByCompanyID() ERROR: ", exc)
        logging.error("company_service.getByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Company could not be retrieved')



def getByStripeID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Company).filter(Company.StripeID == id).first()
        if not result: raise Exception

        return Callback(True, "Got company successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("company_service.getByStripeID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')


def updateCompany(companyName, companyID):
    try:
        callback: Callback = getByCompanyID(companyID)
        if not callback.Success: return Callback(False, "Could not find company")
        callback.Data.Name = companyName
        db.session.commit()

        return Callback(True, "Company has been updated")
    except Exception as exc:
        print("company_service.updateCompany() ERROR: ", exc)
        logging.error("company_service.updateCompany(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Company cold not be updated")