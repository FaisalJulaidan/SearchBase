from models import db, Callback, Appointment
from utilities import helpers
from services import conversation_services
from datetime import datetime


def add(conversationID, assistantID, dateTime):
    try:
        if not datetime: raise Exception('Time slot (datetime) is required')

        callback: Callback = conversation_services.getByID(conversationID, assistantID)
        if not callback.Success: raise Exception("Conversation does not exist anymore")

        db.session.add(
            Appointment(
                DateTime=datetime.strptime(dateTime, "%Y-%m-%d %H:%M"),  # 2019-06-23 16:04
                AssistantID=assistantID,
                ConversationID=conversationID
            )
        )

        db.session.commit()
        return Callback(True, 'Appointment added successfully.')

    except Exception as exc:
        helpers.logError("assistant_services.addAppointment(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't add the appointment")