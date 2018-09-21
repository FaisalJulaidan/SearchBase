from models import db, Callback, ChatbotSession
from utilties import helpers


def getByAssistantID(assistantID):
    try:
        9
        result = db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID).all()
        print(result)
        if not result: raise Exception

        return Callback(True, "Got user input by assistant id successfully.", result)

    except Exception as exc:

        print("getByAssistantID() Error: ", exc)

        return Callback(False, 'Could not retrieve the data.')