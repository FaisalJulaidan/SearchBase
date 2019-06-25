from models import db, Callback, Appointment, Conversation, Assistant, Company
from sqlalchemy import and_
from utilities import helpers
from services import conversation_services
from datetime import datetime
import enums


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


# ----- Getters ----- #
def getAllByCompanyID(companyID):
    try:
        # Get assistant and check if None then raise exception
        appointments: Appointment = Company.query.get(companyID).Assistants.appointments

        print(appointments)

        return Callback(True,"Got open time slots successfully.", appointments)

    except Exception as exc:
        helpers.logError("appointment_services.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not get the appointments')

def setAppointmentStatus(appointmentID, status):
    try:
        appointment = db.session.query(Appointment).filter(Appointment.ID == appointmentID).first()
        if appointment.Status != enums.ApplicationStatus.Pending:
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
        return Callback(True, 'Succesfully gathered appointments.', appointments)
    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not get appointments.')