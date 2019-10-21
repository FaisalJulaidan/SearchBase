from models import db
from utilities import enums
from sqlalchemy import Enum
from datetime import datetime

# Stored files
class URLShortener(db.Model):

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Key = db.Column(db.String(50), nullable=False, default=None, unique=True)
    URL = db.Column(db.String(250), nullable=False, default=None)
    Expiry = db.Column(db.DateTime(), nullable=False, default=None)
    
    def __repr__(self):
        return '<URLShortener {}>'.format(self.ID)
