from datetime import datetime, timedelta
from typing import List

from jsonschema import validate
from sqlalchemy.sql import and_
from sqlalchemy.sql import desc

from models import db, Callback, Conversation, Assistant
from services import assistant_services, stored_file_services, databases_services, auto_pilot_services
from services.CRM import crm_services
from utilities import json_schemas, helpers
from enums import DatabaseType, UserType, ApplicationStatus
import logging


# Process chatbot conversation data
def processConversation(assistantHashID, data: dict) -> Callback:
    try:
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

        collectedData = data['collectedData']
        conversationData = {
            'collectedData': collectedData,
            'selectedSolutions': selectedSolutions,
            'keywordsByDataType': data['keywordsByDataType'],
        }


        # Validate submitted conversation after adding the modified version of selected solutions
        validate(conversationData, json_schemas.conversation)
        if data['score'] > 1:
            raise Exception("Score is corrupted")

        # collectedData is an array, and timeSpent is in seconds.
        conversation = Conversation(Data= conversationData,
                                      TimeSpent=data['timeSpent'],
                                      Completed=data['isConversationCompleted'],
                                      SolutionsReturned=data['solutionsReturned'],
                                      QuestionsAnswered=len(collectedData),
                                      UserType=UserType[data['userType'].replace(" ", "")],
                                      Score=data['score'],
                                      Assistant=assistant)

        # AutoPilot Operations
        if assistant.AutoPilot:
            ap_callback: Callback = auto_pilot_services.processConversation(conversation, assistant.AutoPilot)
            if ap_callback.Success:
                conversation.AutoPilotStatus = True
                conversation.ApplicationStatus = ap_callback.Data['applicationStatus']
                # conversation.AppointmentEmailSentAt = ap_callback.Data['appointmentEmailSentAt']
            conversation.AutoPilotResponse = ap_callback.Message
            print(ap_callback.Data)


        # CRM integration
        # if assistant.CRM:
        #     crm_callback: Callback = crm_services.processConversation(assistant, conversation)
        #     if crm_callback.Success:
        #         conversation.CRMSynced = True
        #     conversation.CRMResponse = crm_callback.Message


        db.session.add(conversation)
        db.session.commit()

        return Callback(True, 'Chatbot data has been processed successfully!', conversation)

    except Exception as exc:
        print("conversation_services.processConversation ERROR 1: " + str(exc))
        logging.error("conversation_services.processConversation(): " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")

# ----- Getters ----- #
def getAllByAssistantID(assistantID):
    try:
        conversations: List[Conversation] = db.session.query(Conversation)\
            .filter(Conversation.AssistantID == assistantID) \
            .order_by(desc(Conversation.DateTime)).all()


        for conversation in conversations:
            filePaths = ""
            storedFile_callback: Callback = stored_file_services.getByConversation(conversation)
            if storedFile_callback.Success:
                filePaths = storedFile_callback.Data.FilePath
            conversation.FilePath =  filePaths
        return Callback(True, "User inputs retrieved successfully.", conversations)

    except Exception as exc:
        print("conversation_services.getAllByAssistantID() Error: ", exc)
        logging.error("conversation_services.getAllByAssistantID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the data.')


def getByID(conversationID, assistantID):
    try:
        conversation = db.session.query(Conversation) \
            .filter(and_(Conversation.AssistantID == assistantID, Conversation.ID == conversationID)).first()
        if not conversation:
            raise Exception

        storedFile_callback: Callback = stored_file_services.getByConversation(conversation)
        if storedFile_callback.Success:
            conversation.FilePath = storedFile_callback.Data.FilePath

        return Callback(True, "ChatbotConversation retrieved successfully.", conversation)

    except Exception as exc:
        print("conversation_services.getByID() Error: ", exc)
        logging.error("conversation_services.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the conversation.')


# ----- Updaters ----- #
def updateStatus(conversationID, assistantID, newStatus):
    try:
        db.session.query(Conversation)\
            .filter(and_(Conversation.AssistantID == assistantID, Conversation.ID == conversationID))\
            .update({'ApplicationStatus': ApplicationStatus[newStatus]})

        db.session.commit()
        return Callback(True, 'Status updated Successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        logging.error("conversation_services.updateStatus(): " + str(exc))
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
        print("conversation_services.getAllRecordsByAssistantIDInTheLast() ERROR / EMPTY: ", exc)
        logging.error("conversation_services.getAllRecordsByAssistantIDInTheLast(): " + str(exc))
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
        print("userInput_services.deleteByID() Error: ", exc)
        logging.error("conversation_services.deleteByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Record could not be removed.')


def deleteAll(assistantID):
    try:
        db.session.query(Conversation).filter(Conversation.AssistantID == assistantID).delete()
        db.session.commit()
        return Callback(True, 'Records have been removed successfully.')
    except Exception as exc:
        print("userInput_services.deleteAll() Error: ", exc)
        logging.error("conversation_services.deleteAll(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Records could not be removed.')