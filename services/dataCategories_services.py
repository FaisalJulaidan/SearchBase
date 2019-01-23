

from models import Callback, db, DataCategory

def getAll() -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(DataCategory).all()
        if not result: raise Exception
        return Callback(True, 'Categories found.',result)

    except Exception as e:
        print(e)
        return Callback(False, 'Error in finding categories')

    # finally:
    # db.session.close()


def getAllByIndustry(industry) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(DataCategory).filter(DataCategory.Industry == industry).all()
        if not result: raise Exception
        return Callback(True, 'Categories found.',result)

    except Exception as e:
        print(e)
        return Callback(False, 'Error in finding data categories based on industry')

    # finally:
    # db.session.close()

def getCategoryByID(id) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(DataCategory).filter(DataCategory.ID == id).first()
        if not result: raise Exception
        return Callback(True, 'Category found.', result)

    except Exception as e:
        print(e)
        return Callback(False, 'Could not find data category')

    # finally:
       # db.session.close()

