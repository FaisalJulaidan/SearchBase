from datetime import datetime
from utilities import helpers
from datetime import timedelta
from sqlalchemy.sql import between
from models import db, Callback, Conversation

#fix datetime

def getAnalytics(assistant, startDate=datetime.now() - timedelta(days=365), endDate=datetime.now()):
    """ Gets analytics for the provided assistant """
    """ startDate defaults to a year ago, and the end date defaults to now, gathering all data for the past year """
    """ currently only gathers amount of conversations held """

    #need to fiugre out whether the start and end dates will affect the whole page, or just the chart hmm

    try:
        monthlyUses = db.session.query(Conversation.ID,
                                    Conversation.DateTime,
                                    Conversation.TimeSpent,
                                    Conversation.ApplicationStatus,
                                    Conversation.Score,
                                    Conversation.UserType)\
                                .filter(between(Conversation.DateTime, startDate, endDate))\
                                .filter(Conversation.AssistantID == assistant.ID) \
                                .all()

        return Callback(True, 'Analytics successfully gathered', monthlyUses)
    except Exception as exc:
        helpers.logError("analytics_services.getAnalytics(): " + str(exc))
        return Callback(False, 'Analytics could not be gathered')

