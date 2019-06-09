import logging
import os
from threading import Thread

from flask import render_template, current_app
from flask_mail import Mail, Message
from werkzeug.datastructures import FileStorage

from config import BaseConfig
from models import Callback
from services import user_services, stored_file_services as sfs
from utilities import helpers

mail = Mail()

tsbEmail = "info@thesearchbase.com"


# def timer_tick():
#     now = datetime.now()
#
#     #  conversation -> splitting the day in 6 parts of 4 hour periods to determine which part of the day it is
#     #  12pm - 4am
#     session1 = [now.replace(hour=0, minute=0, second=0, microsecond=0),
#                 now.replace(hour=3, minute=59, second=59, microsecond=999999)]
#     #  4am - 8am
#     session2 = [now.replace(hour=4, minute=0, second=0, microsecond=0),
#                 now.replace(hour=7, minute=59, second=59, microsecond=999999)]
#     #  8am - 12am
#     session3 = [now.replace(hour=8, minute=0, second=0, microsecond=0),
#                 now.replace(hour=11, minute=59, second=59, microsecond=999999)]
#     #  12am - 16am
#     session4 = [now.replace(hour=12, minute=0, second=0, microsecond=0),
#                 now.replace(hour=15, minute=59, second=59, microsecond=999999)]
#     #  16am - 20am
#     session5 = [now.replace(hour=16, minute=0, second=0, microsecond=0),
#                 now.replace(hour=19, minute=59, second=59, microsecond=999999)]
#     #  20am - 24
#     session6 = [now.replace(hour=20, minute=0, second=0, microsecond=0),
#                 now.replace(hour=23, minute=59, second=59, microsecond=999999)]
#
#     sessions = [session1, session2, session3, session4, session5, session6]
#
#     #  sub -> subscriptions -> determines when a chatbot is enabled for a specific interval ex. 4 hours...
#     #  ... which conversation it should activate notification in
#     sub4 = {"interval": 4, "conversation": [session1, session2, session3, session4, session5, session6]}
#     sub8 = {"interval": 8, "conversation": [session1, session3, session5]}
#     sub12 = {"interval": 12, "conversation": [session2, session5]}
#     sub24 = {"interval": 24, "conversation": [session3]}
#     subs = [sub4, sub8, sub12, sub24]
#
#     for session in sessions:
#         # find which session the timer is currently in
#         if session[0] < now < session[1]:
#             # check which subscriptions should activate depending if they are subscribed to this session or not
#             for sub in subs:
#                 if session in sub["conversation"]:
#                     notifyNewConversationCountForLastXHours(sub["interval"])


def sendDemoRequest(email) -> Callback:
    try:
        send_email(tsbEmail, 'Demo Request', '/emails/arrange_demo.html', email=email)
        return Callback(True, "Demo has been requested. We will be in touch soon.")
    except Exception as exc:
        logging.error("mail_service.sendDemoRequest(): " + str(exc))
        return Callback(False, "Demo Request could not be sent at this time")


def contactUsIndex(name, email, message) -> Callback:
    try:
        send_email(tsbEmail, 'TheSearchBase Contact Us', '/emails/message_sent.html', name=name, email=email,
                   message=message)
        return Callback(True, "Thank you. We will contact you as soon as possible.")
    except Exception as exc:
        logging.error("mail_service.contactUsIndex(): " + str(exc))
        return Callback(False, "We could not send your message at this time. Please try again later.")


def sendVerificationEmail(email, companyName) -> Callback:
    try:

        payload = email + ";" + companyName
        link = "https://www.thesearchbase.com/account/verify/" + \
               helpers.verificationSigner.dumps(payload, salt='email-confirm-key')

        send_email((email), 'Account verification',
                   '/emails/verification.html', link=link)

        return Callback(True, 'Verification email is on its way to ' + email)

    except Exception as exc:
        logging.error("mail_service.sendVerificationEmail(): " + str(exc))
        return Callback(False, 'Could not send a verification email to ' + email)


def sendPasswordResetEmail(email, companyID):
    try:

        payload = email + ";" + str(companyID)
        link = "https://www.thesearchbase.com/reset_password/" + \
               helpers.verificationSigner.dumps(payload, salt='reset-pass-key')

        send_email((email), 'Password reset',
                   '/emails/reset_password.html', link=link)

        return Callback(True, 'Password reset email is on its way to ' + email)

    except Exception as exc:
        logging.error("mail_service.sendPasswordResetEmail(): " + str(exc))
        return Callback(False, 'Could not send a password reset email to ' + email)


def sendNewUserHasRegistered(name, email, companyName, tel):
    try:

        send_email(tsbEmail, companyName + ' has signed up',
                   '/emails/company_signup.html', name=name, email=email, companyName=companyName, tel=tel)

        return Callback(True, 'Signed up email is on its way')

    except Exception as exc:
        logging.error("mail_service.sendNewUserHasRegistered(): " + str(exc))
        return Callback(False, 'Could not send a signed up email')


def addedNewUserEmail(adminEmail, targetEmail, password):
    try:
        link = "https://www.thesearchbase.com/admin/changepassword"

        send_email((targetEmail), 'You have been added to TheSearchBase',
                   'emails/account_invitation.html', password=password, adminEmail=adminEmail)

        return Callback(True, 'Email sent is on its way to ' + targetEmail)

    except Exception as exc:
        logging.error("mail_service.addedNewUserEmail(): " + str(exc))
        return Callback(False, 'Could not send email to ' + targetEmail)


def sendSolutionAlert(record, solutions):
    try:
        targetEmail = record["email"]
        userData = record["record"]

        send_email((targetEmail), 'You have new job matches',
                   'emails/solution_alert.html', userData=userData, solutions=solutions)

        return Callback(True, 'Email sent is on its way to ' + targetEmail)

    except Exception as exc:
        logging.error("mail_service.sendSolutionAlert(): " + str(exc))
        return Callback(False, 'Could not send email')


# NOTIFICATIONS would need a reword
# def notifyNewConversationCountForLastXHours(hours):
#     try:
#         # get all users with enabled notifications
#         user_callback: Callback = user_services.getAllUsersWithEnabled("UserInputNotifications")
#         if not user_callback.Success:
#             raise Exception("userSettings_callback: ", user_callback.Message)
#
#         # loop through every user setting
#         for record in user_callback.Data:
#             # get their assistants by company id
#             assistants_callback: Callback = assistant_services.getAllWithEnabledNotifications(record.CompanyID)
#             if not assistants_callback.Success:
#                 raise Exception("assistants_callback: ", assistants_callback.Message)
#
#             # empty information to send by email
#             information = []
#
#             # for every assistant
#             for assistant in assistants_callback.Data:
#                 # get all chatbot conversation for the last X hours for the assistant
#                 records_callback: Callback = chatbotSession_services.getAllRecordsByAssistantIDInTheLast(hours, assistant.ID)
#                 if not records_callback.Success:
#                     raise Exception("records_callback: " + records_callback.Message)
#
#                 # add to information to be sent
#                 information.append(
#                     {"assistantName": assistant.Name, "data": records_callback.Data, "assistantID": assistant.ID})
#
#             # if no information to send - skip
#             if not information:
#                 continue
#
#             # send email
#             sendRecords_callback: Callback = mailNewConversationsCount(record.Email, information)
#             if not sendRecords_callback.Success:
#                 raise Exception("sendRecords_callback: ", sendRecords_callback.Message)
#
#     except Exception as exc:
#         logging.error("mail_service.notifyNewChatbotSessionsCountForLastXHours(): " + str(exc))
#         return Callback(False, "Error in notifying for new chatbot conversation")


def notifyNewConversation(assistant, conversation, file: FileStorage = None):
    try:
        if "immediately" not in assistant.NotifyEvery:
            return Callback(False, "Assistant is not set to receive instant notification!")
        users_callback: Callback = user_services.getAllByCompanyIDWithEnabledNotifications(assistant.CompanyID)
        if not users_callback.Success:
            return Callback(False, "Users not found!")

        fileInfo = None
        if file:
            # file_callback = sfs.getByConversation(conversation)
            # if not file_callback.Success:
            #     raise Exception(file_callback.Message)
            #
            # print(file_callback.Data.FilePath)
            # file_callback = sfs.downloadFile(file_callback.Data.FilePath)
            # if not file_callback.Success:
            #     raise Exception(file_callback.Message)
            #
            # file = file_callback.Data
            # file_content = file.read()
            savePath = os.path.join(BaseConfig.USER_FILES, file.filename)
            file.save(savePath)
            with current_app.open_resource(savePath) as fp:
                file_content = fp.read()

            fileInfo = {"filename": file.filename, "file_content": file_content}

        logoPath = sfs.PUBLIC_URL + sfs.UPLOAD_FOLDER + sfs.COMPANY_LOGOS_PATH + "/" + (
                    assistant.Company.LogoPath or "")

        completedConversation = "No"
        if conversation.Completed:
            completedConversation = "Yes"

        information = {"assistantName": assistant.Name, "records": [conversation.Data], "assistantID": assistant.ID,
                       "logoPath": logoPath, "userType": conversation.UserType.name,
                       "companyName": assistant.Company.Name, "conversationCompleted": completedConversation}
        # TODO FILE
        # send emails, jobs applied for
        for user in users_callback.Data:  # user.Email "evgeniybtonchev@gmail.com" vvvvvvvvvvvv
            email_callback: Callback = send_email(to="evgeniybtonchev@gmail.com",
                                                  subject='Your new ' + conversation.UserType.name,
                                                  template='emails/new_record_notification.html', file=fileInfo,
                                                  data=information)
            if not email_callback.Success:
                return Callback(False, email_callback.Message)

        return Callback(True, "Emails have been sent")

    except Exception as exc:
        print("mail_service.notifyNewChatbotSession() ERROR: ", exc)
        logging.error("mail_service.notifyNewChatbotSession(): " + str(exc))
        return Callback(False, "Error in notifying for new chatbot session")


# @async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, file=None, **kwargs):
    try:
        # create Message with the Email: title, recipients and sender
        msg = Message(subject, recipients=[to], sender=tsbEmail)

        try:
            # get app context / if it fails assume its working outside the app
            app = current_app._get_current_object()

            # load the template which the email will use
            msg.html = render_template(template, **kwargs)
        except Exception as exc:  # TODO check error code raise exception
            # import app. importing it in the beginning of the file will raise an error as it is still not created
            from app import app

            # use application context to load the template which the email will use
            with app.app_context():
                msg.html = render_template(template, **kwargs)

        if file:
            msg.attach(file.get("filename"), 'application/octect-stream', file.get("file_content"))

        # create and start the Thread of the email sending
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()

        return Callback(True, "Email sent to " + to + " successfully")
    except Exception as exc:
        print("EXCEPTION: ", str(exc))
        logging.error("mail_service.send_email(): " + str(exc))
        return Callback(False, "Sending email to " + to + " failed")
