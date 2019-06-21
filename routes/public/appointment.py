from flask import Blueprint, request
from models import Callback, Assistant, Conversation, Appointment
from services import assistant_services, appointment_services, conversation_services
from utilities import helpers

appointment_router = Blueprint('appointment_router', __name__, template_folder="../templates", static_folder='static')


# Appointment routes
@appointment_router.route("/appointments/<payload>", methods=['GET', 'POST'])
def candidate_appointment(payload):

    try:
        # Token expires in 5 days
        data = helpers.verificationSigner.loads(payload, salt='appointment-key', max_age=432000)

    except Exception as exc:
        return helpers.jsonResponse(False, 400, "Invalid token")

    if request.method == "GET":

        # Get assistant
        assistant_callback: Callback = assistant_services.getByID(data['assistantID'], data['companyID'])
        if not assistant_callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.")
        assistant: Assistant = assistant_callback.Data

        # Get open times slots associated with this assistant if exist
        openTimes_callback: Callback = assistant_services.getOpenTimes(data['assistantID'])
        if not openTimes_callback.Success:
            return helpers.jsonResponse(False, 404, "Couldn't load available time slots")

        data = {
            "companyLogoURL": assistant.Company.LogoPath,
            "openTimes": helpers.getListFromSQLAlchemyList(openTimes_callback.Data or []),
            "takenTimeSlots": helpers.getListFromSQLAlchemyList(assistant.Appointments),
            "userName": data['userName']
        }

        return helpers.jsonResponse(True, 200, "", data)


    if request.method == "POST":

        # Get user conversation
        conversation_callback: Callback = conversation_services.getByID(data['conversationID'], data['assistantID'])
        if not conversation_callback.Success:
            return helpers.jsonResponse(False, 404, "Sorry, but your data does not exist anymore")
        conversation: Conversation = conversation_callback.Data

        # Check if user already has an appointment
        appointment: Appointment = conversation.Appointment
        if appointment:
            return helpers.jsonResponse(False, 404,
                                        "Sorry, but your already have an appointment on " +
                                        '{0:%Y-%m-%d %H:%M:%S}'.format(appointment))

        # Add new appointment
        appointment_callback: Callback = appointment_services.add(data['conversationID'],
                                                                  data['assistantID'],
                                                                  request.json.get('pickedTimeSlot'))

        # TODO send an email to the user about his appointment
        # Send confirmation email


        if not appointment_callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, we couldn't add your appointment")
        return helpers.jsonResponse(True, 200, "Appointment has been added. You should receive a confirmation email")

