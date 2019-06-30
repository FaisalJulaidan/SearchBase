from models import db, MagicJSON
from .Appointment import Appointment
from .Conversation import Conversation
class Assistant(db.Model):

    @property
    def appointments(self):
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

    CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID'))
    CRM = db.relationship('CRM', back_populates='Assistants')

    CalendarID = db.Column(db.Integer, db.ForeignKey('calendar.ID'))
    Calendar = db.relationship('Calendar', back_populates='Assistants')

    AutoPilotID = db.Column(db.Integer, db.ForeignKey('auto_pilot.ID', ondelete='cascade'))
    AutoPilot = db.relationship("AutoPilot", back_populates="Assistants")

    # - Many to one
    Conversations = db.relationship('Conversation', back_populates='Assistant')

    # Constraints:
    # cannot have two assistants with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_assistant'),)

    def __repr__(self):
        return '<Assistant {}>'.format(self.Name)