from flask import session
from services import assistant_services
from utilties import helpers
from typing import List
from config import BaseConfig
from utilties import json_utils
from sqlalchemy.sql import exists


from models import db, Callback, User, Company, ValidationType, Assistant, Answer, Block, BlockType, BlockAction

bot_currentVersion = "1.0.0"


def getBot(assistant: Assistant):
    return {'botVersion': bot_currentVersion,
            'assistant': {'id': assistant.ID, 'name': assistant.Name, 'active': assistant.Active},
            'blocks': getBlocks(assistant)}


def getBlocks(assistant: Assistant) -> List[dict]:
    result: List[Block] = db.session.query(Block).filter(Block.AssistantID == assistant.ID).all()
    blocks = []
    for block in result:
        blocks.append({'id': block.ID, 'type': block.Type.value, 'order': block.Order,
                       'content': block.Content, 'storeInDB': block.StoreInDB})
    return blocks


def updateBot(bot, assistant: Assistant) -> Callback:
    try:
        json_utils.validateSchema(bot, 'bot.json')
    except Exception as exc:
        print(exc.args)
        return Callback(False, "the bot does not doesn't follow the correct format")

    callback: Callback = updateBlocks(bot['blocks'], assistant)
    if not callback.Success:
        return Callback(False, callback.Message, callback.Data)
    return Callback(True, "Bot updated successfully!")


def updateBlocks(blocks, assistant: Assistant) -> Callback:
    # ------ Validations Block Integrity ------ #
    orders = []
    ids = []
    for block in blocks:
        order = block['order']
        id = block['id']

        # Make sure all submitted questions exist in the database
        if not db.session.query(exists().where(Block.ID == id)).scalar():
            return Callback(False, "the block of id '" + str(id) + "' doesn't exist in the database")

        # Make sure each question has a unique id
        if id not in ids:
            ids.append(id)
        else:
            return Callback(False, "two blocks shouldn't have the same id."
                                   " Check block with id '" + str(id) + "'")

        # Make sure each question has a unique order value >> 'order': 1
        if order not in orders:
            orders.append(order)
        else:
            return Callback(False, "two questions shouldn't have the same order value."
                                   " Check question with id '" + str(id) + "'")

    # Make sure order values are consecutive  e.g. [1,2,3] (correct), [1,2,4] (incorrect)
    numOfBlocks = len(blocks)
    if not set(orders).issubset([*range(1, numOfBlocks + 1)]):
        return Callback(False, "blocks' order values should be consecutive"
                               " e.g. [1,2,3] or [1,3,2] (correct), [1,2,4] (incorrect)")

    # Make sure the number of submitted questions is equivalent to what stored in the database
    if numOfBlocks != len(assistant.Blocks):
        return Callback(False, "The number of submitted blocks isn't equivalent to what stored in the database")
    # ------------------------- #

    # ------ Update each block's content ------ #
    for block in blocks:
        callback: Callback = Callback(False, "Block type is not recognised")
        if block['type'].strip() == BlockType.UserInput.value:
            callback = isValidBlock(block, BlockType.UserInput, 'userInput.json')

        elif block['type'].strip() == BlockType.Question.value:
            callback = isValidBlock(block, BlockType.Question, 'question.json')

        elif block['type'].strip() == BlockType.FileUpload.value:
            callback = isValidBlock(block, BlockType.FileUpload, 'fileUpload.json')

        if not callback.Success:
            return callback

        oldBlock: Block = db.session.query(Block).filter(Block.ID == block['id']).first()
        oldBlock.Order = block['order']
        oldBlock.Type = BlockType(block['type'])
        oldBlock.Content = block['content']
        # Save
        db.session.commit()
        print(block['id'])
        print(block['order'])
    return Callback(True, "Blocks updated successfully")


def isValidBlock(block: dict, type: BlockType, fileName):
    try:
        json_utils.validateSchema(block['content'], 'blocks/' + fileName)
    except Exception as exc:
        print(exc.args[0])
        return Callback(False, "the block with id '" +
                        str(block['id']) + "' doesn't follow the correct format of "
                        + type.value + " block type", exc.args[0])
    return Callback(True, "Valid block")


# ===== OLD ========

# def update(botData, assistant: Assistant):
#     try:
#         json_utils.validateSchema(botData, 'bot.json')
#     except Exception as exc:
#         print(exc.args)
#         return Callback(False, "Your bot data doesn't follow the correct format")
#
#     # ------ Validations ------ #
#     orders = []
#     ids = []
#     for question in botData['questions']:
#         order = question['order']
#         id = question['id']
#
#         # Make sure all submitted questions exist in the database
#         if not db.session.query(exists().where(Question.ID == id)).scalar():
#             return Callback(False, "the question of id '" + str(id) + "' doesn't exist in the database")
#
#         # Make sure each question has a unique id
#         if id not in ids:
#             ids.append(id)
#         else:
#             return Callback(False, "two questions shouldn't have the same id."
#                                    " Check question with id '" + str(id) + "'")
#
#         # Make sure each question has a unique order value >> 'order': 1
#         if order not in orders:
#             orders.append(order)
#         else:
#             return Callback(False, "two questions shouldn't have the same order value."
#                                    " Check question with id '" + str(id) + "'")
#
#     # Make sure order values are consecutive  e.g. [1,2,3] (correct), [1,2,4] (incorrect)
#     numOfQuestions = len(botData['questions'])
#     if not set(orders).issubset([*range(1, numOfQuestions+1)]):
#         return Callback(False, "questions' order values should be consecutive"
#                                " e.g. [1,2,3] or [1,3,2] (correct), [1,2,4] (incorrect)")
#
#     # Make sure the number of submitted questions is equivalent to what stored in the database
#     if numOfQuestions != len(assistant.Questions):
#         return Callback(False, "The number of submitted questions isn't equivalent to what stored in the database")
#     # ------------------------- #
#
#     # Update each question
#     for question in botData['questions']:
#         if question['type'].strip() == QuestionType.UserInput.value:
#             try:
#                 json_utils.validateSchema(botData, 'userInput.json')
#             except Exception as exc:
#                 print(exc.args)
#                 return Callback(False, "the question with id '" +
#                                 str(question['id']) + "' doesn't follow the correct format of "
#                                 + QuestionType.UserInput.value + " question type")
#             questionsUIHandler(question)
#         # elif question['type'].strip() == QuestionType.PredefinedAnswers.value:
#         #     questionsPAHandler(question)
#         # elif question['type'].strip() == QuestionType.FileUpload.value:
#         #     questionsFUHandler(question)
#
#     return Callback(True, "COOL")
#
#
# def questionsUIHandler(newQuestion):
#     oldQuestion: Question = db.session.query(Question).filter(Question.ID == newQuestion['id']).first()
#     if newQuestion['type'] != oldQuestion.Type.value:
#         changeInQuestionHandler(oldQuestion, newQuestion)
#     else:
#         oldQuestionUI: QuestionUI = db.session.query(QuestionUI).filter(QuestionUI.ID == newQuestion['id']).first()
#         oldQuestion.Text = newQuestion['question']
#         oldQuestion.Order = newQuestion['order']
#         oldQuestion.StoreInDB = True
#         oldQuestionUI.Action = QuestionAction(newQuestion['action'])
#         oldQuestionUI.Validation = ValidationType(newQuestion['validation'])
#         oldQuestionUI.QuestionToGoID = newQuestion['questionToGoID']
#     db.session.commit()
#
#
# def questionsPAHandler(newQuestion):
#     oldQuestion: Question = db.session.query(Question).filter(Question.ID == newQuestion['id']).first()
#     if newQuestion['type'] != oldQuestion.Type.value:
#         changeInQuestionHandler(oldQuestion, newQuestion)
#     else:
#         oldQuestionPA: QuestionPA = db.session.query(QuestionPA).filter(QuestionPA.ID == newQuestion['id']).first()
#         oldQuestion.Text = newQuestion['question']
#         oldQuestion.Order = newQuestion['order']
#         oldQuestion.StoreInDB = True
#
#
#         oldQuestionPA.Validation = ValidationType(newQuestion['validation'])
#         oldQuestionPA.QuestionToGoID = newQuestion['questionToGoID']
#         oldQuestionPA.Action = QuestionAction(newQuestion['action'])
#
#     db.session.commit()
#
# def answerChangeHnadler(newAnswer):
#     # What to do when deleting, updating and creating new answers???????
#     oldAnswer: Answer = db.session.query(Answer).filter(Question.ID == newAnswer['id']).first()
#
# def questionsFUHandler(question):
#     pass
#
# def changeInQuestionHandler(oldQ: Question, newQ: dict):
#     oldQ.Type = QuestionType(newQ['type'])
#     print()
#     db.session.delete(oldQ)
#     db.session.commit()
#
#
# def getOptions() -> dict:
#     return {
#             'botVersion': bot_currentVersion,
#             'userInputType': {
#                 'name': QuestionType.UserInput.value,
#                 'validations': [uiv.value for uiv in ValidationType],
#                 'actions': [a.value for a in QuestionAction]
#             },
#             'PredefinedAnswersType': {
#                 'name': QuestionType.PredefinedAnswers.value,
#                 'actionsForAnswers': [a.value for a in QuestionAction]
#             },
#             'FileUploadType': {
#                 'name': QuestionType.FileUpload.value,
#                 'actions': [a.value for a in QuestionAction],
#                 'typesAllowed': [t for t in BaseConfig.ALLOWED_EXTENSIONS],
#                 'fileMaxSize': BaseConfig.MAX_CONTENT_LENGTH + 'MB'
#
#             },
#            }
#
#
# def botBuilder(assistant: Assistant) -> dict:
#
#     questions = []
#
#     for question in assistant.Questions:
#         if question.Type == QuestionType.UserInput:
#             questions.append(questionsUIBuilder(question))
#         elif question.Type == QuestionType.PredefinedAnswers:
#             questions.append(questionPABuilder(question))
#         elif question.Type == QuestionType.FileUpload:
#             questions.append(questionsFUBuilder(question))
#
#     bot = {'botVersion': bot_currentVersion,
#            'assistant': {'id': assistant.ID, 'name': assistant.Name, 'active': assistant.Active},
#            'questions': questions}
#
#     return bot
#
#
# def questionsUIBuilder(question: Question) -> dict:
#     questionUI: QuestionUI = db.session.query(QuestionUI).filter(QuestionUI.Question == question).first()
#     return {
#             'id': question.ID,
#             'type': question.Type.value,
#             'order': question.Order,
#             'question': question.Text,
#             'validation': questionUI.Validation.value,
#             'action': questionUI.Action.value,
#             'questionToGoID': questionUI.QuestionToGoID,
#             'storeInDB': True,
#             }
#
#
# def questionPABuilder(question: Question) -> dict:
#     questionPA: QuestionPA = db.session.query(QuestionPA).filter(QuestionPA.Question == question).first()
#     answers = []
#     for answer in questionPA.Answers:
#         answers.append({'id': answer.ID,
#                         'answer': answer.Text,
#                         'action': answer.Action.value,
#                         'questionToGoId': answer.QuestionToGoID,
#                         'keywords': answer.Keywords.split(',')})
#     return {
#             'id': question.ID,
#             'type': question.Type.value,
#             'order': question.Order,
#             'question': question.Text,
#             'answers': answers,
#             'storeInDB': question.StoreInDB,
#             }
#
#
# def questionsFUBuilder(question: Question) -> dict:
#     questionFU: QuestionFU = db.session.query(QuestionFU).filter(QuestionFU.Question == question).first()
#     return {
#             'id': question.ID,
#             'type': question.Type.value,
#             'order': question.Order,
#             'question': question.Text,
#             'fileTypes': questionFU.TypesAllowed.split(','),
#             'action': questionFU.Action.value,
#             'questionToGoID': questionFU.QuestionToGoID,
#             'storeInDB': True,
#             }