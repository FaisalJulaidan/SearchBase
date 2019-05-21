from datetime import datetime, timedelta
from typing import List

from jsonschema import validate
from sqlalchemy.sql import and_
from sqlalchemy.sql import desc

from models import db, Callback, ChatbotSession, Assistant
from services import assistant_services, stored_file_services, databases_services
from services.CRM import crm_services
from utilities import json_schemas, helpers
from enums import DatabaseType, UserType
import logging


# Process chatbot session data
def processSession(assistantHashID, data: dict) -> Callback:
    callback: Callback = assistant_services.getAssistantByHashID(assistantHashID)
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
    sessionData = {
        'collectedData': collectedData,
        'selectedSolutions': selectedSolutions,
        'keywordsByDataType': data['keywordsByDataType'],
    }

    # Validate submitted session after adding the modified version of selected solutions
    try:
        validate(sessionData, json_schemas.chatbot_session)
    except Exception as exc:
        print("chatbotSession_services.processSession ERROR 1: " + str(exc.args))
        logging.error("chatbotSession_services.processSession(): " + str(exc.args))
        return Callback(False, "The submitted chatbot data doesn't follow the correct format.", exc.args[0])

    try:
        # collectedData is an array, and timeSpent is in seconds.
        chatbotSession = ChatbotSession(Data=sessionData,
                                        TimeSpent=data['timeSpent'],
                                        Completed=data['isSessionCompleted'],
                                        SolutionsReturned=data['solutionsReturned'],
                                        QuestionsAnswered=len(collectedData),
                                        UserType=UserType[data['userType'].replace(" ", "")],
                                        Assistant=assistant)
        print("assistant: ", assistant)
        print("chatbotSession: ", chatbotSession)
        # CRM integration
        if assistant.CRM:
            crm_callback: Callback = crm_services.processSession(assistant, chatbotSession)
            print("crm_callback: ", crm_callback)
            print("crm_callback.Success: ", crm_callback.Success)
            print("crm_callback.Message: ", crm_callback.Message)
            if crm_callback.Success:
                chatbotSession.CRMSynced = True
            chatbotSession.CRMResponse = crm_callback.Message

        db.session.add(chatbotSession)
        db.session.commit()

        return Callback(True, 'Chatbot data has been processed successfully!', chatbotSession)

    except Exception as exc:
        print("chatbotSession_services.processSession ERROR 1: " + str(exc))
        logging.error("chatbotSession_services.processSession(): " + str(exc))
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")

# ----- Getters ----- #
def getAllByAssistantID(assistantID):
    try:
        sessions: List[ChatbotSession] = db.session.query(ChatbotSession).filter(
            ChatbotSession.AssistantID == assistantID) \
            .order_by(desc(ChatbotSession.DateTime)).all()


        for session in sessions:
            filePaths = ""
            storedFile_callback: Callback = stored_file_services.getBySession(session)
            if storedFile_callback.Success:
                filePaths = storedFile_callback.Data.FilePath
            session.FilePath =  filePaths
        return Callback(True, "User inputs retrieved successfully.", sessions)

    except Exception as exc:
        print("chatbotSession_services.getAllByAssistantID() Error: ", exc)
        logging.error("chatbotSession_services.getAllByAssistantID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the data.')


def getByID(sessionID, assistantID):
    try:
        session = db.session.query(ChatbotSession) \
            .filter(and_(ChatbotSession.AssistantID == assistantID, ChatbotSession.ID == sessionID)).first()
        if not session:
            raise Exception

        storedFile_callback: Callback = stored_file_services.getBySession(session)
        if storedFile_callback.Success:
            session.FilePath = storedFile_callback.Data.FilePath

        return Callback(True, "ChatbotSession retrieved successfully.", session)

    except Exception as exc:
        print("chatbotSession_services.getByID() Error: ", exc)
        logging.error("chatbotSession_services.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not retrieve the session.')


# ----- Filters ----- #
def getAllRecordsByAssistantIDInTheLast(hours, assistantID):
    try:
        result = db.session.query(ChatbotSession).filter(
            ChatbotSession.AssistantID == assistantID,
            ChatbotSession.DateTime < datetime.now(),
            ChatbotSession.DateTime >= datetime.now() - timedelta(hours=hours)).count()

        if not result:
            raise Exception("No Chatbot sessions to return")

        return Callback(True, "Records retrieved", result)
    except Exception as exc:
        print("chatbotSession_services.getAllRecordsByAssistantIDInTheLast() ERROR / EMPTY: ", exc)
        logging.error("chatbotSession_services.getAllRecordsByAssistantIDInTheLast(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Error in returning records for the last " + str(hours) +
                        " hours for assistant with ID: " + str(assistantID))


# ----- Deletions ----- #
def deleteByID(sessionID):
    try:
        db.session.query(ChatbotSession).filter(ChatbotSession.ID == sessionID).delete()
        db.session.commit()
        return Callback(True, 'Record has been removed successfully.')
    except Exception as exc:
        print("userInput_services.deleteByID() Error: ", exc)
        logging.error("chatbotSession_services.deleteByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Record could not be removed.')


def deleteAll(assistantID):
    try:
        db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID).delete()
        db.session.commit()
        return Callback(True, 'Records have been removed successfully.')
    except Exception as exc:
        print("userInput_services.deleteAll() Error: ", exc)
        logging.error("chatbotSession_services.deleteAll(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Records could not be removed.')