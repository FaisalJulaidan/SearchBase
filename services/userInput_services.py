from models import db, Callback, ChatbotSession
from utilities import helpers


def getByAssistantID(assistantID):
    try:
        result = db.session.query(ChatbotSession).filter(ChatbotSession.AssistantID == assistantID).all()
        return Callback(True, "User inputs retrieved successfully.", result)

    except Exception as exc:
        print("userInput_services.getByAssistantID() Error: ", exc)
        return Callback(False, 'Could not retrieve the data.')

def filterForContainEmails(records):
    try:
        result = []
        for record in records:
            record = record.Data["collectedInformation"]
            for question in record:
                if "@" in question["input"]:
                    result.append({"record" : record, "email" : question["input"]})
                    break

        return Callback(True, "Data has been filtered.", result)

    except Exception as exc:

        print("userInput_services.filterForContainEmails ERROR: ", exc)

        return Callback(False, 'Could not filter the data.')

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
       # db.session.close()

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
       # db.session.close()
