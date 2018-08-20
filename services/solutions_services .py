import sqlalchemy.exc

from models import db,Callback,Product

def getByAssistantID(assistantID):

    products_callback : Callback = db.session.query(Product).get(assistantID)

    return products_callback
