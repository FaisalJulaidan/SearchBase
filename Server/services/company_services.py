from models import db, Callback, Company, User, AppointmentAllocationTime, AppointmentAllocationTimeInfo, StoredFile, StoredFileInfo
from services import stored_file_services
from utilities import helpers, enums
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import logging, stripe



def create(name, url, ownerEmail) -> Company or None:

    try:
        stripeCus = stripe.Customer.create(
            description="Customer for " + name + " company.",
            email=ownerEmail
        )
        newCompany = Company(Name=name, URL=url, StripeID=stripeCus['id'])
        db.session.add(newCompany)

        db.session.commit()
        return Callback(True, "Company has been created successfully.", newCompany)

    except stripe.error as exc:
        helpers.logError("company_service.create() Stripe Issue: " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while creating a stripe customer for the new company.")

    except Exception as exc:
        helpers.logError("company_service.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't create a company entity.")




def getByID(id: int, eager: bool = False) -> Company or None:
    try:
        if not id: raise Exception("id is required")

        # Get result and check if None then raise exception
        query = db.session.query(Company)
        if eager:
            query.options(joinedload('StoredFile').joinedload('StoredFileInfo'))
        result = query.get(id)
        if not result: raise Exception

        return Callback(True,
                        'Company with ID ' + str(id) + ' was successfully retrieved',
                        result)

    except Exception as exc:
        db.session.rollback()
        # print(exc)
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


def getByCompanyID(id, eager: bool = False) -> Callback:
    try:
        query = db.session.query(Company).filter(Company.ID == id)

        if eager:
            query.options(joinedload('StoredFile').joinedload('StoredFileInfo'))

        result = query.first()
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

        # Delete old logo ref from DB. DigitalOcean will override the old logo since they have the same name
        oldLogo: StoredFileInfo = helpers.keyFromStoredFile(company.StoredFile, enums.FileAssetType.Logo)
        if oldLogo.AbsFilePath:
            db.session.delete(oldLogo.StoredFile)
            db.session.delete(oldLogo) # comment this if u want to use a unique filename for every new logo instead of company id encoded

        # Generate unique name: hash_sessionIDEncrypted.extension
        filename = helpers.encodeID(companyID) + "_CompanyLogo" + '.' + \
                   secure_filename(file.filename).rsplit('.', 1)[1].lower()

        sf = StoredFile()
        db.session.add(sf)
        db.session.flush()


        upload_callback: Callback = stored_file_services.uploadFile(file, filename, True, model=Company,
                                identifier="ID",
                                identifier_value=company.ID,
                                stored_file_id=sf.ID,
                                key=enums.FileAssetType.Logo)
        
        return Callback(True, 'Logo uploaded successfully.', upload_callback.Data)

    except Exception as exc:
        helpers.logError("company_service.uploadLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in uploading logo.')


def deleteLogo(companyID):
    try:

        company: Company = getByCompanyID(companyID, True).Data
        if not company: raise Exception


        logo: StoredFile = company.StoredFile
        if not logo: return Callback(False, 'No logo to delete')

        # Delete file from cloud Space and reference from database
        path = helpers.keyFromStoredFile(logo, enums.FileAssetType.Logo).FilePath

        delete_callback : Callback = stored_file_services.deleteFile(path, logo)
        if not delete_callback.Success:
            raise Exception(delete_callback.Message)

        db.session.commit()
        return Callback(True, 'Logo deleted successfully.')

    except Exception as exc:
        helpers.logError("company_service.deleteLogo(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting logo.')

def activateCompany(companyID):
    try:
        # Get company and check if None then raise exception
        company: Company = db.session.query(Company).get(companyID)
        if not company: raise Exception

        company.Active = True
        db.session.commit()
        return Callback(True, 'Company activated successfully')

    except Exception as exc:
        # print(exc)
        db.session.rollback()
        return Callback(False, 'Company activation failed')