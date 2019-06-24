from pytz import utc
from sqlalchemy import and_
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from models import db, Callback, Assistant, User, Conversation, Company
from services import mail_services
# import dateutil
from utilities import helpers
from datetime import date, datetime
import os

jobstores = {
    'default': SQLAlchemyJobStore(url=os.environ['SQLALCHEMY_DATABASE_URI'])
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

''' 
Types
Null - Never notify
0 - Immediately notify but it should not because conversation are already been notified
Any other number - notify after x hours
'''


scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

# If assistantID is supplied, it will only look for data relating to that assistant
def conversationsNotifications(assistantID=None):
    try:
        from app import app
        with app.app_context():

            now = datetime.now()
            assistantsQuery = db.session.query(Assistant.ID, Assistant.CompanyID, Company.Name ,Company.LogoPath, Assistant.NotifyEvery, Assistant.Name, Assistant.LastNotificationDate) \
                .join(Company)\
                .filter(and_(Assistant.NotifyEvery))

            if assistantID != None:
                assistantsQuery.filter(Assistant.ID == assistantID)

            assistants = helpers.getDictFromLimitedQuery(["ID", "CompanyID", "CompanyName", "LogoPath", "NotifyEvery",
                                                           "Name", "LastNotificationDate"],
                                                          assistantsQuery.all())

            for assistant in assistants:
                # Assistant will not get notified in the first passed hour after their notification set active
                if not assistant['LastNotificationDate']:
                    db.session.query(Assistant).filter(Assistant.ID == assistant['ID'])\
                        .update({'LastNotificationDate': now})

                # Check if NotifyEvery hours have passed
                elif ((now - assistant['LastNotificationDate']).total_seconds()/86400) + 1 > assistant['NotifyEvery'] :

                    # Fetch conversation that happen after LastNotificationDate
                    conversations = db.session.query(Conversation)\
                        .filter(and_(Conversation.DateTime > assistant['LastNotificationDate'],
                                     Conversation.AssistantID == assistant['ID']))\
                        .all()

                    if len(conversations) > 0:
                        callback: Callback = mail_services.notifyNewConversations(assistant, conversations, assistant['LastNotificationDate'])
                        if not callback.Success:
                            raise Exception(callback.Message)

                    db.session.query(Assistant).filter(Assistant.ID == assistant['ID'])\
                        .update({'LastNotificationDate': now})

            # Save changes to the db
            db.session.commit()

    except Exception as e:
        helpers.logError(str(e))


scheduler.add_job(conversationsNotifications, 'cron', hour='*/1', id='hourly', replace_existing=True)
# scheduler.start()