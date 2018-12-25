import json
from os.path import join
from typing import List

from sqlalchemy import and_
from sqlalchemy.sql import exists, func

from config import BaseConfig
from models import db, Callback, ValidationType, Assistant, Block, BlockType, BlockAction, Plan, BlockGroup
from utilities import json_utils, helpers

bot_currentVersion = "1.0.0"


# ----- Getters ----- #
# Get the chatbot for the public to use
def getChatbot(assistant: Assistant) -> dict:
    return {'assistant': {'id': helpers.encrypt_id(assistant.ID), 'name': assistant.Name, 'message': assistant.Message,
                          'secondsUntilPopup': assistant.SecondsUntilPopup, 'active': assistant.Active},
            'blocks': getAllBlocks(assistant)}


# Get the flow for the company to manage the blocks
def getFlow(assistant: Assistant) -> Callback:
    blockGroups = getBlockGroups(assistant)
    if not blockGroups:
        data = {'botVersion': bot_currentVersion,
                'assistant': helpers.getDictFromSQLAlchemyObj(assistant),
                'blockGroups': []}
        return Callback(True, 'Could not retrieve flow', data)

    data = {'botVersion': bot_currentVersion,
            'assistant': helpers.getDictFromSQLAlchemyObj(assistant),
            'blockGroups': blockGroups}
    return Callback(True, 'Flow retrieved successfully', data)


# Get the block groups each group having its list of blocks
def getBlockGroups(assistant: Assistant) -> List[dict]:
    try:
        result: List[BlockGroup] = db.session.query(BlockGroup).filter(BlockGroup.AssistantID == assistant.ID)
        groups = []
        for group in result:
            groups.append({'id': group.ID, 'name': group.Name, 'description': group.Description,
                           'blocks': getBlocksByGroup(group)})
        return groups
    except Exception as e:
        print("getBlockGroups ERROR:", e)
        db.session.rollback()
        return None
    # finally:
    # db.session.close()


# Get the block groups each group having its list of blocks
def getGroupByID(id) -> Callback:
    try:
        if not id:
            return Callback(False, "Group id is required")
        group: BlockGroup = db.session.query(BlockGroup).get(id)
        if not group: raise Exception
        return Callback(True, "Group retrieved successfully.", group)

    except Exception as e:
        print("getGroups ERROR:", e)
        db.session.rollback()
        return Callback(False, 'Could not retrieve group.')
    # finally:
    # db.session.close()


# Get the list of blocks by group
def getBlocksByGroup(group: BlockGroup) -> List[dict]:
    try:
        blocks = []
        for block in group.Blocks:
            blocks.append({'id': block.ID, 'type': block.Type.value, 'order': block.Order,
                           'content': block.Content, 'storeInDB': block.StoreInDB,
                           'labels': block.Labels, 'isSkippable': block.Skippable})
        return blocks
    except Exception as e:
        print("getBlocks ERROR:", e)
        db.session.rollback()
    # finally:
    # db.session.close()


# Get all the given assistant blocks without its group. will be used for chatbot to not bother with groups
def getAllBlocks(assistant: Assistant) -> List[dict]:
    try:
        groups: List[BlockGroup] = db.session.query(BlockGroup).filter(BlockGroup.AssistantID == assistant.ID)
        blocks = []
        for group in groups:
            for block in group.Blocks:
                blocks.append({'id': block.ID, 'type': block.Type.value, 'order': block.Order,
                               'content': block.Content, 'storeInDB': block.StoreInDB, 'labels': block.Labels,
                               'isSkippable': block.Skippable})
        return blocks
    except Exception as e:
        print("getBlocks ERROR:", e)
        db.session.rollback()
    # finally:
    # db.session.close()


# ----- Adders ----- #
def addGroup(group: dict, assistant: Assistant) -> Callback:
    try:
        newGroup = BlockGroup(Name=group.get('name'), Description=group.get('description'), Assistant=assistant)
        db.session.add(newGroup)
        db.session.commit()
        return Callback(True, 'Group added successfully!', {"groupID": newGroup.ID})

    except Exception as exc:
        db.session.rollback()
        print("flow_services.addBlock ERROR: ", exc)
        return Callback(False, 'Error occurred while creating a new Group', exc.args[0])
    # finally:
    # db.session.close()


def addBlock(data: dict, group: BlockGroup) -> Callback:
    try:

        # Validate submitted block content using json schema
        json_utils.validateSchema(data, 'blocks/newBlock.json')
        block = data.get('block')

        # Set the block with max order + 1
        maxOrder = db.session.query(func.max(Block.Order)).filter(Block.GroupID == group.ID).scalar()
        if maxOrder is None:
            maxOrder = 0

        newBlock = Block(Type=BlockType(block['type']), Order=maxOrder + 1, Content=block['content'],
                         StoreInDB=block['storeInDB'], Skippable=block['isSkippable'],
                         Labels=block['labels'], Group=group)
        db.session.add(newBlock)
        db.session.commit()

        return Callback(True, 'Block added successfully!', {"newBlockID": newBlock.ID})
    except Exception as exc:
        db.session.rollback()
        print("flow_services.addBlock ERROR: ", exc)
        return Callback(False, 'An error occurred while creating a new Block', exc.args[0])
    # finally:
    # db.session.close()


# ----- Updaters ----- #
def updateFlow(flow, assistant: Assistant) -> Callback:
    try:
        json_utils.validateSchema(flow, 'flow.json')
    except Exception as exc:
        print(exc.args)
        return Callback(False, "The submitted bot data does not doesn't follow the correct format")

    callback: Callback = updateBlocks(flow['blocks'], assistant)
    if not callback.Success:
        return Callback(False, callback.Message, callback.Data)
    return Callback(True, "Bot updated successfully!")


def updateGroup(data: dict, assistant: Assistant, ) -> Callback:
    try:
        # Update the group
        group: BlockGroup = db.session.query(BlockGroup). \
            filter(and_(BlockGroup.ID == data.get('id'), Assistant.ID == assistant.ID)).first()
        group.Name = data.get('name')
        group.Description = data.get('description')

        # Save
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return Callback(False, "An error occurred while updating the group.")
    # finally:
    # db.session.close()
    return Callback(True, "Group updated successfully.")


def updateBlocks(blocks, assistant: Assistant) -> Callback:
    # ------ Block Integrity Validations ------ #
    orders = []
    ids = []
    for block in blocks:
        # order is the visual id to be displayed to the user, while id is is the real id of the block in the DB.
        order = block.get('order')
        id = block.get('id')

        try:
            # Make sure all submitted blocks exist in the database
            if not db.session.query(exists().where(Block.ID == id)).scalar():
                return Callback(False, "the block of id '" + str(order) + "' id doesn't exist in the database")
        except Exception as e:
            db.session.rollback()
            return Callback(False, "Error while dealing with block id '" + str(order) + "'")
        # finally:
        #    db.session.close()

        # Make sure each block has a unique id
        if id not in ids:
            ids.append(id)
        else:
            return Callback(False, "two blocks shouldn't have the same id."
                                   " Check block with id '" + str(order) + "'")

        # Make sure each question has a unique order value >> 'order': 1
        if order not in orders:
            orders.append(order)
        else:
            return Callback(False, "two questions shouldn't have the same order value."
                                   " Check question with id '" + str(order) + "'")

    # Make sure order values are consecutive  e.g. [1,2,3] (correct), [1,2,4] (incorrect)
    numOfBlocks = len(blocks)
    if not set(orders).issubset([*range(1, numOfBlocks + 1)]):
        return Callback(False, "blocks' order values should be consecutive"
                               " e.g. [1,2,3] or [1,3,2] (correct), [1,2,4] (incorrect)")

    # Make sure the number of submitted questions is equivalent to what stored in the database
    # if numOfBlocks != len(group.Blocks):
    #     return Callback(False, "The number of submitted blocks isn't equivalent to what stored in the database")

    # After full validation of blocks' data integrity, we will update the blocks one by one.
    try:
        for block in blocks:
            callback: Callback = isValidBlock(block, str(BlockType(block.get('type')).name))
            if not callback.Success:
                return callback

            # Update the block
            oldBlock: Block = db.session.query(Block). \
                filter(and_(Block.ID == block.get('id'), Assistant.ID == assistant.ID)).first()
            oldBlock.Type = BlockType(block.get('type'))
            oldBlock.Content = block.get('content')
            oldBlock.StoreInDB = block.get('storeInDB')
            oldBlock.Skippable = block.get('isSkippable')
            oldBlock.Order = block.get('order')
            oldBlock.Labels = block.get('labels')
            oldBlock.GroupID = block.get('groupID')

        # Save
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return Callback(False, "Error occurred while updating blocks.")
    # finally:
    # db.session.close()
    return Callback(True, "Blocks updated successfully.")


# ----- Removers ----- #
def deleteGroupByID(id, assistant: Assistant) -> Callback:
    try:
        if not id:
            return Callback(False, "Group id is required")
        group: BlockGroup = db.session.query(BlockGroup).filter(
            and_(BlockGroup.ID == id, Assistant.ID == assistant.ID)).first()
        if not group:
            return Callback(False, "Group doesn't exist")

        # Delete and Save
        db.session.delete(group)
        db.session.commit()
        return Callback(True, "Group removed successfully.", None)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "Group could not be removed.")
    # finally:
    # db.session.close()


def deleteBlockByID(id, assistant: Assistant) -> Callback:
    try:
        if not id:
            return Callback(False, "Group id is required.")
        block: Block = db.session.query(Block).filter(and_(Block.ID == id, Assistant.ID == assistant.ID)).first()
        if not block:
            return Callback(False, "Block doesn't exist.")

        # Save and Delete
        db.session.delete(block)
        db.session.commit()
        return Callback(True, "Block removed successfully.", None)

    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, "Block could not be removed.")
    # finally:
    # db.session.close()


def deleteAllBlock(assistant: Assistant) -> Callback:
    try:
        db.session.query(Block).filter(Block.AssistantID == assistant.ID).delete()
        db.session.commit()
        return Callback(True, 'Blocks has been deleted.')

    except Exception as exc:
        print("Error in deleteAllBlock(): ", exc)
        db.session.rollback()
        return Callback(False, 'Error in deleting blocks.')
    # finally:
    # db.session.close()


def isValidBlock(block: dict, blockType: str):
    try:
        json_utils.validateSchema(block.get('content'), 'blocks/' + blockType + '.json')
    except Exception as exc:
        print(exc.args[0])
        # order is the visual id to be displayed to the user, while id is is the real id of the block in the DB.
        blockID = block.get('order')
        blockType = block.get('type')
        msg = "Block data doesn't follow the correct format"

        if blockType and blockID:
            msg = "the block with id '" + str(blockID) + "' doesn't follow the correct format of " \
                  + str(BlockType(blockType).value) + " block type"

        return Callback(False, msg, exc.args[0])
    return Callback(True, "Valid block")


def getOptions() -> dict:
    return {
        'botVersion': bot_currentVersion,
        'types': [a.value for a in BlockType],
        'blockTypes': [{
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
                'fileMaxSize': str(int(BaseConfig.MAX_CONTENT_LENGTH / 1000000)) + 'MB',
                'alwaysStoreInDB': True
            },
            {
                'name': BlockType.Solutions.value,
                'maxSolutions': 5,
                'actions': [a.value for a in BlockAction],
            },
        ]
    }


# ----- Extras ----- #
def getBlocksCountByAssistant(assistant: Assistant):
    try:
        return db.session.query(func.count(Block.ID)).filter(Block.AssistantID == assistant.ID).scalar()
    except Exception as e:
        db.session.rollback()
    # finally:
    # db.session.close()


def getRemainingBlocksByAssistant(assistant: Assistant):
    try:
        # BlocksCap = numberOfCreatedBlocks
        return db.session.query(Plan.MaxBlocks).filter(Plan.Nickname == 'debug').first()[0] - getBlocksCountByAssistant(
            assistant)
    except Exception as e:
        db.session.rollback()
    # finally:
    # db.session.close()


def genFlowViaTemplateUplaod(assistant: Assistant, data: dict):
    try:
        # Validate submitted block data
        json_utils.validateSchema(data, 'flowTemplate.json')
        print(data.get('bot')['blocks'][0])
        if not deleteAllBlock(assistant).Success:
            return Callback(False, 'Error in deleting blocks')

        counter = 1
        for block in data.get('bot')['blocks']:
            db.session.add(Block(Type=BlockType(block['type']), Order=counter, Content=block['content'],
                                 StoreInDB=block['storeInDB'], Skippable=block['isSkippable'], Assistant=assistant))
            counter += 1
        # Save
        db.session.commit()
        return Callback(True, 'Template was successfully uploaded')
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Error while uploading a bot via a template')
    # finally:
    # db.session.close()


# Generate a bot using an already built template
def genFlowViaTemplate(assistant: Assistant, tempName: str):
    try:
        # Get json template
        relative_path = join('static/bot_templates', tempName + '.json')
        absolute_path = join(BaseConfig.APP_ROOT, relative_path)
        data = json.load(open(absolute_path))

        # Validate submitted block data

        json_utils.validateSchema(data, 'flowTemplate.json')
        counter = 1
        for block in data.get('bot')['blocks']:
            db.session.add(Block(Type=BlockType(block['type']), Order=counter, Content=block['content'],
                                 StoreInDB=block['storeInDB'], Skippable=block['isSkippable'], Assistant=assistant))
            counter += 1
        # Save
        db.session.commit()
        return Callback(True, 'Bot was successfully generated via a template')
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return Callback(False, 'Error while generating a bot via a template')
    # finally:
    # db.session.close()
