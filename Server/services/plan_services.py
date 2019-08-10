from models import Callback, db, Company
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




# Need to add setters and getters