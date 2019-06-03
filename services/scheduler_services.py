from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
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
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


# job = scheduler.add_job(func=tasks.printSomething, trigger='interval', seconds=5,
#                         id="3559a1946b52419899e8841d4317d194", replace_existing=True)
# # job = scheduler.get_job("3559a1946b52419899e8841d4317d194")
#
#
# scheduler.start()
# task: Task = Task(ApschedulerJobID1="3559a1946b52419899e8841d4317d194")
# db.session.add(task)
# print(task.ApschedulerJobID1)
# db.session.commit()
# scheduler.reschedule_job(job_id="3559a1946b52419899e8841d4317d194",trigger='interval', seconds=10)