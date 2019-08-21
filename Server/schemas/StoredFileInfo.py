from models import db

# Stored files
class StoredFileInfo(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Key = db.Column(db.String(250), nullable=True)
    FilePath = db.Column(db.String(250), nullable=True, default=None)

    StoredFileID = db.Column(db.Integer, db.ForeignKey('stored_file.ID', ondelete='cascade'), nullable=False)
    StoredFile = db.relationship('StoredFile', back_populates='StoredFileInfo')


    def __repr__(self):
        return '<StoredFileInfo {}>'.format(self.ID)
