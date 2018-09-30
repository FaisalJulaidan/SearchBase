import sqlalchemy.exc

from flask import session
from models import db, Company, Statistics, Callback
from services import user_services, db_services

def getByAssistantID(id) -> Statistics:
    return db.session.query(Statistics).get(id)

def getTotalAll(assistants) -> Callback:
    answered = 0
    products = 0
    try:
        for assistant in assistants:
            statistic = getByAssistantID(assistant.ID)
            answered += statistic.QuestionsAnswered
            products += statistic.ProductsReturned

        return Callback(True,
                        "Got all numbers",
                        Statistics(Name="Average", QuestionsAnswered=answered, ProductsReturned=products))

    except Exception as exc:
        print(exc)
        return Callback(False,
                        "Error: Couldn't get total numbers for all assistants")
