from models import Callback, db, Question


def getByAssistantID(assistantID):
    try:
        result = db.session.query(Question).filter(Question.AssistantID == assistantID).all()

        return Callback(True,
                        "Got questions successfully.",
                        result)
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not get questions by assistant id.')

def getUserInput(assistantID):
    try:
        result = db.session.query(Question)\
            .filter(Question.AssistantID == assistantID)\
            .filter(Question.Type == "userInfoRetrieval")\
            .all()

        return Callback(True,
                        "Got questions successfully.",
                        result)
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not get questions by assistant id.')

def reset(assistantID):
    try:
        db.session.query(Question).filter(Question.AssistantID == assistantID).delete()
        db.session.commit()

        return Callback(True,
                        "All questions deleted related to assistant. Ready for updated batch.")
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not delete all questions by assistant id.')

def add(question):
    try:
        db.session.add(question)
        db.session.commit()

        return Callback(True,
                        "Question added")
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not delete all questions by assistant id.')
