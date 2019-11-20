from threading import Thread
from flask import render_template, current_app
from flask_mail import Mail, Message
from typing import List

from models import Callback, Assistant, Conversation, Company, StoredFileInfo
from services import user_services, stored_file_services as sfs
from utilities import helpers,enums

mail = Mail()
tsbSendEmail = "notifications@thesearchbase.com"
tsbReceiveEmail = "info@thesearchbase.com"


def sendDemoRequest(data) -> Callback:
    try:
        # if not data["name"] or data["company"] or (data["phone"] or data["email"]):
        #     return Callback(False, "Required information is missing")

        callback: Callback = __sendEmail(tsbReceiveEmail, 'Demo Request', '/emails/arrange_demo.html', data=data)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, "Demo has been requested. We will be in touch soon.")
    except Exception as exc:
        helpers.logError("mail_service.sendDemoRequest(): " + str(exc))
        return Callback(False, "Demo Request could not be sent at this time")


def contactUsIndex(name, email, message) -> Callback:
    try:
        callback: Callback = __sendEmail(tsbReceiveEmail, 'TheSearchBase Contact Us', '/emails/message_sent.html',
                                         name=name, email=email, message=message)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, "Thank you. We will contact you as soon as possible.")

    except Exception as exc:
        helpers.logError("mail_service.contactUsIndex(): " + str(exc))
        return Callback(False, "We could not send your message at this time. Please try again later.")


def sendVerificationEmail(firstName, lastName, email, companyName, companyID) -> Callback:
    try:

        # Create the verification link with token attached
        verificationLink = helpers.getDomain() + "/verify_account/" + \
                           helpers.verificationSigner\
                               .dumps({'email': email, 'companyID': companyID}, salt='account-verify-key')

        callback: Callback = __sendEmail(email,
                  'Account Verification',
                  '/emails/account_verification.html',
                                         companyName=companyName,
                                         userName= firstName + ' ' + lastName,
                                         verificationLink= verificationLink)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Verification email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendVerificationEmail(): " + str(exc))
        return Callback(False, 'Could not send a verification email to ' + email)

def sendAppointmentConfirmationEmail(name, email, dateTime, userTimeZone, companyName, logoPath):
    try:
        callback: Callback = __sendEmail(
            email,
            'Appointment Confirmation',
            '/emails/appointment_confirmation.html',
            companyName=companyName,
            userName=name,
            dateTime=dateTime.strftime("%d/%m/%Y %H:%M"),
            userTimeZone=userTimeZone,
            logoPath=logoPath)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Appointment confirmation email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendAppointmentConfirmationEmail(): " + str(exc))
        return Callback(False, 'Could not send the confirmation email to ' + email)


def sendAcceptanceEmail(title, body, userName, email, logoPath, companyName):
    try:
        callback: Callback = __sendEmail(
            email,
            title or 'Acceptance Letter',
            '/emails/acceptance_letter.html',
            body=body,
            companyName=companyName,
            logoPath=logoPath,
            userName=userName)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Appointment picker email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendAcceptanceEmail(): " + str(exc))
        return Callback(False, 'Could not send a acceptance email to ' + email)


def sendRejectionEmail(title, body, userName, email, logoPath, companyName):
    try:
        callback: Callback = __sendEmail(
            email,
            title or 'Rejection Letter',
            '/emails/rejection_letter.html',
            body=body,
            companyName=companyName,
            logoPath=logoPath,
            userName=userName)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Appointment picker email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendAcceptanceEmail(): " + str(exc))
        return Callback(False, 'Could not send a acceptance email to ' + email)


def sendAppointmentsPicker(email, userName, logoPath, conversationID, assistantID, companyName, companyID):
    try:

        payload = {
            'conversationID': conversationID,
            'assistantID': assistantID,
            'companyID': companyID,
            'email': email,
            'userName': userName,
        }

        callback: Callback = __sendEmail(
            email,
            'Appointment',
            '/emails/appointment_picker.html',
            companyName=companyName,
            logoPath=logoPath,
            userName=userName,
            appointmentLink=helpers.getDomain() + "/appointments_picker/" + \
                                helpers.verificationSigner.dumps(payload, salt='appointment-key')
        )

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Appointment picker email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.SendAppointmentsPicker(): " + str(exc))
        return Callback(False, 'Could not send a appointment picker email to ' + email)


def sendPasswordResetEmail(email, userID):
    try:

        payload = email + ";" + str(userID)
        link = helpers.getDomain() + "/reset_password/" + \
               helpers.verificationSigner.dumps(payload, salt='reset-pass-key')

        callback: Callback = __sendEmail((email), 'Password reset',
                   '/emails/reset_password.html', link=link)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Password reset email is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendPasswordResetEmail(): " + str(exc))
        return Callback(False, 'Could not send a password reset email to ' + email)


def sendNewCompanyHasRegistered(name, email, companyName, companyID, tel):
    try:

        callback: Callback = __sendEmail(tsbReceiveEmail,
                                         companyName + ' has signed up',
                                         '/emails/company_registered.html',
                                         name=name,
                                         email=email,
                                         companyName=companyName,
                                         tel=tel,
                                         activationLink= helpers.getDomain() + "/api/staff/activate_company/" + helpers.verificationSigner
                                         .dumps({'email': email, 'companyID': companyID}, salt='company-activate-key')
                                         )

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Signed up email is on its way')

    except Exception as exc:
        helpers.logError("mail_service.sendNewUserHasRegistered(): " + str(exc))
        return Callback(False, 'Could not send a signed up email')


def sendAccountInvitation(firstName, lastName, email, password, companyName, logoPath, companyID):
    try:

        callback: Callback = \
            __sendEmail(email,
                       'Account Invitation',
                       '/emails/account_invitation.html',
                        companyName=companyName,
                        logoPath=logoPath,
                        userName= firstName + ' ' + lastName,
                        password=password,
                        verificationLink= helpers.getDomain() + "/verify_account/" + helpers.verificationSigner
                        .dumps({'email': email, 'companyID': companyID}, salt='account-verify-key')
                        )

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Email sent is on its way to ' + email)

    except Exception as exc:
        helpers.logError("mail_service.sendAccountInvitation(): " + str(exc))
        return Callback(False, 'Could not send account invitation email to ' + email)


def sendSolutionAlert(record, solutions):
    try:
        targetEmail = record["email"]
        userData = record["record"]

        callback: Callback = __sendEmail((targetEmail), 'You have new job matches',
                   'emails/solution_alert.html', userData=userData, solutions=solutions)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Email sent is on its way to ' + targetEmail)

    except Exception as exc:
        helpers.logError("mail_service.sendSolutionAlert(): " + str(exc))
        return Callback(False, 'Could not send email')


def simpleSend(to, title, text):
    try:

        callback: Callback = __sendEmail(to, title, text)

        if not callback.Success:
            raise Exception(callback.Message)

        return Callback(True, 'Email sent is on its way to ' + to)

    except Exception as exc:
        helpers.logError("mail_service.sendSolutionAlert(): " + str(exc))
        return Callback(False, 'Could not send email')


# Notify company about a new conversation
def notifyNewConversations(assistant: Assistant, conversations: List[Conversation], lastNotificationDate):
    try:

        users_callback: Callback = user_services.getAllByCompanyIDWithEnabledNotifications(assistant.CompanyID)
        if not users_callback.Success:
            return Callback(False, "Users not found!")


        # Get Company
        company: Company = assistant.Company

        if len(users_callback.Data) == 0:
            return Callback(True, "No user has notifications enabled")

        conversationsList = []
        for conversation in conversations:
            # Get pre singed url to download the file via links
            fileURLsSinged = []
            if conversation.StoredFile:
                if conversation.StoredFile.StoredFileInfo:
                    for file in conversation.StoredFile.StoredFileInfo:
                        fileURLsSinged.append(sfs.genPresigendURL(file.FilePath, 2592000).Data) # Expires in a month

            conversationsList.append({
                'userType': conversation.UserType.name,
                'data': conversation.Data,
                'status': conversation.ApplicationStatus.name,
                'fileURLsSinged': fileURLsSinged,
                'completed': "Yes" if conversation.Completed else "No",
                'dateTime': conversation.DateTime.strftime("%Y/%m/%d %H:%M"),
                'link': helpers.getDomain() + "/dashboard/assistants/" +
                        str(assistant.ID) + "?tab=Conversations&conversation_id=" + str(conversation.ID)
            })

        if not len(conversationsList) > 0:
            return Callback(True, "No new conversation to send")

        # Get company logo
        logoPath = helpers.keyFromStoredFile(company.StoredFile, enums.FileAssetType.Logo).AbsFilePath

        # send emails, jobs applied for
        for user in users_callback.Data:
            print("SEND TO :")
            print(user)
            email_callback: Callback = __sendEmail(to=user.Email,
                                                   subject="New users has engaged with your "
                                                          + assistant.Name + " assistant",
                                                   template='/emails/new_conversations_notification.html',
                                                   assistantName = assistant.Name,
                                                   assistantID = assistant.ID,
                                                   conversations = conversationsList,
                                                   logoPath = logoPath,
                                                   companyName = company.Name,
                                                   companyURL=company.URL,
                                                   )
            if not email_callback.Success:
                raise Exception(email_callback.Message)

        return Callback(True, "Emails have been sent")

    except Exception as exc:
        helpers.logError("mail_service.notifyNewChatbotSession(): " + str(exc))
        return Callback(False, "Error in notifying for new chatbot session")


# @async
def __sendAsyncEmail(app, msg):
    with app.app_context():
        mail.send(msg)


def __sendEmail(to, subject, template, files=None, **kwargs) -> Callback:
    try:
        # create Message with the Email: title, recipients and sender
        msg = Message(subject, recipients=[to], sender=tsbSendEmail)
        if template[0] == "/":
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
        else:
            try:
                # get app context / if it fails assume its working outside the app
                app = current_app._get_current_object()

            except Exception as exc:  # TODO check error code raise exception
                # import app. importing it in the beginning of the file will raise an error as it is still not created
                from app import app
                
            msg.html = template

        if files:
            for file in files:
                msg.attach(file.filename, 'application/octect-stream', file.read())

        # create and start the Thread of the email sending
        thr = Thread(target=__sendAsyncEmail, args=[app, msg])
        thr.start()

        return Callback(True, "Email sent to " + to + " successfully")
    except Exception as exc:
        helpers.logError("mail_service.send_email(): " + str(exc))
        return Callback(False, "Sending email to " + to + " failed")
