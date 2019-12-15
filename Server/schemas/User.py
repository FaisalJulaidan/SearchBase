from models import db
from datetime import datetime
from sqlalchemy_utils import PasswordType

# from schemas.Webhook import owners_table


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Firstname = db.Column(db.String(64), nullable=False)
    Surname = db.Column(db.String(64), nullable=False)
    Email = db.Column(db.String(64), nullable=False)
    PhoneNumber = db.Column(db.String(30))
    TimeZone = db.Column(db.String(200))
    Password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ))

    Verified = db.Column(db.Boolean(), nullable=False, default=False)
    ChatbotNotifications = db.Column(db.Boolean, nullable=False, default=True)
    LastAccess = db.Column(db.DateTime(), nullable=True)
    CreatedOn = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Users')

    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID', ondelete='SET NULL'))
    Role = db.relationship('Role', back_populates='Users')

    Assistants = db.relationship('Assistant', back_populates='User')

    # Assistants = db.relationship(
    #     "Assistant",
    #     secondary=owners_table,
    #     back_populates="Users")

    # Constraints:
    __table_args__ = (db.UniqueConstraint('Email', name='uix1_user'),)

    def __repr__(self):
        return '<User {}>'.format(self.Email)
