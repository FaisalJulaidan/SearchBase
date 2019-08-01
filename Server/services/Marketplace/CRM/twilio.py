import os

from twilio.rest import Client

from models import Callback
from utilities import helpers

# Fetched from the twilio console:
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

client = Client(account_sid, auth_token)

sendNumber = "+441143032341"
# Purpose? --> Send sms containing links for various usages
# Functionality required? --> send_sms


def exampleFunc(dueIn, payment):
    try:


        sms_message = "This is the text of the message"

        send_sms_callback: Callback = send_sms("reciever phone", sms_message)
        if not send_sms_callback.Success:
            raise Exception(send_sms_callback.Message)

        return Callback(True, "Payment Notification SMS has been sent")
    except Exception as e:
        helpers.logError("sms_services.sendPaymentDueNotification() ERROR: " + str(e))
        return Callback(False, "Error in sending Payment Notification SMS")


def send_sms(sendto, body):
    print("Attempting to send message")
    try:
        message = client.messages.create(
            to=sendto,
            from_=sendNumber,
            body=body)

        print(message.sid)

        return Callback(True, "SMS has been sent")
    except Exception as e:
        print("sms_services.send_sms() ERROR: ", e)
        return Callback(False, "Error in sending SMS")


# NOTE: Temp for testing sms
# send_sms("+447860285032", "Place TEXT above: \n https://www.thesearchbase.com/")
