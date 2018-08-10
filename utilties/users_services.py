from models import User


class UserServices:

    def getByID(id):
        return User.query.get(id)
