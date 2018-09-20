from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, event, ForeignKey, types
from sqlalchemy.ext import mutable
from datetime import datetime
import enum
import json

from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

db = SQLAlchemy(model_class=FlaskBaseModel)
db = initialize_flask_sqlathanor(db)

from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

secret_key = 's23ecg5e5%$G$4wg4bbw65b653hh65h%^Gbf'
useEncryption = False


# Activate Foreign Keys
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class JsonEncodedDict(types.TypeDecorator):
    """Stores and retrieves JSON as TEXT."""

    impl = types.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


 # TypeEngine.with_variant says "use StringyJSON instead when
# connecting to 'sqlite'"
# MagicJSON = types.JSON().with_variant(JsonEncodedDict, 'sqlite')
mutable.MutableDict.associate_with(JsonEncodedDict)


# ============= Models ===================

class Company(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    if useEncryption:
        Name = db.Column(EncryptedType(db.String(80), secret_key, AesEngine, 'pkcs5'),
                         nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
        URL = db.Column(EncryptedType(db.String(250), secret_key, AesEngine, 'pkcs5'),
                        nullable=False,
                        supports_json=True,
                        supports_dict=True,
                        on_serialize=None,
                        on_deserialize=None
                        )
    else:
        Name = db.Column(db.String(80),
                         nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
        URL = db.Column(db.String(250),
                        nullable=False,
                        supports_json=True,
                        supports_dict=True,
                        on_serialize=None,
                        on_deserialize=None
                        )

    StripeID = db.Column(db.String(68), unique=True, nullable=False,)
    SubID = db.Column(db.String(68), unique=True, default=None)

    # Size = db.Column(db.String(60))

    # Relationships:
    Users = db.relationship('User', back_populates='Company', cascade="all, delete, delete-orphan")
    Assistants = db.relationship('Assistant', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)


class User(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                 )
    if useEncryption:
        Firstname = db.Column(EncryptedType(db.String(64), secret_key, AesEngine, 'pkcs5'), nullable=False)
        Surname = db.Column(EncryptedType(db.String(64), secret_key, AesEngine, 'pkcs5'), nullable=False,
                            supports_json=True,
                            supports_dict=True,
                            on_serialize=None,
                            on_deserialize=None
                            )
        Email = db.Column(EncryptedType(db.String(64), secret_key, AesEngine, 'pkcs5'), nullable=False, unique=True,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
        PhoneNumber = db.Column(EncryptedType(db.String(30), secret_key, AesEngine, 'pkcs5'),
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )
    else:
        Firstname = db.Column(db.String(64), nullable=False)
        Surname = db.Column(db.String(64), nullable=False,
                            supports_json=True,
                            supports_dict=True,
                            on_serialize=None,
                            on_deserialize=None
                            )
        Email = db.Column(db.String(64), nullable=False, unique=True,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
        PhoneNumber = db.Column(db.String(30),
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )
    Password = db.Column(db.String(255),nullable=False,
                         supports_json=False,
                         supports_dict=False,
                         on_serialize=None,
                         on_deserialize=None
                         )
    Verified = db.Column(db.Boolean(), nullable=False, default=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    LastAccess = db.Column(db.DateTime(), nullable=True,
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )

    CreatedOn = db.Column(db.DateTime(), nullable=False, default=datetime.now,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Users',
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID', ondelete='SET NULL'))
    Role = db.relationship('Role', back_populates='Users',
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )

    Settings = db.relationship("UserSettings", uselist=False, back_populates="User")

    def __repr__(self):
        return '<User {}>'.format(self.Email)


class Role(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Name = db.Column(db.String(64),
                     supports_json=True,
                     supports_dict=True,
                     on_serialize=None,
                     on_deserialize=None
                     )
    EditChatbots = db.Column(db.Boolean(), nullable=False, default=False,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )
    EditUsers = db.Column(db.Boolean(), nullable=False, default=False,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
    DeleteUsers = db.Column(db.Boolean(), nullable=False, default=False,
                            supports_json=True,
                            supports_dict=True,
                            on_serialize=None,
                            on_deserialize=None
                            )
    AccessBilling = db.Column(db.Boolean(), nullable=False, default=False,
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Roles')

    Users = db.relationship('User', back_populates="Role")

    # Constraints:
    db.UniqueConstraint('Name', 'CompanyID', name='uix1_role')

    def __repr__(self):
        return '<Role {}>'.format(self.Name)


class Assistant(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128),nullable=False)
    Route = db.Column(db.String(64), unique=True)
    Message = db.Column(db.String(500), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0 )
    Active = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False,)
    Company = db.relationship('Company', back_populates='Assistants')

    Solutions = db.relationship('Solution', back_populates='Assistant')
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Blocks = db.relationship('Block', back_populates='Assistant')
    ChatbotSessions = db.relationship('ChatbotSession', back_populates='Assistant')

    # Constraints:
    db.UniqueConstraint('CompanyID', 'Nickname', name='uix1_assistant')


    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class Solution(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    SolutionID = db.Column(db.String(128), nullable=False,
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )
    MajorTitle = db.Column(db.String(128), nullable=False,
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )
    SecondaryTitle = db.Column(db.String(128), nullable=False,
                               supports_json=True,
                               supports_dict=True,
                               on_serialize=None,
                               on_deserialize=None
                               )
    ShortDescription = db.Column(db.String(128), nullable=False,
                                 supports_json=True,
                                 supports_dict=True,
                                 on_serialize=None,
                                 on_deserialize=None
                                 )
    Money = db.Column(db.String(128), nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    Keywords = db.Column(db.String(128), nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    URL = db.Column(db.String(), nullable=False,
                    supports_json=True,
                    supports_dict=True,
                    on_serialize=None,
                    on_deserialize=None
                    )
    TimesReturned = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Solutions')

    def __repr__(self):
        return '<Solution {}>'.format(self.MajorTitle)


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


class ValidationType(enum.Enum):

    Email = 'Email'
    Telephone = 'Telephone'


class BlockType(enum.Enum):
    UserInput = 'User Input'
    Question = 'Question'
    FileUpload = 'File Upload'
    Solutions = 'Solutions'


class BlockAction(enum.Enum):

    GoToNextBlock = 'Go To Next Block'
    GoToSpecificBlock = 'Go To Specific Block'
    ShowSolutions = 'Show Solutions'


class Block(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(BlockType), nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    Content = db.Column(JsonEncodedDict, nullable=False)
    StoreInDB = db.Column(db.Boolean(), nullable=False, default=True)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Blocks')

    # Constraints:
    db.UniqueConstraint('AssistantID', 'Order', name='uix1_question')

    def __repr__(self):
        return '<Block {}>'.format(self.Type)


class ChatbotSession(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Data = db.Column(JsonEncodedDict, nullable=False)
    FilePath = db.Column(db.String(), nullable=True, default=None)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    TimeSpent = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)


    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='ChatbotSessions')

    def __repr__(self):
        return '<UserInput {}>'.format(self.Input)


class Answer(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Text = db.Column(db.String(), nullable=False)
    Keywords = db.Column(db.String(), nullable=False)
    TimesClicked = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    BlockID = db.Column(db.Integer, db.ForeignKey('block.ID', ondelete='SET NULL'), nullable=False)
    Block = db.relationship('Block', foreign_keys=[BlockID])

    def __repr__(self):
        return '<Answer {}>'.format(self.Text)


class UserFiles(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    SessionID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(), nullable=False)
    URL = db.Column(db.String(), nullable=False, unique=True)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now )

    # Relationships:
    BlockID = db.Column(db.Integer, db.ForeignKey('block.ID', ondelete='SET NULL'), nullable=False)
    Block = db.relationship('Block', foreign_keys=[BlockID])

    def __repr__(self):
        return '<UserFiles {}>'.format(self.Name)


class Plan(db.Model):

    ID = db.Column(db.String(), primary_key=True, unique=True)
    Nickname = db.Column(db.String(), nullable=False, unique=True)
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
    Email = db.Column(db.String(), nullable=False, unique=True)

    # Relationships:
    ###

    def __repr__(self):
        return '<Newsletters {}>'.format(self.Email)


class UserSettings(db.Model):

    ID = db.Column(db.Integer, db.ForeignKey("user.ID", ondelete='cascade'), primary_key=True, unique=True)
    TrackingData = db.Column(db.Boolean, nullable=False, default=False)
    TechnicalSupport = db.Column(db.Boolean, nullable=False, default=False)
    AccountSpecialist = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    User = db.relationship('User', back_populates='Settings')

    def __repr__(self):
        return '<UserSettings {}>'.format(self.ID)


class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data
    pass
    # if success else 'Error: ' + message

