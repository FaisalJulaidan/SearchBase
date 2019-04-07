from models import db, Assistant


def migrate_flow():
    assistants = db.session.query(Assistant).all()
    for assistant in assistants:
        if assistant.Flow:
            newFlow = assistant.Flow
            for group in newFlow['groups']:
                for block in group['blocks']:
                    if block['Type'] == "Solutions":
                        block['GGGGG'] = 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
            # print(newFlow)
            db.session.query(Assistant).filter(Assistant == assistant).update({"Flow": newFlow})
    print("Flow Before commit: ", assistants[0].Flow)
    db.session.commit()
    print()
    print("Flow After commit: ", assistants[0].Flow)
