from datetime import datetime

from models import db, Callback, Conversation, AutoPilot, Assistant, Messenger, Company, CRMAutoPilot
from services import mail_services, stored_file_services as sfs
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.CRM import crm_services
from sqlalchemy import and_
from utilities import helpers, enums
from utilities.enums import UserType, Status


def create(name, desc, crmType, companyID: int) -> Callback:
    try:

        crmEnum : enums.CRM = enums.CRM.get_value(crmType)

        if crmEnum is None:
          raise Exception("Trying to use unknown CRM")

        crm = crm_services.getCRMByType(crmEnum, companyID)

        if crm is None:
          raise Exception("You are not connected to {}".format(crmEnum.value))

        crmAutoPilot = CRMAutoPilot(Name=name, Description=desc, CRMID=crm.ID, companyID=companyID)
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

def updateConfigs(id, name, desc, active, referralAssistantID, referralEmailTitle, referralEmailBody, referralSMSBody, sendReferralEmail, sendReferralSMS, companyID: int) -> Callback:
    try:

        # Get AutoPilot
        crmAutopilot_callback: Callback = getByID(id, companyID)
        if not crmAutopilot_callback.Success: return crmAutopilot_callback
        crmAutopilot : CRMAutoPilot = crmAutopilot_callback.Data

        # Update the autoPilot
        crmAutopilot.Name = name
        crmAutopilot.Description = desc
        crmAutopilot.Active = active
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

# def updateStatus(autoPilotID, newStatus, companyID):
#     try:

#         if not newStatus: raise Exception("Please provide the new status true/false")
#         db.session.query(AutoPilot).filter(and_(AutoPilot.ID == autoPilotID, AutoPilot.CompanyID == companyID)) \
#             .update({"Active": newStatus})

#         db.session.commit()
#         return Callback(True, 'AutoPilot status has been changed.')

#     except Exception as exc:
#         helpers.logError("auto_pilot.changeStatus(): " + str(exc))
#         db.session.rollback()
#         return Callback(False, "Could not change the AutoPilot's status.")


# def removeByID(id, companyID):
#     try:
#         db.session.query(AutoPilot).filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID)).delete()
#         db.session.commit()
#         return Callback(True, 'AutoPilot has been deleted.')

#     except Exception as exc:
#         helpers.logError("auto_pilot.removeByID(): " + str(exc))
#         db.session.rollback()
#         return Callback(False, 'Error in deleting AutoPilot.')


# # ----- Private Functions (shouldn't be accessed from the outside) ----- #

# def __getApplicationResult(score, autoPilot: AutoPilot) -> Status:
#     if autoPilot.AcceptApplications and (score >= autoPilot.AcceptanceScore):
#         return Status.Accepted
#     if autoPilot.RejectApplications and (score < autoPilot.RejectionScore):
#         return Status.Rejected
#     return Status.Pending
