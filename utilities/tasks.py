from models import db, Assistant
from utilities import json_schemas
from jsonschema import validate
import enums
from services import flow_services


def migrate_flow():
    try:
        assistants = db.session.query(Assistant).all()
        for assistant in assistants:
            if assistant.Flow:
                newFlow = assistant.Flow
                for group in newFlow['groups']:
                    for block in group['blocks']:
                        # if block['Type'] == "Solutions":

                        block['SkipText'] = "DFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFFDFFDDDFF"
                        # validate block
                        validate(block.get('Content'), getattr(json_schemas, str(enums.BlockType(block.get('Type')).name)))

                # print(newFlow)

                # validate whole flow then update
                validate(newFlow, json_schemas.flow)
                # assistant.Flow = newFlow
                # callback = flow_services.updateFlow(newFlow, assistant)
                # if not callback.Success:
                #     print("lkjsdflkjsdflkgjsdflkgj")
                #     return

                db.session.query(Assistant).filter(Assistant == assistant).update({"Flow": newFlow})
        print("Flow Before commit: ", assistants[0].Flow)

        db.session.flush()
        db.session.commit()
        print("Flow After commit: ", assistants[0].Flow)

        print("Flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("Flow migration failed :(")



