import sqlalchemy.exc

from models import Callback, db, Role


def getByID(id) -> Role or None:
    try:
        return Callback(True, 'Role does exist.', db.session.query(Role).get(id))
    except Exception as e:
        return Callback(False, 'Role with id ' + str(id) + ' does not exist')


def getByName(name) -> Role or None:
    try:
        return Callback(True, 'Role does exist.', db.session.query(Role).filter(Role.Name == name).first())
    except Exception as e:
        return Callback(False, 'Role ' + str(name) + ' does not exist')
