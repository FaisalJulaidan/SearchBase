from models import db, Assistant
from utilities import json_schemas, helpers
from jsonschema import validate
import enums
from services import flow_services



def migrate_flow():
    try:

        # assistant.Flow = {'gggggg':'elkrjglkwerjglkewrj'}
        # print(assistant.Flow)
        # db.session.commit()



        for i, assistant in enumerate(db.session.query(Assistant).all()):
            assistant.Name = "A" + str(i)
            if assistant.Flow:
                newFlow = helpers.getDictFromSQLAlchemyObj(assistant)['Flow']
                for group in newFlow['groups']:
                    for block in group['blocks']:
                        print(block)
                        # if block['Type'] == "Solutions":
                        block['SkipText'] = "DFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFF"
                        # validate block
                        # validate(block.get('Content'), getattr(json_schemas, str(enums.BlockType(block.get('Type')).name)))

                # print(newFlow)

                # validate whole flow then update
                # validate(newFlow, json_schemas.flow)
                # assistant.Flow = newFlow
                # callback = flow_services.updateFlow(newFlow, assistant)
                # if not callback.Success:
                #     print("lkjsdflkjsdflkgjsdflkgj")
                #     return

                assistant.Flow = newFlow
        # print("Flow Before commit: ", assistants[0].Flow)
        db.session.commit()
        # print("Flow After commit: ", assistants[0].Flow)

        print("Flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("Flow migration failed :(")



