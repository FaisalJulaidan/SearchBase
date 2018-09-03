from flask import session
from services import assistant_services
from utilties import helpers
from typing import List
from config import BaseConfig

from models import db, Callback, User, Company, Question, QuestionUI, QuestionPA, QuestionFU, QuestionType,\
    UserInputValidation, QuestionAction, Assistant

bot_currentVersion = "1.0.0"


def getFeatures() -> dict:
    return {
            'botVersion': bot_currentVersion,
            'userInputType': {
                'name': QuestionType.UserInput.value,
                'validations': [uiv.value for uiv in UserInputValidation],
                'actions': [a.value for a in QuestionAction]
            },
            'PredefinedAnswersType': {
                'name': QuestionType.PredefinedAnswers.value,
                'actionsForAnswers': [a.value for a in QuestionAction]
            },
            'FileUploadType': {
                'name': QuestionType.FileUpload.value,
                'actions': [a.value for a in QuestionAction],
                'typesAllowed': [t for t in BaseConfig.ALLOWED_EXTENSIONS],
                'fileMaxSize': str(BaseConfig.MAX_CONTENT_LENGTH) + 'MB'
            },
           }


def botBuilder(assistant: Assistant) -> dict:

    questions = []

    for question in assistant.Questions:
        if question.Type == QuestionType.UserInput:
            questions.append(questionsUIBuilder(question))
        elif question.Type == QuestionType.PredefinedAnswers:
            questions.append(questionPABuilder(question))
        elif question.Type == QuestionType.FileUpload:
            questions.append(questionsFUBuilder(question))

    bot = {'botVersion': bot_currentVersion,
           'assistant': {'id': assistant.ID, 'name': assistant.Name, 'active': assistant.Active},
           'questions': questions}

    return bot


def questionsUIBuilder(question: Question) -> dict:
    questionUI: QuestionUI = db.session.query(QuestionUI).filter(QuestionUI.Question == question).first()
    return {
            'id': question.ID,
            'type': question.Type.value,
            'order': question.Order,
            'question': question.Text,
            'validation': questionUI.Validation.value,
            'action': questionUI.Action.value,
            'questionToGoID': questionUI.QuestionToGoID,
            'storeInDB': True,
            }


def questionPABuilder(question: Question) -> dict:
    questionPA: QuestionPA = db.session.query(QuestionPA).filter(QuestionPA.Question == question).first()
    answers = []
    for answer in questionPA.Answers:
        answers.append({'answer': answer.Text,
                        'action': answer.Action.value,
                        'questionToGoId': answer.QuestionToGoID,
                        'keywords': answer.Keywords.split(',')})
    return {
            'id': question.ID,
            'type': question.Type.value,
            'order': question.Order,
            'question': question.Text,
            'answers': answers,
            'storeInDB': question.StoreInDB,
            }


def questionsFUBuilder(question: Question) -> dict:
    questionFU: QuestionFU = db.session.query(QuestionFU).filter(QuestionFU.Question == question).first()
    return {
            'id': question.ID,
            'type': question.Type.value,
            'order': question.Order,
            'question': question.Text,
            'fileTypes': questionFU.TypesAllowed.split(','),
            'action': questionFU.Action.value,
            'questionToGoID': questionFU.QuestionToGoID,
            'storeInDB': True,
            }
