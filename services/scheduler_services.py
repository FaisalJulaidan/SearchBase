from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from models import db, Callback, Assistant, User, Notifications
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

def getNextInterval():
    try:
        now = datetime.now()
        monthlyUses = helpers.getDictFromLimitedQuery(["NotifyEvery", "Name", "Email", "LastSentDate"],
                          db.session.query(Assistant.NotifyEvery, Assistant.Name, User.Email, Notifications.LastSentDate) \
                                .filter(Assistant.NotifyEvery != None) \
                                .outerjoin(Notifications) \
                                .filter(Assistant.CompanyID == User.CompanyID) \
                                .all())
        users = []
        for record in monthlyUses:
            if record['LastSentDate'] == None:
                #Send first notification
                print('sending first notification')
                continue
            if ((now - record['LastSentDate']).total_seconds()/86400) > record['NotifyEvery']:
                #Send new notification
                print('sending new notification')
    except Exception as e:
        print(e)

scheduler.add_job(getNextInterval, 'cron', hour='*/1', id='hourly', replace_existing=True)
scheduler.start()