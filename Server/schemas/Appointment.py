from models import db
from sqlalchemy import Enum
from utilities import enums
from datetime import datetime

class Appointment(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    DateTime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    Status = db.Column(Enum(enums.Status), nullable=False,
                       default=enums.Status.Pending)
    UserTimeZone = db.Column(db.String(200), nullable=False)

    ConversationID = db.Column(db.Integer, db.ForeignKey('conversation.ID', ondelete='cascade'),
                               nullable=False, unique=True)
    Conversation = db.relationship('Conversation', back_populates='Appointment')

    # Constraints:
    __table_args__ = (db.UniqueConstraint('ConversationID', 'DateTime', name='uix2_appointment'),)
