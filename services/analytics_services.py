import sqlalchemy.exc
from models import db, Statistics, Callback, ChatbotSession, Assistant, Solution
from datetime import datetime, timedelta
from sqlalchemy.sql import exists, func


def getAnalytics(assistant, daysOvertime: int, topSolustions: int):
    id = assistant.ID
    try:
        result = {'usersOvertime': getUsersOvertime(id, daysOvertime),
                  'popularSolutions': getPopularSolutions(id, topSolustions),
                  'totalReturnedSolutions': getTotalReturnedSolutions(id),
                  'timeSpentAvgOvertime': getTimeSpentAvgOvertime(id, daysOvertime)}

        return Callback(True, 'Analytics processed successfully.', result)
    except Exception as e:
        return Callback(False, 'Error while finding analytics', e.args)


def getUsersOvertime(assistantID, days):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).first()[0]
    print(oldestDate)
    now = datetime.now()
    datetime.now().strftime('%Y-%m-%d')
    print(now.strftime('%Y-%m-%d'))
    result = []
    while True:
        current = now
        now -= timedelta(days=days)
        result.append({'x': now.strftime('%Y-%m-%d'), 'y':db.session.query(ChatbotSession).filter(
            ChatbotSession.AssistantID == assistantID,
            ChatbotSession.DateTime < current,
            ChatbotSession.DateTime >= now).count()})
        if now < oldestDate:
            break
    return result


def getPopularSolutions(assistantID, top=5):
    return db.session.query(Solution.SolutionID, Solution.MajorTitle, Solution.TimesReturned).filter(Solution.AssistantID == assistantID)\
        .order_by(Solution.TimesReturned.desc()).limit(top).all()


def getTotalReturnedSolutions(assistantID):
    return db.session.query(func.sum(Solution.TimesReturned)).filter(Solution.AssistantID == assistantID).first()[0]


def getTimeSpentAvgOvertime(assistantID, days):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).scalar()
    print(oldestDate)
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
