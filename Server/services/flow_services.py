import os

from flask import request
from jsonschema import validate

from sqlalchemy.orm import joinedload
from models import db, Callback, Assistant
from services import options_services
from utilities import json_schemas, helpers, enums
import json


# ----- Getters ----- #
# Get the chatbot for the public to use
def getChatbot(assistantHashID) -> Callback:
    try:
        assistantID = helpers.decodeID(assistantHashID)
        if not assistantID:
            return Callback(False, "Assistant not found!", None)

        assistant: Assistant = db.session.query(Assistant).options(joinedload("Company").joinedload("StoredFile").joinedload("StoredFileInfo"))\
                                     .filter(Assistant.ID == assistantID[0]).first()
        
        if not assistant:
            return Callback(False, '')

        # Check for restricted countries
        try:
            ip = helpers.getRemoteAddress()
            if ip != '127.0.0.1' and assistant.Config:
                restrictedCountries = assistant.Config.get('restrictedCountries', [])
                if len(restrictedCountries):
                    if helpers.geoIP.country(ip).country.iso_code in restrictedCountries:
                        return Callback(True, '', {'assistant': assistant, 'isDisabled': True})
        except Exception as exc:
            helpers.logError("flow_service.getChatbot() geoIP restrict countries: " + str(exc))
            pass

        assistantDict = helpers.getDictFromSQLAlchemyObj(assistant)

        # Get assistant logo if null then override it with company logo
        logoPath = helpers.keyFromStoredFile(assistant.StoredFile, enums.FileAssetType.Logo).AbsFilePath
        if not logoPath:
            logoPath = helpers.keyFromStoredFile(assistant.Company.StoredFile, enums.FileAssetType.Logo).AbsFilePath
        assistantDict['LogoPath'] = logoPath

        data = {
            "assistant": assistantDict,
            "companyName": assistant.Company.Name,
            "isDisabled": False,
            "currencies": options_services.getOptions().Data['databases']['currencyCodes']
        }

        return Callback(True, '', data)

    except Exception as exc:
        helpers.logError("flow_service.getChatbot(): " + str(exc))
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
        helpers.logError("flow_service.updateFlow(): " + str(exc.args))
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
        helpers.logError("flow_service.isValidFlow(): " + str(exc.args))
        return Callback(False, "The submitted Flow doesn't follow the correct format")


# Check if the block valid using json_schema.py based on the block's type
def isValidBlock(block: dict, blockType: str):
    try:
        validate(block.get('Content'), getattr(json_schemas, blockType))
    except Exception as exc:
        helpers.logError("flow_service.getChatbot(): " + str(exc.args[0]))
        blockType = block.get('Type')
        msg = "Block data doesn't follow the correct format"
        if blockType:
            msg = "the Block with id '" + block.get('ID') + "' doesn't follow the correct format of " \
                  + str(enums.BlockType(blockType).value) + " block type"
        return Callback(False, msg, exc.args[0])

    return Callback(True, "Valid block")


# This function will be used to replace all enum.name to enums.value
def parseFlow(flow: dict):
    try:
        for group in flow['groups']:
            for block in group['blocks']:
                block['DataType'] = enums.DataType[block['DataType']].value
        return flow
    except Exception as exc:
        helpers.logError("flow_service.parseFlow(): " + str(exc))
