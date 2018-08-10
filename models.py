from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Company(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    Size = db.Column(db.String(60))
    PhoneNumber = db.Column(db.String(30))
    URL = db.Column(db.String(250), nullable=False)
    # Users = db.relationship('User', backref='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Firstname = db.Column(db.String(64), nullable=False)
    Surname = db.Column(db.String(64), nullable=False)
    Email = db.Column(db.String(64), nullable=False, unique=True)
    Password = db.Column(db.String(128),nullable=False)
    StripeID = db.Column(db.String(128), default=None, unique=True)
    Verified = db.Column(db.String(64), nullable=False, default=None)
    SubID = db.Column(db.String(64), default=None, unique=True)

    # Company = db.relationship('Company')
    # billing_address_id = db.column(Integer, ForeignKey("address.id"))
    # shipping_address_id = db.column(Integer, ForeignKey("address.id"))
    #
    # billing_address = db.relationship("Address", foreign_keys=[billing_address_id])
    # shipping_address = relationship("Address", foreign_keys=[shipping_address_id])

    # Company = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)
    RoleID = db.column(db.Integer, db.ForeignKey('role.ID'))

    def __repr__(self):
        return '<User {}>'.format(self.Email)


class Role(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64))
    Users = db.relationship('User', backref='Role')

    # a role has users
    # Users = Users = db.relationship('User', backref='User')

    # PermissionsID = db.column(db.Integer, db.ForeignKey('Permissions.ID'), nullable=False)
    # Permissions = db.relationship('Permissions', backref='Role')
    def __repr__(self):
        return '<Role {}>'.format(self.Name)

class Permissions(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EditChatbots = db.Column(db.Boolean(), nullable=False, default=False)
    EditUsers = db.Column(db.Boolean(), nullable=False, default=False)
    AccessBilling = db.Column(db.Boolean(), nullable=False, default=False)
    # RoleID
    # RoleID = db.column(db.Integer, db.ForeignKey('Role.ID'), nullable=False)
    # Role = db.relationship('Role', backref='Role')
    def __repr__(self):
        return '<Permissions {}>'.format(self.EditChatbots)

class Callback:
    def __init__(self, success,message):
        self.Success:bool = success
        self.Message:str = message
    pass
