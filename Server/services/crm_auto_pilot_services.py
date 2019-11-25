from datetime import datetime

from models import db, Callback, Conversation, AutoPilot, Assistant, Messenger, Company, CRMAutoPilot
from services import mail_services, stored_file_services as sfs
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.CRM import crm_services
from sqlalchemy import and_
from utilities import helpers, enums
from utilities.helpers import APIException
from utilities.enums import UserType, Status


def create(name, desc, companyID: int) -> Callback:
    try:

        crmAutoPilot = CRMAutoPilot(Name=name, Description=desc, CompanyID=companyID)
        db.session.add(crmAutoPilot)
        db.session.commit()
        return Callback(True, "Created CRMAutoPilot succesfully", crmAutoPilot)
    except Exception as exc:
        helpers.logError("crm_auto_pilot_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create CRMAutoPilot.')


# ----- Getters ----- #
def getByID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result: CRMAutoPilot = db.session.query(CRMAutoPilot) \
            .filter(and_(CRMAutoPilot.ID == id, CRMAutoPilot.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got CRMAutoPilot successfully.", result)

    except Exception as exc:
        helpers.logError("crm_auto_pilot_services.getByID(): " + str(exc))
        return Callback(False, 'Could not get the CRMAutoPilot.')


# Get the list of autoPilots
def fetchAll(companyID) -> Callback:
    try:

        result = db.session.query(CRMAutoPilot).filter(CRMAutoPilot.CompanyID == companyID).all()
        return Callback(True, "Fetched all CRMAutoPilots successfully.", result)

    except Exception as exc:
        helpers.logError("crm_auto_pilot_services.fetchAll(): " + str(exc))
        return Callback(False, 'Could not fetch all the AutoPilots.')

# ----- Updaters ----- #
def update(id, name, desc, companyID: int) -> Callback:
    try:

        # Get AutoPilot
        crm_autoPilot_callback: Callback = getByID(id, companyID)
        if not crm_autoPilot_callback.Success: return crm_autoPilot_callback
        crm_autoPilot = crm_autoPilot_callback.Data

        # Update the autoPilot
        crm_autoPilot.Name = name
        crm_autoPilot.Description = desc

        # Save all changes
        db.session.commit()
        return Callback(True, "Updated the AutoPilot successfully.", crm_autoPilot)

    except Exception as exc:
        helpers.logError("crm_auto_pilot_services.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't update the AutoPilot.")

def updateConfigs(id, name, desc, referralAssistantID, referralEmailTitle, referralEmailBody, referralSMSBody, sendReferralEmail, sendReferralSMS, companyID: int) -> Callback:
    try:

        # Get AutoPilot
        crmAutopilot_callback: Callback = getByID(id, companyID)
        if not crmAutopilot_callback.Success: return crmAutopilot_callback
        crmAutopilot : CRMAutoPilot = crmAutopilot_callback.Data

        # Update the autoPilot
        crmAutopilot.Name = name
        crmAutopilot.Description = desc
        crmAutopilot.LastReferral = datetime.now() if referralAssistantID else None

        crmAutopilot.SendReferralEmail = sendReferralEmail
        crmAutopilot.ReferralEmailTitle = referralEmailTitle
        crmAutopilot.ReferralEmailBody = referralEmailBody

        crmAutopilot.SendReferralSMS = sendReferralSMS
        crmAutopilot.ReferralSMSBody = referralSMSBody
        
        # crmAutopilot.CRMID = 1
        
        crmAutopilot.ReferralAssistantID = referralAssistantID


        # Save all changes

        db.session.commit()
        return Callback(True, "Updated the CRM AutoPilot successfully.", crmAutopilot)

    except Exception as exc:
        helpers.logError("crm_auto_pilot_services.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not update the AutoPilot.')

def updateStatus(autoPilotID, newStatus, companyID):
    try:

        if newStatus is None: raise Exception("Please provide the new status true/false")
        db.session.query(CRMAutoPilot).filter(and_(CRMAutoPilot.ID == autoPilotID, CRMAutoPilot.CompanyID == companyID)) \
            .update({"Active": newStatus})

        db.session.commit()
        return Callback(True, 'CRM AutoPilot status has been changed.')

    except Exception as exc:
        helpers.logError("auto_pilot.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the CRM  AutoPilot's status.")


def removeByID(id, companyID):
    try:
        db.session.query(CRMAutoPilot).filter(and_(CRMAutoPilot.ID == id, CRMAutoPilot.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'CRMAutoPilot has been deleted.')

    except Exception as exc:
        helpers.logError("crm_auto_pilot.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting CRMAutoPilot.')


# # ----- Private Functions (shouldn't be accessed from the outside) ----- #

# def __getApplicationResult(score, autoPilot: AutoPilot) -> Status:
#     if autoPilot.AcceptApplications and (score >= autoPilot.AcceptanceScore):
#         return Status.Accepted
#     if autoPilot.RejectApplications and (score < autoPilot.RejectionScore):
#         return Status.Rejected
#     return Status.Pending
