from models import db, Assistant
import enums

def migrate_flow():
    assistants = db.session.query(Assistant).all()
    for assistant in assistants:
        if(assistant.Flow):
            newFlow = assistant.Flow
            for group in newFlow['groups']:
                for block in group['blocks']:
                    if block['Type'] == "Solutions":
                        block['GGGGG'] = 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
            print(newFlow)
            assistant.Flow = newFlow
        db.session.commit()