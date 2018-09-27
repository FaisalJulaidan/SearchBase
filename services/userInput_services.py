from models import db, Callback, ChatbotSession
from utilities import helpers


def getByAssistantID(assistantID):
    try:
        result = db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID).all()
        print(result)
        if not result: raise Exception

        return Callback(True, "Got user input by assistant id successfully.", result)

    except Exception as exc:

        print("userInput_services.getByAssistantID() Error: ", exc)

        return Callback(False, 'Could not retrieve the data.')

def deleteByID(id):
    try:
        record: ChatbotSession = db.session.query(ChatbotSession).filter(ChatbotSession.ID == id).first()
        if not record:
            return Callback(False, "the doesn't exist")

        db.session.query(ChatbotSession).filter(ChatbotSession.ID == id).delete()
    except Exception as exc:
        print("userInput_services.deleteByID() Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Record could not be removed.')
    # Save
    db.session.commit()
    return Callback(True, 'Block has been removed successfully.')