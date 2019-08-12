from models import db, MagicJSON
from datetime import datetime
from sqlalchemy import Enum
from utilities import enums

class Conversation(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    Name = db.Column(db.String(64), nullable=True)
    Email = db.Column(db.String(64), nullable=True)
    PhoneNumber = db.Column(db.String(30), nullable=True)

    Data = db.Column(MagicJSON, nullable=False)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    TimeSpent = db.Column(db.Integer, nullable=False, default=0)
    SolutionsReturned = db.Column(db.Integer, nullable=False, default=0)
    QuestionsAnswered = db.Column(db.Integer, nullable=False, default=0)
    UserType = db.Column(Enum(enums.UserType), nullable=False)

    Completed = db.Column(db.Boolean, nullable=False, default=True)
    ApplicationStatus = db.Column(Enum(enums.Status), nullable=False,
                                  default=enums.Status.Pending)
    Score = db.Column(db.Float(), nullable=False)

    AcceptanceEmailSentAt = db.Column(db.DateTime(), default=None)
    RejectionEmailSentAt = db.Column(db.DateTime(), default=None)
    AcceptanceSMSSentAt = db.Column(db.DateTime(), default=None)
    RejectionSMSSentAt = db.Column(db.DateTime(), default=None)
    AppointmentEmailSentAt = db.Column(db.DateTime(), default=None)

    AutoPilotStatus = db.Column(db.Boolean, nullable=False, default=False)
    AutoPilotResponse = db.Column(db.String(250), nullable=True)

    CRMSynced = db.Column(db.Boolean, nullable=False, default=False)
    CRMResponse = db.Column(db.String(2500), nullable=True)

    # Relationships:
    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='cascade'), nullable=False)
    Assistant = db.relationship('Assistant', back_populates='Conversations')

    StoredFileID = db.Column(db.Integer, db.ForeignKey('stored_file.ID'), nullable=True)
    StoredFile = db.relationship('StoredFile')

    Appointment = db.relationship('Appointment', uselist=False, back_populates='Conversation')

    def __repr__(self):
        return '<Conversation {} with AssistantID {}>'.format(self.ID, self.AssistantID)
