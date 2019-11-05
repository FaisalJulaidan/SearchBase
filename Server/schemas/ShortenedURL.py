from models import db
from utilities import enums
from sqlalchemy import Enum
from datetime import datetime

# Stored files
class ShortenedURL(db.Model):

    ID = db.Column(db.String(50), primary_key=True, unique=True)
    URL = db.Column(db.String(250), nullable=False, default=None)
    Expiry = db.Column(db.DateTime(), nullable=True, default=None)
    
    def __repr__(self):
        return '<ShortenedURL {}>'.format(self.ID)
