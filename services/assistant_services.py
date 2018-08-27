import sqlalchemy.exc
from models import db, Company, Assistant,Callback
from utilties import helpers


def getByID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant).get(id)
        if not result: raise Exception

        return Callback(True,
                        "Got assistant by id successfully.",
                        result)
    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        print(exc)
        return Callback(False,
                        'Could not get the assistant by id.')
    

def getByNickname(nickname) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Assistant).filter(Assistant.Nickname == nickname).first()
        if not result: raise Exception

        return Callback(True,
                        "Got assistant by nickname successfully.",
                        result)
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not get the assistant by nickname.')


def getAll(companyID) -> Callback:
    try:
        if companyID:
            # Get result and check if None then raise exception
            result = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
            if len(result) == 0:
                return Callback(True,"No assistants  to be retrieved.", [])

            return Callback(True, "Got all assistants  successfully.", result)

    except Exception as exc:
        print(exc)
        return Callback(True,
                        'Could not get all assistants.')


def create(nickname, route, message, secondsUntilPopup, company: Company) -> Assistant or None:
    try:
        assistant = Assistant(Nickname=nickname, Route=route, Message=message,
                              SecondsUntilPopup=secondsUntilPopup,
                              Company=company)

        db.session.add(assistant)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
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
        db.session.rollback()
        return Callback(False,
                        "Couldn't update assistant "+nickname)

def removeByNickname(nickname) -> bool:
    try:
        db.session.query(Assistant).filter(Assistant.Nickname == nickname).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
        return False

    return True
