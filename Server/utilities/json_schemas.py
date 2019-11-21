from config import BaseConfig
from utilities import enums

assistant_config = {
    "type": "object",
    "properties": {
        "restrictedCountries": {"type": "array", "items": {"type": "string"}},
        "chatbotPosition": {"enum": ["Right", "Left"]},
        # "buttonColor": {"type": "string"},
    },
    "required": ["restrictedCountries", "chatbotPosition"],
    "additionalProperties": False
}


conversation = {
    "type": "object",
    "properties": {
        "collectedData": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "blockID": {"type": "string"},
                "questionText": {"type": "string"},
                "dataType": {"enum": [e.value['name'] for e in enums.DataType]},
                "input": {"type": "string"},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "fileName": {"type": "string"}, # not required
            },
            "required": ["blockID", "questionText", "dataType", "input", "keywords"],
            "additionalProperties": False
        }},
        "keywordsByDataType": {"type": "object", "items": {"type": "array"}},
        "selectedSolutions": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "data": {"type": "object"},
                "databaseType": {"enum": [e.name for e in enums.DatabaseType]},
            },
            "required": ["data", "databaseType"],
            "additionalProperties": False
        }},
    },
    "required": ["collectedData", "keywordsByDataType", "selectedSolutions"],
    "additionalProperties": False
}

flow = {
    "type": "object",
    "properties": {
        "groups": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "blocks": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "ID": {"type": "string"},
                        "DataType": {"enum": [e.name for e in enums.DataType]},
                        "Type": {"enum": [e.value for e in enums.BlockType]},
                        "StoreInDB": {"type": "boolean"},
                        "Skippable": {"type": "boolean"},
                        "SkipText": {"type": ["string"]},
                        "SkipAction": {"enum": [e.value for e in enums.BlockAction]},
                        "SkipBlockToGoID": {"type": ["string", "null"]},
                        "Content": {"type": "object"},
                    },
                    "required": ["ID", "DataType", "Type", "StoreInDB", "Skippable", "SkipAction",
                                 "SkipBlockToGoID", "SkipText", "Content"],
                    "additionalProperties": False
                }
                           }
            },
            "required": ["id", "name", "description", "blocks"],
            "additionalProperties": False
        }
                   },
    },
    "required": ["groups"],
    "additionalProperties": False
}

# ==== Block Types Schemas ====
# Note: the variables names start with capital letters to match the BlockType enums
Question = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "answers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                    "keywords": {"type": "array", "items": {"type": "string"}},
                    "blockToGoID": {"type": ["string", "null"]},
                    "action": {"enum": [e.value for e in enums.BlockAction]},
                    "afterMessage": {"type": "string"},
                    "score": {"type": "integer"},
                },
                "required": ["id", "text", "keywords", "action", "afterMessage", "blockToGoID", "score"],
                "additionalProperties": False
            }
        }
    },
    "required": ["text", "answers"],
    "additionalProperties": False
}

UserInput = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "blockToGoID": {"type": ["string", "null"]},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "afterMessage": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["text", "action", "afterMessage", "blockToGoID", "keywords"],
    "additionalProperties": False
}

FileUpload = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "fileTypes": {"type": "array", "items": {"type": "string", "enum": [t for t in BaseConfig.ALLOWED_EXTENSIONS]}},
        "blockToGoID": {"type": ["string", "null"]},
        "afterMessage": {"type": "string"}
    },
    "required": ["text", "action", "blockToGoID", "afterMessage"
                 ],
    "additionalProperties": False
}

Solutions = {
    "type": "object",
    "properties": {
        "showTop": {"type": "integer", "minimum": 1},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "blockToGoID": {"type": ["string", "null"]},
        "afterMessage": {"type": "string"},
        "databaseType": {"enum": [dbt.name for dbt in enums.DatabaseType]}
    },
    "required": ["showTop", "action", "afterMessage", "blockToGoID", "databaseType"],
    "additionalProperties": False
}

RawText = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "blockToGoID": {"type": ["string", "null"]},
    },
    "required": ["text", "action", "blockToGoID"],
    "additionalProperties": False
}

SalaryPicker = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "min": {"type": "integer", "minimum": 0},
        "max": {"type": "integer", "minimum": 1},
        "period": {"enum": ["Annually", "Daily"]},
        "currency": {"enum": ['GBP', 'USD', 'EUR', 'CAD', 'AUD']},
        "blockToGoID": {"type": ["string", "null"]},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "afterMessage": {"type": "string"},
    },
    "required": ["text", "min", "max", "period", "currency", "blockToGoID", "action", "afterMessage",],
    "additionalProperties": False
}

UserType = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "types": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "value": {"enum": [ut.value for ut in enums.UserType]},
                    "blockToGoID": {"type": ["string", "null"]},
                    "action": {"enum": [e.value for e in enums.BlockAction]},
                    "score": {"type": "integer"},
                    "afterMessage": {"type": "string"},
                },
                "required": ["text", "value", "blockToGoID", "action", "score", "afterMessage"],
                "additionalProperties": False
            }
        }
    },
    "required": ["text", "types"],
    "additionalProperties": False
}

JobType = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "types": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "value": {"enum": [jt.value for jt in enums.JobType]},
                    "blockToGoID": {"type": ["string", "null"]},
                    "action": {"enum": [e.value for e in enums.BlockAction]},
                    "score": {"type": "integer"},
                    "afterMessage": {"type": "string"},
                },
                "required": ["text", "value", "blockToGoID", "action", "score", "afterMessage"],
                "additionalProperties": False
            }
        }
    },
    "required": ["text", "types"],
    "additionalProperties": False
}

DatePicker = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "type": {"enum": ["Exact", "Multiple"]},
        "blockToGoID": {"type": ["string", "null"]},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "afterMessage": {"type": "string"},
    },
    "required": ["text", "type", "action", "blockToGoID", "afterMessage"],
    "additionalProperties": False
}
