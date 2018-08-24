import sqlalchemy.exc
from models import db, Statistics, Callback

def getStatistics(assistantID):
    try:
        result = db.session.query(Statistics).get(assistantID)
        if not result: result = []

        return Callback(True, 'Statistics Found.',
                        result)
    except Exception as e:
        return Callback(False, 'Could not find a statistics with assistantID: ' + assistantID)