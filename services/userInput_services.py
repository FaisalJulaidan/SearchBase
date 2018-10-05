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

    # finally:
    #     db.session.close()
        
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
    #     db.session.close()

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
    #     db.session.close()
