from models import db
from sqlalchemy import Enum
from utilities import enums

class Database(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64), nullable=False)
    Type = db.Column(Enum(enums.DatabaseType), nullable=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    Company = db.relationship('Company', back_populates='Databases')

    # Constraints:
    # Cannot have two databases with the same name under one company
    __table_args__ = (db.UniqueConstraint('CompanyID', 'Name', name='uix1_database'),)

    def __repr__(self):
        return '<Database {}>'.format(self.Name)