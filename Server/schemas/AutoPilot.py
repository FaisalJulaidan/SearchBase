from models import db
class AutoPilot(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Active = db.Column(db.Boolean, nullable=False, default=True)

    AcceptApplications = db.Column(db.Boolean, nullable=False, default=False)
    AcceptanceScore = db.Column(db.Float(), nullable=False, default=1)
    SendAcceptanceEmail = db.Column(db.Boolean, nullable=False, default=False)

    RejectApplications = db.Column(db.Boolean, nullable=False, default=False)
    RejectionScore = db.Column(db.Float(), nullable=False, default=0.05)
    SendRejectionEmail = db.Column(db.Boolean, nullable=False, default=False)

    SendCandidatesAppointments = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='AutoPilots')

    AppointmentAllocationTimeID = db.Column(db.Integer, db.ForeignKey('appointment_allocation_time.ID', ondelete='SET NULL'), nullable=True)
    AppointmentAllocationTime = db.relationship('AppointmentAllocationTime', back_populates='AutoPilots')

    Assistants = db.relationship('Assistant', back_populates='AutoPilot')

    # Constraints:
    # cannot have two auto pilot with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_auto_pilot'),)

    def __repr__(self):
        return '<AutoPilot {}>'.format(self.ID)
