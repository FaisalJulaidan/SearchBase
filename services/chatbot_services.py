from flask import session
from services import assistant_services
from models import db, Callback, UserInput



# Process chatbot data
def processData(data: dict) -> Callback:
    try:
        userInput = UserInput(Content=data)
    except Exception as exc:
        return Callback(False, "An error occurred while processing chatbot data.")
    return Callback(True, 'Chatbot data has been processed successfully!', userInput)

