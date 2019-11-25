from datetime import datetime

from models import db, Callback, Conversation, AutoPilot, Assistant, Messenger, Company
from services import mail_services, stored_file_services as sfs
from services.Marketplace.Messenger import messenger_servicess
from sqlalchemy import and_
from utilities import helpers, enums
from utilities.enums import UserType, Status


def processConversation(conversation: Conversation, autoPilot: AutoPilot, assistant: Assistant):
    try:
        result = {
            "applicationStatus": Status.Pending,
            "appointmentEmailSentAt": None,
            "acceptanceEmailSentAt": None,
            "acceptanceSMSSentAt": None,
            "rejectionEmailSentAt": None,
            "rejectionSMSSentAt": None,
            # "response": None
        }

        # Do automation only if the autoPilot is active
        if not autoPilot.Active:
            return Callback(True, autoPilot.Name + " was not active.", result)

        email = conversation.Email
        phone = conversation.PhoneNumber

        def __processSendingEmails(email, status: Status, autoPilot: AutoPilot):
            company: Company = autoPilot.Company
            companyName = company.Name
            userName = conversation.Name or 'Anonymous'
            logoPath = helpers.keyFromStoredFile(company.StoredFile, enums.FileAssetType.Logo).AbsFilePath

            # ======================
            # Send Acceptance Letters
            if status is Status.Accepted:

                # Process candidates Appointment email only if score is accepted
                if autoPilot.SendCandidatesAppointments:

                    appointments_email_callback: Callback = \
                        mail_services.sendAppointmentsPicker(
                            email,
                            userName,
                            logoPath,
                            conversation.ID,
                            assistant.ID,
                            companyName,
                            autoPilot.CompanyID)

                    if appointments_email_callback.Success:
                        result['appointmentEmailSentAt'] = datetime.now()

                elif autoPilot.SendAcceptanceEmail:
                    # Process candidates Acceptance email
                    emailTitle = autoPilot.AcceptanceEmailTitle \
                        .replace("${candidateName}$", userName) \
                        .replace("${candidateEmail}$", email)
                    emailBody = autoPilot.AcceptanceEmailBody \
                        .replace("${candidateName}$", userName) \
                        .replace("${candidateEmail}$", email)

                    acceptance_email_callback: Callback = \
                        mail_services.sendAcceptanceEmail(emailTitle, emailBody, userName, email, logoPath, companyName)

                    if acceptance_email_callback.Success:
                        result['acceptanceEmailSentAt'] = datetime.now()


            # ======================
            # Send Rejection Letters
            elif status is Status.Rejected and autoPilot.SendRejectionEmail:

                emailTitle = autoPilot.RejectionEmailTitle \
                    .replace("${candidateName}$", userName) \
                    .replace("${candidateEmail}$", email)
                emailBody = autoPilot.RejectionEmailBody \
                    .replace("${candidateName}$", userName) \
                    .replace("${candidateEmail}$", email)

                rejection_email_callback: Callback = \
                    mail_services.sendRejectionEmail(emailTitle, emailBody, userName, email, logoPath, companyName)

                if rejection_email_callback.Success:
                    result['rejectionEmailSentAt'] = datetime.now()

        def __processSendingSMS(phone, status: Status, autoPilot: AutoPilot):

            messenger: Messenger = assistant.Messenger
            userName = conversation.Name or '[Candidate.Name]'
            # companyName = autoPilot.Company.Name

            # ======================
            # Send Acceptance Letters
            if status is Status.Accepted and autoPilot.SendAcceptanceSMS:
                # Process candidates Acceptance sms
                SMSBody = autoPilot.AcceptanceSMSBody \
                    .replace("${candidateName}$", userName) \
                    .replace("${candidateEmail}$", email or "${candidateEmail}$") \
                    .replace("&nbsp;", "\n")

                acceptance_SMS_callback: Callback = \
                    messenger_servicess.sendMessage(messenger.Type, phone, SMSBody, messenger.Auth)

                if acceptance_SMS_callback.Success:
                    result['acceptanceSMSSentAt'] = datetime.now()

            # ======================
            # Send Rejection Letters SMS
            elif status is Status.Rejected and autoPilot.SendRejectionSMS:

                SMSBody = autoPilot.RejectionSMSBody \
                    .replace("${candidateName}$", userName) \
                    .replace("${candidateEmail}$", email or "${candidateEmail}$") \
                    .replace("&nbsp;", "\n")

                rejection_SMS_callback: Callback = \
                    messenger_servicess.sendMessage(messenger.Type, phone, SMSBody, messenger.Auth)

                if rejection_SMS_callback.Success:
                    result['rejectionSMSSentAt'] = datetime.now()

        # Get application status
        result['applicationStatus'] = __getApplicationResult(conversation.Score, autoPilot)

        # Send candidates emails
        if conversation.UserType is UserType.Candidate:
            if email:
                __processSendingEmails(email, result['applicationStatus'], autoPilot)
            if phone and assistant.MessengerID:
                __processSendingSMS(phone, result['applicationStatus'], autoPilot)

        return Callback(True, "Automation done via " + autoPilot.Name + " pilot successfully.", result)

    except Exception as exc:
        helpers.logError("auto_pilot.processConversation(): " + str(exc))
        return Callback(False,
                        autoPilot.Name + " pilot failed to function. Please contact TSB support and let them know",
                        None)


# The new AutoPilot will be returned parsed
def create(name, desc, companyID: int) -> Callback:
    try:
        autoPilot = AutoPilot(Name=name,
                              Description=desc,
                              CompanyID=companyID,
                              AcceptanceEmailTitle="Acceptance Letter",
                              AcceptanceEmailBody="<h2>Hello ${candidateName}$,</h2><p>We are happy to announce that your application has been accepted based on your responses and we will get back to you very soon.</p><p>Regards,</p>",
                              AcceptanceSMSBody="Hello ${candidateName}$,\n\nWe are happy to announce that your application has been accepted based on your responses and we will get back to you very soon.\n\nRegard,",
                              RejectionEmailTitle="Rejection Letter",
                              RejectionEmailBody="<h2>Hello ${candidateName}$,</h2><p>Unfortunately, we are very sorry to announce that your application has been rejected based on your responses.<br><br>Please feel free to visit our website and explore other opportunities that you feel may be better suited.<br>&nbsp;</p><p>Regards,</p>",
                              RejectionSMSBody="Hello ${candidateName}$,\n\nUnfortunately, we are very sorry to announce that your application has been rejected based on your responses.Please feel free to visit our website and explore other opportunities that you feel may be better suited.\n\nRegards,",
                              )
        db.session.add(autoPilot)
        db.session.commit()
        return Callback(True, "Got AutoPilot successfully.", autoPilot)

    except Exception as exc:
        helpers.logError("auto_pilot_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create AutoPilot.')


# ----- Getters ----- #
def getByID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result: AutoPilot = db.session.query(AutoPilot) \
            .filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got AutoPilot successfully.", result)

    except Exception as exc:
        helpers.logError("auto_pilot_services.getByID(): " + str(exc))
        return Callback(False, 'Could not get the AutoPilot.')


# Get the list of autoPilots
def fetchAll(companyID) -> Callback:
    try:

        result = db.session.query(AutoPilot).filter(AutoPilot.CompanyID == companyID).all()
        return Callback(True, "Fetched all AutoPilots successfully.", result)

    except Exception as exc:
        helpers.logError("auto_pilot_services.fetchAll(): " + str(exc))
        return Callback(False, 'Could not fetch all the AutoPilots.')


# Add openTimes to the autoPilot object after parsing it
def parseAutoPilot(autoPilot: AutoPilot) -> dict:
    return {
        **helpers.getDictFromSQLAlchemyObj(autoPilot),
        "AppointmentAllocationTime": helpers.getDictFromSQLAlchemyObj(autoPilot.AppointmentAllocationTime)
    }


# ----- Updaters ----- #
def update(id, name, desc, companyID: int) -> Callback:
    try:

        # Get AutoPilot
        autoPilot_callback: Callback = getByID(id, companyID)
        if not autoPilot_callback.Success: return autoPilot_callback
        autoPilot = autoPilot_callback.Data

        # Update the autoPilot
        autoPilot.Name = name
        autoPilot.Description = desc

        # Save all changes
        db.session.commit()
        return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

    except Exception as exc:
        helpers.logError("auto_pilot.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't update the AutoPilot.")


def updateConfigs(id, name, desc, active, acceptApplications, acceptanceScore, sendAcceptanceEmail,
                  acceptanceEmailTitle,
                  acceptanceEmailBody, sendAcceptanceSMS, acceptanceSMSBody, rejectApplications, rejectionScore,
                  sendRejectionEmail, rejectionEmailTitle, rejectionEmailBody, sendRejectionSMS, rejectionSMSBody,
                  sendCandidatesAppointments, appointmentAllocationTimes, companyID: int) -> Callback:
    try:

        # Get AutoPilot
        autoPilot_callback: Callback = getByID(id, companyID)
        if not autoPilot_callback.Success: return autoPilot_callback
        autoPilot = autoPilot_callback.Data

        # Update the autoPilot
        autoPilot.Name = name
        autoPilot.Description = desc
        autoPilot.Active = active

        autoPilot.AcceptApplications = acceptApplications
        autoPilot.AcceptanceScore = acceptanceScore
        autoPilot.SendAcceptanceEmail = sendAcceptanceEmail
        autoPilot.AcceptanceEmailTitle = acceptanceEmailTitle
        autoPilot.AcceptanceEmailBody = acceptanceEmailBody
        autoPilot.SendAcceptanceSMS = sendAcceptanceSMS
        autoPilot.AcceptanceSMSBody = acceptanceSMSBody

        autoPilot.AppointmentAllocationTimeID = appointmentAllocationTimes

        autoPilot.RejectApplications = rejectApplications
        autoPilot.RejectionScore = rejectionScore
        autoPilot.SendRejectionEmail = sendRejectionEmail
        autoPilot.RejectionEmailTitle = rejectionEmailTitle
        autoPilot.RejectionEmailBody = rejectionEmailBody
        autoPilot.SendRejectionSMS = sendRejectionSMS
        autoPilot.RejectionSMSBody = rejectionSMSBody

        autoPilot.SendCandidatesAppointments = sendCandidatesAppointments

        # Save all changes

        db.session.commit()
        return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

    except Exception as exc:
        helpers.logError("auto_pilot.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not update the AutoPilot.')


def updateStatus(autoPilotID, newStatus, companyID):
    try:

        if newStatus is None: raise Exception("Please provide the new status true/false")
        db.session.query(AutoPilot).filter(and_(AutoPilot.ID == autoPilotID, AutoPilot.CompanyID == companyID)) \
            .update({"Active": newStatus})

        db.session.commit()
        return Callback(True, 'AutoPilot status has been changed.')

    except Exception as exc:
        helpers.logError("auto_pilot.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the AutoPilot's status.")


def removeByID(id, companyID):
    try:
        db.session.query(AutoPilot).filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'AutoPilot has been deleted.')

    except Exception as exc:
        helpers.logError("auto_pilot.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting AutoPilot.')


# ----- Private Functions (shouldn't be accessed from the outside) ----- #

def __getApplicationResult(score, autoPilot: AutoPilot) -> Status:
    if autoPilot.AcceptApplications and (score >= autoPilot.AcceptanceScore):
        return Status.Accepted
    if autoPilot.RejectApplications and (score < autoPilot.RejectionScore):
        return Status.Rejected
    return Status.Pending
