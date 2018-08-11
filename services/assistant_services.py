import sqlalchemy.exc

from models import db, Company, Assistant


def getByID(id) -> Assistant:
    return db.session.query(Assistant).get(id)


def getByEmail(nickname) -> Assistant:
    return db.session.query(Assistant).filter(Assistant.Nickname == nickname).first()


def getAll()-> list:
    return db.session.query(Assistant)


def createAssistant(nickname, route, message , secondsUntilPopup, company: Company) -> Assistant:

    try:
        # Create a new user with its associated company and role
        assistant = Assistant(Nickname=nickname, Route=route, Message=message,
                              SecondsUntilPopup=secondsUntilPopup,
                              Company=company)

        db.session.add(assistant)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return None

    return assistant


def removeByNickname(nickname) -> bool:

    try:
     db.session.query(Assistant).filter(Assistant.Nickname == nickname).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        return False

    return True
