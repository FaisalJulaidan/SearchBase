from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from models import db, Callback, Assistant, User
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
0 - Immediately notify
any other number - notify after x hours
'''


scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

# If assistantID is supplied, it will only look for data relating to that assistant
def getNextInterval(assistantID=None):
    try:
        helpers.HPrint('kek')
        now = datetime.now()
        query =  db.session.query(Assistant.ID, Assistant.NotifyEvery, Assistant.Name, User.Email, Assistant.LastNotificationDate) \
            .filter(Assistant.NotifyEvery != None) \
            .filter(Assistant.CompanyID == User.CompanyID)

        if assistantID != None:
            query.filter(Assistant.ID == assistantID)

        monthlyUses = helpers.getDictFromLimitedQuery(["AssistantID", "NotifyEvery", "Name", "Email", "LastNotificationDate"],
                         query.all())

        for record in monthlyUses:
            if ((now - record['LastNotificationDate']).total_seconds()/86400) > record['NotifyEvery'] \
                    or record['LastNotificationDate'] == None:
                db.session.query(Assistant).filter(Assistant.ID == record['AssistantID']).update({'LastNotificationDate': now})
    except Exception as e:
        print(e)


scheduler.add_job(getNextInterval, 'cron', second='*/5', id='hourly', replace_existing=True)
scheduler.start()