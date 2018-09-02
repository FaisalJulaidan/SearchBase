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
    PhoneNumber = db.Column(db.String(30))
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

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Firstname = db.Column(db.String(64), nullable=False,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
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
    Name = db.Column(db.String(64))

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
    Company = db.relationship('Company', back_populates='Roles',
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    Users = db.relationship('User', back_populates="Role")

    # Constraints:
    db.UniqueConstraint('Name', 'CompanyID', name='uix1_role')

    def __repr__(self):
        return '<Role {}>'.format(self.Name)


class Assistant(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Name = db.Column(db.String(128),nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    Route = db.Column(db.String(64), unique=True,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    Message = db.Column(db.String(500), nullable=False,
                        supports_json=True,
                        supports_dict=True,
                        on_serialize=None,
                        on_deserialize=None
                        )
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0,
                                  supports_json=True,
                                  supports_dict=True,
                                  on_serialize=None,
                                  on_deserialize=None
                                  )
    Active = db.Column(db.Boolean(), nullable=False, default=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False,)
    Company = db.relationship('Company', back_populates='Assistants',
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    Products = db.relationship('Product', back_populates='Assistant')
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Questions = db.relationship('Question', back_populates='Assistant')

    # Constraints:
    db.UniqueConstraint('CompanyID', 'Nickname', name='uix1_assistant')


    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)


class Product(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    ProductID = db.Column(db.Integer, nullable=False,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
    Name = db.Column(db.String(128), nullable=False,
                     supports_json=True,
                     supports_dict=True,
                     on_serialize=None,
                     on_deserialize=None
                     )
    Brand = db.Column(db.String(128), nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    Model = db.Column(db.String(128), nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    Price = db.Column(db.String(128), nullable=False,
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
    Discount = db.Column(db.String(128), nullable=False,
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

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Products',
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )

    def __repr__(self):
        return '<Product {}>'.format(self.Name)


class Statistics(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Name = db.Column(db.String(128), nullable=False,
                     supports_json=True,
                     supports_dict=True,
                     on_serialize=None,
                     on_deserialize=None
                     )
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    Opened = db.Column(db.Integer, nullable=False, default=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0,
                                  supports_json=True,
                                  supports_dict=True,
                                  on_serialize=None,
                                  on_deserialize=None
                                  )
    ProductsReturned = db.Column(db.Integer, nullable=False, default=0,
                                 supports_json=True,
                                 supports_dict=True,
                                 on_serialize=None,
                                 on_deserialize=None
                                 )

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Statistics',
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )

    def __repr__(self):
        return '<Statistics {}>'.format(self.Name)


class QuestionType(enum.Enum):
    UserInput = 'User Input'
    PredefinedAnswers = 'Predefined Answers'
    FileUpload = 'File Upload'

    # def __str__(self):
    #     return str(self.value)


class QuestionAction(enum.Enum):
    GoToNextQuestion = 'Go To Next Question'
    GoToSpecificQuestion = 'Go To Specific Question'
    ShowSolutions = 'Show Solutions'

    def __str__(self):
        return str(self.value)

class UserInputValidation(enum.Enum):
    Email = 'Email'
    Telephone = 'Telephone'
    Decimal = 'Decimal'
    Integer = 'Integer'

    def __str__(self):
        return str(self.value)


class Question(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Text = db.Column(db.String(), nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )

    Type = db.Column(Enum(QuestionType), nullable=False,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )
    Order = db.Column(db.Integer, nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    StoreInDB = db.Column(db.Boolean(), nullable=False, default=True,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Questions',
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )

    # Constraints:
    db.UniqueConstraint('AssistantID', 'Order', name='uix1_question')

    def __repr__(self):
        return '<Question {}>'.format(self.Text)


class QuestionUI(db.Model):
    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )

    Action = db.Column(Enum(QuestionAction), nullable=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    Validation = db.Column(Enum(UserInputValidation), nullable=False,
                           supports_json=True,
                           supports_dict=True,
                           on_serialize=None,
                           on_deserialize=None
                           )
    # Relationships:
    Question = db.relationship('Question', foreign_keys=[ID])
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'),
                               supports_json=True,
                               supports_dict=True,
                               on_serialize=None,
                               on_deserialize=None
                               )
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<QuestionUI {}>'.format(self.Question)


class UserInput(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    SessionID = db.Column(db.Integer, nullable=False,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
    Text = db.Column(db.String(), nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )

    QuestionText = db.Column(db.String(), nullable=False,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )
    Keywords = db.Column(db.String(), nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )

    # Relationships:
    QuestionUIID = db.Column(db.Integer, db.ForeignKey('questionUI.ID'), nullable=False)
    QuestionUI = db.relationship('QuestionUI', foreign_keys=[QuestionUIID],
                                 supports_json=True,
                                 supports_dict=True,
                                 on_serialize=None,
                                 on_deserialize=None
                                 )

    def __repr__(self):
        return '<UserInput {}>'.format(self.Text)

class QuestionPA(db.Model):
    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    # Relationships:
    Answers = db.relationship('Answer', back_populates='QuestionPA')

    Question = db.relationship('Question', foreign_keys=[ID])

    def __repr__(self):
        return '<QuestionPA {}>'.format(self.Question)



class Answer(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Text = db.Column(db.String(), nullable=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    Keywords = db.Column(db.String(), nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    Action = db.Column(Enum(QuestionAction), nullable=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    TimesClicked = db.Column(db.Integer, nullable=False, default=0,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )

    # Relationships:
    QuestionPAID = db.Column(db.Integer, db.ForeignKey('questionPA.ID'), nullable=False)
    QuestionPA = db.relationship('QuestionPA', back_populates='Answers', foreign_keys=[QuestionPAID],
                                 supports_json=False,
                                 supports_dict=False,
                                 on_serialize=None,
                                 on_deserialize=None
                                 )
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=True)
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<Answer {}>'.format(self.Text)


class QuestionFU(db.Model):
    ID = db.Column(db.Integer, db.ForeignKey(Question.ID), primary_key=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Action = db.Column(Enum(QuestionAction), nullable=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    TypesAllowed = db.Column(db.String(), nullable=False,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )
    # Relationships:
    Question = db.relationship('Question', foreign_keys=[ID])
    QuestionToGoID = db.Column(db.Integer, db.ForeignKey('question.ID'),
                               supports_json=True,
                               supports_dict=True,
                               on_serialize=None,
                               on_deserialize=None
                               )
    QuestionToGo = db.relationship('Question', foreign_keys=[QuestionToGoID])

    def __repr__(self):
        return '<QuestionFU {}>'.format(self.Question)


class UserFiles(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    SessionID = db.Column(db.Integer, nullable=False,
                          supports_json=True,
                          supports_dict=True,
                          on_serialize=None,
                          on_deserialize=None
                          )
    Name = db.Column(db.String(), nullable=False,
                    supports_json=True,
                    supports_dict=True,
                    on_serialize=None,
                    on_deserialize=None
                    )
    URL = db.Column(db.String(), nullable=False, unique=True,
                    supports_json=True,
                    supports_dict=True,
                    on_serialize=None,
                    on_deserialize=None
                    )

    QuestionText = db.Column(db.String(), nullable=False,
                             supports_json=True,
                             supports_dict=True,
                             on_serialize=None,
                             on_deserialize=None
                             )
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )

    # Relationships:
    QuestionFUID = db.Column(db.Integer, db.ForeignKey('questionFU.ID'), nullable=False)
    QuestionFU = db.relationship('QuestionFU', foreign_keys=[QuestionFUID],
                                 supports_json=True,
                                 supports_dict=True,
                                 on_serialize=None,
                                 on_deserialize=None
                                 )

    def __repr__(self):
        return '<UserFiles {}>'.format(self.Name)


class Plan(db.Model):
    ID = db.Column(db.String(), primary_key=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Nickname = db.Column(db.String(), nullable=False, unique=True,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )
    MaxProducts = db.Column(db.Integer, nullable=False, default=0,
                            supports_json=True,
                            supports_dict=True,
                            on_serialize=None,
                            on_deserialize=None
                            )
    ActiveBotsCap = db.Column(db.Integer, nullable=False, default=0,
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )
    InactiveBotsCap = db.Column(db.Integer, nullable=False, default=0,
                                supports_json=True,
                                supports_dict=True,
                                on_serialize=None,
                                on_deserialize=None
                                )
    AdditionalUsersCap = db.Column(db.Integer, nullable=False, default=0,
                                   supports_json=True,
                                   supports_dict=True,
                                   on_serialize=None,
                                   on_deserialize=None
                                   )
    ExtendedLogic = db.Column(db.Boolean, nullable=False, default=False,
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )
    ImportDatabase = db.Column(db.Boolean, nullable=False, default=False,
                               supports_json=True,
                               supports_dict=True,
                               on_serialize=None,
                               on_deserialize=None
                               )
    CompanyNameOnChatbot = db.Column(db.Boolean, nullable=False, default=False,
                                     supports_json=True,
                                     supports_dict=True,
                                     on_serialize=None,
                                     on_deserialize=None
                                     )

    # Relationships:
    ###

    def __repr__(self):
        return '<Plan {}>'.format(self.Nickname)


class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message if success else 'Error: ' + message
        self.Data: str or dict or bool = data
    pass
