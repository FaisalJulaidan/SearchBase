from models import Callback, db, Company, Plan
from sqlalchemy import and_
from utilities import helpers
from services import company_services


def isAuthorised(operation, companyID) -> bool:
    try:

        # Get company to check its permissions
        security_callback: Callback = company_services.getByCompanyID(companyID)
        if not security_callback.Success:
            raise Exception('Company cannot be found')
        editorCompany: Company = security_callback.Data

        # Check editor company permission:
        if operation == 'AccessAssistants':
            if not editorCompany.Plan.AccessAssistants:
                raise Exception('Plan does not include assistant access')

        if operation == 'AccessCampaigns':
            if not editorCompany.Plan.AccessCampaigns:
                raise Exception('Plan does not include campaign access')

        if operation == 'AccessAutoPilots':
            if not editorCompany.Plan.AccessAutoPilot:
                raise Exception('Plan does not include autopilot access')

        if operation == 'AccessDatabases':
            if not editorCompany.Plan.AccessDatabases:
                raise Exception('Plan does not include databases access')

        if operation == 'AccessAppointments':
            if not editorCompany.Plan.AccessAppointments:
                raise Exception('Plan does not include appointment access')

        # Otherwise company is authorised to perform operation
        return True

    except Exception as exc:
        helpers.logError(str(exc))
        db.session.rollback()
        return False


def create(name: str, accessAssistants: bool, accessCampaigns: bool, accessAutoPilot: bool,
           accessAppointments: bool, companyID: int) -> Callback:

    try:
        newPlan = Plan(Name=name, AccessAssistants=accessAssistants, AccessCampaigns=accessCampaigns,
                       AccessAutoPilot=accessAutoPilot, AccessAppointments=accessAppointments, CompanyID=companyID)
        db.session.add(newPlan)

        db.session.commit()
        return Callback(True, 'Company plan has been created successfully!')

    except Exception as exc:
        helpers.logError("plan_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create new plan.')


def getByID(id) -> Plan or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).get(id)
        if not result:
            raise Exception
        return Callback(True, 'Plan does exist.', result)

    except Exception as exc:
        helpers.logError("plan_service.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plan does not exist')


def getByName(name) -> Plan or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.Name == name).first()
        if not result:
            raise Exception
        return Callback(True, 'Role does exist.', result)

    except Exception as exc:
        helpers.logError("plan_service.getByName(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plan does not exist')


def getAllByCompanyID(companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(Plan.CompanyID == companyID).all()
        return Callback(True, 'Plans retrieved successfully.',result)

    except Exception as exc:
        helpers.logError("plan_service.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plans cannot be retrieved.')


def getByIDAndCompanyID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(and_(Plan.CompanyID == companyID, Plan.ID == id)).first()
        if not result:
            raise Exception

        return Callback(True,'Plan was successfully retrieved.', result)

    except Exception as exc:
        helpers.logError("plan_service.getByIDAndCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plan could not be retrieved.')


def getByNameAndCompanyID(name: str, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Plan).filter(and_(Plan.CompanyID == companyID, Plan.Name == name)).first()
        if not result:
            raise Exception

        return Callback(True,
                        'Plan was successfully retrieved.',
                        result)
    except Exception as exc:
        helpers.logError("plan_service.getByNameAndCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plan could not be retrieved.')


def removeAllByCompany(company: Company) -> Callback:
    try:
        db.session.query(Plan).filter(Plan.Company == company).delete()
        db.session.commit()
        return Callback(True, 'Plan has been removed successfully.')

    except Exception as exc:
        helpers.logError("plan_service.removeAllByCompany(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Plan could not be removed.')
