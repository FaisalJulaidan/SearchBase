from models import db, Assistant
from utilities import json_schemas
from jsonschema import validate
import enums
import copy


# NOTE: Make sure to take a backup of the database before running this function
def migrateFlow():
    try:
        for assistant in db.session.query(Assistant).all():
            if assistant.Flow:
                newFlow = copy.deepcopy(assistant.Flow) # deep clone is IMPORTANT
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

                # Update flow
                assistant.Flow = newFlow

        # Save all changes
        db.session.commit()
        print("Flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("Flow migration failed :(")



