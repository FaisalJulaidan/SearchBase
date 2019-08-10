from models import db


class Plan(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # Record ID
    Name = db.Column(db.String(64))  # Name of plan
    AccessAssistants = db.Column(db.Boolean(), nullable=False, default=False)
    AccessCampaigns = db.Column(db.Boolean(), nullable=False, default=False)
    AccessAutoPilot = db.Column(db.Boolean(), nullable=False, default=False)
    AccessDatabases = db.Column(db.Boolean(), nullable=False, default=False)
    AccessAppointments = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=True)
    Company = db.relationship('Company', back_populates='Plan')

    # Constraints:
    __table_args__ = (db.UniqueConstraint('Name', 'CompanyID', name='uix1_plan'),)

    def __repr__(self):
        return '<Plan {}>'.format(self.Name)