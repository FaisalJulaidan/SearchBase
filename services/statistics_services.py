from models import db, Company, Statistics, Callback
from services import user_services

def getByAssistantID(id) -> Statistics:
    try:
        query = db.session.query(Statistics).get(id)

        return Callback(True, "Statistic has been retrieved", query) #CHANGED

    except Exception as exc:
        print("statistics_services.getByAssistantID ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Could not retrieve statistic")

    # finally:
       # db.session.close()

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
        db.session.rollback()
        return Callback(False,
                        "Error: Couldn't get total numbers for all assistants")

    # finally:
       # db.session.close()
