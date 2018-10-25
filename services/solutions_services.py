import sqlalchemy.exc
import re
from models import db,Callback,Solution, Assistant
from sqlalchemy import func, exists
from utilities import helpers


# Scoring System
def getBasedOnKeywords(assistant: Assistant, keywords: list, max=999999) -> Callback:

    try:
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
        print(dic)

        # return the first 'max' solutions
        count = 1
        result = []
        for key, value in dic.items():
            for s in solutions:
                if s.ID == key and value !=0:
                    # incrementing TimesReturned value for every returned solutions by +1
                    s.TimesReturned +=1
                    result.append(s)
                    break
            if count == max:
                break
            count += 1
            # Save
            db.session.commit()
        return Callback(True, 'Solutions based on keywords retrieved successfully!!', result)
    except Exception as exc:
        print("solutions_services.getBasedOnKeywords() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Solutions could not be retrieved at this time')

    # finally:
       # db.session.close()


def createNew(assistant, majorTitle, money, url, solId='',  secTitle='', shortDesc='', keywords=''):
    try:
        # Create a new user with its associated company and role
        solution = Solution(Assistant=assistant, SolutionID=solId, MajorTitle=majorTitle, SecondaryTitle=secTitle,
                            ShortDescription=shortDesc,Money=money, Keywords=keywords, URL=url, TimesReturned=0)
        db.session.add(solution)

        db.session.commit()
        return Callback(True, 'Solution has been successfully created.')

    except Exception as exc:
        print("createNew Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the solution.')

    # finally:
       # db.session.close()


def getByID(id):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).get(id)
        if not result: raise Exception

        return Callback(True, 'Solutions have been successfully retrieved', result)
    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve solutions for ID: ' + str(id))

    # finally:
       # db.session.close()


def update(solution: Solution, solId, majorTitle, money, URL, secTitle='', shortDesc='', keywords=''):
    try:
        # Validate the keywords address using a regex. (k,k) correct (k) correct (,k) incorrect
        if len(keywords) > 0:
            if not re.match("^([a-zA-Z]+|\\b,\\b)+$", keywords):
                return Callback(False, "keyword doesn't follow the correct format ex. key1,key2...")

        # Update solution
        solution.SolutionID = solId
        solution.MajorTitle = majorTitle
        solution.SecondaryTitle = secTitle
        solution.ShortDescription = shortDesc
        solution.Money = money
        solution.Keywords = keywords
        solution.URL = URL

        db.session.commit()
        return Callback(True, 'Solution has been successfully edited.')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the solution')

    # finally:
       # db.session.close()


def remove(solution: Solution) -> Callback:
    try:
        db.session.delete(solution)

        db.session.commit()
        return Callback(True, "Solution with id has been successfully removed.")

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "Solution could not be removed.")

    # finally:
       # db.session.close()


def getByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).get(assistantID)
        if not result: raise Exception

        return Callback(True, 'Solutions have been successfully retrieved', result)

    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve solutions for ID: ' + str(assistantID))

    # finally:
       # db.session.close()


def getAllByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).filter(Solution.AssistantID == assistantID).all()
        if not result: raise Exception
        return Callback(True, 'Solutions have been successfully retrieved', result)
    except Exception as exc:
        print("getAllByAssistantID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve solutions for ID: ' + str(assistantID))

    # finally:
       # db.session.close()


def deleteAllByAssistantID(assistantID):

    try:
        db.session.query(Solution).filter(Solution.AssistantID == assistantID).delete()

        return True
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print("deleteAllByAssistantID Error: ", exc)
        db.session.rollback()
        return False

    # finally:
       # db.session.close()




def bulkAdd(objects):
    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
        return Callback(True, 'Solutions has been created successfully!')
    except Exception as exc:
        print("bulkAdd Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the solutions.')

    # finally:
       # db.session.close()


def countRecordsByAssistantID(assistantID):
    try:
        if assistantID:
            # Get result and check if None then raise exception
            result = db.session.query(Solution).get(assistantID).count()
            if not result: raise Exception

            return result
        else:
            raise Exception
        return numberOfRecords
    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        db.session.rollback()
        return 0

    # finally:
       # db.session.close()


def deleteByAssitantID(assistantID, message):
    deleteOldData : bool = deleteAllByAssistantID(assistantID)
    if not deleteOldData:
        return helpers.redirectWithMessage("admin_solutions", message)


def addOldByAssitantID(assistantID, message, currentSolutions):
    addOldSolutions_callback : Callback = bulkAdd(currentSolutions)
    if not addOldSolutions_callback.Success:
        return helpers.redirectWithMessage("admin_solutions", message)
