from models import db

class AppointmentAllocationTime(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)

    # Relationships:
    #  - Bidirectional
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='AppointmentAllocationTimes')

    AutoPilots = db.relationship('AutoPilot', back_populates='AppointmentAllocationTime')

    Info = db.relationship('AppointmentAllocationTimeInfo', back_populates='AppointmentAllocationTime')

    # Constraints:
    # cannot have two assistants with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_appointment_allocation_time'),)

    def __repr__(self):
        return '<AppointmentAllocationTime {}>'.format(self.Name)