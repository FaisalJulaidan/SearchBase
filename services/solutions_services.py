import sqlalchemy.exc

from models import db,Callback,Solution
from sqlalchemy import func
from utilties import helpers

def getByAssistantID(assistantID):

    try:
        if assistantID:
            # Get result and check if None then raise exception
            result = db.session.query(Solution).get(assistantID)
            if not result: raise Exception

            return Callback(True, 'Solutions have been successfully retrieved', result)
        else:
            raise Exception
    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        return Callback(False, 'Could not retrieve solutions for ID: ' + assistantID)

def deleteAllByAssistantID(assistantID):

    try:
        db.session.query(Solution).filter(Solution.AssistantID == assistantID).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print("deleteAllByAssistantID Error: ", exc)
        db.session.rollback()
        return False

    return True

def createNew(assistantID, id, name, brand, model, price, keywords, discount, url):
    try:
        # Create a new user with its associated company and role
        solution = Solution(AssistantID=assistantID, ProductID=id, Name=name, Brand=brand,
                            Model=model, Price=price, Keywords=keywords, Discount=discount, URL=url)
        db.session.add(solution)

    except Exception as exc:
        print("createNew Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the solution.')
    # Save
    db.session.commit()
    return Callback(True, 'Solution has been created successfully!')

def bulkAdd(objects):
    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
    except Exception as exc:
        print("bulkAdd Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the solutions.')
    # Save
    db.session.commit()
    return Callback(True, 'Solutions has been created successfully!')

def countRecordsByAssistantID(assistantID):
    try:
        if assistantID:
            # Get result and check if None then raise exception
            result = db.session.query(Solution).get(assistantID).count()
            if not result: raise Exception

            return result
        else:
            raise Exception
    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        return 0
    return numberOfRecords

def deleteByAssitantID(assistantID, message):
    deleteOldData : bool = deleteAllByAssistantID(assistantID)
    if not deleteOldData: 
        return helpers.redirectWithMessage("admin_solutions", message)

def addOldByAssitantID(assistantID, message, currentSolutions):
    addOldSolutions_callback : Callback = bulkAdd(currentSolutions)
    if not addOldSolutions_callback.Success: 
        return helpers.redirectWithMessage("admin_solutions", message)
