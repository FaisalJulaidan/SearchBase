import sqlalchemy.exc
from models import db, Statistics, Callback, ChatbotSession, Assistant, Solution
from datetime import datetime, timedelta
from monthdelta import monthdelta
from sqlalchemy.sql import exists, func, extract
import random


def getAnalytics(assistant, periodSpace: int, topSolustions: int):
    id = assistant.ID
    try:
        result = {
                  'popularSolutions': getPopularSolutions(id, topSolustions),
                  'totalReturnedSolutions': getTotalReturnedSolutions(id),
                  'timeSpentAvgOvertime': getTimeSpentAvgOvertime(id, periodSpace),
                  'TotalQuestionsOverMonth':getTotalQuestionsOverMonth(id),
                  'UsersOvertime': getUsersOvertime(id, periodSpace),
                  'TotalSolutionsOverMonth':getTotalSolutionsOverMonth(id),
                  'TotalUsers': getTotalUsers(id)}


        return Callback(True, 'Analytics processed successfully.', result)
    except Exception as e:
        print("getPopularSolutions(id, topSolustions): ", getPopularSolutions(id, topSolustions))
        print("getTotalReturnedSolutions(id): ", getTotalReturnedSolutions(id))
        print("getTimeSpentAvgOvertime(id, periodSpace): ", getTimeSpentAvgOvertime(id, periodSpace))
        print("getTotalQuestionsOverMonth(id): ", getTotalQuestionsOverMonth(id))
        print("getUsersOvertime(id, periodSpace): ", getUsersOvertime(id, periodSpace))
        print("getTotalSolutionsOverMonth(id): ", getTotalSolutionsOverMonth(id))
        print("getTotalUsers(id): ", getTotalUsers(id))
        print(e)
        return Callback(False, 'Error while finding analytics')

def getUsersOvertime(assistantID, periodSpace):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).first()[0]
    newestDate = db.session.query(func.max(ChatbotSession.DateTime)).first()[0]
    now = datetime.now()
    result = []
    begginingOfYear = datetime.strptime(str(now).split('-')[0]+"-01-01",'%Y-%m-%d')
    endOfYear = datetime.strptime(str(now).split('-')[0]+"-12-30",'%Y-%m-%d')
    if not oldestDate: 
        oldestDate = begginingOfYear
        newestDate = endOfYear
    while True:
        current = now
        now -= timedelta(days=7 * periodSpace)

        if current >= oldestDate:
            result.append({'x': now.strftime('%Y-%m-%d'), 'y':db.session.query(ChatbotSession).filter(
                ChatbotSession.AssistantID == assistantID,
                ChatbotSession.DateTime < current,
                ChatbotSession.DateTime >= now).count()})
        else:
            if current >= begginingOfYear:
                #result.append({'x':now.strftime('%Y-%m-%d'), 'y':random.randint(420,500)}) random data for empty
                result.append({'x':now.strftime('%Y-%m-%d'), 'y':0})
            else:
                break
    now = datetime.now()
    while True:
        now += timedelta(days=7 * periodSpace)
        if now >= newestDate:
            if now <= endOfYear:
                #result = [{'x': now.strftime('%Y-%m-%d'), 'y': random.randint(360,500)}] + result random data for empty
                result = [{'x': now.strftime('%Y-%m-%d'), 'y':0}] + result
            else:
                break
    return result

def getTotalUsersForCompany(assistants):
    try:
        totalClicks = 0

        for assistant in assistants:
            totalClicks += db.session.query(ChatbotSession).filter( ChatbotSession.AssistantID == assistant.ID, ChatbotSession.DateTime < datetime.now()).count()
            
        return Callback(True, 'Users successfully counted.', totalClicks)
    except Exception as e:
        print("analytics_services.getTotalUsersForCompany() ERROR: ", e)
        return Callback(False, 'Error while counting Users.')

def getTotalUsers(assistantID):

    return db.session.query(ChatbotSession).filter( ChatbotSession.AssistantID == assistantID, ChatbotSession.DateTime < datetime.now()).count()

def getTotalQuestionsOverMonth(assistantID):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    now = datetime.now()

    result = []
    while True:
        current = now


        # total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
        #     ChatbotSession.AssistantID == assistantID,
        #     ChatbotSession.DateTime < current,
        #     ChatbotSession.DateTime >= now).scalar()
        total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
                ChatbotSession.AssistantID == assistantID,
                extract('month', ChatbotSession.DateTime) == now.month,
                ).scalar()
        if not total:
            total = 0
        result.append([now.month, total])
        now -= monthdelta(1)
        if now.year < oldestDate.year:
            break
    position = 0
    returnArray = []
    for i in range(12,0,-1):
        if not result: 
            returnArray.append(0)
            continue
        if result[position][1] == 0:
            del result[position]
        if position >= len(result): 
            returnArray.append(0)
            continue
        if not i == result[position][0]:
            returnArray.append(0)
        else:
            returnArray.append(result[position][1])
            result[position] = result[position][1]
            position += 1
    print(returnArray)
    return returnArray

def getTotalSolutionsOverMonth(assistantID):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    now = datetime.now()

    result = []
    while True:
        current = now


        # total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
        #     ChatbotSession.AssistantID == assistantID,
        #     ChatbotSession.DateTime < current,
        #     ChatbotSession.DateTime >= now).scalar()
        total = db.session.query(func.sum(ChatbotSession.SolutionsReturned)).filter(
                ChatbotSession.AssistantID == assistantID,
                extract('month', ChatbotSession.DateTime) == now.month,
                ).scalar()
        if not total:
            total = 0
        result.append([now.month, total])
        now -= monthdelta(1)
        if now.year < oldestDate.year:
            break
    position = 0
    returnArray = []
    for i in range(12,0,-1):
        if not result:
            returnArray.append(0)
            continue
        if result[position][1] == 0:
            del result[position]
        if position >= len(result): 
            returnArray.append(0)
            continue
        if not i == result[position][0]:
            returnArray.append(0)
        else:
            returnArray.append(result[position][1])
            result[position] = result[position][1]
            position += 1
    print(returnArray)
    return returnArray


def getPopularSolutions(assistantID, top=5):
    return db.session.query(Solution.SolutionID, Solution.MajorTitle, Solution.TimesReturned).filter(Solution.AssistantID == assistantID)\
        .order_by(Solution.TimesReturned.desc()).limit(top).all()


def getTotalReturnedSolutionsForCompany(assistants):
    try:
        total = 0

        for assistant in assistants:
            timersReturned = db.session.query(func.sum(Solution.TimesReturned)).filter(Solution.AssistantID == assistant.ID).first()[0]
            if timersReturned:
                total += timersReturned

        return Callback(True, 'Solutions number retrieved', total)
    except Exception as e:
        print("analytics_services.getTotalReturnedSolutionsForCompany() ERROR: ", e)
        return Callback(False, 'Error while counting solutions.')

def getTotalReturnedSolutions(assistantID):
    return db.session.query(func.sum(Solution.TimesReturned)).filter(Solution.AssistantID == assistantID).first()[0]


def getTimeSpentAvgOvertime(assistantID, days):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    now = datetime.now()

    result = []
    while True:
        current = now
        now -= timedelta(days=days)
        avg =db.session.query(func.avg(ChatbotSession.TimeSpent)).filter(
            ChatbotSession.AssistantID == assistantID,
            ChatbotSession.DateTime < current,
            ChatbotSession.DateTime >= now).scalar()
        if not avg:
            avg = 0
        result.append(avg)
        if now < oldestDate:
            break

    return result
