from flask import session
from services import assistant_services
from utilties import helpers
from typing import List
from config import BaseConfig
from utilties import json_utils
from sqlalchemy.sql import exists, func


from models import db, Callback, User, Company, ValidationType, Assistant, Answer, Block, BlockType, BlockAction, Plan

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


def getBlocksCountByAssistant(assistant: Assistant):
    return db.session.query(func.count(Block)).filter(Block.AssistantID == assistant.ID).scalar()


def addBlock(block: dict, assistant: Assistant) -> Callback:
    # Get company MaxBlocks.
    # Note: we will get Debug plan for now
    print(db.session.query(Plan.MaxBlocks).filter(Plan.Nickname == 'debug').first())
    if getBlocksCountByAssistant(assistant) > db.session.query(Plan.MaxBlocks).filter(Plan.Nickname == 'debug').first():
        return Callback(False, "Blocks limit has been exceeded!")

    # Create a question block with max order + 1 and then return it to client
    # newBlock = Block(Type=BlockType.Question, Order=)
    data =  {
            "id": 1,
            "order": 1,
            "type": "User Input",
            "storeInDB": True,
            "content": {
                "action": "Go To Next Block",
                "text": "What's your email?",
                "blockToGoID": 2,
                "validation": "Email"
            }
     }

    callback: Callback = isValidBlock(block)
    if not callback.Success:
        return callback

    db.session.add(Block(Type=BlockType(block['type']), StoreInDB=block['storeInDB'],
                         Content=block['content'], Assistant=assistant))
    db.session.commit()
    return Callback(True, 'Block added successfully!')




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
    # ------ Block Integrity Validations ------ #
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
    # Validate each block's content depends on its type
    for block in blocks:
        callback: Callback = isValidBlock(block)
        if not callback.Success:
            return callback

        # Update the block
        oldBlock: Block = db.session.query(Block).filter(Block.ID == block['id']).first()
        oldBlock.Order = block['order']
        oldBlock.Type = BlockType(block['type'])
        oldBlock.Content = block['content']

    # Save
    db.session.commit()
    return Callback(True, "Blocks updated successfully")


def isValidBlock(block: dict):

    try:
        json_utils.validateSchema(block['content'], 'blocks/' + str(BlockType(block['type']).name + '.json'))
    except Exception as exc:
        print(exc.args[0])
        db.session.rollback()
        return Callback(False, "the block with id '" +
                        str(block['id']) + "' doesn't follow the correct format of "
                        + str(BlockType(block['type']).value) + " block type", exc.args[0])

    return Callback(True, "Valid block")


def getOptions() -> dict:
    return {
            'botVersion': bot_currentVersion,
            'blockTypes': [ {
                'name': BlockType.UserInput.value,
                'validations': [uiv.value for uiv in ValidationType],
                'actions': [a.value for a in BlockAction],
                'alwaysStoreInDB': True
                },
                {
                'name': BlockType.Question.value,
                'actions': [a.value for a in BlockAction],
                'alwaysStoreInDB': False
                },
                {
                'name': BlockType.FileUpload.value,
                'actions': [a.value for a in BlockAction],
                'typesAllowed': [t for t in BaseConfig.ALLOWED_EXTENSIONS],
                'fileMaxSize': str(int(BaseConfig.MAX_CONTENT_LENGTH/1000000)) + 'MB',
                'alwaysStoreInDB': True

    }
            ],
        'types': ['User Input', 'Question', 'File Upload']

    }
