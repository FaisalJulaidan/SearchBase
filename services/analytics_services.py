import sqlalchemy.exc
from models import db, Statistics, Callback, ChatbotSession, Assistant, Solution
from datetime import datetime, timedelta
from monthdelta import monthdelta
from sqlalchemy.sql import exists, func, extract
import random


def getAnalytics(assistant, daysOvertime: int, topSolustions: int):
    id = assistant.ID
    # 'usersOvertime': getUsersOvertime(id, daysOvertime)
    try:
        result = {
                  'popularSolutions': getPopularSolutions(id, topSolustions),
                  'totalReturnedSolutions': getTotalReturnedSolutions(id),
                  'timeSpentAvgOvertime': getTimeSpentAvgOvertime(id, daysOvertime),
                  'TotalQuestionsOverMonth':getTotalQuestionsOverMonth(id),
                  'TotalSolutionsOverMonth':getTotalSolutionsOverMonth(id)}


        return Callback(True, 'Analytics processed successfully.', result)
    except Exception as e:
        print(e)
        return Callback(False, 'Error while finding analytics', e.args)


def getUsersOvertime(assistantID, days):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).first()[0]
    newestDate = db.session.query(func.max(ChatbotSession.DateTime)).first()[0]
    print(oldestDate)
    now = datetime.now()
    # print(now.split('-')[0])
    # print(now.strftime('%Y-%m-%d'))
    result = []
    print(1)
    begginingOfYear = datetime.strptime(str(now).split('-')[0]+"-01-01",'%Y-%m-%d')
    endOfYear = datetime.strptime(str(now).split('-')[0]+"-12-30",'%Y-%m-%d')
    while True:
        print(2)
        current = now
        now -= timedelta(days=days)

        print(3)
        if now > oldestDate:
            print("ADDED")
            result.append({'x': now.strftime('%Y-%m-%d'), 'y':db.session.query(ChatbotSession).filter(
                ChatbotSession.AssistantID == assistantID,
                ChatbotSession.DateTime < current,
                ChatbotSession.DateTime >= now).count()})
        else:
            print(4)
            print(now, " ", datetime.strptime(str(now).split('-')[0]+"-01-01",'%Y-%m-%d'))
            if now > begginingOfYear:
                print(5)
                result.append({'x':now.strftime('%Y-%m-%d'), 'y':random.randint(1,5)})
            else:
                print(6)
                break
    now = datetime.now()
    while True:
        now += timedelta(days=days)
        if now >= newestDate:
            if now < endOfYear:
                result = [{'x': now.strftime('%Y-%m-%d'), 'y': random.randint(1,5)}] + result
            else:
                break
    print(result)
    return result


def getTotalQuestionsOverMonth(assistantID):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    now = datetime.now()

    result = []
    while True:
        current = now

        print(now.month)


        # total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
        #     ChatbotSession.AssistantID == assistantID,
        #     ChatbotSession.DateTime < current,
        #     ChatbotSession.DateTime >= now).scalar()
        total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
                ChatbotSession.AssistantID == assistantID,
                extract('month', ChatbotSession.DateTime) == now.month,
                ).scalar()
        print(total)
        if not total:
            total = 0
        result.append(total)
        now -= monthdelta(1)
        if now.year < oldestDate.year:
            break
    print(result)
    return result

def getTotalSolutionsOverMonth(assistantID):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    now = datetime.now()

    result = []
    while True:
        current = now

        print("now.weekday():", now.weekday())


        # total = db.session.query(func.sum(ChatbotSession.QuestionsAnswered)).filter(
        #     ChatbotSession.AssistantID == assistantID,
        #     ChatbotSession.DateTime < current,
        #     ChatbotSession.DateTime >= now).scalar()
        total = db.session.query(func.sum(ChatbotSession.SolutionsReturned)).filter(
                ChatbotSession.AssistantID == assistantID,
                extract('month', ChatbotSession.DateTime) == now.month,
                ).scalar()
        print(total)
        if not total:
            total = 0
        result.append(total)
        now -= monthdelta(1)
        if now.year < oldestDate.year:
            break
    print(result)
    return result


def getPopularSolutions(assistantID, top=5):
    return db.session.query(Solution.SolutionID, Solution.MajorTitle, Solution.TimesReturned).filter(Solution.AssistantID == assistantID)\
        .order_by(Solution.TimesReturned.desc()).limit(top).all()


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
