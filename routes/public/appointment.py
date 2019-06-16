from flask import Blueprint, request
from models import Callback, Assistant
from services import assistant_services
from utilities import helpers

appointment_router = Blueprint('appointment_router', __name__, template_folder="../templates", static_folder='static')


# Appointment routes
@appointment_router.route("/appointments/<payload>", methods=['GET', 'POST'])
def candidate_appointment(payload):
    try:

        # token expires in 5 days
        data = helpers.verificationSigner.loads(payload, salt='appointment-key', max_age=432000).split(";")

        conversationID = int(data[0])
        assistantID = int(data[1])
        companyID = int(data[2])
        userName = data[3]

        assistant_callback: Callback = assistant_services.getByID(assistantID, companyID)
        if not assistant_callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.")
        assistant: Assistant = assistant_callback.Data



        if request.method == "GET":
            openTimes_callback: Callback = assistant_services.getOpenTimes(assistantID)
            if not openTimes_callback.Success:
                return helpers.jsonResponse(False, 404, openTimes_callback.Message)

            data = {
                "companyLogoURL": assistant.Company.LogoPath,
                "openTimes": helpers.getListFromSQLAlchemyList(openTimes_callback.Data or []),
                "takenTimeSlots": helpers.getListFromSQLAlchemyList(assistant.Appointments),
                "userName": userName
            }

            return helpers.jsonResponse(True, 200, "", data)



        if request.method == "POST":
            callback: Callback = assistant_services.addAppointment(conversationID,
                                                                   assistantID,
                                                                   request.json.get('pickedTimeSlot'))

            if not callback.Success:
                return helpers.jsonResponse(False, 400, callback.Message)
            return helpers.jsonResponse(True, 200, callback.Message)

    except Exception as e:
        print(e)
        return helpers.jsonResponse(False, 400, "Couldn't load available appointments")