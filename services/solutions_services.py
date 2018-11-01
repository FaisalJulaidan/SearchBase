import sqlalchemy.exc
import re
from models import db,Callback,Solution, Assistant
from sqlalchemy import func, exists
from utilities import helpers
from sqlalchemy.ext.mutable import MutableDict
from services import userInput_services, mail_services

import xml.etree.ElementTree as ET
from json import dumps
from collections import OrderedDict
from xmljson import BadgerFish
from lxml import etree


import time #used for checking code execution time

def getSolutionsSortKey(item):
    result = 0
    for key,value in item["matches"].items():
        result += value
    return result

# Scoring System
def getBasedOnKeywords(assistantID, keywords: list, max=999999) -> Callback:

    try:
        # Get solutions
        t0 = time.time()
        solution = db.session.query(Solution).filter(Solution.AssistantID == assistantID).first()
        if not solution:
            return Callback(True, "There are no solutions associated with this assistant", None)
        t2 = time.time()

        result = getSolutions(solution.Content, keywords)
        t3 = time.time()

        result = sorted(result, key=getSolutionsSortKey, reverse=True)
        # for c in result:
        #     print(c["matches"])
        result = result[0:max]
        t5 = time.time()

        print("Time to get JSON from DB: ", t2-t0)
        print("Time to get solutions from JSON: ", t3-t2)
        print("Total Time: ", t5-t0)

        return Callback(True, 'Solutions based on keywords retrieved successfully!!', result)
    except Exception as exc:
        print("solutions_services.getBasedOnKeywords() ERROR: ", exc)
        return Callback(False, 'Solutions could not be retrieved at this time')

def getSolutions(content, keywords):
    try:
        jobs = content["{http://tempuri.org/JSExport.xsd}JobShopExport"]["{http://tempuri.org/JSExport.xsd}Jobs"]["{http://tempuri.org/JSExport.xsd}Job"]
        result = []
        matches = ""
        originalString = dumps(content).split("SysKeys")[1]
        for value in jobs:
            matches = loopThroughAllJSON(value, {"command":"get solutions", "value":keywords}, originalString, {})
            if matches:
                result.append({"data": value, "matches": matches})
        return result
    except Exception as exc:
        print("solutions_services.getSolutions ERROR: ", exc)
        return result

def loopThroughAllJSON(item, action, originalString="", result={}):
    try:
        if type(item) is dict or type(item) is MutableDict:
            for key,value in item.items():
                result = actOnJSONItem(action, key, originalString, result)
                loopThroughAllJSON(item[key], action, originalString, result)
        elif type(item) is list:
            for value in item:
                result = actOnJSONItem(action, value, originalString, result)
                loopThroughAllJSON(value, action, originalString, result)
        else:
            result = actOnJSONItem(action, item, originalString, result)
        return result
    except Exception as exc:
        print("solutions_services.loopThroughAllJSON ERROR: ", exc)
        return result

def actOnJSONItem(action, item, originalString, result):
    try:
        if action["command"] == "print":
            print("JSON Item: ", item)
        elif action["command"] == "get solutions":
            if type(item) is int:
                try:
                    item = originalString.split('DBID": '+str(item)+', "@Desc": "')[1].split('"')[0]
                except:
                    pass
            if type(item) is str:
                item = item.lower()
                for keyword in action["value"]:
                    keyword = str(keyword).lower()
                    if keyword in item:
                        if keyword in result:
                            result[keyword] += 1
                        else:
                            result[keyword] = 1
        return result
    except Exception as exc:
        print("solutions_services.actOnJSONItem ERROR: ", exc)
        return result

def replaceIDsWithDataRBD(content):
    jobs = content["{http://tempuri.org/JSExport.xsd}JobShopExport"]["{http://tempuri.org/JSExport.xsd}Jobs"]["{http://tempuri.org/JSExport.xsd}Job"]
    IDsString = dumps(content).split("SysKeys")[1]

    result = convertionLoopRDB(jobs, IDsString)
    content["{http://tempuri.org/JSExport.xsd}JobShopExport"]["{http://tempuri.org/JSExport.xsd}Jobs"]["{http://tempuri.org/JSExport.xsd}Job"] = result

    return content

def convertionLoopRDB(item, IDsString):
    try:
        if type(item) is dict or type(item) is MutableDict or type(item) is OrderedDict:
            for key,value in item.items():
                item[key] = convertionLoopRDB(value, IDsString)
        elif type(item) is list:
            for value in item:
                item[item.index(value)] = convertionLoopRDB(value, IDsString)
        else:
            if type(item) is int:
                try:
                    item = IDsString.split('DBID": '+str(item)+', "@Desc": "')[1].split('"')[0]
                except Exception as exc:
                    print(exc)
                    pass
        return item
    except Exception as exc:
        print("solutions_services.loopThroughAllJSON ERROR: ", exc)
        return item

def createNew(assistantID, content):
    try:
        # Create a new user with its associated company and role
        content = replaceIDsWithDataRBD(content)
        #print(content)
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
        solution.Content = replaceIDsWithDataRBD(content)

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
        #get start and all of xml in written format
        root = tree.getroot()
        #convert to string
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')
        #convert to json
        parser = etree.XMLParser(recover=True)
        bf = BadgerFish(dict_type=OrderedDict)
        jsonstr = bf.data(ET.fromstring(xmlstr, parser=parser))

        return Callback(True, "File has been converted", jsonstr)
    except Exception as exc:
        print("solutions_services.convertXMLtoJSON ERROR: ", exc)
        return Callback(False, "An error occured while converting xml file")

def getSolutionByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Solution).filter(Solution.AssistantID == assistantID).first()
        if not result: raise Exception

        return Callback(True, 'JSON has been successfully retrieved', result)

    except Exception as exc:
        print("solutions_services.getSolutionByAssistantID ERROR/EMPTY: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not retrieve JSON')

def createUpdateJSONByAssistantID(assistantID, content):
    try:
        # Get result and check if None then raise exception
        result = getSolutionByAssistantID(assistantID)
        if not result.Success: createNew(assistantID, content)

        result.Content = content

        db.session.commit()

        return Callback(True, 'Solutions file has been updated')

    except Exception as exc:
        print("solutions_services.createUpdateJSONByAssistantID ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not update solutions file')

def sendSolutionsAlerts(assistantID):
    try:
        userInput_callback : Callback = userInput_services.getByAssistantID(assistantID)
        if not userInput_callback.Success: raise Exception("Error in retrieving user input")

        filterEmails_callback : Callback = userInput_services.filterForContainEmails(userInput_callback.Data)
        if not filterEmails_callback.Success: raise Exception("Error in filtering for emails")

        errors = 0

        for record in filterEmails_callback.Data:
            keywords = []
            for inputs in record["record"]:
                keywords += inputs['keywords']
            solutions_callback : Callback = getBasedOnKeywords(assistantID, keywords, 5)
            if not solutions_callback.Success: raise Exception("Error in getting solutions")
            if not solutions_callback.Data: continue

            sendMail_callback : Callback = mail_services.sendSolutionAlert(record, solutions_callback.Data)
            if not sendMail_callback.Success: errors += 1

        if errors > 0: return Callback(True, 'Alerts have been sent however there was an error with sending the email to ' + str(errors) + " users.")

        return Callback(True, 'Alerts have been sent.')

    except Exception as exc:
        print("solutions_services.sendJobAlerts ERROR: ", exc)
        return Callback(False, 'Could not send alerts at this time')

def switchAutomaticSolutionAlerts(assistantID, setTo):
    try:
        result = getSolutionByAssistantID(assistantID)
        if not result.Success: raise Exception("Could not find alerts record")

        result.automaticSolutionAlerts = setTo

        db.session.commit()

        return Callback(True, 'Automatic alerts have been set.')

    except Exception as exc:
        print("solutions_services.switchAutomaticSolutionAlerts ERROR: ", exc)
        db.session.rollback()
        return Callback(False, 'Could not set automatic alerts at this time. Please insure you have a database connected or uploaded')
