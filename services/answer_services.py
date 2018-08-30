from models import Callback, db, Answer


def getByQuestionID(questionID):
    try:
        result = db.session.query(Answer).filter(Answer.QuestionID == questionID).all()

        return Callback(True,
                        "Got answers successfully.",
                        result)
    except Exception as exc:
        print(exc)
        return Callback(False,
                        'Could not get answers by assistant id.')
