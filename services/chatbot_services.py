from services import solutions_services
from models import db, Callback, UserInput



# Process chatbot data
def processData(data: dict) -> Callback:
    try:
        userInput = UserInput(Content=data)
        db.session.add(userInput)
    except Exception as exc:
        db.session.rollback()
        return Callback(False, "An error occurred while processing chatbot data.")
    db.session.commit()
    return Callback(True, 'Chatbot data has been processed successfully!', userInput)

