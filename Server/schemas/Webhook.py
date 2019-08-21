from models import db

# Stored files
class Webhook(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    URL = db.Column(db.String(250), nullable=False)
    Secret = db.Column(db.String(250), nullable=True)
    Subscriptions = db.Column(db.String(250), nullable=False)
    LastSent = db.Column(db.DateTime(), nullable=True)
    LastError = db.Column(db.String(250), nullable=True)

    #Relationships
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Webhooks')


def __repr__(self):
        return '<Webhooks {}>'.format(self.ID)
