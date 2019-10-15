from models import db
from sqlalchemy_utils import CurrencyType

class Candidate(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    CandidateName = db.Column(db.String(64), nullable=True)
    CandidateEmail = db.Column(db.String(64), nullable=True)
    CandidateMobile = db.Column(db.String(20), nullable=True)
    CandidateLocation = db.Column(db.String(64), nullable=False) # Required
    CandidateSkills = db.Column(db.String(5000), nullable=False) # Required
    CandidateLinkdinURL = db.Column(db.String(512), nullable=True)
    CandidateAvailability = db.Column(db.String(120), nullable=True)
    CandidateConsultantName = db.Column(db.String(64), nullable=True)
    CandidateJobTitle = db.Column(db.String(120), nullable=True)
    CandidateEducation = db.Column(db.String(64), nullable=True)
    CandidateYearsExperience = db.Column(db.Float(), nullable=True)
    CandidateDesiredSalary = db.Column(db.Float(), nullable=True)
    Currency = db.Column(CurrencyType, nullable=False) # Required

    # Relationships:
    DatabaseID = db.Column(db.Integer, db.ForeignKey('database.ID', ondelete='cascade'), nullable=False)
    Database = db.relationship('Database')

    def __repr__(self):
        return '<Candidate {}>'.format(self.CandidateName)
