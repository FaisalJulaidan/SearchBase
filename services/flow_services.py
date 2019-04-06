

import enums
from models import db, Callback, Assistant
from services import assistant_services
from jsonschema import validate
from utilities import json_schemas, helpers
import logging

bot_currentVersion = "1.0.0"


# ----- Getters ----- #
# Get the chatbot for the public to use
def getChatbot(assistantHashID) -> Callback:
    try:

        callback: Callback = assistant_services.getAssistantByHashID(assistantHashID)
        if not callback.Success:
            return Callback(False, "Assistant not found!")
        assistant: Assistant = helpers.getDictFromSQLAlchemyObj(callback.Data)

        assistant['ID'] = assistantHashID  # Use the assistant hashID instead of the integer one
        del assistant['CompanyID']
        del assistant['MailEnabled']
        del assistant['MailPeriod']

        data = {
            "assistant": assistant,
            # "dataTypes": [dt.value for dt in enums.DataType]
        }

        return Callback(True, '', data)

    except Exception as exc:
        print(" flow_service.getChatbot() ERROR: ", exc)
        logging.error("flow_service.getChatbot(): " + str(exc))
        return Callback(False, 'Could not retrieve the chatbot flow. Contact TSB team please!')


# ----- Updaters ----- #
def updateFlow(flow, assistant: Assistant) -> Callback:
    try:

        callback: Callback = isValidFlow(flow)
        if not callback.Success:
            return callback

        # Update flow and save
        assistant.Flow = flow
        db.session.commit()
        return Callback(True, "Flow updated successfully!")

    except Exception as exc:
        print(exc.args)
        logging.error("flow_service.updateFlow(): " + str(exc.args))
        return Callback(False, "The submitted Flow doesn't follow the correct format")


def isValidFlow(flow):
    try:
        # Validate the flow in high level
        validate(flow, json_schemas.flow)

        groupIDs = []
        for group in flow['groups']:
            # Make sure each Group has a unique id
            if group['id'] not in groupIDs:
                groupIDs.append(id)
            else:
                return Callback(False, "two groups shouldn't have the same id."
                                       " Check group with id '" + str(group['id']) + "'")

            # Ensure each Block has a unique id
            blockIDs = []
            for block in group['blocks']:
                if block['ID'] not in blockIDs:
                    blockIDs.append(id)
                else:
                    return Callback(False, "two blocks shouldn't have the same id."
                                           " Check Block with ID '" + str(block['id']) +
                                    "' in Group of ID '" + str(group['id']) + "'")

                # Validate the individual block against the json_schemas based on block's type
                callback: Callback = isValidBlock(block, str(enums.BlockType(block.get('Type')).name))
                if not callback.Success:
                    return callback
        return Callback(True, "Flow is valid")

    except Exception as exc:
        print(exc.args)
        logging.error("flow_service.isValidFlow(): " + str(exc.args))
        return Callback(False, "The submitted Flow doesn't follow the correct format")

# Check if the block valid using json_schema.py based on the block's type
def isValidBlock(block: dict, blockType: str):
    try:
        validate(block.get('Content'), getattr(json_schemas, blockType))
    except Exception as exc:

        print(exc.args[0])
        logging.error("flow_service.getChatbot(): " + str(exc.args[0]))

        blockType = block.get('Type')
        msg = "Block data doesn't follow the correct format"
        if blockType:
            msg = "the Block with id '" + block.get('ID') + "' doesn't follow the correct format of " \
                  + str(enums.BlockType(blockType).value) + " block type"
        return Callback(False, msg, exc.args[0])
    return Callback(True, "Valid block")


# This function will be used to replace all enum.name to enums.value
# flow is passed by reference so no need to return  a new one
def parseFlow (flow: dict):
    for group in flow['groups']:
        for block in group['blocks']:
            block['DataType'] = enums.DataType[block['DataType']].value

