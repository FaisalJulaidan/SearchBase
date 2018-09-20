from models import db, Callback, ChatbotSession
from utilties import helpers


def getByQuestionID(questionID):
    try:

        result = db.session.query(ChatbotSession).get(questionID)
        if not result: raise Exception

        return Callback(True, "Got user input by question id successfully.", result)

    except Exception as exc:

        print("getByQuestionID() Error: ", exc)

        return Callback(False, 'Could not get the user input.')