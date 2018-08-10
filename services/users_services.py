from models import User
from .db_services import _safeCommit

class UserServices:

    def getByID(id):
        return User.query.get(id)

    def getAll():
        return User.query.get()
