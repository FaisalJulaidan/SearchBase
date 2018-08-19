import sqlalchemy.exc
from models import db, Company, Assistant,Callback
from utilties import helpers


def getByID(id) -> Callback:
    try:
        return Callback(True,
                        "Got assistant by id successfully.",
                        db.session.query(Assistant).get(id))
    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        print(exc)
        return Callback(False,
                        'Could not get the assistant by id.')


def getByNickname(nickname) -> Assistant or None:
    return db.session.query(Assistant).filter(Assistant.Nickname == nickname).first()


def getAll(companyID) -> list:
    return db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()


def create(nickname, route, message, secondsUntilPopup, company: Company) -> Assistant or None:
    try:
        assistant = Assistant(Nickname=nickname, Route=route, Message=message,
                              SecondsUntilPopup=secondsUntilPopup,
                              Company=company)

        db.session.add(assistant)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return None

    return assistant


def update(id, nickname, message, secondsUntilPopup)-> Callback:
    try:
        db.session.query(Assistant).filter(Assistant.ID == id).update({'Nickname': nickname,
                                                                       'Message': message,
                                                                       'SecondsUntilPopup': secondsUntilPopup})
        db.session.commit()

        return Callback(True,
                        nickname+' Updated Successfully')

    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return Callback(False,
                        "Couldn't update assistant "+nickname)

def removeByNickname(nickname) -> bool:
    try:
     db.session.query(Assistant).filter(Assistant.Nickname == nickname).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        return False

    return True
