import time
from threading import Thread

from models import Callback
from utilities import helpers

from twilio.rest import Client


def testConnection(auth):
    try:

        sms_message = "If you are receiving this message then the Twilio test was successful. " + \
                      "If you do not know why you are receiving this, please contact SearchBase on " + \
                      "support@thesearchbase.com"

        send_sms_callback: Callback = sendMessage("+447578721001", sms_message, auth)
        if not send_sms_callback.Success:
            raise Exception(send_sms_callback.Message)

        return Callback(True, "Testing has been successful", auth)
    except Exception as exc:
        helpers.logError("Marketplace.Messaging.Twilio.logout() ERROR: " + str(exc))
        return Callback(False, "Error in testing")


def sendMessage(numbers, body, auth, whatsapp=False):
    try:
        client = Client(auth.get("account_sid"), auth.get("auth_token"))
        notify_service_sid = auth.get("notify_service_sid")

        # if whatsapp:
        #     sendto = "whatsapp:" + numbers

        if type(numbers) is str:
            numbers = [numbers]

        binding = []
        for number in numbers:
            if number[0] == "0":
                number = "+44" + number[1:]
            binding.append("{\"binding_type\":\"sms\",\"address\":\"" + number + "\"}")

        from app import app
        thr = Thread(target=__sendAsyncMessage, args=[app, client, notify_service_sid, binding, body])
        thr.start()

        return Callback(True, "Message has been sent")
    except Exception as exc:
        helpers.logError("Marketplace.Messaging.Twilio.sendMessage() ERROR: " + str(exc))
        return Callback(False, "Error in sending Message")


def __sendAsyncMessage(app, client, notify_service_sid, binding, body):
    with app.app_context():
        client.notify.services(notify_service_sid) \
            .notifications.create(
            to_binding=binding,
            body=body)
