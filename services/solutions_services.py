import sqlalchemy.exc

from models import db,Callback,Solution, Assistant
from sqlalchemy import func
from utilties import helpers


def getBasedOnKeywords(assistant: Assistant, keywords: list, max=999999) -> Callback:

    # Get solutions
    solutions = db.session.query(Solution).filter(Solution.AssistantID == assistant.ID).all()
    if len(solutions) == 0:
        return Callback(True, "There are no solutions associated with this assistant", None)

    # Create a dict with keys as solution ids and values as the number occurrences
    # of keywords of each solution in the given keywords list
    dic = {}
    for s in solutions:
        c = sum(k in keywords for k in s.Keywords.split(','))
        dic[s.ID] = c

    # Sort dict based on value
    dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))

    # return the first 'max' solutions
    count = 1
    result = []
    for key, value in dic.items():
        for s in solutions:
            if s.ID == key and value !=0:
                result.append(s)
                break
        if count == max:
            break
        count += 1

    print(result)
    return Callback(True, 'Solutions based on keywords retrieved successfully!!', result)


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
