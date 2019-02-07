from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, event, types
from sqlalchemy.ext import mutable
from datetime import datetime
import json
import enums
from sqlalchemy_utils import PasswordType, CurrencyType, Currency

from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

db = SQLAlchemy(model_class=FlaskBaseModel)
db = initialize_flask_sqlathanor(db)
# force_auto_coercion()


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
    StripeID = db.Column(db.String(68), unique=True, nullable=False,)
    SubID = db.Column(db.String(68), unique=True, default=None)

    # Relationships:
    Users = db.relationship('User', back_populates='Company', cascade="all, delete, delete-orphan")
    Assistants = db.relationship('Assistant', back_populates='Company', cascade="all, delete, delete-orphan")
    Databases = db.relationship('Database', back_populates='Company', cascade="all, delete, delete-orphan")
    Roles = db.relationship('Role', back_populates='Company', cascade="all, delete, delete-orphan")

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
    LastAccess = db.Column(db.DateTime(), nullable=True)
    CreatedOn = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Users')

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID', ondelete='SET NULL'))
    Role = db.relationship('Role', back_populates='Users')

    Settings = db.relationship("UserSettings", uselist=False, back_populates="User", cascade="all, delete, delete-orphan")

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
    Name = db.Column(db.String(128),nullable=False)
    Route = db.Column(db.String(64), unique=True)
    Message = db.Column(db.String(500), nullable=False)
    TopBarText = db.Column(db.String(64), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0)
    Config = db.Column(MagicJSON, nullable=True)
    Active = db.Column(db.Boolean(), nullable=False, default=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False,)
    Company = db.relationship('Company', back_populates='Assistants')

    Solutions = db.relationship('Solution', back_populates='Assistant')
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    BlockGroups = db.relationship('BlockGroup', back_populates='Assistant')
    ChatbotSessions = db.relationship('ChatbotSession', back_populates='Assistant')

    # Constraints:
    # Cannot have two assistants with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)

    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class Solution(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64), nullable=False)

    Content = db.Column(MagicJSON, nullable=False)
    RequiredFilters = db.Column(MagicJSON, nullable=True)
    DisplayTitles = db.Column(MagicJSON, nullable=True)

    Type = db.Column(db.String(64), nullable=False)
    WebLink = db.Column(db.String(128), nullable=True)
    IDReference = db.Column(db.String(64), nullable=True)
    automaticSolutionAlerts = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Solutions')

    def __repr__(self):
        return '<Solution {}>'.format(self.ID)


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

    # Relationships:
    ###

    def __repr__(self):
        return '<Newsletters {}>'.format(self.Email)


class UserSettings(db.Model):

    ID = db.Column(db.Integer, db.ForeignKey("user.ID", ondelete='cascade'), primary_key=True, unique=True)
    TrackingData = db.Column(db.Boolean, nullable=False, default=False)
    TechnicalSupport = db.Column(db.Boolean, nullable=False, default=False)
    AccountSpecialist = db.Column(db.Boolean, nullable=False, default=False)
    UserInputNotifications = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    User = db.relationship('User', back_populates='Settings')

    def __repr__(self):
        return '<UserSettings {}>'.format(self.ID)


class ChatbotSession(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Data = db.Column(MagicJSON, nullable=False)
    FilePath = db.Column(db.String(250), nullable=True, default=None)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    TimeSpent = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    UserType = db.Column(Enum(enums.UserType), nullable=False)


# Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='ChatbotSessions')

    def __repr__(self):
        return '<ChatbotSession {}>'.format(self.Data)


class BlockGroup(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(128), nullable=False)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='BlockGroups')
    Blocks = db.relationship('Block', back_populates='Group', order_by='Block.Order', cascade="all, delete, delete-orphan")

    # Constraints:
    # __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)

    def __repr__(self):
        return '<BlockGroup {}>'.format(self.Name)


class Block(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.BlockType), nullable=False)
    DataType = db.Column(Enum(enums.DataType), nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    Content = db.Column(MagicJSON, nullable=False)
    StoreInDB = db.Column(db.Boolean(), nullable=False, default=True)
    Skippable = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    GroupID = db.Column(db.Integer, db.ForeignKey('block_group.ID', ondelete='cascade'), nullable=False)
    Group = db.relationship('BlockGroup', back_populates='Blocks')
    #
    # DataCategoryID = db.Column(db.Integer, db.ForeignKey('data_category.ID', ondelete='SET NULL'))
    # DataCategory = db.relationship('DataCategory', back_populates='Blocks')

    # Labels = db.relationship('BlockLabel', back_populates='Blocks', secondary=BlocksLabels)

    # Constraints:
    # __table_args__ = (db.UniqueConstraint('AssistantID', 'Order', name='uix1_question'),)

    def __repr__(self):
        return '<Block {}>'.format(self.Type)


class BlockLabel(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Text = db.Column(db.String(128), nullable=False)
    Colour = db.Column(db.String(128), nullable=False)
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False,)

    # Relationships:
    # Blocks = db.relationship('Block', back_populates='Labels', secondary=BlocksLabels)

    def __repr__(self):
        return '<BlockLabel {}>'.format(self.Text)


class Database(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64),nullable=False)
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
    Name = db.Column(db.String(64), nullable=True)
    Email = db.Column(db.String(64), nullable=True)
    Telephone = db.Column(db.String(64), nullable=True)
    LinkdinURL = db.Column(db.String(512), nullable=True)
    PostCode = db.Column(db.String(64), nullable=True)

    Gender = db.Column(db.String(24), nullable=True)
    Degree = db.Column(db.String(64), nullable=True)
    # Resume = db.Column(db.String(64), nullable=True) # this will be a file
    ContactTime = db.Column(db.String(64), nullable=True)
    Availability = db.Column(db.String(64), nullable=True)
    CurrentSalary = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType)
    CurrentRole = db.Column(db.String(64), nullable=True)
    JobTitle = db.Column(db.String(64), nullable=True)
    CurrentEmployer = db.Column(db.String(64), nullable=True)
    CurrentEmploymentType = db.Column(db.String(64), nullable=True)

    DesiredSalary = db.Column(db.Float(), nullable=True)
    DesiredPosition = db.Column(db.String(64), nullable=True)
    CandidateSkills = db.Column(db.String(64), nullable=True)
    YearsExp = db.Column(db.Float(), nullable=True)
    PreferredLocation = db.Column(db.String(64), nullable=True)
    PreferredEmploymentType = db.Column(db.String(64), nullable=True)
    DesiredHourlyRate = db.Column(db.Float(), nullable=True)


    # Relationships:
    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Candidate {}>'.format(self.Name)

class Job(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    JobTitle = db.Column(db.String(64), nullable=True)
    Location = db.Column(db.String(64), nullable=True)
    PositionType = db.Column(db.String(64), nullable=True)
    EmploymentType = db.Column(db.String(64), nullable=True)
    Salary = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType)
    StartDate = db.Column(db.DateTime(), nullable=True)

    # Relationships:

    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Client {}>'.format(self.Name)

class Client(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64), nullable=True)
    Email = db.Column(db.String(64), nullable=True)
    Telephone = db.Column(db.String(64), nullable=True)
    LinkdinURL = db.Column(db.String(128), nullable=True)
    PostCode = db.Column(db.String(64), nullable=True)

    Location = db.Column(db.String(64), nullable=True)
    NearbyStation = db.Column(db.String(64), nullable=True)
    JobSalaryOffered = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType)
    EmploymentTypeOffered = db.Column(db.String(64), nullable=True)
    CandidatesNeeded = db.Column(db.Integer(), nullable=True)
    EssentialSkills = db.Column(db.String(512), nullable=True)
    EssentialYearsExp = db.Column(db.Float(), nullable=True)
    ContractRate = db.Column(db.Float(), nullable=True)
    JobDescription = db.Column(db.String(512), nullable=True)
    JobAvailability = db.Column(db.String(64), nullable=True)

    # Relationships:

    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Client {}>'.format(self.Name)





class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data