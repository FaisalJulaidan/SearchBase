from datetime import datetime, timedelta
from typing import List

from jsonschema import validate
from sqlalchemy.sql import and_
from sqlalchemy.sql import desc

from utilities.enums import UserType, Status, Webhooks
from models import db, Callback, Conversation, Assistant
from services import assistant_services, stored_file_services, auto_pilot_services, mail_services, webhook_services
from services.Marketplace.CRM import crm_services
from utilities import json_schemas, helpers


# Process chatbot conversation data
def processConversation(assistantHashID, data: dict) -> Callback:
    try:
        if data['score'] > 1:
            raise Exception("Score is corrupted")

        callback: Callback = assistant_services.getByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = callback.Data

        # Fetch selected solutions from the database to get their complete details as they were hidden in the chatbot
        selectedSolutions = []
        for solution in data['selectedSolutions']:
            selectedSolutions.append({
                'data': helpers.decrypt(solution['output'], isDict=True),
                'databaseType': solution.get('databaseType')['enumName']
            })

        # collectedData is an array
        collectedData = data['collectedData']
        conversationData = {
            'collectedData': collectedData,
            'selectedSolutions': selectedSolutions,
            'keywordsByDataType': data['keywordsByDataType'],
        }

        # Validate submitted conversation after adding the modified version of selected solutions
        validate(conversationData, json_schemas.conversation)

        # timeSpent is in seconds.
        conversation = Conversation(Data=conversationData,
                                    Name=data['name'],
                                    Email=data['email'],
                                    PhoneNumber=data['phone'],
                                    TimeSpent=data['timeSpent'],
                                    Completed=data['isConversationCompleted'],
                                    SolutionsReturned=data['solutionsReturned'],
                                    QuestionsAnswered=len(collectedData),
                                    UserType=UserType[data['userType']],
                                    Score=round(data['score'], 2),
                                    ApplicationStatus=Status.Pending,
                                    Assistant=assistant)
        webhookData = {
            **conversationData,
            'name': data['name'],
            'email': data['email'],
            'phoneNumber': data['phone'],
            'userType': UserType[data['userType']].value
        }

        webhook_services.fireRequests(webhookData, callback.Data.CompanyID, Webhooks.Conversations)

        # AutoPilot Operations
        if assistant.AutoPilot and conversation.Completed:
            ap_callback: Callback = auto_pilot_services.processConversation(conversation, assistant.AutoPilot, assistant)
            if ap_callback.Success:
                conversation.AutoPilotStatus = True
                conversation.ApplicationStatus = ap_callback.Data['applicationStatus']
                conversation.AcceptanceEmailSentAt = ap_callback.Data['acceptanceEmailSentAt']
                conversation.AcceptanceSMSSentAt = ap_callback.Data['acceptanceSMSSentAt']
                conversation.RejectionEmailSentAt = ap_callback.Data['rejectionEmailSentAt']
                conversation.RejectionSMSSentAt = ap_callback.Data['rejectionSMSSentAt']
                conversation.AppointmentEmailSentAt = ap_callback.Data['appointmentEmailSentAt']
            conversation.AutoPilotResponse = ap_callback.Message

        # CRM integration
        if assistant.CRM and conversation.Completed:
            crm_callback: Callback = crm_services.processConversation(assistant, conversation)
            if crm_callback.Success:
                conversation.CRMSynced = True
            conversation.CRMResponse = crm_callback.Message

        # Notify company about the new chatbot session only if set as immediate -> NotifyEvery=0
        # Note: if there is a file upload the /file route in chatbot.py will handle the notification instead
        if assistant.NotifyEvery == 0:
            if not data['hasFiles']:
                callback_mail: Callback = mail_services.notifyNewConversation(assistant, conversation)
                if callback_mail.Success:
                    assistant.LastNotificationDate = datetime.now()


        # Save conversation data
        db.session.add(conversation)
        db.session.commit()


        return Callback(True, 'Chatbot data has been processed successfully!', conversation)

    except Exception as exc:
        helpers.logError("conversation_services.processConversation(): " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")


# ----- Getters ----- #
def getAllByAssistantID(assistantID):
    try:
        conversations: List[Conversation] = db.session.query(Conversation) \
            .filter(Conversation.AssistantID == assistantID) \
            .order_by(desc(Conversation.DateTime)).all()
        for conversation in conversations:
            if(conversation.StoredFile != None):
                conversation.__Files = helpers.getListFromSQLAlchemyList(conversation.StoredFile.StoredFileInfo)
        return Callback(True, "Conversations retrieved successfully.", conversations)
    except Exception as exc:
        helpers.logError("conversation_services.getAllByAssistantID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the data.')


def getByID(conversationID, assistantID):
    try:
        conversation = db.session.query(Conversation) \
            .filter(and_(Conversation.AssistantID == assistantID, Conversation.ID == conversationID)).first()
        if not conversation:
            return Callback(False, "Conversation does not exist")

        storedFile_callback: Callback = stored_file_services.getByConversation(conversation)
        if storedFile_callback.Success:
            conversation.__Files = storedFile_callback.Data.StoredFileInfo

        return Callback(True, "ChatbotConversation retrieved successfully.", conversation)

    except Exception as exc:
        helpers.logError("conversation_services.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the conversation.')


# ----- Updaters ----- #
def updateStatus(conversationID, assistantID, newStatus):
    try:
        db.session.query(Conversation) \
            .filter(and_(Conversation.AssistantID == assistantID, Conversation.ID == conversationID)) \
            .update({'ApplicationStatus': Status[newStatus]})

        db.session.commit()
        return Callback(True, 'Status updated Successfully')

    except Exception as exc:
        helpers.logError("conversation_services.updateStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't update status")


# ----- Filters ----- #
def getAllRecordsByAssistantIDInTheLast(hours, assistantID):
    try:
        result = db.session.query(Conversation).filter(
            Conversation.AssistantID == assistantID,
            Conversation.DateTime < datetime.now(),
            Conversation.DateTime >= datetime.now() - timedelta(hours=hours)).count()

        if not result:
            raise Exception("No Chatbot conversation to return")

        return Callback(True, "Records retrieved", result)
    except Exception as exc:
        helpers.logError("conversation_services.getAllRecordsByAssistantIDInTheLast(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Error in returning records for the last " + str(hours) +
                        " hours for assistant with ID: " + str(assistantID))


# ----- Deletions ----- #
def deleteByID(conversationID):
    try:
        db.session.query(Conversation).filter(Conversation.ID == conversationID).delete()
        db.session.commit()
        return Callback(True, 'Record has been removed successfully.')
    except Exception as exc:
        helpers.logError("conversation_services.deleteByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Record could not be removed.')


def deleteAll(assistantID):
    try:
        db.session.query(Conversation).filter(Conversation.AssistantID == assistantID).delete()
        db.session.commit()
        return Callback(True, 'Records have been removed successfully.')
    except Exception as exc:
        helpers.logError("conversation_services.deleteAll(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Records could not be removed.')
