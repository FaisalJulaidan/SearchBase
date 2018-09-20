from flask import session
from services import assistant_services
from utilties import helpers
from typing import List
from config import BaseConfig
from utilties import json_utils
from sqlalchemy.sql import exists, func


from models import db, Callback, User, Company, ValidationType, Assistant, Answer, Block, BlockType, BlockAction, Plan

bot_currentVersion = "1.0.0"


# Get the chatbot for the public to use
def getChatbot(assistant: Assistant) -> dict:
    return {'assistant': {'id': assistant.ID, 'name': assistant.Name, 'message': assistant.Message,
                          'secondsUntilPopup': assistant.SecondsUntilPopup, 'active': assistant.Active},
            'blocks': getBlocks(assistant)}


# Get the bot for the company to manage the blocks in bot.html
def getBot(assistant: Assistant) -> dict:
    return {'botVersion': bot_currentVersion,
            'assistant': {'id': assistant.ID, 'name': assistant.Name, 'message': assistant.Message,
                          'secondsUntilPopup': assistant.SecondsUntilPopup, 'active': assistant.Active},
            'remainingBlocks': getRemainingBlocksByAssistant(assistant),
            'blocks': getBlocks(assistant)}


def getBlocks(assistant: Assistant) -> List[dict]:
    result: List[Block] = db.session.query(Block).filter(Block.AssistantID == assistant.ID)\
        .order_by(Block.Order.asc()).all()
    blocks = []
    for block in result:
        blocks.append({'id': block.ID, 'type': block.Type.value, 'order': block.Order,
                       'content': block.Content, 'storeInDB': block.StoreInDB})
    return blocks


def getBlocksCountByAssistant(assistant: Assistant):
    return db.session.query(func.count(Block.ID)).filter(Block.AssistantID == assistant.ID).scalar()


def getRemainingBlocksByAssistant(assistant: Assistant):
    # BlocksCap - numberOfCreatedBlocks
    return db.session.query(Plan.MaxBlocks).filter(Plan.Nickname == 'debug').first()[0] - getBlocksCountByAssistant(assistant)


def addBlock(data: dict, assistant: Assistant) -> Callback:
    # Get company MaxBlocks.
    # Note: we will get Debug plan for now
    if getBlocksCountByAssistant(assistant) >= db.session.query(Plan.MaxBlocks).filter(Plan.Nickname == 'debug').first()[0]:
        return Callback(False, "Blocks limit has been exceeded!")

    # Set the block with max order + 1
    maxOrder = db.session.query(func.max(Block.Order)).filter(Block.AssistantID == assistant.ID).scalar()
    if maxOrder is None: maxOrder = 0

    try:
        # Validate submitted block data
        json_utils.validateSchema(data, 'blocks/newBlock.json')
        block = data.get('block')
        newBlock = Block(Type=BlockType(block['type']), Order=maxOrder + 1, Content=None,
                         StoreInDB=block['storeInDB'], Assistant=assistant)
        db.session.add(newBlock)
    except Exception as exc:
        db.session.rollback()
        print(exc.args[0])
        return Callback(False, 'Error occurred while creating a new Block object', exc.args[0])

    db.session.commit()
    return Callback(True, 'Block added successfully!', {"newBlockID": newBlock.ID,
                                                        "remainingBlocks": getRemainingBlocksByAssistant(assistant)})


def updateBot(bot, assistant: Assistant) -> Callback:
    try:
        json_utils.validateSchema(bot, 'bot.json')
    except Exception as exc:
        print(exc.args)
        return Callback(False, "The submitted bot data does not doesn't follow the correct format")

    callback: Callback = updateBlocks(bot['blocks'], assistant)
    if not callback.Success:
        return Callback(False, callback.Message, callback.Data)
    return Callback(True, "Bot updated successfully!")


def updateBlocks(blocks, assistant: Assistant) -> Callback:
    # ------ Block Integrity Validations ------ #
    orders = []
    ids = []
    for block in blocks:
        order = block.get('order')
        id = block.get('id')

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
        callback: Callback = isValidBlock(block, str(BlockType(block.get('type')).name))
        if not callback.Success:
            return callback

        # Update the block
        oldBlock: Block = db.session.query(Block).filter(Block.ID == block.get('id')).first()
        oldBlock.Order = block.get('order')
        oldBlock.Type = BlockType(block.get('type'))
        oldBlock.Content = block.get('content')
        oldBlock.StoreInDB = block.get('storeInDB')

    # Save
    db.session.commit()
    return Callback(True, "Blocks updated successfully")


def deleteBlockByID(id) -> Callback:
    try:
        block: Block = db.session.query(Block).filter(Block.ID == id).first()
        if not block:
            return Callback(False, "the block with id '" + str(id) + "' doesn't exist")
        assistant: Assistant = block.Assistant
        db.session.query(Block).filter(Block.ID == id).delete()
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Block with id' + str(id) + " could not be removed.")
    # Save
    db.session.commit()
    return Callback(True, 'Block with id ' + str(id) + " has been removed successfully.",
                    {"remainingBlocks": getRemainingBlocksByAssistant(assistant)})


def isValidBlock(block: dict, blockType: str):

    try:
        json_utils.validateSchema(block.get('content'), 'blocks/' + blockType + '.json')
    except Exception as exc:
        print(exc.args[0])
        db.session.rollback()
        blockID = block.get('id')
        blockType = block.get('type')
        msg = "Block data doesn't follow the correct format"

        if blockType and blockID:
            msg = "the block with id '" + str(blockID) + "' doesn't follow the correct format of "\
                  + str(BlockType(blockType).value) + " block type"

        return Callback(False, msg, exc.args[0])
    return Callback(True, "Valid block")


def getOptions() -> dict:
    return {
        'botVersion': bot_currentVersion,
        'types': [a.value for a in BlockType],
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
            },
            {
            'name': BlockType.Solutions.value,
            'maxSolutions': 5
            },
        ]
    }
