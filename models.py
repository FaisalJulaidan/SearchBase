from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(model_class=FlaskBaseModel)
db = initialize_flask_sqlathanor(db)


class Company(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Name = db.Column(db.String(80), nullable=False,
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
    Nickname = db.Column(db.String(128),nullable=False,
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
        return '<Assistant {}>'.format(self.Nickname)


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


class Question(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Question = db.Column(db.String(), nullable=False,
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

    QuestionTypeID = db.Column(db.Integer, db.ForeignKey('question_type.ID'), nullable=False)
    QuestionType = db.relationship('QuestionType', back_populates='Questions',
                                   supports_json=True,
                                   supports_dict=True,
                                   on_serialize=None,
                                   on_deserialize=None
                                   )

    Answers = db.relationship('Answer', back_populates='Question',
                              supports_json=True,
                              supports_dict=True,
                              on_serialize=None,
                              on_deserialize=None
                              )

    UserInputs = db.relationship('UserInput', back_populates='Question')

    def __repr__(self):
        return '<Question {}>'.format(self.Question)


class QuestionType(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
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

    # Relationships:
    Questions = db.relationship('Question', back_populates='QuestionType')

    def __repr__(self):
        return '<QuestionType {}>'.format(self.Name)


class Answer(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Answer = db.Column(db.String(), nullable=False,
                       supports_json=True,
                       supports_dict=True,
                       on_serialize=None,
                       on_deserialize=None
                       )
    Keyword = db.Column(db.String(), nullable=False,
                        supports_json=True,
                        supports_dict=True,
                        on_serialize=None,
                        on_deserialize=None
                        )
    Action = db.Column(db.String(), nullable=False, default='Next Question by Order',
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
    QuestionID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=False)
    Question = db.relationship('Question', back_populates='Answers',
                               supports_json=False,
                               supports_dict=False,
                               on_serialize=None,
                               on_deserialize=None
                               )

    def __repr__(self):
        return '<Answer {}>'.format(self.Answer)



class UserInput(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True,
                   supports_json=True,
                   supports_dict=True,
                   on_serialize=None,
                   on_deserialize=None
                   )
    Input = db.Column(db.String(), nullable=False,
                      supports_json=True,
                      supports_dict=True,
                      on_serialize=None,
                      on_deserialize=None
                      )
    QuestionString = db.Column(db.String(), nullable=False,
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
    SessionID = db.Column(db.Integer, nullable=False,
                         supports_json=True,
                         supports_dict=True,
                         on_serialize=None,
                         on_deserialize=None
                         )

    # Relationships:
    QuestionID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=False)
    Question = db.relationship('Question', back_populates='UserInputs',
                               supports_json=True,
                               supports_dict=True,
                               on_serialize=None,
                               on_deserialize=None
                               )

    def __repr__(self):
        return '<UserInput {}>'.format(self.Input)


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
