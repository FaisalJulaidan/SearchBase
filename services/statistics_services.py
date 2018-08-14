import sqlalchemy.exc

from flask import session
from models import db, Company, Statistics, Callback
from services import user_services, db_services

def getByAssistantID(id) -> Statistics:
    return db.session.query(Statistics).get(id)

def getTotalAll() -> Callback:
    answered = 0
    products = 0
    try:
        user = user_services.getByID(session['userID'])
        for assistant in user.Company.Assistants:
            statistic = getByAssistantID(assistant.ID)
            answered += statistic.QuestionsAnswered
            products += statistic.ProductsReturned

        return Callback(True,
                        "Got all numbers",
                        Statistics(Name="Average", QuestionsAnswered=answered, ProductsReturned=products))

    except (sqlalchemy.exc.SQLAlchemyError, KeyError) as exc:
        print(exc)
        return Callback(False,
                        "Error: Couldn't get total numbers for all assistants")
