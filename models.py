from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime
import enum

db = SQLAlchemy(model_class=FlaskBaseModel)
db = initialize_flask_sqlathanor(db)


class Company(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Name = db.Column(db.String(80), nullable=False, unique=True,
                     supports_json=True,
                     supports_dict=True,
                     on_serialize=None,
                     on_deserialize=None
                     )
    Size = db.Column(db.String(60),
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
    URL = db.Column(db.String(250), nullable=False,
                    supports_json=True,
                    supports_dict=True,
                    on_serialize=None,
                    on_deserialize=None
                    )

    # Relationships:
    Users = db.relationship('User', back_populates='Company', cascade="all, delete, delete-orphan")
    Assistants = db.relationship('Assistant', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)


class User(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                 )
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
    Password = db.Column(db.String(255),nullable=False,
                         supports_json=False,
                         supports_dict=False,
                         on_serialize=None,
                         on_deserialize=None
                         )
    StripeID = db.Column(db.String(128), default=None, unique=True,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    SubID = db.Column(db.String(64), default=None, unique=True,
                      supports_json=True,
                      supports_dict=True,
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
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
    Company = db.relationship('Company', back_populates='Users',
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID'))
    Role = db.relationship('Role', back_populates='Users',
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )

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
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
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
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False,)
    Company = db.relationship('Company', back_populates='Assistants')

    Products = db.relationship('Product', back_populates='Assistant')
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Questions = db.relationship('Question', back_populates='Assistant')

    # Constraints:
    db.UniqueConstraint('CompanyID', 'Nickname', name='uix1_assistant')


    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class Product(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ProductID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Brand = db.Column(db.String(128), nullable=False)
    Model = db.Column(db.String(128), nullable=False)
    Price = db.Column(db.String(128), nullable=False)
    Keywords = db.Column(db.String(128), nullable=False)
    Discount = db.Column(db.String(128), nullable=False)
    URL = db.Column(db.String(), nullable=False)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Products')

    def __repr__(self):
        return '<Product {}>'.format(self.Name)


class Statistics(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    Opened = db.Column(db.Integer, nullable=False, default=False)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    ProductsReturned = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Statistics')

    def __repr__(self):
        return '<Statistics {}>'.format(self.Name)


class QuestionType(enum.Enum):
    UserInput = 'User Input'
    PredefinedAnswers = 'Predefined Answers'
    FileUpload = 'File Upload'


class QuestionAction(enum.Enum):

    GoToNextQuestion = 'Go To Next Question'
    GoToSpecificQuestion = 'Go To Specific Question'
    ShowSolutions = 'Show Solutions'


class UserInputValidation(enum.Enum):

    Email = 'Email'
    Telephone = 'Telephone'
    Decimal = 'Decimal'
    Integer = 'Integer'


class Question(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Text = db.Column(db.String(), nullable=False)
    Type = db.Column(Enum(QuestionType), nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    StoreInDB = db.Column(db.Boolean(), nullable=False, default=True)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Questions')

    # Constraints:
    db.UniqueConstraint('AssistantID', 'Order', name='uix1_question')

    def __repr__(self):
        return '<Question {}>'.format(self.Text)


class QuestionUI(db.Model):

    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True)
    Action = db.Column(Enum(QuestionAction), nullable=False )
    Validation = db.Column(Enum(UserInputValidation), nullable=False)

    # Relationships:
    Question = db.relationship('Question', foreign_keys=[ID])
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'))
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<QuestionUI {}>'.format(self.Question)


class UserInput(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    SessionID = db.Column(db.Integer, nullable=False)
    Text = db.Column(db.String(), nullable=False)
    QuestionText = db.Column(db.String(), nullable=False)
    Keywords = db.Column(db.String(), nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    QuestionUIID = db.Column(db.Integer, db.ForeignKey('questionUI.ID'), nullable=False)
    QuestionUI = db.relationship('QuestionUI', foreign_keys=[QuestionUIID])

    def __repr__(self):
        return '<UserInput {}>'.format(self.Text)

class QuestionPA(db.Model):
    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True)
    # Relationships:
    Answers = db.relationship('Answer', back_populates='QuestionPA')
    Question = db.relationship('Question', foreign_keys=[ID])

    def __repr__(self):
        return '<QuestionPA {}>'.format(self.Question)


class Answer(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Text = db.Column(db.String(), nullable=False)
    Keywords = db.Column(db.String(), nullable=False)
    Action = db.Column(Enum(QuestionAction), nullable=False)
    TimesClicked = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    QuestionPAID = db.Column(db.Integer, db.ForeignKey('questionPA.ID'), nullable=False)
    QuestionPA = db.relationship('QuestionPA', back_populates='Answers', foreign_keys=[QuestionPAID])
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=True)
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<Answer {}>'.format(self.Text)


class QuestionFU(db.Model):

    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True)
    Action = db.Column(Enum(QuestionAction), nullable=False)
    TypesAllowed = db.Column(db.String(), nullable=False)

    # Relationships:
    Question = db.relationship('Question', foreign_keys=[ID])
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'))
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<QuestionFU {}>'.format(self.Question)


class UserFiles(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    SessionID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(), nullable=False)
    URL = db.Column(db.String(), nullable=False, unique=True)

    QuestionText = db.Column(db.String(), nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now )

    # Relationships:
    QuestionFUID = db.Column(db.Integer, db.ForeignKey('questionFU.ID'), nullable=False)
    QuestionFU = db.relationship('QuestionFU', foreign_keys=[QuestionFUID])

    def __repr__(self):
        return '<UserFiles {}>'.format(self.Name)


class Plan(db.Model):

    ID = db.Column(db.String(), primary_key=True, unique=True)
    Nickname = db.Column(db.String(), nullable=False, unique=True)
    MaxProducts = db.Column(db.Integer, nullable=False, default=0)
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


class Newsletters(db.Model):

    Email = db.Column(db.String(), nullable=False, unique=True)


    # Relationships:
    ###

    def __repr__(self):
        return '<Newsletters {}>'.format(self.Email)


class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message if success else 'Error: ' + message
        self.Data: str or dict or bool = data
    pass
