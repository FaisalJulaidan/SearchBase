from datetime import datetime, time
from pytz import timezone, utc

from models import db, Callback, Appointment, Conversation, Assistant,\
    AppointmentAllocationTime, AppointmentAllocationTimeInfo, Company
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, contains_eager
from utilities import helpers, enums
from services import mail_services, company_services
from services.Marketplace import marketplace_helpers
import json

def dummyCreateAppointmentAllocationTime(name, companyID: int):
    try:

        allocationTime= AppointmentAllocationTime(Name=name, CompanyID=companyID) # Create new AutoPilot

        # Create the AppointmentAllocationTime with default times info
        default = {"From": time(8,30), "To": time(12,0), "Duration": 30, "AppointmentAllocationTime": allocationTime, "Active": False}
        times = [
            AppointmentAllocationTimeInfo(Day=0, **default),  # Sunday
            AppointmentAllocationTimeInfo(Day=1, **default),
            AppointmentAllocationTimeInfo(Day=2, **default),
            AppointmentAllocationTimeInfo(Day=3, **default),
            AppointmentAllocationTimeInfo(Day=4, **default),
            AppointmentAllocationTimeInfo(Day=5, **default),
            AppointmentAllocationTimeInfo(Day=6, **default),  # Saturday
        ]
        db.session.add_all(times)
        db.session.commit()
        return Callback(True, "Created successfully.", allocationTime)

    except Exception as exc:
        helpers.logError("appointment_services.createAppointmentAllocationTime(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create a new Appointment Allocation Time.')

def saveAppointmentAllocationTime(companyID, ID, name, times, duration):
    try:
        appointmentAllocationTime = db.session.query(AppointmentAllocationTime)\
                                                .filter(and_(AppointmentAllocationTime.ID == ID,
                                                             AppointmentAllocationTime.CompanyID == companyID))\
                                                .first()


        appointmentAllocationTime.Name = name
        for day in appointmentAllocationTime.Info:
            for newDay in times:
                if newDay['Day'] == day.Day:
                    day.Active = newDay['Active']
                    day.From = newDay['From']
                    day.Duration = duration
                    day.To = newDay['To']
                    break

        db.session.commit()
        return Callback(True, "Timetable saved succesfully.", appointmentAllocationTime)

    except Exception as exc:
        helpers.logError("appointment_services.saveAppointmentAllocationTime(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create a new Appointment Allocation Time.')

def deleteAppointmentAllocationTime(companyID, ID):
    try:
        db.session.query(AppointmentAllocationTime) \
            .filter(and_(AppointmentAllocationTime.ID == ID,
                         AppointmentAllocationTime.CompanyID == companyID)) \
            .delete()
        db.session.commit()
        return Callback(True, 'Deleted Appointment Allocation Time.')
    except Exception as exc:
        helpers.logError("appointment_services.deleteAppointmentAllocationTime(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create a new Appointment Allocation Time.')

def createAppointmentAllocationTime(companyID, name, times, duration):
    try:

        appointmentAllocationTime = AppointmentAllocationTime(CompanyID=companyID, Name=name)

        db.session.add(appointmentAllocationTime)
        db.session.flush()

        toAdd = []

        appointmentAllocationTime.Name = name
        for newDay in times:
            day = AppointmentAllocationTimeInfo(AppointmentAllocationTimeID=appointmentAllocationTime.ID,
                                                Active=newDay['Active'],
                                                Day=newDay['Day'],
                                                Duration=duration,
                                                To=newDay['To'],
                                                From=newDay['From'])
            toAdd.append(day)

        db.session.add_all(toAdd)
        db.session.commit()
        db.session.flush()
        return Callback(True, "Timetable saved successfully.", appointmentAllocationTime)

    except Exception as exc:
        helpers.logError("appointment_services.createAppointmentAllocationTime(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not create a new Appointment Allocation Time.')

# Add new appointment selected through the appointment picker page
def addNewAppointment(conversationID, dateTime, userTimezone: str):
    try:

        conversation : Conversation = Conversation.query.get(conversationID)
        if not (datetime and userTimezone): raise Exception('Time picked and user timezone are required')
        if not conversation: raise Exception("Conversation does not exist anymore")

        db.session.add(
            Appointment(
                DateTime=datetime.strptime(dateTime, "%Y-%m-%d %H:%M"),
                UserTimeZone = userTimezone,
                ConversationID=conversationID,
                Status= enums.Status.Pending,
            )
        )

        db.session.commit()
        marketplace_helpers.sync(conversation.Assistant.CompanyID)
        return Callback(True, 'Appointment added successfully.')

    except Exception as exc:
        helpers.logError("assistant_services.addAppointment(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't add the appointment")

def generateEmailUrl(appointmentID):
    try:
        appointment = db.session.query(Appointment).filter(Appointment.ID == appointmentID).first()
        if appointment:
            if appointment.Status != enums.Status.Pending:
                raise Exception("Appointment status has already been set!")
            else:
                return helpers.verificationSigner.dumps({'id': appointmentID}, salt='verify-appointment')
    except Exception as exc:
        helpers.logError("appointment_services.generateEmailUrl(): " + str(exc))


def verifyRequest(token):
    try:
        verificationLink = helpers.verificationSigner.loads(token, salt='verify-appointment')
        appointment = db.session.query(Appointment.Status, Appointment.ID, Appointment.DateTime, Conversation.Data)\
            .join(Conversation).filter(Appointment.ID == verificationLink['id']).first()
        if appointment:
            appointment = helpers.getDictFromLimitedQuery(["Status", "ID", "DateTime", "Data"], appointment)
            if appointment['Status'] == 'Pending':
                return Callback(True, "Successfully gathered appointment data", appointment)
            else:
                return Callback(False, "Appointment status has already been set")
    except Exception as  exc:
        helpers.logError("appointment_services.verifyRequest(): " + str(exc))
        return Callback(False, "Could not gather appointment")

def setAppointmentStatusPublic(token, appointmentID, status):
    try:
        verificationLink = helpers.verificationSigner.loads(token, salt='verify-appointment')
        appointment = db.session.query(Appointment).join(Appointment.Conversation)\
                                            .join(Conversation.Assistant)\
                                            .join(Assistant.Company)\
                                            .filter(Appointment.ID == appointmentID).first()
        logoPath = helpers.keyFromStoredFile(appointment.Conversation.Assistant.Company.StoredFile, enums.FileAssetType.Logo).AbsFilePath

        marketplace_helpers.sync(company.ID)
        company: Company = appointment.Conversation.Assistant.Company
        
        if appointment.Status != enums.Status.Pending:
            return Callback(False, "Appointment status is {} and cannot be modified.".format(appointment.Status.value)) 

        appointment.Status = enums.Status[status]

        if status == enums.Status.Rejected.name:
            db.session.delete(appointment)

        db.session.commit()

        # When appointment is accepted
        if status == enums.Status.Accepted.name and appointment.Conversation.Email:
            email_callback: Callback = mail_services.sendAppointmentConfirmationEmail(
                appointment.Conversation.Name,
                appointment.Conversation.Email,
                utc.localize(appointment.DateTime).astimezone(timezone(appointment.UserTimeZone)),
                appointment.UserTimeZone,
                company.Name,
                logoPath
            )
            if not email_callback.Success:
                  email_callback
            return Callback(True, "The client has been informed about their application being {}.".format(appointment.Status.value))

        # When appointment is rejected


        db.session.commit()
        return Callback(True, "Appointment status has been set to {}.".format(appointment.Status.value))
        # TODO send confirmation email when appointment Accepted

    except Exception as exc:
        helpers.logError("appointment_services.setAppointmentStatusPublic(): " + str(exc))
        return Callback(False, 'Could not set appointment status.')

#appointmentID: int, status: str, companyID: int, name: str = None, email: str = None, phone: str = None
def setAppointmentStatus(req, companyID: int) -> Callback:
    try:
        resp: dict = helpers.validateRequest(req, {"appointmentID": {"type": int, "required": True},
                                            "status": {"type": str, "required": True},})

        company: Company = company_services.getByID(companyID).Data
        logoPath = helpers.keyFromStoredFile(company.StoredFile, enums.FileAssetType.Logo).AbsFilePath
        if not company: raise Exception("Company does not exist")
                                    
        appointment = db.session.query(Appointment).join(Appointment.Conversation)\
                                                    .join(Conversation.Assistant)\
                                                    .join(Assistant.Company)\
                                                    .filter(and_(Appointment.ID == resp['inputs']['appointmentID'], Company.ID == companyID)).first()

        marketplace_helpers.sync(company.ID)
                     
        if appointment is None:
            return Callback(False, "Either you do not own this appointment, or it does not exist!")
        
        if appointment.Status != enums.Status.Pending:
            return Callback(False, "Appointment status is {} and cannot be modified.".format(appointment.Status.value))


        appointment.Status = resp['inputs']['status']

        if resp['inputs']['status'] == enums.Status.Rejected.name:
            db.session.delete(appointment)
            
        db.session.commit()        


        # When appointment is accepted
        if resp['inputs']['status'] == enums.Status.Accepted.name and appointment.Conversation.Email:
            email_callback: Callback = mail_services.sendAppointmentConfirmationEmail(
                appointment.Conversation.Name,
                appointment.Conversation.Email,
                utc.localize(appointment.DateTime).astimezone(timezone(appointment.UserTimeZone)),
                appointment.UserTimeZone,
                company.Name,
                logoPath
            )
            if not email_callback.Success:
                  email_callback
            return Callback(True, "The client has been informed about their application being {}.".format(appointment.Status.value))

        # When appointment is rejected


        
        db.session.commit()
        return Callback(True, "Appointment status has been set to {}.".format(appointment.Status.value))
    except helpers.requestException as exc:
        helpers.logError("appointment_services.setAppointmentStatus(): " + str(exc))
        return Callback(False, str(exc))
    except Exception as exc:
        helpers.logError("appointment_services.setAppointmentStatus(): " + str(exc))
        return Callback(False, 'Could not set appointment status.')


def getAppointments(companyID):
    try:

        assistants = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
        appointments = []

        for assistant in assistants:
            for idx, appointment in enumerate(helpers.getListFromSQLAlchemyList(assistant.Appointments)):
                appointment['Conversation'] = helpers.getDictFromSQLAlchemyObj(assistant.Appointments[idx].Conversation)
                appointments.append(appointment)

        return Callback(True, 'Successfully gathered appointments.', appointments)

    except Exception as exc:
        helpers.logError("appointment_services.getAppointments(): " + str(exc))
        return Callback(False, 'Could not get appointments.')

def getAppointmentAllocationTimes(id) -> Callback:
    try:
        result = db.session.query(AppointmentAllocationTime) \
            .join(AppointmentAllocationTimeInfo) \
            .filter(AppointmentAllocationTime.CompanyID == id) \
            .all()
        return Callback(True, 'Gathered Appointment Allocation Times', result)
    except Exception as exc:
        # print(exc)
        return Callback(False, 'Failed to get any Appointment Allocation Times')

def hasAppointment(companyID, id):
    try:
        assistants = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
        valid = False
        for assistant in assistants:
            for idx, appointment in enumerate(helpers.getListFromSQLAlchemyList(assistant.Appointments)):
                appointment['Conversation'] = assistant.Appointments[idx].Conversation.Data
                if appointment['ID'] == id:
                    valid = True
                    break
                if valid:
                    break
        if not valid:
            raise Exception("You do not own this appointment")
        return Callback(True, 'You own this appointment')
    except Exception as exc:
        helpers.logError("appointment_services.getAppointments(): " + str(exc))
        return Callback(False, 'You do not have access to this appointment.')
