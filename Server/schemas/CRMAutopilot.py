from models import db
class CRMAutoPilot(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Active = db.Column(db.Boolean, nullable=False, default=True)

    LastReferral = db.Column(db.DateTime(), default=None)

    SendReferralEmail = db.Column(db.Boolean, nullable=True, default=False)
    ReferralEmailTitle = db.Column(db.String(260), nullable=True, default=None)
    ReferralEmailBody = db.Column(db.Text, nullable=True, default=None)

    SendReferralSMS = db.Column(db.Boolean, nullable=True, default=False)
    ReferralSMSBody = db.Column(db.Text, nullable=True, default=None)
    
    ReferralAssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='SET NULL'), nullable=True)
    ReferralAssistant = db.relationship('Assistant', back_populates='CRMAutoPilots')

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='CRMAutoPilots')

    CRMS = db.relationship('CRM', back_populates='CRMAutoPilot')


    # Constraints:
    # cannot have two auto pilot with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_crm_auto_pilot'),)

    def __repr__(self):
        return '<CRMAutoPilot {}>'.format(self.ID)
