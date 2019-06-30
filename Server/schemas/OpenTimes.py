from models import db
from sqlalchemy import types

class OpenTimes(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Day = db.Column(db.Integer, nullable=False)
    From = db.Column(types.TIME, nullable=False)
    To = db.Column(types.TIME, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    AutoPilotID = db.Column(db.Integer, db.ForeignKey('auto_pilot.ID', ondelete='cascade'), nullable=False)
    AutoPilot = db.relationship('AutoPilot', back_populates='OpenTimes')

    # Constraints:
    __table_args__ = (
        db.CheckConstraint(db.and_(Day >= 0, Day <= 6)),  # 0 = Sunday, 6 = Saturday
        db.CheckConstraint(From < To),
        db.CheckConstraint(db.and_(Duration > 0, Duration <= 60)),
        db.UniqueConstraint('Day', 'AutoPilotID', name='uix1_open_time_slot'),
    )

    def __repr__(self):
        return '<OpenTime {}>'.format(self.Day)