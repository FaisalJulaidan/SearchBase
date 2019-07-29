from models import db
from sqlalchemy import types

class AppointmentAllocationTimeInfo(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Day = db.Column(db.Integer, nullable=False)
    From = db.Column(types.TIME, nullable=False)
    To = db.Column(types.TIME, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    AppointmentAllocationTimeID = db.Column(db.Integer, db.ForeignKey('appointment_allocation_time.ID', ondelete='cascade'), nullable=False)
    AppointmentAllocationTime = db.relationship('AppointmentAllocationTime', back_populates='Info')

    # Constraints:
    __table_args__ = (
        db.CheckConstraint(db.and_(Day >= 0, Day <= 6)),  # 0 = Sunday, 6 = Saturday
        db.CheckConstraint(From < To),
        db.CheckConstraint(db.and_(Duration > 0, Duration <= 60)),
        db.UniqueConstraint('Day', 'AppointmentAllocationTimeID', name='uix1_appointment_allocation_time_info'),
    )

    def __repr__(self):
        return '<AppointmentAllocationTimeInfo {}>'.format(self.Day)