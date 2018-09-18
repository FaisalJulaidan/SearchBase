import sqlalchemy.exc
from models import db, Statistics, Callback, ChatbotSession, Assistant
from datetime import datetime, timedelta
from sqlalchemy.sql import exists, func


def getStatistics(assistantID):
    try:
        result = db.session.query(Statistics).get(assistantID)
        if not result: result = []

        return Callback(True, 'Statistics Found.',
                        result)
    except Exception as e:
        return Callback(False, 'Could not find a statistics with assistantID: ' + assistantID)


def getActiveUsersInYear(assistant: Assistant, days):

    oldestDate = db.session.query(func.min(ChatbotSession.DateTime)).first()[0]
    print(oldestDate)
    now = datetime.now()

    result = []
    while(True):
        current = now
        now -= timedelta(days=days)
        result.append(db.session.query(ChatbotSession).filter(
            ChatbotSession.DateTime < current,
            ChatbotSession.DateTime >= now)
            .count())
        if now < oldestDate:
            break
    print(result)