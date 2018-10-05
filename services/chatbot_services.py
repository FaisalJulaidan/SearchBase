from models import db, Callback, ChatbotSession, Assistant
from utilities import json_utils



# Process chatbot data
def processData(assistant: Assistant, data: dict) -> Callback:
    try:
        json_utils.validateSchema(data, 'chatbot_session.json')
    except Exception as exc:
        print(exc.args)
        return Callback(False, "The submitted chatbot data doesn't follow the correct format."
                               " Please check /static/json_schema/chatbot_session.json", exc.args[0])
    try:

        # collectedInformation is an array, and timeSpent is in seconds.
        collectedInformation = data['collectedInformation']
        chatbotSession = ChatbotSession(Data={'collectedInformation': collectedInformation},
                                   TimeSpent=44,
                                   SolutionsReturned=data['solutionsReturned'],
                                   QuestionsAnswered=len(collectedInformation),
                                   Assistant=assistant)

        db.session.add(chatbotSession)
        db.session.commit()
        return Callback(True, 'Chatbot data has been processed successfully!', chatbotSession)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")
    # finally:
    #     db.session.close()


def getBySessionID(sessionID) -> Callback:
    try:
        result = db.session.query(ChatbotSession).get(sessionID)
        if not result: raise Exception
        return Callback(True, "Got user input by question id successfully.", result)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not get the user input.')
    # finally:
    #     db.session.close()



def addFilePath(sessionID: int, path: str):

    try:
        userSession_callback: Callback = getBySessionID(sessionID)
        if not userSession_callback.Success:
            return Callback(False, 'Could not find the chatbot session record to add the given file path')
        userSession_callback.Data.FilePath = path

        db.session.commit()
        return Callback(True, "File path has been added successfully!")

    except Exception as exc:
        db.session.rollback()
        return Callback(False, 'Could not add the given file path')

    # finally:
    #     db.session.close()




