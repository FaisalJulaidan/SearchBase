from models import db
from schemas import Assistant, Conversation

class CampaignFollowup(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    HasResponded = db.Column(db.Boolean, nullable=False, default=False)
    LastSent =  db.Column(db.DateTime(), nullable=True)

    # Relationships:
    CampaignID = db.Column(db.Integer, db.ForeignKey('campaign.ID', ondelete='cascade'), nullable=False)
    Campaign = db.relationship('Campaign', back_populates='CampaignFollowup')
    
    UserID = db.Column(db.Integer, db.ForeignKey('user.ID', ondelete='cascade'), nullable=False)
    User = db.relationship('User', back_populates='CampaignFollowup')

    def __repr__(self):
        return '<CampaignFollowup {}>'.format(self.Name)


# SELECT * FROM thesearchbase.conversation WHERE TIMESTAMPDIFF(HOUR, "2019-09-30 14:24:17", CURRENT_TIMESTAMP)



# -- 2019-09-30 14:24:17