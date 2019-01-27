from models import db, Callback, ChatbotSession
from utilities import helpers
from typing import List
from sqlalchemy.sql import desc

from sqlalchemy.sql import and_


# ----- Getters ----- #
def getAllByAssistantID(assistantID):
    try:
        sessions= db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID) \
            .order_by(desc(ChatbotSession.DateTime)).all()
        if not sessions: raise Exception

        data = chatbotSessionDictList(sessions) # will convert to json and solve Enums issue
        return Callback(True, "User inputs retrieved successfully.", data)

    except Exception as exc:
        print("chatbotSession_services.getByAssistantID() Error: ", exc)
        return Callback(False, 'Could not retrieve the data.')


def getByID(id, assistant):
    try:
        session = db.session.query(ChatbotSession)\
            .filter(and_(ChatbotSession.AssistantID == assistant.ID, ChatbotSession.ID == id))\
            .first()
        if not session: raise Exception
        return Callback(True, "User input retrieved successfully.", session)

    except Exception as exc:
        print("userInput_services.getByID() Error: ", exc)
        return Callback(False, 'Could not retrieve the data.')



# ----- Filters ----- #
def filterForContainEmails(records):
    try:
        result = []
        for record in records:
            record = record.Data["collectedInformation"]
            for question in record:
                if "@" in question["input"]:
                    result.append({"record" : record, "email" : question["input"]})
                    break

        return Callback(True, "Data has been filtered.", result)

    except Exception as exc:

        print("userInput_services.filterForContainEmails ERROR: ", exc)

        return Callback(False, 'Could not filter the data.')


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


# ----- Extras ----- #


def chatbotSessionDictList(sessions: List[ChatbotSession]):
    try:
        data= []
        for session in sessions:
            data.append(createDictFromSession(session))
        return data
    except Exception as e:
        print(" __chatbotSessionJsonList ERROR:", e)
        db.session.rollback()
        raise Exception('Error: __chatbotSessionJsonList')


def createDictFromSession(session: ChatbotSession):
    try:
        session = {'ID': session.ID, 'Data': session.Data, 'FilePath': session.FilePath,
                   'DateTime': session.DateTime, 'TimeSpent': session.TimeSpent,
                   'SolutionsReturned': session.SolutionsReturned,
                   'QuestionsAnswered': session.QuestionsAnswered,
                   'UserType': session.UserType.value,
                   'AssistantID': session.AssistantID
                   }
        return session
    except Exception as e:
        print("createBlockFromDict ERROR:", e)
        raise Exception('Error: createBlockFromDict()')