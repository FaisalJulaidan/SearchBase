from models import Callback, db, Question


def getByAssistantID(assistantID):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Question).filter(Question.AssistantID == assistantID).all()
        if not result: raise Exception

        return Callback(True,
                        "Got questions successfully.",
                        result)
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not questions by assistant id.')
