from models import db
from sqlalchemy_utils import CurrencyType

class Job(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    JobTitle = db.Column(db.String(64), nullable=False) # Required
    JobDescription = db.Column(db.String(5000), nullable=True)
    JobStreet = db.Column(db.String(64), nullable=True)
    JobCity = db.Column(db.String(64), nullable=True) 
    JobPostCode = db.Column(db.String(64), nullable=True)
    JobCountry = db.Column(db.String(64), nullable=True) 
    JobSalary = db.Column(db.Float(), nullable=False, default=0)
    Currency = db.Column(CurrencyType, nullable=False) # Required
    JobType = db.Column(db.String(64), nullable=True)
    JobEssentialSkills = db.Column(db.String(5000), nullable=True)
    JobYearsRequired = db.Column(db.Integer, nullable=True, default=0)
    JobStartDate = db.Column(db.DateTime(), nullable=True)
    JobEndDate = db.Column(db.DateTime(), nullable=True)
    JobLinkURL = db.Column(db.String(612), nullable=True)

    # Relationships:
    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Job {}>'.format(self.JobTitle)
