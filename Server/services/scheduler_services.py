# import os
# from datetime import datetime
#
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
# from pytz import utc
# from sqlalchemy import and_
# from sqlalchemy.orm import joinedload
#
# from models import db, Callback, Assistant, Conversation, Company
# from services import mail_services
# from utilities import helpers
#
# jobstores = {
#     'default': SQLAlchemyJobStore(url=os.environ['SQLALCHEMY_DATABASE_URI'])
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     # 'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 1
# }
#
#
# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


''' 
Types:
 Null - Never notify
 0 - Immediately: notify but it should not because conversation are already been notified immediately
 Any other number - Notify after x hours
'''

# If assistantID is supplied, it will only look for data relating to that assistant
def sendConversationsNotifications(event, context):
    print(context)
    print("FASIAL FAISAL FIASLALS L FLSELFWLE")
    print(event)
    # try:
    #     from app import app
    #     with app.app_context():
    #         #NEEDS STORED FILEREIMPLEMENTED
    #         now = datetime.now()
    #         assistantsQuery = db.session.query(Assistant).options(joinedload("Company").joinedload("StoredFile").joinedload("StoredFileInfo")) \
    #             .filter(and_(Assistant.NotifyEvery))
    #
    #         if assistantID != None:
    #             assistantsQuery.filter(Assistant.ID == assistantID)
    #
    #         assistants = assistantsQuery.all()
    #
    #         for assistant in assistants:
    #             # Assistant will not get notified in the first passed hour after their notification set active
    #             if not assistant.LastNotificationDate:
    #                 db.session.query(Assistant).filter(Assistant.ID == assistant.ID)\
    #                     .update({'LastNotificationDate': now})
    #
    #             # Check if NotifyEvery hours have passed
    #             elif ((now - assistant.LastNotificationDate).total_seconds()/86400) > assistant.NotifyEvery :
    #
    #                 # Fetch conversation that happen after LastNotificationDate
    #                 conversations = db.session.query(Conversation)\
    #                     .filter(and_(Conversation.DateTime > assistant.LastNotificationDate,
    #                                  Conversation.AssistantID == assistant.ID))\
    #                     .all()
    #
    #                 if len(conversations) > 0:
    #                     callback: Callback = mail_services.notifyNewConversations(assistant, conversations, assistant.LastNotificationDate)
    #                     if not callback.Success:
    #                         raise Exception(callback.Message)
    #
    #                 db.session.query(Assistant).filter(Assistant.ID == assistant.ID)\
    #                     .update({'LastNotificationDate': now})
    #
    #         # Save changes to the db
    #         db.session.commit()
    #
    # except Exception as e:
    #     helpers.logError(str(e))

#
# '''
# This function is to fix the constant lose of database connection after the wait_timeout has passed.
# It will make the simplest query to the database every while to make sure the connection is alive
# '''
# def pingDatabaseConnection():
#     try:
#         from app import app
#         with app.app_context():
#             db.engine.execute("SELECT NOW();")
#             db.session.commit()
#     except Exception as e:
#         helpers.logError("Ping! Database Connection ERROR: " + str(e))
#
#
# def test():
#     try:
#         print("TEST!!!")
#     except Exception as e:
#         print("ERROOORRR")
#
# # Run scheduled tasks
# scheduler.add_job(sendConversationsNotifications, 'cron', hour='*/1', id='sendConversationsNotifications', replace_existing=True)
# scheduler.add_job(pingDatabaseConnection, 'cron', hour='*/5', id='pingDatabaseConnection', replace_existing=True)
# # scheduler.add_job(test, 'cron', second='*/3', id='test', replace_existing=True)
