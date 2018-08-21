import sqlalchemy.exc
from models import db, Company, Assistant, Callback
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

