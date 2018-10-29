import sqlalchemy.exc
import re
from models import db,Callback,Solution, Assistant
from sqlalchemy import func, exists
from utilities import helpers
from sqlalchemy.ext.mutable import MutableDict

import xml.etree.ElementTree as ET
from json import dumps
from collections import OrderedDict
from xmljson import BadgerFish
from lxml import etree

        ## Create a dict with keys as solution ids and values as the number occurrences
        ## of keywords of each solution in the given keywords list
        #dic = {}
        #for s in solutions:
        #    c = sum(k in keywords for k in s.Keywords.split(','))
        #    dic[s.ID] = c

        ## Sort dict based on value
        #dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
        #print(dic)

        ## return the first 'max' solutions
        #count = 1
        #result = []
        #for key, value in dic.items():
        #    for s in solutions:
        #        if s.ID == key and value !=0:
        #            # incrementing TimesReturned value for every returned solutions by +1
        #            s.TimesReturned +=1
        #            result.append(s)
        #            break
        #    if count == max:
        #        break
        #    count += 1
        #    # Save
        #    db.session.commit()

# Scoring System
def getBasedOnKeywords(assistant: Assistant, keywords: list, max=999999) -> Callback:

    try:
        # Get solutions
        solution = db.session.query(Solution).filter(Solution.AssistantID == assistant.ID).first()
        if not solution:
            return Callback(True, "There are no solutions associated with this assistant", None)
        
        #print(solution.Content)
        #print(dumps(solution.Content))
        #print(solution.Content["{http://tempuri.org/JSExport.xsd}JobShopExport"])
        matches = loopThroughAllJSON(solution.Content, {"command":"get solutions", "value":keywords}, solution.Content)
        print(matches)

        result = []
        return Callback(True, 'Solutions based on keywords retrieved successfully!!', result)
    except Exception as exc:
        print("solutions_services.getBasedOnKeywords() ERROR: ", exc)
        return Callback(False, 'Solutions could not be retrieved at this time')

    # finally:
       # db.session.close()

def loopThroughAllJSON(item, action, original, result={}):
    try:
        #print("Type: ", type(item))
        if type(item) is dict or type(item) is MutableDict:
            for key,value in item.items():
                result = actOnJSONItem(action, key, original, result)
                loopThroughAllJSON(item[key], action, original, result)
        elif type(item) is list:
            for value in item:
                result = actOnJSONItem(action, value, original, result)
                loopThroughAllJSON(value, action, original, result)
        else:
            result = actOnJSONItem(action, item, original, result)
        return result
    except Exception as exc:
        print("solutions_services.loopThroughAllJSON ERROR: ", exc)
        return result

def actOnJSONItem(action, item, result, original):
    try:
        if action["command"] == "print":
            print("JSON Item: ", item)
        elif action["command"] == "get solutions":
            if type(item) is int:
                oristr = dumps(original)
                #item = oristr.split("DBID=\""+str(item)+"\"")[1].split("Desc=\"")[1]
                try:
                    item = oristr.split('DBID": '+str(item)+', "@Desc": "')[1].split('"')[0]
                except:
                    pass
            if type(item) is str: 
                item = item.lower()
                #print(item)
                for keyword in action["value"]:
                    keyword = str(keyword)
                    if keyword in item:
                        print("ITEM: ", item)
                        print("KEYWORD: ", keyword)
                        if keyword in result:
                            result[keyword] += 1
                        else:
                            result[keyword] = 1
        return result
    except Exception as exc:
        print("solutions_services.actOnJSONItem ERROR: ", exc)
        return result

def createNew(assistantID, content):
    try:
        # Create a new user with its associated company and role
        solution = Solution(AssistantID=assistantID, Content=content)
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


def update(solution: Solution, content):
    try:
        # Validate the keywords address using a regex. (k,k) correct (k) correct (,k) incorrect
        # if len(keywords) > 0:
        #     if not re.match("^([a-zA-Z]+|\\b,\\b)+$", keywords):
        #         return Callback(False, "keyword doesn't follow the correct format ex. key1,key2...")

        # Update solution
        solution.Content = content

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
        result = db.session.query(Solution.ID,
                                  Solution.SolutionID,
                                  Solution.MajorTitle,
                                  Solution.SecondaryTitle,
                                  Solution.ShortDescription,
                                  Solution.Money,
                                  Solution.Keywords,
                                  Solution.URL,
                                  Solution.TimesReturned,
                                  Solution.AssistantID).filter(Solution.AssistantID == assistantID).all()
        if not result: raise Exception
        return Callback(True, 'Solutions have been successfully retrieved', result)
    except Exception as exc:
        print("getByAssistantID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve solutions for ID: ' + str(assistantID))

    # finally:
       # db.session.close()

def getFirstByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).filter(Solution.AssistantID == assistantID).first()
        if not result: raise Exception
        return Callback(True, 'Solution records have been successfully retrieved', result)
    except Exception as exc:
        print("solutions_services.getFirstByAssistantID Error/Empty: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve solution records')

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

def convertXMLtoJSON(xmlfile):
    try:
        #read the file
        tree = ET.parse(xmlfile)
        print("TREE")
        #get start and all of xml in written format
        root = tree.getroot()
        print("ROOT")
        #convert to string
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')
        print("XMLSTR")
        #convert to json
        parser = etree.XMLParser(recover=True)
        bf = BadgerFish(dict_type=OrderedDict)
        jsonstr = bf.data(ET.fromstring(xmlstr, parser=parser))
        print("JSONSTR")

        return Callback(True, "File has been converted", jsonstr)
    except Exception as exc:
        print("solutions_services.convertXMLtoJSON ERROR: ", exc)
        return Callback(False, "An error occured while converting xml file")

def getJSONByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).filter(Solution.AssistantID == assistantID).first()
        if not result: raise Exception

        return Callback(True, 'JSON has been successfully retrieved', result)

    except Exception as exc:
        print("solutions_services.getJSONByAssistantID ERROR/EMPTY: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve JSON')

def createUpdateJSONByAssistantID(assistantID, content):
    try:
        # Get result and check if None then raise exception
        result = getJSONByAssistantID(assistantID)
        if not result.Success: createNew(assistantID, content)

        result.Content = content

        db.session.commit()

        return Callback(True, 'Solutions file has been updated')

    except Exception as exc:
        print("solutions_services.createUpdateJSONByAssistantID ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not update solutions file')
