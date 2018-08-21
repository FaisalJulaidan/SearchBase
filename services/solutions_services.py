import sqlalchemy.exc

from models import db,Callback,Product

def getByAssistantID(assistantID):

    try:
        if assistantID:
            # Get result and check if None then raise exception
            result = db.session.query(Product).get(assistantID)
            if not result: raise Exception

            return Callback(True, 'Solutions have been successfully retrieved', result)
        else:
            raise Exception
    except Exception as exc:
        return Callback(False, 'Could not retrieve solutions for ID: ' + assistantID)

def deleteAllByAssistantID(assistantID):

    try:
        db.session.query(Product).filter(Product.AssistantID == assistantID).delete()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        print(exc)
        db.session.rollback()
        return False

    return True
