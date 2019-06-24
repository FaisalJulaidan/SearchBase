from sqlalchemy import and_
from models import db, Callback, AutoPilot, OpenTimes, Conversation
from datetime import datetime, time
import logging
from utilities import helpers
from services import mail_services, stored_file_services as sfs
from enums import UserType, DataType, ApplicationStatus


def processConversation(conversation: Conversation, autoPilot: AutoPilot):
    try:
        result = {
            "applicationStatus": ApplicationStatus.Pending,
            "appointmentEmailSentAt": None,
            "acceptanceEmailSentAt": None,
            "rejectionEmailSentAt": None,
            # "response": None
        }

        # Do automation only if the autoPilot is active
        if autoPilot.Active:
            keywords = conversation.Data.get('keywordsByDataType')
            email = keywords.get(DataType.CandidateEmail.value['name'], [""])[0]

            def __processSendingEmails (email, status: ApplicationStatus, autoPilot: AutoPilot):

                userName = " ".join(keywords.get(DataType.CandidateName.value['name'], [""])) # get candidate name
                logoPath = sfs.PUBLIC_URL + sfs.UPLOAD_FOLDER + sfs.COMPANY_LOGOS_PATH + "/" + autoPilot.Company.LogoPath
                companyName = autoPilot.Company.Name

                # Send Acceptance Letters
                if status is ApplicationStatus.Accepted and AutoPilot.SendAcceptanceEmail:

                    acceptance_callback: Callback = \
                        mail_services.sendAcceptanceEmail(userName, email, logoPath, companyName)

                    if acceptance_callback.Success:
                        result['acceptanceEmailSentAt'] = datetime.now()

                    # Process candidates appointment email only if score is accepted
                    if AutoPilot.SendCandidatesAppointments:

                        appointments_callback: Callback = \
                            mail_services.sendAppointmentsPicker(
                                email,
                                userName,
                                logoPath,
                                conversation.ID,
                                conversation.Assistant.ID,
                                companyName,
                                autoPilot.CompanyID)

                        if appointments_callback.Success:
                            result['appointmentEmailSentAt'] = datetime.now()


                # Send Rejection Letters
                elif status is ApplicationStatus.Rejected and AutoPilot.SendRejectionEmail:

                    rejection_callback: Callback = \
                        mail_services.sendRejectionEmail(userName, email, logoPath, companyName)

                    if rejection_callback.Success:
                        result['rejectionEmailSentAt'] = datetime.now()


            # Get application status
            result['applicationStatus'] = __getApplicationResult(conversation.Score, autoPilot)

            # Send candidates emails
            if email and conversation.UserType is UserType.Candidate:
                __processSendingEmails(email, result['applicationStatus'], autoPilot)


        return Callback(True, "Automation done via " + autoPilot.Name + " pilot successfully.", result)

    except Exception as exc:
        helpers.logError("auto_pilot.processConversation(): " + str(exc))
        return Callback(False,
                        autoPilot.Name + " pilot failed to function. Please contact TSB support and let them know",
                        None)


# The new AutoPilot will be returned parsed
def create(name, desc, companyID: int) -> Callback:
    try:

        autoPilot= AutoPilot(Name=name, Description=desc, CompanyID=companyID) # Create new AutoPilot

        # Create the AutoPilot with default open time slots
        default = {"From": time(8,30), "To": time(12,0), "Duration": 30, "AutoPilot": autoPilot, "Active": False}
        openTimes = [OpenTimes(Day=0, **default),  # Sunday
                     OpenTimes(Day=1, **default),
                     OpenTimes(Day=2, **default),
                     OpenTimes(Day=3, **default),
                     OpenTimes(Day=4, **default),
                     OpenTimes(Day=5, **default),
                     OpenTimes(Day=6, **default),  # Saturday
                     ]
        db.session.add_all(openTimes)
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
        "OpenTimes": helpers.getListFromSQLAlchemyList(autoPilot.OpenTimes)
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


def updateConfigs(id, name, desc, active, acceptApplications, acceptanceScore, sendAcceptanceEmail, rejectApplications,
                  rejectionScore, sendRejectionEmail, SendCandidatesAppointments, openTimes, companyID: int) -> Callback:
    try:

        # Check all OpenTimes are given
        if len(openTimes) != 7: raise Exception("Number of open time slots should be 7")

        # Get AutoPilot
        autoPilot_callback: Callback = getByID(id, companyID)
        if not autoPilot_callback.Success: return autoPilot_callback
        autoPilot = autoPilot_callback.Data
        autoPilot_temp = autoPilot_callback.Data

        # Update the autoPilot
        autoPilot.Name = name
        autoPilot.Description = desc
        autoPilot.Active = active
        autoPilot.AcceptApplications = acceptApplications
        autoPilot.AcceptanceScore = acceptanceScore
        autoPilot.SendAcceptanceEmail = sendAcceptanceEmail

        autoPilot.RejectApplications = rejectApplications
        autoPilot.RejectionScore = rejectionScore
        autoPilot.SendRejectionEmail = sendRejectionEmail

        autoPilot.SendCandidatesAppointments = SendCandidatesAppointments

        # Update the openTimes
        for (oldSlot, newSlot) in zip(autoPilot_temp.OpenTimes, openTimes):
            if oldSlot.Day == newSlot['day']:
                oldSlot.Active = newSlot['active']
                oldSlot.From = time(newSlot['from'][0], newSlot['from'][1])
                oldSlot.To = time(newSlot['to'][0], newSlot['to'][1])
                oldSlot.Duration = newSlot['duration']

        # Save all changes
        db.session.commit()
        return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

    except Exception as exc:
        helpers.logError("auto_pilot.update(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could update the AutoPilot.')

def updateStatus(autoPilotID, newStatus, companyID):
    try:

        if not newStatus: raise Exception("Please provide the new status true/false")
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

def __getApplicationResult(score, autoPilot: AutoPilot) -> ApplicationStatus:
    result = ApplicationStatus.Pending
    if autoPilot.AcceptApplications and (score > autoPilot.AcceptanceScore):
        result = ApplicationStatus.Accepted
    if autoPilot.RejectApplications and (score < autoPilot.RejectionScore):
        result = ApplicationStatus.Rejected
    return result


def __sendAppointmentEmail(conversation: Conversation, autoPilot):
    return None
