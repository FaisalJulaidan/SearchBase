from models import db
class Role(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(64))
    EditChatbots = db.Column(db.Boolean(), nullable=False, default=False)
    AddUsers = db.Column(db.Boolean(), nullable=False, default=False)
    EditUsers = db.Column(db.Boolean(), nullable=False, default=False)
    DeleteUsers = db.Column(db.Boolean(), nullable=False, default=False)
    AccessBilling = db.Column(db.Boolean(), nullable=False, default=False)

    # Relationships:
    CompanyID = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=True)
    Company = db.relationship('Company', back_populates='Roles')

    Users = db.relationship('User', back_populates="Role")

    # Constraints:
    __table_args__ = (db.UniqueConstraint('Name', 'CompanyID', name='uix1_role'),)

    def __repr__(self):
        return '<Role {}>'.format(self.Name)