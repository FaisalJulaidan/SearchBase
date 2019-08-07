from datetime import datetime, time

from models import db, Callback, Appointment, Conversation, Assistant,\
    AppointmentAllocationTime, AppointmentAllocationTimeInfo
from sqlalchemy import and_
from utilities import helpers, enums

def dummyCreateAppointmentAllocationTime(name, companyID: int):
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
        return Callback(True, "Timetable saved succesfully.", appointmentAllocationTime)

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
        assistants = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
        appointments = []
        for assistant in assistants:
            for idx, appointment in enumerate(helpers.getListFromSQLAlchemyList(assistant.Appointments)):
                appointment['Conversation'] = assistant.Appointments[idx].Conversation.Data
                appointments.append(appointment)
        return Callback(True, 'Successfully gathered appointments.', appointments)
    except Exception as exc:
        helpers.logError("appointment_services.getAppointments(): " + str(exc))
        return Callback(False, 'Could not get appointments.')

def getAppointmentAllocationTimes(id):
    try:
        result = db.session.query(AppointmentAllocationTime) \
            .join(AppointmentAllocationTimeInfo) \
            .filter(AppointmentAllocationTime.CompanyID == id) \
            .all()
        return Callback(True, 'Gathered Appointment Allocation Times', result)
    except Exception as exc:
        print(exc)
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