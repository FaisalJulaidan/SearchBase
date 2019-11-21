from datetime import datetime

from models import db, Callback, Conversation, AutoPilot, Assistant, Messenger, Company, CRMAutoPilot
from services import mail_services, stored_file_services as sfs
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.CRM import crm_services
from sqlalchemy import and_
from utilities import helpers, enums
from utilities.enums import UserType, Status


# from models import db
# class CRMAutopilot(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
#     Name = db.Column(db.String(128), nullable=False)
#     Description = db.Column(db.String(260), nullable=True)
#     Active = db.Column(db.Boolean, nullable=False, default=True)

#     LastReferral = db.Column(db.DateTime(), default=None)

#     CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID', ondelete='cascade'), nullable=False)
#     CRM = db.relationship('CRM', back_populates='CRMAutopilot')

#     # Relationships:
#     CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
#     Company = db.relationship('Company', back_populates='CRMAutoPilots')

#     # Constraints:
#     # cannot have two auto pilot with the same name under one company
#     __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_crm_auto_pilot'),)

#     def __repr__(self):
#         return '<CRMAutopilot {}>'.format(self.ID)


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

# # ----- Updaters ----- #
# def update(id, name, desc, companyID: int) -> Callback:
#     try:

#         # Get AutoPilot
#         autoPilot_callback: Callback = getByID(id, companyID)
#         if not autoPilot_callback.Success: return autoPilot_callback
#         autoPilot = autoPilot_callback.Data

#         # Update the autoPilot
#         autoPilot.Name = name
#         autoPilot.Description = desc

#         # Save all changes
#         db.session.commit()
#         return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

#     except Exception as exc:
#         helpers.logError("auto_pilot.update(): " + str(exc))
#         db.session.rollback()
#         return Callback(False, "Couldn't update the AutoPilot.")


# def updateConfigs(id, name, desc, active, acceptApplications, acceptanceScore, sendAcceptanceEmail,
#                   acceptanceEmailTitle,
#                   acceptanceEmailBody, sendAcceptanceSMS, acceptanceSMSBody, rejectApplications, rejectionScore,
#                   sendRejectionEmail, rejectionEmailTitle, rejectionEmailBody, sendRejectionSMS, rejectionSMSBody,
#                   sendCandidatesAppointments, appointmentAllocationTimes, companyID: int) -> Callback:
#     try:

#         # Get AutoPilot
#         autoPilot_callback: Callback = getByID(id, companyID)
#         if not autoPilot_callback.Success: return autoPilot_callback
#         autoPilot = autoPilot_callback.Data

#         # Update the autoPilot
#         autoPilot.Name = name
#         autoPilot.Description = desc
#         autoPilot.Active = active

#         autoPilot.AcceptApplications = acceptApplications
#         autoPilot.AcceptanceScore = acceptanceScore
#         autoPilot.SendAcceptanceEmail = sendAcceptanceEmail
#         autoPilot.AcceptanceEmailTitle = acceptanceEmailTitle
#         autoPilot.AcceptanceEmailBody = acceptanceEmailBody
#         autoPilot.SendAcceptanceSMS = sendAcceptanceSMS
#         autoPilot.AcceptanceSMSBody = acceptanceSMSBody

#         autoPilot.AppointmentAllocationTimeID = appointmentAllocationTimes

#         autoPilot.RejectApplications = rejectApplications
#         autoPilot.RejectionScore = rejectionScore
#         autoPilot.SendRejectionEmail = sendRejectionEmail
#         autoPilot.RejectionEmailTitle = rejectionEmailTitle
#         autoPilot.RejectionEmailBody = rejectionEmailBody
#         autoPilot.SendRejectionSMS = sendRejectionSMS
#         autoPilot.RejectionSMSBody = rejectionSMSBody

#         autoPilot.SendCandidatesAppointments = sendCandidatesAppointments

#         # Save all changes

#         db.session.commit()
#         return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

#     except Exception as exc:
#         helpers.logError("auto_pilot.update(): " + str(exc))
#         db.session.rollback()
#         return Callback(False, 'Could not update the AutoPilot.')


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
