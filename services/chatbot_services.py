from services import solutions_services
from models import db, Callback, UserInput, Assistant



# Process chatbot data
def processData(assistant: Assistant, data: dict) -> Callback:
    try:
        userInput = UserInput(Data={'collectedInformation': data['collectedInformation']}, Assistant=assistant)
        db.session.add(userInput)
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")
    db.session.commit()
    return Callback(True, 'Chatbot data has been processed successfully!', userInput)


def getBySessionID(sessionID) -> Callback:
    try:
        result = db.session.query(UserInput).get(sessionID)
        if not result: raise Exception

        return Callback(True, "Got user input by question id successfully.", result)

    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not get the user input.')


def addFilePath(sessionID: int, path: str):
    try:
        userInput_callback: Callback = getBySessionID(sessionID)
        if not userInput_callback.Success:
            return Callback(False, 'Could not find the userInput for that session to add the given file path')
        userInput_callback.Data.FilePath = path
    except Exception as exc:
        db.session.rollback()
        return Callback(False, 'Could not add the given file path')
    db.session.commit()
    return Callback(True, "file path has been added successfully!")



