from models import db
from schemas import Assistant, Conversation
from utilities import enums

from sqlalchemy import Enum

class Company(db.Model):

    # @property
    # def Conversations(self):
    #     c = db.session.query(Conversation).join(Assistant).filter(Assistant. == self)
    #     return c.all()

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False)
    URL = db.Column(db.String(250), nullable=False)
    StripeID = db.Column(db.String(68), unique=True, nullable=False)
    SubID = db.Column(db.String(68), unique=True, default=None)

    StoredFileID = db.Column(db.Integer, db.ForeignKey('stored_file.ID', ondelete='SET NULL'), nullable=True)
    StoredFile = db.relationship('StoredFile', order_by="desc(StoredFile.ID)")

    TrackingData = db.Column(db.Boolean, nullable=False, default=False)
    TechnicalSupport = db.Column(db.Boolean, nullable=False, default=True)
    AccountSpecialist = db.Column(db.Boolean, nullable=False, default=False)

    HideSignature = db.Column(db.Boolean, nullable=False, default=False)
    Active = db.Column(db.Boolean, nullable=False, default=False)
    # Plan = db.Column(Enum(enums.Plan), server_default=enums.Plan.Basic.name)

    # Relationships:
    Users = db.relationship('User', back_populates='Company')
    Assistants = db.relationship('Assistant', back_populates='Company')
    Databases = db.relationship('Database', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')
    CRMs = db.relationship('CRM', back_populates='Company')
    Calendars = db.relationship('Calendar', back_populates='Company')
    Messengers = db.relationship('Messenger', back_populates='Company')
    AutoPilots = db.relationship('AutoPilot', back_populates='Company')
    Campaigns = db.relationship('Campaign', back_populates='Company')
    AppointmentAllocationTimes = db.relationship('AppointmentAllocationTime', back_populates='Company')
    Webhooks = db.relationship('Webhook', back_populates='Company')


    def __repr__(self):
        return '<Company {}>'.format(self.Name)
