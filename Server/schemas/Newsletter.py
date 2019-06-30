from models import db

class Newsletter(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Email = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return '<Newsletters {}>'.format(self.Email)