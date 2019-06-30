import copy
import json
import os
from os.path import join

from config import BaseConfig
from jsonschema import validate
from models import db, Assistant
from utilities import json_schemas, enums


# NOTE: Make sure to take a backup of the database before running this function
# =============================================================================


def migrateFlows():
    try:
        for assistant in db.session.query(Assistant).all():
            if assistant.Flow:
                # Update flow
                newFlow = __migrateFlow(assistant.Flow)
                if not newFlow:
                    raise Exception(assistant.ID + ' failed')

                # Update in database only if there are 0 errors
                assistant.Flow = newFlow

        # Save all changes
        db.session.commit()
        print("Flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("migrateFlows failed :(")


def migrateFlowTemplates():
    try:
        directory = join(BaseConfig.APP_ROOT, 'static/assistant_templates')
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                jsonFile = open(directory+'/'+filename, 'r') # Open the JSON file for reading
                flow = json.load(jsonFile) # Read the JSON into the buffer
                jsonFile.close() # Close the JSON file

                # Migrate
                newFlow = __migrateFlow(flow)
                if not newFlow:
                    raise Exception(filename + ' failed')

                ## Save our changes to JSON file
                jsonFile = open(directory+'/'+filename, "w+")
                jsonFile.write(json.dumps(newFlow))
                jsonFile.close()
                continue
            else:
                continue

        print("Templates flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        print("migrateFlowTemplates failed :(")


def __migrateFlow(flow):
    try:
        newFlow = copy.deepcopy(flow) # deep clone is IMPORTANT
        for group in newFlow['groups']: # loop groups
            for block in group['blocks']: # loop blocks

                if block['Type'] == enums.BlockType.Question.value:
                    for answer in block['Content']['answers']:
                        answer['score']= 0

                if block['Type'] == enums.BlockType.UserInput.value:
                    block['Content']['keywords']= []

                if block['Type'] == enums.BlockType.Solutions.value:
                    pass

                if block['Type'] == enums.BlockType.FileUpload.value:
                    pass

                # validate block content based on block type
                validate(block.get('Content'), getattr(json_schemas, str(enums.BlockType(block.get('Type')).name)))

        # validate whole flow then update
        validate(newFlow, json_schemas.flow)

        return newFlow

    except Exception as exc:
        print(exc.args)
        print("Flow migration failed :(")
        return None
