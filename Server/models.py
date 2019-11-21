import json
from sqlite3 import Connection as SQLite3Connection

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, types
from sqlalchemy.engine import Engine
from sqlalchemy.ext import mutable

db = SQLAlchemy()

# Activate Foreign Keys
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()

    # if not isinstance(dbapi_connection, SQLite3Connection):
    #     cursor.execute("SET wait_timeout=31536000;")
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class JsonEncodedDict(types.TypeDecorator):
    """Stores and retrieves JSON as TEXT."""
    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

# TypeEngine.with_variant says "use StringyJSON instead when connecting to 'sqlite'"
MagicJSON = types.JSON().with_variant(JsonEncodedDict, 'sqlite')
mutable.MutableDict.associate_with(JsonEncodedDict)

class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data

# ============= Models ===================


from schemas.Appointment import Appointment
Appointment: Appointment = Appointment

from schemas.Conversation import Conversation
Conversation: Conversation = Conversation

from schemas.Assistant import Assistant
Assistant: Assistant = Assistant

from schemas.AutoPilot import AutoPilot
AutoPilot: AutoPilot = AutoPilot

from schemas.Calendar import Calendar
Calendar: Calendar = Calendar

from schemas.Candidate import Candidate
Candidate: Candidate = Candidate

from schemas.Company import Company
Company: Company = Company

from schemas.Campaign import Campaign
Campaign: Campaign = Campaign

from schemas.Conversation import Conversation
Conversation: Conversation = Conversation

from schemas.CRM import CRM
CRM: CRM = CRM


from schemas.CRMAutopilot import CRMAutopilot
CRMAutopilot: CRMAutopilot = CRMAutopilot

from schemas.Database import Database
Database: Database = Database

from schemas.Job import Job
Job: Job = Job

from schemas.Newsletter import Newsletter
Newsletter: Newsletter = Newsletter

from schemas.Messenger import Messenger
Messenger: Messenger = Messenger

from schemas.AppointmentAllocationTime import AppointmentAllocationTime
AppointmentAllocationTime: AppointmentAllocationTime = AppointmentAllocationTime

from schemas.AppointmentAllocationTimeInfo import AppointmentAllocationTimeInfo
AppointmentAllocationTimeInfo: AppointmentAllocationTimeInfo = AppointmentAllocationTimeInfo

from schemas.Role import Role
Role: Role = Role

from schemas.StoredFile import StoredFile
StoredFile: StoredFile = StoredFile

from schemas.StoredFileInfo import StoredFileInfo
StoredFileInfo: StoredFileInfo = StoredFileInfo

from schemas.Webhook import Webhook
Webhook: Webhook = Webhook

from schemas.User import User
User: User = User

from schemas.ShortenedURL import ShortenedURL
ShortenedURL: ShortenedURL = ShortenedURL

# =================== Triggers ============================

# Example of how triggers works
# Also check: https://docs.sqlalchemy.org/en/latest/orm/session_events.html

# @event.listens_for(Assistant, 'before_insert')
# def receive_after_insert(mapper, connection, target):
#     print("before_insert")
#     print(mapper)
#     print(target) # prints Assistant

# @event.listens_for(Conversation, 'before_delete')
# def receive_after_insert(mapper, connection, target):
#     print("before_delete")
#     print(target) # prints Conversation
#
#
# @event.listens_for(Conversation, 'after_delete')
# def receive_after_insert(mapper, connection, target):
#     print("after_delete")
#     print(target) # prints Conversation