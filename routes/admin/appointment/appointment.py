from flask import Blueprint, request
from services import assistant_services, conversation_services, appointment_services
from models import Callback, Assistant, Conversation, Appointment
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


appointment_router: Blueprint = Blueprint('appointment_router', __name__, template_folder="../../templates")

# Get all appointments for a company
@appointment_router.route("/appointments", methods=['GET'])
@jwt_required
def appointments():

    # Authenticate
    user = get_jwt_identity()['user']

    if request.method == "GET":
        pass



# Get all open times for a user to pick up from, it uses the payload to know for which company and other details...
@appointment_router.route("/open_times/<payload>", methods=['GET', 'POST'])
def open_times(payload):

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
            "companyName": assistant.Company.Name,
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
                                                                  request.json.get('pickedTimeSlot'),
                                                                  confirmed=False)

        if not appointment_callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, we couldn't add your appointment")
        return helpers.jsonResponse(True, 200, "Appointment has been added. You should receive a confirmation email")