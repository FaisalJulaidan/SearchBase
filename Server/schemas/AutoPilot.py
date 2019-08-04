from models import db, Assistant
class AutoPilot(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.String(260), nullable=True)
    Active = db.Column(db.Boolean, nullable=False, default=True)

    AcceptApplications = db.Column(db.Boolean, nullable=False, default=False)
    AcceptanceScore = db.Column(db.Float(), nullable=False, default=1)
    SendAcceptanceEmail = db.Column(db.Boolean, nullable=False, default=False)
    AcceptanceEmailTitle = db.Column(db.String(128), nullable=False)
    AcceptanceEmailBody = db.Column(db.Text, nullable=False)
    SendAcceptanceSMS = db.Column(db.Boolean, nullable=False, default=False)
    AcceptanceSMSBody = db.Column(db.Text, nullable=False)

    RejectApplications = db.Column(db.Boolean, nullable=False, default=False)
    RejectionScore = db.Column(db.Float(), nullable=False, default=0.05)
    SendRejectionEmail = db.Column(db.Boolean, nullable=False, default=False)
    RejectionEmailTitle = db.Column(db.String(128), nullable=False)
    RejectionEmailBody = db.Column(db.Text, nullable=False)
    SendRejectionSMS = db.Column(db.Boolean, nullable=False, default=False)
    RejectionSMSBody = db.Column(db.Text, nullable=False)

    SendCandidatesAppointments = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='AutoPilots')

    AcceptanceFollowUpAssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', name="fk_acceptance_follow_up_assistant"), nullable=True)
    AcceptanceFollowUpAssistant = db.relationship('Assistant', primaryjoin=AcceptanceFollowUpAssistantID==Assistant.ID, post_update=True)

    RejectionFollowUpAssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', name="fk_rejection_follow_up_assistant"), nullable=True)
    RejectionFollowUpAssistant = db.relationship('Assistant', primaryjoin=RejectionFollowUpAssistantID==Assistant.ID, post_update=True)

    Assistants = db.relationship('Assistant', back_populates='AutoPilot', primaryjoin= ID==Assistant.AutoPilotID)
    OpenTimes = db.relationship('OpenTimes', back_populates='AutoPilot')

    # Constraints:
    # cannot have two auto pilot with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_auto_pilot'),)

    def __repr__(self):
        return '<AutoPilot {}>'.format(self.ID)
