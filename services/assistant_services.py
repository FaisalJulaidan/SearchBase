import sqlalchemy.exc
from flask import session
from services import user_services
from models import db, Company, Assistant


def getByID(id) -> Assistant or None:
    return db.session.query(Assistant).get(id)


def getByNickname(nickname) -> Assistant or None:
    return db.session.query(Assistant).filter(Assistant.Nickname == nickname).first()


def getAll()-> list:
    user = user_services.getByID(session['userID'])
    return user.Company.Assistants

def getAllAsList()-> list:
    myList = []
    user = user_services.getByID(session['userID'])
    for assistant in user.Company.Assistants:
        myList.append({
            "ID": assistant.ID,
            "Nickname": assistant.Nickname
        })

    return myList


def create(nickname, route, message, secondsUntilPopup, company: Company) -> Assistant or None:

    try:
        # Create a new user with its associated company and role
        assistant = Assistant(Nickname=nickname, Route=route, Message=message,
                              SecondsUntilPopup=secondsUntilPopup,
                              Company=company)

        db.session.add(assistant)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return None

    return assistant


def removeByNickname(nickname) -> bool:

    try:
     db.session.query(Assistant).filter(Assistant.Nickname == nickname).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return False

    return True
