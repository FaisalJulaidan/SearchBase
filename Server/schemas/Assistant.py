from models import db, MagicJSON
# from schemas.Webhook import owners_table
from .Appointment import Appointment
from .Conversation import Conversation


class Assistant(db.Model):

    @property
    def Appointments(self):
        q = Appointment.query.join(Conversation).filter(Conversation.Assistant == self)
        return q.all()

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Flow = db.Column(MagicJSON, nullable=True)
    Message = db.Column(db.String(500), nullable=False)
    TopBarText = db.Column(db.String(64), nullable=False)
    SecondsUntilPopup = db.Column(db.Float, nullable=False, default=0.0)

    LastNotificationDate = db.Column(db.DateTime(), nullable=True)
    NotifyEvery = db.Column(db.Integer, nullable=True)
    Active = db.Column(db.Boolean(), nullable=False, default=True)
    Config = db.Column(MagicJSON, nullable=True)

    # Relationships:
    #  - Bidirectional
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Assistants')

    CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID', ondelete='SET NULL'))
    CRM = db.relationship('CRM', back_populates='Assistants')

    CalendarID = db.Column(db.Integer, db.ForeignKey('calendar.ID', ondelete='SET NULL'))
    Calendar = db.relationship('Calendar', back_populates='Assistants')

    MessengerID = db.Column(db.Integer, db.ForeignKey('messenger.ID', ondelete='SET NULL'))
    Messenger = db.relationship("Messenger", back_populates="Assistants")

    AutoPilotID = db.Column(db.Integer, db.ForeignKey('auto_pilot.ID', ondelete='SET NULL'))
    AutoPilot = db.relationship("AutoPilot", back_populates="Assistants", foreign_keys=[AutoPilotID])

    StoredFileID = db.Column(db.Integer, db.ForeignKey('stored_file.ID', ondelete='SET NULL'), nullable=True)
    StoredFile = db.relationship('StoredFile', order_by="desc(StoredFile.ID)")

    UserID = db.Column(db.Integer, db.ForeignKey('user.ID', ondelete='SET NULL'))
    User = db.relationship('User', back_populates='Assistants')
    #  - Many to one
    Conversations = db.relationship('Conversation', back_populates='Assistant')

    Campaigns = db.relationship('Campaign', back_populates='Assistant')

    # Users = db.relationship("Parent", secondary=owners_table, back_populates="Assistants")

    # Constraints:
    # cannot have two assistants with the same name under one company
    
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)

    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)