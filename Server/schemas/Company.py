from models import db

class Company(db.Model):

    @property
    def logo(self):
        from services import stored_file_services as sfs
        logo = sfs.PUBLIC_URL + sfs.UPLOAD_FOLDER + sfs.COMPANY_LOGOS_PATH + "/" + (
                self.LogoPath or "")
        return logo if self.LogoPath else None

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(80), nullable=False)
    URL = db.Column(db.String(250), nullable=False)
    LogoPath = db.Column(db.String(64), nullable=True)
    StripeID = db.Column(db.String(68), unique=True, nullable=False)
    SubID = db.Column(db.String(68), unique=True, default=None)

    TrackingData = db.Column(db.Boolean, nullable=False, default=False)
    TechnicalSupport = db.Column(db.Boolean, nullable=False, default=True)
    AccountSpecialist = db.Column(db.Boolean, nullable=False, default=False)

    HideSignature = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships:
    Users = db.relationship('User', back_populates='Company')
    Assistants = db.relationship('Assistant', back_populates='Company')
    Databases = db.relationship('Database', back_populates='Company')
    Roles = db.relationship('Role', back_populates='Company')
    CRMs = db.relationship('CRM', back_populates='Company')
    Calendars = db.relationship('Calendar', back_populates='Company')
    Messengers = db.relationship('Messenger', back_populates='Company')
    AutoPilots = db.relationship('AutoPilot', back_populates='Company')
    Plan = db.relationship('Plan', back_populates='Company')

    def __repr__(self):
        return '<Company {}>'.format(self.Name)
