from models import db, JsonEncodedDict
from sqlalchemy import Enum
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy_utils import EncryptedType
from utilities import enums
import os

class Messenger(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.Messenger), nullable=True)
    Auth = db.Column(EncryptedType(JsonEncodedDict, os.environ['DB_SECRET_KEY'], AesEngine, 'pkcs5'), nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Messengers')

    # Constraints:
    # each company will have one Messenger of each type
    __table_args__ = (db.UniqueConstraint('Type', 'CompanyID', name='uix1_messenger'),)

    def __repr__(self):
        return '<Messenger {}>'.format(self.ID)