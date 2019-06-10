from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, event, types
from sqlalchemy.ext import mutable
from datetime import datetime, timedelta
import os
import json
import enums
from sqlalchemy_utils import PasswordType, CurrencyType

from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

db = SQLAlchemy(model_class=FlaskBaseModel)
db = initialize_flask_sqlathanor(db)
# Activate Foreign Keys
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
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


# ============= Models ===================

class Company(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False)
    URL = db.Column(db.String(250), nullable=False)
    LogoPath = db.Column(db.String(64), nullable=True)
    StripeID = db.Column(db.String(68), unique=True, nullable=False, )
    SubID = db.Column(db.String(68), unique=True, default=None)

    # Relationships:
    Users = db.relationship('User', back_populates='Company')
    Assistants = db.relationship('Assistant', back_populates='Company')
    Databases = db.relationship('Database', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')
    CRMs = db.relationship('CRM', back_populates='Company')
    AutoPilots = db.relationship('AutoPilot', back_populates='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Firstname = db.Column(db.String(64), nullable=False)
    Surname = db.Column(db.String(64), nullable=False)
    Email = db.Column(db.String(64), nullable=False)
    PhoneNumber = db.Column(db.String(30))
    Password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ))
    Verified = db.Column(db.Boolean(), nullable=False, default=False)

    TrackingData = db.Column(db.Boolean, nullable=False, default=False)
    TechnicalSupport = db.Column(db.Boolean, nullable=False, default=False)
    AccountSpecialist = db.Column(db.Boolean, nullable=False, default=False)
    UserInputNotifications = db.Column(db.Boolean, nullable=False, default=False)

    LastAccess = db.Column(db.DateTime(), nullable=True)
    CreatedOn = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Users')

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID', ondelete='SET NULL'))
    Role = db.relationship('Role', back_populates='Users')


    # __table_args__ = (db.UniqueConstraint('Email', name='uix1_user'),)

    def __repr__(self):
        return '<User {}>'.format(self.Email)


class Role(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64))
    EditChatbots = db.Column(db.Boolean(), nullable=False, default=False)
    EditUsers = db.Column(db.Boolean(), nullable=False, default=False)
    DeleteUsers = db.Column(db.Boolean(), nullable=False, default=False)
    AccessBilling = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Roles')

    Users = db.relationship('User', back_populates="Role")

    # Constraints:
    __table_args__ = (db.UniqueConstraint('Name', 'CompanyID', name='uix1_role'),)

    def __repr__(self):
        return '<Role {}>'.format(self.Name)


class Assistant(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Flow = db.Column(MagicJSON, nullable=True)
    Message = db.Column(db.String(500), nullable=False)
    TopBarText = db.Column(db.String(64), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0)

    NotifyEvery = db.Column(db.String(64), nullable=True)
    Active = db.Column(db.Boolean(), nullable=False, default=True)
    Config = db.Column(MagicJSON, nullable=True)

    # Relationships:
    #  - Bidirectional
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Assistants')

    CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID'))
    CRM = db.relationship('CRM', back_populates='Assistants')

    AutoPilotID = db.Column(db.Integer, db.ForeignKey('auto_pilot.ID'))
    AutoPilot = db.relationship("AutoPilot", back_populates="Assistants")

    # NotifySchedulerJobID = db.Column(db.Integer, db.ForeignKey('apscheduler_jobs.FakeID', ondelete='cascade'), nullable=True, unique=True)
    # NotifySchedulerJob = db.relationship('ApschedulerJobs', foreign_keys=[NotifySchedulerJobID], back_populates='NotifySchedulerJob')

    # - Many to one
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Conversations = db.relationship('Conversation', back_populates='Assistant')
    Appointments = db.relationship('Appointment', back_populates='Assistant')

    # Constraints:
    # cannot have two assistants with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)
    # db.CheckConstraint(NotifyEvery.in_(['never', 'immediately', '6hrs', 'daily', 'weekly'])


    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class Conversation(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Data = db.Column(MagicJSON, nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    TimeSpent = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    UserType = db.Column(Enum(enums.UserType), nullable=False)

    Completed = db.Column(db.Boolean, nullable=False, default=True)
    ApplicationStatus = db.Column(Enum(enums.ApplicationStatus), nullable=False, default=enums.ApplicationStatus.Pending)
    Score = db.Column(db.Float(), nullable=False)

    AcceptanceEmailSentAt = db.Column(db.DateTime(), default=None)
    RejectionEmailSentAt = db.Column(db.DateTime(), default=None)
    AppointmentEmailSentAt = db.Column(db.DateTime(), default=None)


    AutoPilotStatus = db.Column(db.Boolean, nullable=False, default=False)
    AutoPilotResponse = db.Column(db.String(250), nullable=True)

    CRMSynced = db.Column(db.Boolean, nullable=False, default=False)
    CRMResponse = db.Column(db.String(250), nullable=True)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Conversations')

    StoredFile = db.relationship('StoredFile', uselist=False, back_populates='Conversation')
    Appointment = db.relationship('Appointment', uselist=False, back_populates='Conversation')

    def __repr__(self):
        return '<Conversation {}>'.format(self.Data)


class AutoPilot(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Active = db.Column(db.Boolean, nullable=False, default=True)

    AcceptApplications = db.Column(db.Boolean, nullable=False, default=False)
    AcceptanceScore = db.Column(db.Float(), nullable=False, default=1)
    SendAcceptanceEmail = db.Column(db.Boolean, nullable=False, default=False)

    RejectApplications = db.Column(db.Boolean, nullable=False, default=False)
    RejectionScore = db.Column(db.Float(), nullable=False, default=0.05)
    SendRejectionEmail = db.Column(db.Boolean, nullable=False, default=False)

    SendCandidatesAppointments = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='AutoPilots')

    Assistants = db.relationship('Assistant', back_populates='AutoPilot')
    OpenTimeSlots = db.relationship('OpenTimeSlot', back_populates='AutoPilot')

    # Constraints:
    # cannot have two auto pilot with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_auto_pilot'),)

    def __repr__(self):
        return '<AutoPilot {}>'.format(self.ID)


class OpenTimeSlot(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Day = db.Column(db.Integer, nullable=False)
    From = db.Column(types.TIME, nullable=False)
    To = db.Column(types.TIME, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    AutoPilotID = db.Column(db.Integer, db.ForeignKey('auto_pilot.ID', ondelete='cascade'), nullable=False)
    AutoPilot = db.relationship('AutoPilot', back_populates='OpenTimeSlots')

    # Constraints:
    __table_args__ = (
        db.CheckConstraint(db.and_(Day >= 0, Day <= 6)), # 0 = Monday, 6 = Sunday
        db.CheckConstraint(From < To),
        db.CheckConstraint(db.and_(Duration > 0, Duration <= 60)),
        db.UniqueConstraint('Day','AutoPilotID', name='uix1_open_time_slot'),
    )

    def __repr__(self):
        return '<OpenTimeSlot {}>'.format(self.Day)


class Appointment(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Appointments')

    ConversationID = db.Column(db.Integer, db.ForeignKey('conversation.ID', ondelete='cascade'), nullable=False)
    Conversation = db.relationship('Conversation', back_populates='Appointment')


    # Constraints:
    __table_args__ = (db.UniqueConstraint('AssistantID', 'DateTime', name='uix1_appointment'),)


class CRM(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.CRM), nullable=True)
    Auth = db.Column(EncryptedType(JsonEncodedDict, os.environ['SECRET_KEY_DB'], AesEngine, 'pkcs5'), nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='CRMs')

    Assistants = db.relationship('Assistant', back_populates='CRM')

    # Constraints:
    # each company will have one CRM of each type
    __table_args__ = (db.UniqueConstraint('Type', 'CompanyID', name='uix1_crm'),)

    def __repr__(self):
        return '<CRM {}>'.format(self.ID)


class Statistics(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    Opened = db.Column(db.Integer, nullable=False, default=False)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Statistics')

    def __repr__(self):
        return '<Statistics {}>'.format(self.Name)


class Plan(db.Model):
    ID = db.Column(db.String(25), primary_key=True, unique=True)
    Nickname = db.Column(db.String(40), nullable=False, unique=True)
    MaxSolutions = db.Column(db.Integer, nullable=False, default=0)
    MaxBlocks = db.Column(db.Integer, nullable=False, default=0)
    ActiveBotsCap = db.Column(db.Integer, nullable=False, default=0)
    InactiveBotsCap = db.Column(db.Integer, nullable=False, default=0)
    AdditionalUsersCap = db.Column(db.Integer, nullable=False, default=0)
    ExtendedLogic = db.Column(db.Boolean, nullable=False, default=False)
    ImportDatabase = db.Column(db.Boolean, nullable=False, default=False)
    CompanyNameOnChatbot = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    ###

    def __repr__(self):
        return '<Plan {}>'.format(self.Nickname)


class Newsletter(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Email = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return '<Newsletters {}>'.format(self.Email)


# Stored files for conversation
class StoredFile(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    FilePath = db.Column(db.String(250), nullable=True, default=None)

    # Relationships:
    ConversationID = db.Column(db.Integer, db.ForeignKey('conversation.ID', ondelete='SET NULL'))
    Conversation = db.relationship('Conversation', back_populates='StoredFile')

    def __repr__(self):
        return '<StoredFile {}>'.format(self.ID)


class Database(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64), nullable=False)
    Type = db.Column(Enum(enums.DatabaseType), nullable=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Databases')

    # Constraints:
    # Cannot have two databases with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_database'),)

    def __repr__(self):
        return '<Database {}>'.format(self.Name)


class Candidate(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    CandidateName = db.Column(db.String(64), nullable=True)
    CandidateEmail = db.Column(db.String(64), nullable=True)
    CandidateMobile = db.Column(db.String(20), nullable=True)
    CandidateLocation = db.Column(db.String(64), nullable=False) # Required
    CandidateSkills = db.Column(db.String(1080), nullable=False) # Required
    CandidateLinkdinURL = db.Column(db.String(512), nullable=True)
    CandidateAvailability = db.Column(db.String(64), nullable=True)
    CandidateJobTitle = db.Column(db.String(120), nullable=True)
    CandidateEducation = db.Column(db.String(64), nullable=True)
    CandidateYearsExperience = db.Column(db.Float(), nullable=True)
    CandidateDesiredSalary = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType)


    # Relationships:
    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Candidate {}>'.format(self.CandidateName)



class Job(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    JobTitle = db.Column(db.String(64), nullable=False) # Required
    JobDescription = db.Column(db.String(5000), nullable=True)
    JobLocation = db.Column(db.String(64), nullable=False) # Required
    JobType = db.Column(db.String(64), nullable=True)
    JobSalary = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType)
    JobEssentialSkills = db.Column(db.String(512), nullable=True)
    JobDesiredSkills = db.Column(db.String(512), nullable=True)
    JobYearsRequired = db.Column(db.Integer, nullable=True)
    JobStartDate = db.Column(db.DateTime(), nullable=True)
    JobEndDate = db.Column(db.DateTime(), nullable=True)
    JobLinkURL = db.Column(db.String(612), nullable=True)

    # Relationships:
    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Job {}>'.format(self.JobTitle)

class Notifications(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    LastSentDate = db.Column(db.DateTime(), nullable=True)
    Type = db.Column(db.String(50), nullable=True)

    # Relationships

# a hidden table was made by APScheduler being redefined to be able use foreign keys
# class ApschedulerJobs(db.Model):
#
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     }
#
#     FakeID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
#     id = db.Column(db.VARCHAR(200), primary_key=True)
#     next_run_time = db.Column(db.REAL)
#     job_state = db.Column(db.BLOB)
#
#     NotifySchedulerJob = db.relationship('Assistant', uselist=False, back_populates='NotifySchedulerJob')


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



class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data