from models import db

# Stored files for conversation
class StoredFile(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    FilePath = db.Column(db.String(250), nullable=True, default=None)

    # Relationships:
    ConversationID = db.Column(db.Integer, db.ForeignKey('conversation.ID', ondelete='SET NULL'))
    Conversation = db.relationship('Conversation', back_populates='StoredFile')

    def __repr__(self):
        return '<StoredFile {}>'.format(self.ID)
