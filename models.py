from app import db


class Company(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    Size = db.Column(db.String(60))
    PhoneNumber = db.Column(db.String(30))
    URL = db.Column(db.String(250), nullable=False)
    Users = db.relationship('User', backref='company')

    def __repr__(self):
        return '<User {}>'.format(self.Name)


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Firstname = db.Column(db.String(64), nullable=False)
    Surname = db.Column(db.String(64), nullable=False)
    AccessLevel = db.Column(db.String(64), nullable=False)
    Email = db.Column(db.String(64), nullable=False, unique=True)
    Password = db.Column(db.String(128),nullable=False)
    StripeID = db.Column(db.String(128), default=None, unique=True)
    Verified = db.Column(db.String(64), nullable=False, default=None)
    SubID = db.Column(db.String(64), default=None, unique=True)

    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID'), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.Email)
