import os
from datetime import datetime, timedelta

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from sqlalchemy import and_, text
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func

from models import db, Callback, Assistant, Conversation, Company, AutoPilot
from services import mail_services
from services.Marketplace.CRM import crm_services
from utilities import helpers, enums

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


scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


''' 
Types:
 Null - Never notify
 0 - Immediately: notify but it should not because conversation are already been notified immediately
 Any other number - Notify after x hours
'''

# If assistantID is supplied, it will only look for data relating to that assistant
def sendConversationsNotifications(assistantID=None):
    try:
        from app import app
        with app.app_context():
            #NEEDS STORED FILEREIMPLEMENTED
            now = datetime.now()
            assistantsQuery = db.session.query(Assistant).options(joinedload("Company").joinedload("StoredFile").joinedload("StoredFileInfo")) \
                .filter(Assistant.NotifyEvery != None)
            if assistantID != None:
                assistantsQuery.filter(Assistant.ID == assistantID)

            assistants = assistantsQuery.all()

            for assistant in assistants:
                if not assistant.LastNotificationDate:
                    assistant.LastNotificationDate = now
                elif ((now - assistant.LastNotificationDate).total_seconds()/3600) > assistant.NotifyEvery :
                    # Fetch conversation that happen after LastNotificationDate
                    conversations = db.session.query(Conversation)\
                        .filter(and_(Conversation.DateTime > assistant.LastNotificationDate,
                                     Conversation.AssistantID == assistant.ID))\
                        .all()
                    if len(conversations) != 0:
                        assistant.LastNotificationDate = now
                        callback: Callback = mail_services.notifyNewConversations(assistant, conversations, assistant.LastNotificationDate)
                        if not callback.Success:
                            raise Exception(callback.Message)

            # Save changes to the db
            db.session.commit()

    except Exception as e:
        print('rah')
        helpers.logError(str(e))


# If assistantID is supplied, it will only look for data relating to that assistant
def sendAutopilotReferrals():
    try:
        from app import app
        with app.app_context():
            #NEEDS STORED FILEREIMPLEMENTED
            yesterday = datetime.now() - timedelta(days=1)
            now = datetime.now()
            autopilots = db.session.query(AutoPilot).filter(and_(AutoPilot.LastReferral != None, 24 <= func.TIMESTAMPDIFF(text('HOUR'), AutoPilot.LastReferral, yesterday))).all()

            for ap in autopilots:
                crm_callback = crm_services.getCRMByType(enums.CRM.Bullhorn, ap.CompanyID)
                if not crm_callback.Success:
                    raise Exception("Company is not connected to bullhorn")

                crm = crm_callback.Data
                params = [{"input": "dateBegin", "match": ap.LastReferral, "queryType": "BETWEEN", "match2": now}]
                search_callback = crm_services.searchPlacements(crm, ap.CompanyID, params)

                if not search_callback.Success:
                    raise Exception("Placement search failed")
                
                if len(search_callback.Data) == 0:
                    return

                ids = [item['candidate']['id'] for item in search_callback.Data]

                candidate_search = crm_services.searchCandidatesCustom(crm, ap.CompanyID, {"ids": ids}, customData=True, fields="fields=mobile,email")

                print("-----")
                print(candidate_search.Data)
                print("-----")
            # Save changes to the db
            db.session.commit()

    except Exception as e:
        print('rah')
        helpers.logError(str(e))

''' 
This function is to fix the constant lose of database connection after the wait_timeout has passed.
It will make the simplest query to the database every while to make sure the connection is alive
'''
def pingDatabaseConnection():
    try:
        from app import app
        with app.app_context():
            db.engine.execute("SELECT NOW();")
            db.session.commit()
    except Exception as e:
        helpers.logError("Ping! Database Connection ERROR: " + str(e))


def test():
    try:
        print("TEST!!!")
    except Exception as e:
        print("ERROOORRR")

# Run scheduled tasks
scheduler.add_job(sendConversationsNotifications, 'cron', hour='*/1', id='sendConversationsNotifications', replace_existing=True)
scheduler.add_job(pingDatabaseConnection, 'cron', hour='*/5', id='pingDatabaseConnection', replace_existing=True)
scheduler.add_job(sendAutopilotReferrals, 'cron', minute='*/3', id='sendAutopilotReferrals', replace_existing=True)
# scheduler.add_job(test, 'cron', second='*/3', id='test', replace_existing=True)
