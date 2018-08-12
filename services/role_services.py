import sqlalchemy.exc

from models import db, Role


def getByID(id) -> Role or None:
    return db.session.query(Role).get(id)


def getByName(name) -> Role or None:
    return db.session.query(Role).filter(Role.Name == name).first()
