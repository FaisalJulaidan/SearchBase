import sqlalchemy.exc
from flask import session
from services import user_services
from models import db, Company, Assistant
from utilties import helpers

def getByID(id) -> Assistant or None:
    return db.session.query(Assistant).get(id)


def getByNickname(nickname) -> Assistant or None:
    return db.session.query(Assistant).filter(Assistant.Nickname == nickname).first()


def getAll(companyID):
    # we map each record to be a dict then the map object we convert it to a list
    # Explanation: map(function_to_apply, list_of_inputs)

    # Note the results variable is just for explanation purposes we can remove it later
    results = db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()
    return list(map(helpers.object_as_dict, results))

    # return db.session.query(Assistant).filter(Assistant.CompanyID == companyID).all()


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
