from sqlalchemy import and_
from models import db, Callback, AutoPilot, OpenTimeSlot, Conversation
from datetime import datetime, time
import logging
from utilities import helpers
from services import mail_services, stored_file_services as sfs
from enums import UserType, DataType, ApplicationStatus
import os


def processConversation(conversation: Conversation, autoPilot: AutoPilot):
    try:
        result = {
            "applicationStatus": ApplicationStatus.Pending,
            "appointmentEmailSentAt": None,
            "acceptanceEmailSentAt": None,
            # "response": None
        }

        # Do automation only if the autoPilot is active
        if autoPilot.Active:
            keywords = conversation.Data.get('keywordsByDataType')
            email = keywords.get(DataType.CandidateEmail.value['name'], [""])[0]

            # Get application status
            result['applicationStatus'] = __getApplicationResult(conversation.Score, autoPilot)

            # Process appointment email if score is accepted
            # result['appointmentEmailSentAt'] = __sendAppointmentEmail(conversation, autoPilot)

            # Process acceptance email if score is accepted
            if conversation.UserType is UserType.Candidate and result['applicationStatus'] is ApplicationStatus.Accepted and email:
                email_callback: Callback = __sendAcceptanceLetterEmail(
                    email,
                    " ".join(keywords.get(DataType.CandidateName.value['name'], [""])),
                    autoPilot.Company.Name,
                    conversation.Assistant.LogoName
                )

                if email_callback.Success:
                    result['acceptanceEmailSentAt'] = datetime.now()

        return Callback(True, "Automation done via " + autoPilot.Name + " pilot successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.processConversation(): " + str(exc))
        return Callback(False,
                        autoPilot.Name + " pilot failed to function. Please contact TSB support and let them know",
                        None)


# The new AutoPilot will be returned parsed
def create(name, desc, companyID: int) -> Callback:
    try:

        autoPilot= AutoPilot(Name=name, CompanyID=companyID) # Create new AutoPilot

        # Create the AutoPilot with default open time slots
        default = {"From": time(8,30), "To": time(12,0), "Duration": 30, "AutoPilot": autoPilot, "Active": False}
        openTimeSlots = [OpenTimeSlot(Day=0, **default), # Monday
                         OpenTimeSlot(Day=1, **default),
                         OpenTimeSlot(Day=2, **default),
                         OpenTimeSlot(Day=3, **default),
                         OpenTimeSlot(Day=4, **default),
                         OpenTimeSlot(Day=5, **default),
                         OpenTimeSlot(Day=6, **default), # Sunday
                         ]
        db.session.add_all(openTimeSlots)
        db.session.commit()
        return Callback(True, "Got AutoPilot successfully.", __parseAutoPilot(autoPilot))

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.create(): " + str(exc))
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
        print(exc)
        logging.error("auto_pilot.getByID(): " + str(exc))
        return Callback(False, 'Could not get the AutoPilot.')

# AutoPilots will be returned parsed
def fetchAll(companyID) -> Callback:
    try:

        result: list = []
        for autoPilot in db.session.query(AutoPilot).filter(AutoPilot.CompanyID == companyID).all():
            result.append(__parseAutoPilot(autoPilot))

        return Callback(True, "Fetched all AutoPilots successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.fetchAll(): " + str(exc))
        return Callback(False, 'Could not fetch all the AutoPilots.')


# ----- Updaters ----- #
def update(id, name, desc, active, acceptApplications, acceptanceScore, rejectApplications,
           rejectionScore, SendCandidatesAppointments, companyID: int) -> Callback:
    try:

        # TODO OpenTimeSlots & Appointments Feature
        # Check all OpenTimeSlots are given
        # if len(openTimeSlots) != 7: raise Exception("Number of open time slots should be 7")

        # Get AutoPilot
        autoPilot_callback: Callback = getByID(id, companyID)
        if not autoPilot_callback.Success: return autoPilot_callback
        autoPilot = autoPilot_callback.Data

        # Update the autoPilot
        autoPilot.Name = name
        autoPilot.Name = name
        autoPilot.Active = active
        autoPilot.AcceptApplication = acceptApplications
        autoPilot.AcceptanceScore = acceptanceScore
        autoPilot.RejectApplications = rejectApplications
        autoPilot.RejectionScore = rejectionScore
        autoPilot.SendCandidatesAppointments = SendCandidatesAppointments

        # TODO OpenTimeSlots & Appointments Feature
        # Update the openTimeSlots
        # for (oldSlot, newSlot) in zip(AutoPilot.OpenTimeSlots, openTimeSlots):
        #     if oldSlot.Day == newSlot['day']:
        #         oldSlot.Active = newSlot['active']
        #         oldSlot.From = time(newSlot['from'][0], newSlot['from'][1])
        #         oldSlot.To = time(newSlot['to'][0], newSlot['to'][1])
        #         oldSlot.Duration = newSlot['duration']

        # Save all changes
        db.session.commit()
        return Callback(True, "Updated the AutoPilot successfully.", autoPilot)

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.update(): " + str(exc))
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
        print("Error in auto_pilot.changeStatus(): ", exc)
        logging.error("auto_pilot.changeStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the AutoPilot's status.")


def removeByID(id, companyID):
    try:
        db.session.query(AutoPilot).filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'AutoPilot has been deleted.')

    except Exception as exc:
        print("Error in auto_pilot.removeByID(): ", exc)
        logging.error("auto_pilot.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting AutoPilot.')


# ----- Private Functions (shouldn't be accessed from the outside) ----- #
# It takes an autoPilot object and join all its children tables into one dict
def __parseAutoPilot(autoPilot: AutoPilot) -> dict:
    return {
        **helpers.getDictFromSQLAlchemyObj(autoPilot),
        "OpenTimeSlots": helpers.getListFromSQLAlchemyList(autoPilot.OpenTimeSlots)
    }


def __getApplicationResult(score, autoPilot: AutoPilot) -> ApplicationStatus:
    result = ApplicationStatus.Pending
    if autoPilot.AcceptApplications and (score > autoPilot.AcceptanceScore):
        result = ApplicationStatus.Accepted
    if autoPilot.RejectApplications and (score < autoPilot.RejectionScore):
        result = ApplicationStatus.Rejected
    return result


def __sendAcceptanceLetterEmail(receiverEmail, userName, companyName, logoPath) -> Callback:
    return mail_services.send_email(receiverEmail, 'Acceptance Letter', '/emails/acceptance_letter.html',
                             companyName=companyName, logoPath=logoPath, userName=userName)


def __sendAppointmentEmail(conversation: Conversation, autoPilot):
    return None