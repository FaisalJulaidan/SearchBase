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

