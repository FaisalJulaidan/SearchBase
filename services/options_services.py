
import enums
from config import BaseConfig
from models import Callback, Candidate, Job

bot_currentVersion = "1.0.0"


# ----- Getters ----- #
def getOptions(industry=None) -> Callback:

    options =  {
        'flow': {
            'botVersion': bot_currentVersion,
            'types': [a.value for a in enums.BlockType],
            'userTypes': [uiv.value for uiv in enums.UserType],
            'dataTypes': [uiv.value for uiv in enums.DataType],
            'blockTypes': [
                {
                    'name': enums.BlockType.UserInput.value,
                    'actions': [a.value for a in enums.BlockAction],
                    'alwaysStoreInDB': True
                },
                {
                    'name': enums.BlockType.Question.value,
                    'actions': [a.value for a in enums.BlockAction],
                    'alwaysStoreInDB': False
                },
                {
                    'name': enums.BlockType.FileUpload.value,
                    'actions': [a.value for a in enums.BlockAction],
                    'typesAllowed': [t for t in BaseConfig.ALLOWED_EXTENSIONS],
                    'fileMaxSize': str(int(BaseConfig.MAX_CONTENT_LENGTH / 1000000)) + 'MB',
                    'alwaysStoreInDB': True
                },
                {
                    'name': enums.BlockType.Solutions.value,
                    'maxSolutions': 5,
                    'actions': [a.value for a in enums.BlockAction],
                },
            ]
        },
        'databases': {
            'types': [dt.name for dt in enums.DatabaseType ],
            enums.DatabaseType.Candidates.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                                 for c in Candidate.__table__.columns
                                                 if (c.key != 'ID' and c.key != 'DatabaseID')],
            enums.DatabaseType.Jobs.name: [{'column':c.key, 'type':str(c.type), 'nullable': c.nullable}
                                           for c in Job.__table__.columns
                                           if (c.key != 'ID' and c.key != 'DatabaseID')],
            'currencyCodes': ['GBP', 'USD', 'EUR', 'AED', 'CAD']
        },
        'assistantTemplates':
        [
            {
                'group': 'Recruitment',
                'children': [
                    {'label': 'Recruitment 1', 'fileName': 'recruitment1'},
                ]
             }
        ]

    }
    return Callback(True, '', options)