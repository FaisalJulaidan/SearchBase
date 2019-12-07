from models import db, JsonEncodedDict
from sqlalchemy import Enum
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy_utils import EncryptedType
from utilities import enums
import os

class CRM(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Type = db.Column(Enum(enums.CRM), nullable=True)
    Auth = db.Column(EncryptedType(JsonEncodedDict, os.environ['DB_SECRET_KEY'], AesEngine, 'pkcs5'), nullable=True)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='CRMs')

    Assistants = db.relationship('Assistant', back_populates='CRM')

    Campaigns = db.relationship('Campaign', back_populates='CRM')

    CRMAutoPilotID = db.Column(db.Integer, db.ForeignKey('crm_auto_pilot.ID', name="CRMAutoPilotID", ondelete='SET NULL'))
    CRMAutoPilot = db.relationship("CRMAutoPilot", back_populates="CRMS", foreign_keys=[CRMAutoPilotID])


    # Constraints:
    # each company will have one CRM of each type
    __table_args__ = (db.UniqueConstraint('Type', 'CompanyID', name='uix1_crm'),)

    def __repr__(self):
        return '<CRM {}>'.format(self.ID)