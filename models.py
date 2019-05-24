from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, event, types
from sqlalchemy.ext import mutable
from datetime import datetime
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
    StripeID = db.Column(db.String(68), unique=True, nullable=False, )
    SubID = db.Column(db.String(68), unique=True, default=None)

    # Relationships:
    Users = db.relationship('User', back_populates='Company', cascade="all, delete, delete-orphan")
    Assistants = db.relationship('Assistant', back_populates='Company', cascade="all, delete, delete-orphan")
    Databases = db.relationship('Database', back_populates='Company', cascade="all, delete, delete-orphan")
    Roles = db.relationship('Role', back_populates='Company', cascade="all, delete, delete-orphan")
    CRM = db.relationship('CRM', back_populates='Company', cascade="all, delete, delete-orphan")

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
    Flow = db.Column(MagicJSON, nullable=True)
    Message = db.Column(db.String(500), nullable=False)
    TopBarText = db.Column(db.String(64), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0)

    MailEnabled = db.Column(db.Boolean, nullable=False, default=False)
    MailPeriod = db.Column(db.Integer, nullable=False, default=12)
    Active = db.Column(db.Boolean(), nullable=False, default=True)
    LogoName = db.Column(db.String(64), nullable=True)
    Config = db.Column(MagicJSON, nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False, )
    Company = db.relationship('Company', back_populates='Assistants')

    CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID'))
    CRM = db.relationship('CRM', back_populates='Assistants')

    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Conversations = db.relationship('Conversation', back_populates='Assistant')

    # Constraints:
    # cannot have two assistants with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)

    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class CRM(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.CRM), nullable=True)
    Auth = db.Column(EncryptedType(JsonEncodedDict, os.environ['SECRET_KEY_DB'], AesEngine, 'pkcs5'), nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='CRM')

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


class Conversation(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Data = db.Column(MagicJSON, nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    TimeSpent = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    UserType = db.Column(Enum(enums.UserType), nullable=False)
    Completed = db.Column(db.Boolean, nullable=False, default=True)
    Type = db.Column(Enum(enums.ConversationStatus), nullable=False, default=enums.ConversationStatus.Pending)


    CRMSynced = db.Column(db.Boolean, nullable=False, default=False)
    CRMResponse = db.Column(db.String(250), nullable=True)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Conversations')

    StoredFile = db.relationship('StoredFile', uselist=False, back_populates='Conversation')

    def __repr__(self):
        return '<Conversation {}>'.format(self.Data)


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
    CandidateSkills = db.Column(db.String(150), nullable=False) # Required
    CandidateLinkdinURL = db.Column(db.String(512), nullable=True)
    CandidateAvailability = db.Column(db.String(64), nullable=True)
    CandidateJobTitle = db.Column(db.String(64), nullable=True)
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


# =================== Triggers ============================

# Example of how triggers works
# Also check: https://docs.sqlalchemy.org/en/latest/orm/session_events.html

# @event.listens_for(Conversation, 'before_delete')
# def receive_after_insert(mapper, connection, target):
#     print("before_delete")
#     print(target) # prints Conversation
#
# @event.listens_for(Conversation, 'after_delete')
# def receive_after_insert(mapper, connection, target):
#     print("after_delete")
#     print(target) # prints Conversation
#


class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data

class CandidateDict():
    def __init__(self, id, name: str, email: str, mobile: str, location: str, skills: str, linkdinURL: str,
                 availability: str, jobTitle: str, education: str, yearsExperience: int, desiredSalary: float,
                 currency: str, source: str):
        self.C
