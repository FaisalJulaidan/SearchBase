from datetime import datetime

from models import db, Callback, Appointment, Conversation, Assistant
from utilities import helpers, enums


def add(conversationID, assistantID, dateTime, confirmed=False):
    try:
        if not datetime: raise Exception('Time slot (datetime) is required')

        if not Conversation.query.get(conversationID): raise Exception("Conversation does not exist anymore")

        db.session.add(
            Appointment(
                DateTime=datetime.strptime(dateTime, "%Y-%m-%d %H:%M"),  # 2019-06-23 16:04
                AssistantID=assistantID,
                ConversationID=conversationID,
                Confirmed= confirmed
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
            if appointment.Status != "Pending":
                raise(Exception("Appointment status has already been set!"))
            else:
                return helpers.verificationSigner.dumps({'id': appointmentID}, salt='verify-appointment')
    except Exception as e:
        print(e)

def verifyRequest(token):
    try:
        verificationLink = helpers.verificationSigner.loads(token, salt='verify-appointment')
        appointment = db.session.query(Appointment.Status, Appointment.ID, Appointment.DateTime, Conversation.Data)\
            .join(Conversation).filter(Appointment.ID == verificationLink['id']).first()
        if appointment:
            appointment = helpers.getDictFromLimitedQuery(["Status", "ID", "DateTime", "Data"], appointment)
            if appointment['Status'] == 'Pending':
                return Callback(True, "Succesfully gathered appointment data", appointment)
            else :
                return Callback(False, "Appointment status has already been set")
    except Exception as  e:
        print(e)
        return Callback(False, "Could not gather appointment")


# ----- Getters ----- #

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
        print(exc)
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
        print(exc)
        return Callback(False, 'Could not set appointment status.')

def getAppointments(companyID):
    try:
        assistants = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
        appointments = []
        for assistant in assistants:
            for idx, appointment in enumerate(helpers.getListFromSQLAlchemyList(assistant.appointments)):
                appointment['Conversation'] = assistant.appointments[idx].Conversation.Data
                appointments.append(appointment)
        return Callback(True, 'Successfully gathered appointments.', appointments)
    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not get appointments.')
