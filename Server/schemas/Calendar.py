from models import db, JsonEncodedDict, MagicJSON
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy_utils import EncryptedType
from sqlalchemy import Enum
from utilities import enums

import os

class Calendar(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.Calendar), nullable=True)
    Auth = db.Column(EncryptedType(JsonEncodedDict, os.environ['DB_SECRET_KEY'], AesEngine, 'pkcs5'), nullable=True)
    MetaData = db.Column(MagicJSON, nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Calendars')

    Assistants = db.relationship('Assistant', back_populates='Calendar')

    # Constraints:
    # each company will have one CRM of each type
    __table_args__ = (db.UniqueConstraint('Type', 'CompanyID', name='uix1_calendar'),)

    def __repr__(self):
        return '<Calendar {}>'.format(self.ID)