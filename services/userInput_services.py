from models import db, Callback, UserInput
from utilties import helpers


def getByAssistantID(assistantID):
    try:
        9
        result = db.session.query(UserInput).filter(UserInput.AssistantID == assistantID).all()
        print(result)
        if not result: raise Exception

        return Callback(True, "Got user input by assistant id successfully.", result)

    except Exception as exc:

        print("getByAssistantID() Error: ", exc)

        return Callback(False, 'Could not get the user input.')