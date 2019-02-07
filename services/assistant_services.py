from models import db, Company, Assistant, Callback
from sqlalchemy import and_
from utilities import helpers


def getAssistantByHashID(hashID):
    try:
        assistantID = helpers.decrypt_id(hashID)
        if len(assistantID) == 0:
            return Callback(False, "Assistant not found!", None)

        # Get result and check if None then raise exception
        assistant: Assistant = db.session.query(Assistant).get(assistantID[0])
        if not assistant: raise Exception
        return Callback(True, "", assistant)


    except Exception as exc:
        print("getAssistantByHashID() ERROR:" + str(exc))
        return Callback(False, "Assistant not found!")

    # finally:
            # db.session.close()

def getByID(id, companyID) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant)\
            .filter(and_(Assistant.ID == id, Assistant.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got assistant successfully.", result)

    except Exception as exc:
        print(exc)
        return Callback(False, 'Could not get the assistant.')
    # finally:
       # db.session.close()


def getByName(name) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant).filter(Assistant.Name == name).first()
        if not result: raise Exception

        return Callback(True,
                        "Got assistant by nickname successfully.",
                        result)
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Could not get the assistant by nickname.')
    # finally:
       # db.session.close()



def getAll(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
            if len(result) == 0:
                return Callback(True,"No assistants  to be retrieved.", [])

            return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False,'Could not get all assistants.')
    # finally:
       # db.session.close()


def create(name, message, topBarText, secondsUntilPopup, companyID) -> Assistant or None:
    try:
        assistant = Assistant(Name=name, Route=None, Message=message, TopBarText=topBarText,
                              SecondsUntilPopup=secondsUntilPopup,
                              CompanyID=companyID)
        db.session.add(assistant)
        # Save
        db.session.commit()
        return Callback(True, 'Assistant has ben created successfully!', assistant)
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Failed to create the assistant', None)
    # finally:
       # db.session.close()


def update(id, name, message, topBarText, secondsUntilPopup)-> Callback:
    try:
        db.session.query(Assistant).filter(Assistant.ID == id).update({'Name': name,
                                                                       'Message': message,
                                                                       'TopBarText': topBarText,
                                                                       'SecondsUntilPopup': secondsUntilPopup})
        db.session.commit()
        return Callback(True, name + ' Updated Successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False,
                        "Couldn't update assistant "+name)
    # finally:
       # db.session.close()



def changeStatus(assistant: Assistant, statusValue):
    try:
        isActive = False
        if statusValue > 0:
           isActive = True

        assistant.Active = isActive
        db.session.commit()
        return Callback(True, 'Assistant status has been changed.')

    except Exception as exc:
        print("Error in assistant_services.changeStatus(): ", exc)
        db.session.rollback()
        return Callback(False, "Could not change the assistant's status.")
    # finally:
       # db.session.close()


def removeByID(id) -> Callback:
    try:
        db.session.query(Assistant).filter(Assistant.ID == id).delete()
        db.session.commit()
        return Callback(True, 'Assistant has been deleted.')

    except Exception as exc:
        print("Error in assistant_services.removeByID(): ", exc)
        db.session.rollback()
        return Callback(False, 'Error in deleting assistant.')
    # finally:
       # db.session.close()

def checkOwnership(assistantID, companyID):
    try:
        assistant_callback : Callback = getByID(assistantID, companyID)
        if not assistant_callback.Success: 
            return Callback(False, "Error in retrieving necessary information.")

        # Check if the user is from the company that owns the assistant
        if companyID != assistant_callback.Data.CompanyID:
            return Callback(False, 'Security check failed. Process terminated.')

        return Callback(True, 'Ownership check passed')
    except Exception as exc:
        print("Error in assistant_services.checkOwnership(): ", exc)
        db.session.rollback()
        return Callback(False, 'Error in verifying ownership over assistant.')
    # finally:
       # db.session.close()
