from datetime import datetime, timedelta
from typing import List

from jsonschema import validate
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import desc

from models import db, Callback, Conversation, Assistant, StoredFile, StoredFileInfo
from services import assistant_services, stored_file_services, auto_pilot_services, mail_services, webhook_services, \
    databases_services
from services.Marketplace.CRM import crm_services
from utilities import json_schemas, helpers, enums
from utilities.enums import UserType, Status, Webhooks


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

        if not data.get("crmInformation"):
            # AutoPilot Operations
            if assistant.AutoPilot and conversation.Completed:
                ap_callback: Callback = auto_pilot_services.processConversation(conversation, assistant.AutoPilot,
                                                                                assistant)
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
        else:
            crmInformation = helpers.decodeID(data["crmInformation"].get("source"))

            crmInformation = helpers.verificationSigner.loads(data["crmInformation"].get("source"),
                                                              salt='crm-information')
            print(crmInformation)
            source = crmInformation["source"]
            sourceID = crmInformation["crmID"]
            candidateID = crmInformation["candidateID"]
            # CAMPAIGN SOURCES - ID vs TEXT to make url shorter
            # 1 - DATABASE
            # 2 - CR
            if source == "crm":
                crm_callback: Callback = crm_services.updateCandidate(candidateID, conversation, assistant.CompanyID,
                                                                      sourceID)
                if crm_callback.Success:
                    conversation.CRMSynced = True
                conversation.CRMResponse = crm_callback.Message
            elif source == "db":
                database_callback: Callback = databases_services.updateCandidate(candidateID, conversation)

        # Notify company about the new chatbot session only if set as immediate -> NotifyEvery=0
        # Note: if there is a file upload the /file route in chatbot.py will handle the notification instead
        if assistant.NotifyEvery == 0:
            callback_mail: Callback = mail_services.notifyNewConversations(assistant, [conversation], None)
            if callback_mail.Success:
                assistant.LastNotificationDate = datetime.now()

        # Save conversation data
        db.session.add(conversation)
        db.session.commit()

        return Callback(True, 'Chatbot data has been processed successfully!', (conversation, data,))

    except Exception as exc:
        helpers.logError("conversation_services.processConversation(): " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")


def getFileByConversationID(assistantID, conversationID, filePath):
    try:
        file: StoredFileInfo = db.session.query(StoredFileInfo) \
            .filter(and_(Assistant.ID == assistantID,
                         Conversation.ID == conversationID,
                         StoredFileInfo.FilePath == filePath)) \
            .first()

        if not file:
            return Callback(False, "Could not gather file.")

        return Callback(False, "Gathered storedfile.", file)
    except Exception as exc:
        helpers.logError("conversation_services.getFileByConversationID(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not gather file.")


def uploadFiles(files, conversation, data, keys):
    try:
        sf: StoredFile = StoredFile()

        db.session.add(sf)
        db.session.flush()
        uploadedFiles = []
        uploadedFilesCallbacks = []
        for item in data['collectedData']:
            if item['input'] == "&FILE_UPLOAD&":  # enum for this?
                for file in files:
                    if file.filename in uploadedFiles:
                        continue
                    for submittedFile in data['submittedFiles']:
                        if file.filename == submittedFile['uploadedFileName']:
                            uploadedFiles.append(file.filename)
                            key = enums.FileAssetType.NoType  # TODO once BlockType-Upgrade is done
                            upload_callback: Callback = stored_file_services.uploadFile(file,
                                                                                        submittedFile['fileName'],
                                                                                        True, model=Conversation,
                                                                                        identifier="ID",
                                                                                        identifier_value=conversation.ID,
                                                                                        stored_file_id=sf.ID,
                                                                                        key=key)
                            crm_upload_callback: Callback = crm_services.uploadFile(upload_callback.Data, file.filename,
                                                                                    conversation)

                            uploadedFilesCallbacks.append(upload_callback)

        # Check if a file failed to be uploaded
        for callback in uploadedFilesCallbacks:
            if not callback.Success:
                raise Exception(callback.Message)

        db.session.commit()
        return Callback(True, "Gathered storedfile.")

    except Exception as exc:
        # helpers.logError("conversation_services.uploadFiles(): " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while uploading files.")


# ----- Getters ----- #
def getAllByAssistantID(assistantID):
    try:
        conversations: List[Conversation] = db.session.query(Conversation) \
            .options(joinedload('StoredFile').joinedload("StoredFileInfo")) \
            .filter(Conversation.AssistantID == assistantID) \
            .order_by(desc(Conversation.DateTime)).all()
        # for conversation in conversations:
        # if(conversation.StoredFile != None):
        # conversation.__Files = helpers.getListFromSQLAlchemyList()
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

        # storedFile_callback: Callback = stored_file_services.getByConversation(conversation)
        # if storedFile_callback.Success:
        #     conversation.__Files = storedFile_callback.Data.StoredFileInfo

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


def setFileByID(conversationID: int, fileID: int) -> Callback:
    try:
        result: Conversation = db.session.query(Conversation).filter(Conversation.ID == conversationID).first()
        result.StoredFileID = fileID

        if not result:
            raise Exception("Conversation files failed to be set")

        return Callback(True, "Conversations found", result)
    except Exception as exc:
        helpers.logError("conversation_services.setFileByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not set file by ID")


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
