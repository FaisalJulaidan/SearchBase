from models import db

# Stored files
class StoredFile(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    #  - Many to one
    StoredFileInfo = db.relationship('StoredFileInfo', back_populates='StoredFile')


    def __repr__(self):
        return '<StoredFile {}>'.format(self.ID)
