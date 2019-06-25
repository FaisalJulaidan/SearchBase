from models import db, Callback, Company, User
from services import stored_file_services
from utilities import helpers
from werkzeug.utils import secure_filename
import logging , stripe



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
        helpers.logError("company_service.create() Stripe Issue: " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while creating a stripe customer for the new company.")

    except Exception as exc:
        helpers.logError("company_service.create(): " + str(exc))
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
        db.session.rollback()
        return Callback(False,
                        'Company with ID ' + str(id) + ' does not exist')


def removeByName(name) -> bool:
    try:
        db.session.query(Company).filter(Company.Name == name).delete()
        db.session.commit()
        return True
    except Exception as exc:
        helpers.logError("company_service.removeByName(): " + str(exc))
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
        helpers.logError("company_service.getByEmail(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Company could not be retrieved')


def getByCompanyID(id) -> Callback:
    try:
        result = db.session.query(Company).filter(Company.ID == id).first()
        if not result: return Callback(False, 'Could not retrieve company\'s data.')

        return Callback(True, 'Company was successfully retrieved.', result)
    except Exception as exc:
        helpers.logError("company_service.getByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Company could not be retrieved')


def getByStripeID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Company).filter(Company.StripeID == id).first()
        if not result: raise Exception

        return Callback(True, "Got company successfully.", result)

    except Exception as exc:
        helpers.logError("company_service.getByStripeID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')


def update(companyName, websiteURL, trackData: bool, techSupport: bool, accountSpecailst: bool, companyID):
    try:

        if not (companyName
                and websiteURL
                and isinstance(trackData, bool)
                and isinstance(techSupport, bool)
                and isinstance(accountSpecailst, bool)):
            raise Exception("Did not provide all required fields")

        callback: Callback = getByCompanyID(companyID)
        if not callback.Success: return Callback(False, "Could not find company")
        company: Company = callback.Data

        company.Name = companyName
        company.URL = websiteURL
        company.TrackingData = trackData
        company.TechnicalSupport = techSupport
        company.AccountSpecialist = accountSpecailst

        db.session.commit()

        return Callback(True, "Company has been updated")

    except Exception as exc:
        helpers.logError("company_service.updateCompany(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Company cold not be updated")

# ----- Logo Operations ----- #
def uploadLogo(file, companyID):
    try:

        company: Company = getByCompanyID(companyID).Data
        if not company: raise Exception

        # Generate unique name: hash_sessionIDEncrypted.extension
        filename = helpers.encodeID(companyID) + '.' + \
                   secure_filename(file.filename).rsplit('.', 1)[1].lower()
        company.LogoPath = filename

        # Upload file to cloud Space
        upload_callback : Callback = stored_file_services.uploadFile(file,
                                                                     filename,
                                                                     stored_file_services.COMPANY_LOGOS_PATH,
                                                                     public=True)
        if not upload_callback.Success:
            raise Exception(upload_callback.Message)

        db.session.commit()

        return Callback(True, 'Logo uploaded successfully.', filename)

    except Exception as exc:
        helpers.logError("company_service.uploadLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in uploading logo.')


def deleteLogo(companyID):
    try:

        company: Company = getByCompanyID(companyID).Data
        if not company: raise Exception


        logoPath = company.LogoPath
        if not logoPath: return Callback(False, 'No logo to delete')

        # Delete file from cloud Space and reference from database
        company.LogoPath = None
        delete_callback : Callback = stored_file_services.deleteFile(logoPath,
                                                                     stored_file_services.COMPANY_LOGOS_PATH)
        if not delete_callback.Success:
            raise Exception(delete_callback.Message)

        db.session.commit()
        return Callback(True, 'Logo deleted successfully.')

    except Exception as exc:
        helpers.logError("company_service.deleteLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting logo.')