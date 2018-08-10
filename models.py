from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Company(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    Size = db.Column(db.String(60))
    PhoneNumber = db.Column(db.String(30))
    URL = db.Column(db.String(250), nullable=False)

    # Relationships:
    Users = db.relationship('User', back_populates='Company')

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
    Verified = db.Column(db.String(64), nullable=False, default=False)

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
    AccessBilling = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    # The Role refers back to the relationship in Model.User NOT the table
    Users = db.relationship('User', back_populates="Role")

    def __repr__(self):
        return '<Role {}>'.format(self.Name)


class Assistant(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Nickname = db.Column(db.String(128),nullable=False)
    Route = db.Column(db.String(64), nullable=False)
    Message = db.Column(db.String(64), nullable=False)
    SecondsUntilPopup = db.Column(db.String(64), nullable=False, unique=True)
    Active = db.Column(db.String(64), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)

    def __repr__(self):
        return '<Assistant {}>'.format(self.Email)


class Callback:
    def __init__(self, success, message):
        self.Success:bool = success
        self.Message:str = message
    pass
