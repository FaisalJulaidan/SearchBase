import sqlalchemy.exc

from models import db,Callback,Product

def getByAssistantID(assistantID):

    products_callback : Callback = db.session.query(Product).get(assistantID)

    return products_callback

def deleteAllByAssistantID(assistantID):

    try:
        db.session.query(Product).filter(Product.AssistantID == assistantID).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
        return False

    return True
