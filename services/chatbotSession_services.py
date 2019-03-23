from datetime import datetime, timedelta
from typing import List

from jsonschema import validate
from sqlalchemy.sql import and_
from sqlalchemy.sql import desc

from models import db, Callback, ChatbotSession, Assistant
from services import assistant_services, stored_file_services, databases_services
from utilities import json_schemas, helpers
from enums import DatabaseType, UserType


# Process chatbot session data
def processSession(assistantHashID, data: dict) -> Callback:
    callback: Callback = assistant_services.getAssistantByHashID(assistantHashID)
    if not callback.Success:
        return Callback(False, "Assistant not found!")
    assistant: Assistant = callback.Data

    # Fetch selected solutions from the database to get their complete details as they were hidden in the chatbot
    selectedSolutions = []
    for solution in data['selectedSolutions']:
        callback = databases_services.getRecord(solution['id'],
                                                DatabaseType[solution.get('databaseType')['enumName']])
        if callback.Success:
            selectedSolutions.append({
                'data': helpers.getDictFromSQLAlchemyObj(callback.Data),
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
        print(exc.args)
        return Callback(False, "The submitted chatbot data doesn't follow the correct format.", exc.args[0])

    try:
        # collectedData is an array, and timeSpent is in seconds.

        chatbotSession = ChatbotSession(Data= sessionData,
                                        TimeSpent=data['timeSpent'],
                                        SolutionsReturned=data['solutionsReturned'],
                                        QuestionsAnswered=len(collectedData),
                                        UserType=UserType[data['userType'].replace(" ", "")],
                                        Assistant=assistant)
        db.session.add(chatbotSession)
        db.session.commit()
        return Callback(True, 'Chatbot data has been processed successfully!', chatbotSession)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")
    # finally:
    # db.session.close()


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
        print("chatbotSession_services.getByAssistantID() Error: ", exc)
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
        db.session.rollback()
        return Callback(False, 'Could not retrieve the session.')


# ----- Filters ----- #
def filterForContainEmails(records):
    try:
        result = []
        for record in records:
            record = record.Data["collectedInformation"]
            for question in record:
                if "@" in question["input"]:
                    result.append({"record": record, "email": question["input"]})
                    break

        return Callback(True, "Data has been filtered.", result)

    except Exception as exc:

        print("userInput_services.filterForContainEmails ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not filter the data.')


def getAllRecordsByAssistantIDInTheLast(hours, assistantID):
    try:
        result = db.session.query(ChatbotSession).filter(
            ChatbotSession.AssistantID == assistantID,
            ChatbotSession.DateTime < datetime.now(),
            ChatbotSession.DateTime >= datetime.now() - timedelta(hours=hours)).count()

        if not result:
            raise Exception("Empty")

        return Callback(True, "Records retrieved", result)
    except Exception as e:
        db.session.rollback()
        print("analytics_services.getAllRecordsByAssistantIDInTheLast() ERROR: ", e)
        return Callback(False, "Error in returning records")


# ----- Deletions ----- #
def deleteByID(id):
    try:
        db.session.query(ChatbotSession).filter(ChatbotSession.ID == id).delete()
        db.session.commit()
        return Callback(True, 'Record has been removed successfully.')
    except Exception as exc:
        print("userInput_services.deleteByID() Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Record could not be removed.')
    # finally:
    # db.session.close()


def deleteAll(assistantID):
    try:
        db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID).delete()
        db.session.commit()
        return Callback(True, 'Records have been removed successfully.')
    except Exception as exc:
        print("userInput_services.deleteAll() Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Records could not be removed.')
    # finally:
    # db.session.close()
