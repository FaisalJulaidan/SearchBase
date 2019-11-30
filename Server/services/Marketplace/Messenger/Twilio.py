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


def sendMessage(sendto, body, auth, whatsapp=False):
    try:
        client = Client(auth.get("account_sid"), auth.get("auth_token"))
        sender = auth.get("phone_number")

        if whatsapp:
            sendto = "whatsapp:" + sendto
            sender = "whatsapp:" + sender

        message = client.messages.create(
            to=sendto,
            from_=sender,
            body=body) # add break-lines to sms message

        return Callback(True, "Message has been sent")
    except Exception as exc:
        helpers.logError("Marketplace.Messaging.Twilio.sendMessage() ERROR: " + str(exc))
        return Callback(False, "Error in sending Message")

# NOTE: Temp for testing sms
# send_sms("+447860285032", "Place TEXT above: \n https://www.thesearchbase.com/")
