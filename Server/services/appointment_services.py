from datetime import datetime, time

from models import db, Callback, Appointment, Conversation, Assistant,\
    AppointmentAllocationTime, AppointmentAllocationTimeInfo
from utilities import helpers, enums

def createAppointmentAllocationTime(name, companyID: int):
    try:

        allocationTime= AppointmentAllocationTime(Name=name, CompanyID=companyID) # Create new AutoPilot

        # Create the AppointmentAllocationTime with default times info
        default = {"From": time(8,30), "To": time(12,0), "Duration": 30, "AppointmentAllocationTime": allocationTime, "Active": False}
        times = [AppointmentAllocationTimeInfo(Day=0, **default),  # Sunday
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

def addNewAppointment(conversationID, dateTime):
    try:
        if not datetime: raise Exception('Time slot (datetime) is required')

        if not Conversation.query.get(conversationID): raise Exception("Conversation does not exist anymore")

        db.session.add(
            Appointment(
                DateTime=datetime.strptime(dateTime, "%Y-%m-%d %H:%M"),  # 2019-06-23 16:04
                ConversationID=conversationID,
                Status= enums.Status.Pending
            )
        )

        db.session.commit()
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
        appointment = db.session.query(Appointment).filter(Appointment.ID == appointmentID).first()
        if appointment.Status != enums.Status.Pending:
            return Callback(False, "Appointment status is {} and cannot be modified.".format(appointment.Status.value))
        appointment.Status = status
        db.session.commit()
        return Callback(True, "Appointment status has been set to {}.".format(appointment.Status.value))

    except Exception as exc:
        helpers.logError("appointment_services.setAppointmentStatusPublic(): " + str(exc))
        return Callback(False, 'Could not set appointment status.')

def setAppointmentStatus(appointmentID, status):
    try:
        appointment = db.session.query(Appointment).filter(Appointment.ID == appointmentID).first()
        if appointment.Status != enums.Status.Pending:
          return Callback(False, "Appointment status is {} and cannot be modified.".format(appointment.Status.value))
        appointment.Status = status
        db.session.commit()
        return Callback(True, "Appointment status has been set to {}.".format(appointment.Status.value))

    except Exception as exc:
        helpers.logError("appointment_services.setAppointmentStatus(): " + str(exc))
        return Callback(False, 'Could not set appointment status.')

def getAppointments(companyID):
    try:
        print(generateEmailUrl(1))
        assistants = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
        appointments = []
        for assistant in assistants:
            for idx, appointment in enumerate(helpers.getListFromSQLAlchemyList(assistant.appointments)):
                appointment['Conversation'] = assistant.appointments[idx].Conversation.Data
                appointments.append(appointment)
        return Callback(True, 'Successfully gathered appointments.', appointments)
    except Exception as exc:
        helpers.logError("appointment_services.getAppointments(): " + str(exc))
        return Callback(False, 'Could not get appointments.')