from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Company(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    Size = db.Column(db.String(60))
    PhoneNumber = db.Column(db.String(30))
    URL = db.Column(db.String(250), nullable=False)

    # Relationships:
    Users = db.relationship('User', back_populates='Company', cascade="all, delete, delete-orphan")
    Assistants = db.relationship('Assistant', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)


class User(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Firstname = db.Column(db.String(64), nullable=False)
    Surname = db.Column(db.String(64), nullable=False)
    Email = db.Column(db.String(64), nullable=False, unique=True)
    Password = db.Column(db.String(128),nullable=False)
    StripeID = db.Column(db.String(128), default=None, unique=True)
    SubID = db.Column(db.String(64), default=None, unique=True)
    Verified = db.Column(db.Boolean(), nullable=False, default=False)
    LastAccess = db.Column(db.DateTime(), nullable=True)
    CreatedOn = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
    Company = db.relationship('Company', back_populates='Users')

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID'))
    Role = db.relationship('Role', back_populates='Users')

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
    # The User refers back to the relationship in Model.User NOT the table
    Users = db.relationship('User', back_populates="Role")

    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
    Company = db.relationship('Company', back_populates='Roles')

    # Constraints:
    db.UniqueConstraint('Name', 'CompanyID', name='uix1_role')

    def __repr__(self):
        return '<Role {}>'.format(self.Name)


class Assistant(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Nickname = db.Column(db.String(128),nullable=False)
    Route = db.Column(db.String(64), unique=True)
    Message = db.Column(db.String(500), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0)
    Active = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
    Company = db.relationship('Company', back_populates='Assistants')

    Products = db.relationship('Product', back_populates='Assistant')
    Statistics = db.relationship('Statistics', back_populates='Assistant')
    Questions = db.relationship('Question', back_populates='Assistant')

    # Constraints:
    db.UniqueConstraint('CompanyID', 'Nickname', name='uix1_assistant')


    def __repr__(self):
        return '<Assistant {}>'.format(self.Nickname)


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


class Question(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Question = db.Column(db.String(), nullable=False)
    Type = db.Column(db.String(), nullable=False)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Questions')

    Answers = db.relationship('Answer', back_populates='Question')

    UserInputs = db.relationship('UserInput', back_populates='Question')


    def __repr__(self):
        return '<Question {}>'.format(self.Question)


class Answer(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Answer = db.Column(db.String(), nullable=False)
    Keyword = db.Column(db.String(), nullable=False)
    Action = db.Column(db.String(), nullable=False, default='Next Question by Order')
    TimesClicked = db.Column(db.Integer, nullable=False, default=0)

    # Relationships:
    QuestionID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=False)
    Question = db.relationship('Question', back_populates='Answers')

    def __repr__(self):
        return '<Answer {}>'.format(self.Answer)


class UserInput(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Input = db.Column(db.String(), nullable=False)
    QuestionString = db.Column(db.String(), nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    QuestionID = db.Column(db.Integer, db.ForeignKey('question.ID'), nullable=False)
    Question = db.relationship('Question', back_populates='UserInputs')

    def __repr__(self):
        return '<UserInput {}>'.format(self.Input)


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


class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message if success else 'Error: ' + message
        self.Data: str or dict or bool = data
    pass
