from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Callback, Assistant, Conversation, Appointment, AppointmentAllocationTime, AppointmentAllocationTimeInfo
from services import assistant_services, conversation_services, appointment_services, company_services
from utilities import helpers, wrappers, enums

appointment_router: Blueprint = Blueprint('appointment_router', __name__, template_folder="../../templates")


# Get all appointments for a company
@appointment_router.route("/appointments", methods=['GET'])
@jwt_required
@wrappers.AccessAppointmentsRequired
def appointments():
    user = get_jwt_identity()['user']
    callback = appointment_services.getAppointments(user['companyID'])

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
    else:
        return helpers.jsonResponse(False, 404, callback.Message)


'''
POST REQUEST EXAMPLE:
{
    "appointmentID": 1,
    "status": "Accepted"
}
'''

@appointment_router.route("/appointments/set_status", methods=['POST'])
@jwt_required
@wrappers.AccessAppointmentsRequired
def set_appointment_status():
    # Authenticate
    user = get_jwt_identity()['user']

    data = request.get_json()

    callback = appointment_services.setAppointmentStatus(data, user['companyID'])

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)


@appointment_router.route("/appointments/set_status_public", methods=['POST'])
# @wrappers.AccessAppointmentsRequired
def set_appointment_status_public():
    data = request.get_json()
    callback = appointment_services.setAppointmentStatusPublic(data['token'], data['appointmentID'], data['status'])

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)


@appointment_router.route("/appointments/verify/<token>", methods=['GET'])
# @wrappers.AccessAppointmentsRequired
def verify_get_appointment(token):
    callback = appointment_services.verifyRequest(token)

    if callback.Success:
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)
    else:
        return helpers.jsonResponse(False, 401, callback.Message)

@appointment_router.route("/allocation_times/<token>", methods=['GET', 'POST'])
def allocation_time(token):
    try:
        # Token expires in 5 days
        data = helpers.verificationSigner.loads(token, salt='appointment-key', max_age=432000)

    except Exception as exc:
        return helpers.jsonResponse(False, 400, "Invalid token")

    if request.method == "GET":

        # Get assistant
        assistant_callback: Callback = assistant_services.getByID(data['assistantID'], data['companyID'])
        if not assistant_callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.")
        assistant: Assistant = assistant_callback.Data

        # Get open times slots associated with this assistant if exist
        times_callback: Callback = assistant_services.getAppointmentAllocationTime(data['assistantID'])
        if not times_callback.Success:
            return helpers.jsonResponse(False, 404, "Couldn't load available time slots")

        times: AppointmentAllocationTime = times_callback.Data

        data = {
            "companyName": assistant.Company.Name,
            "logoPath": helpers.keyFromStoredFile(assistant.Company.StoredFile, enums.FileAssetType.Logo).AbsFilePath,
            "appointmentAllocationTime": helpers.getListFromSQLAlchemyList(times.Info if times else []),
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
                                        '{0:%Y-%m-%d %H:%M:%S}'.format(appointment.DateTime))

        # Add new appointment
        appointment_callback: Callback = appointment_services.addNewAppointment(data['conversationID'],
                                                                                request.json.get('pickedTimeSlot'),
                                                                                request.json.get('userTimeZone'))

        if not appointment_callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, we couldn't add your appointment")
        return helpers.jsonResponse(True, 200, "Appointment has been added. You should receive a confirmation email")

@appointment_router.route("/allocation_times", methods=['PUT'])
@jwt_required
def save_allocation_time():
    companyID = get_jwt_identity()['user']['companyID']
    data = request.get_json()
    #e(companyID, name, times, duration)
    save_callback : Callback = \
        appointment_services.saveAppointmentAllocationTime(companyID,
                                                           data['ID'],
                                                           data['Name'],
                                                           data['Info'],
                                                           data['Duration'])

    if not save_callback.Success:
        return helpers.jsonResponse(False, 400, "Sorry, we couldn't save your timetable changes")
    return helpers.jsonResponse(True, 200, "Timetable changes have successfully been saved", __parseAppointmentAllocationlist(save_callback.Data))

@appointment_router.route("/allocation_times", methods=['POST'])
@jwt_required
def create_allocation_time():
    companyID = get_jwt_identity()['user']['companyID']
    data = request.get_json()
    #e(companyID, name, times, duration)
    save_callback : Callback = appointment_services.createAppointmentAllocationTime(companyID, data['Name'], data['Info'], data['Duration'])

    if not save_callback.Success:
        return helpers.jsonResponse(False, 400, "Sorry, we couldn't save your timetable changes")
    return helpers.jsonResponse(True, 200, "Timetable changes have successfully been saved", __parseAppointmentAllocationlist(save_callback.Data))

@appointment_router.route("/allocation_times/<id>", methods=['DELETE'])
@jwt_required
def delete_allocation_time(id):
    companyID = get_jwt_identity()['user']['companyID']
    save_callback : Callback = appointment_services.deleteAppointmentAllocationTime(companyID, id)

    if not save_callback.Success:
        return helpers.jsonResponse(False, 400, "Sorry, we couldn't delete your timetable")
    return helpers.jsonResponse(True, 200, "Timetable has been successfully deleted")


@appointment_router.route("/allocation_times_list/", methods=['GET'])
@jwt_required
def allocation_time_list():
    companyID = get_jwt_identity()['user']['companyID']
    times_callback: Callback = appointment_services.getAppointmentAllocationTimes(companyID)
    returnObj =__parseAppointmentAllocationlist(times_callback.Data) if times_callback.Data is not None else []

    if not times_callback.Success:
        return helpers.jsonResponse(False, 400, times_callback.Message)
    return helpers.jsonResponse(True, 200, times_callback.Message, returnObj)

# hmm should move this
def __parseAppointmentAllocationlist(aatList):
    returnObj = []
    ret = aatList if type(aatList) is list else [aatList]
    for aat in ret:
        appItem = helpers.getDictFromSQLAlchemyObj(aat)
        info = []
        for item in aat.Info:
            info.append(helpers.getDictFromSQLAlchemyObj(item))
        appItem['Info'] = info
        returnObj.append(appItem)
    return returnObj
