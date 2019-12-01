from models import db
from schemas import Assistant, Conversation

class Campaign(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80))
    PreferredJobTitle = db.Column(db.String(80))
    Skills = db.Column(db.String(80))
    Location = db.Column(db.String(80))
    Message = db.Column(db.String(512))
    UseCRM = db.Column(db.Boolean(), nullable=False, default=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Campaigns')

    AssistantID = db.Column(db.Integer, db.ForeignKey('assistant.ID', ondelete='SET NULL'))
    Assistant = db.relationship("Assistant", back_populates="Campaigns")

    MessengerID = db.Column(db.Integer, db.ForeignKey('messenger.ID', ondelete='SET NULL'))
    Messenger = db.relationship("Messenger", back_populates="Campaigns")

    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='SET NULL'))
    Database = db.relationship("Database", back_populates="Campaigns")

    CRMID = db.Column(db.Integer, db.ForeignKey('CRM.ID', ondelete='SET NULL'))
    CRM = db.relationship('CRM', back_populates='Campaigns')

    def __repr__(self):
        return '<Campaign {}>'.format(self.Name)
