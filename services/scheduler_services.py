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
    now = datetime.now()

    # make it more efficient by only querying what is nbuecessary maybe
    notify = {'6hrs': {'data':[], 'lastSent': None}, 'daily': [], 'weekly': []}
    try:
        notifications = helpers.getDictFromLimitedQuery(["LastSentDate", "Type"],
                             db.session.query(Notifications.LastSentDate, Notifications.Type).all())
        monthlyUses = helpers.getDictFromLimitedQuery(["NotifyEvery", "Name", "Email"],
                              db.session.query(Assistant.NotifyEvery, Assistant.Name, User.Email) \
                                .filter(Assistant.NotifyEvery != "never") \
                                .filter(Assistant.CompanyID == User.CompanyID) \
                                .all())
        for obj in notifications:
            notify[obj['Type']].append()
        for obj in monthlyUses:
            notify[obj['NotifyEvery']].append(obj)
        # if now.weekday() == 0:
        #     for i in notify['weekly']:
        #         #send email?
        # if now.hour % 6 == 0:
        #     for i in notify['6hrs']:
        #         #send email?
        # if now.hour == 0:
            # for i in notify['daily']:
    except Exception as e:
        print(e)
        # return Callback(False, 'Analytics could not be gathered')
#
# @scheduler.scheduled_job('interval', seconds=6)
# def notifyUserAboutChats():
#     getNextInterval()



# @scheduler.scheduled_job('cron', id='kekistan', hour='every 6')
# def notifyUserAboutChats():
    # print('lol')

# print(db)

# scheduler.add_job(getNextInterval, 'cron', second='*/6', id='hourly', replace_existing=True)
# scheduler.add_job(getNextInterval, 'cron', second='*/6', id='daily', replace_existing=True)
# scheduler.add_job(getNextInterval, 'cron', second='*/6', id='weekly', replace_existing=True)

now = datetime.now()
kek = now.replace(hour=0, minute=0, second=0)
# print(kek)




# print("lol")
scheduler.start()
# job = scheduler.add_job(func=tasks.printSomething, trigger='interval', seconds=5)                                                                                                                          id="3559a1946b52419899e8841d4317d194", replace_existing=True)
# job = scheduler.get_job("3559a1946b52419899e8841d4317d194")
#
#
# scheduler.start()
# task: Task = Task(ApschedulerJobID1="3559a1946b52419899e8841d4317d194")
# db.session.add(task)
# print(task.ApschedulerJobID1)
# db.session.commit()
# scheduler.reschedule_job(job_id="3559a1946b52419899e8841d4317d194",trigger='interval', seconds=10)