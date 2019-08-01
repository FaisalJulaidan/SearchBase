from models import Callback
from utilities import helpers

from twilio.rest import Client

    
def testConnection(auth):
    try:

        sms_message = "Test"

        send_sms_callback: Callback = sendMessage(auth.get("phone_number"), sms_message, auth)
        if not send_sms_callback.Success:
            raise Exception(send_sms_callback.Message)

        return Callback(True, "Testing has been successful", auth)
    except Exception as exc:
        helpers.logError("Marketplace.Messaging.Twilio.logout() ERROR: " + str(exc))
        return Callback(False, "Error in testing")


def sendMessage(sendto, body, auth):
    print("Attempting to send message")
    try:
        client = Client(auth.get("account_sid"), auth.get("auth_token"))

        message = client.messages.create(
            to=sendto,
            from_=auth.get("phone_number"),
            body=body)

        print(message.sid)

        return Callback(True, "Message has been sent")
    except Exception as exc:
        helpers.logError("Marketplace.Messaging.Twilio.sendMessage() ERROR: " + str(exc))
        return Callback(False, "Error in sending Message")

# NOTE: Temp for testing sms
# send_sms("+447860285032", "Place TEXT above: \n https://www.thesearchbase.com/")
