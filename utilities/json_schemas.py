import enums
from config import BaseConfig


chatbot_session = {
    "type": "object",
    "properties": {
        "collectedData": {"type": "array", "items": {
            "type": "object",
            "properties":{
                "blockID": {"type": "integer"},
                "questionText": {"type": "string"},
                "dataType": {"enum": [e.value['name'] for e in enums.DataType]},
                "input": {"type": "string"},
                "keywords": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["blockID", "questionText", "dataType", "input", "keywords"],
            "additionalProperties": False
        }
                          },
        "keywords": {"type": "array", "items": {"type": "string"}},
        "keywordsByDataType": {"type": "object", "items": {"type": "object"}},
        "showTop": {"type": "integer"},
        "solutionsReturned": {"type": "integer"},
        "userType": {"enum": [e.value for e in enums.UserType]}
    },
    "required": ["collectedData", "keywords", "keywordsByDataType", "showTop", "solutionsReturned", "userType"],
    "additionalProperties": False
}


flow = {
    "type": "object",
    "properties": {
        "blocks": {"type": "array", "items": {
            "type": "object",
            "properties":{
                "ID": {"type": "integer"},
                "GroupID": {"type": "integer"},

                "DataType": {"type": "object",
                             "properties": {
                                 "name": {"enum": [e.value['name'] for e in enums.DataType]},
                                 "validation": {"enum": [e.value for e in enums.ValidationType]}
                             },
                             "required": ["name", "validation"],
                             "additionalProperties": True
                             },

                "Type": {"enum": [e.value for e in enums.BlockType]},
                "Order": {"type": "integer", "minimum": 1},
                "StoreInDB": {"type": "boolean"},
                "Skippable": { "type": "boolean" },
                "Content": {"type": "object"}
            },
            "required": ["ID", "GroupID", "DataType", "Type", "Order", "StoreInDB", "Skippable", "Content"],
            "additionalProperties": False
        }
                   }
    },
    "required": ["blocks"],
    "additionalProperties": False
}


new_block = {
    "type": "object",
    "properties": {
        "block": {
            "type": "object",
            "properties": {
                "Type": { "enum": [e.value for e in enums.BlockType]},
                "GroupID": {"type": "integer"},
                "DataType": {"type": "object",
                                 "properties": {
                                     "name": {"enum": [e.value['name'] for e in enums.DataType]},
                                     "validation": {"enum": [e.value for e in enums.ValidationType]}
                                 },
                                 "required": ["name", "validation"],
                                 "additionalProperties": True
                             },
                "StoreInDB": { "type": "boolean" },
                "Skippable": { "type": "boolean" },
                "Content": { "type": "object" } # Depends on BlockType, see below schemas for content
            },
            "required": ["Type","GroupID", "DataType", "StoreInDB", "Skippable", "Content"],
            "additionalProperties": False
        }
    },
    "required": ["block"],
    "additionalProperties": False
}


# ==== Block Types Schemas ====
# Note: the variables names start with capital letters intentionally
Question = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "answers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": { "type": "string" },
                    "keywords": { "type": "array", "items": { "type": "string" } },
                    "blockToGoID": { "type": [ "number",  "null" ] },
                    "action": { "enum": [e.value for e in enums.BlockAction]},
                    "afterMessage": { "type": "string"}
                },
                "required": ["text", "keywords", "action", "afterMessage", "blockToGoID"],
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
        "blockToGoID": {"type": ["integer", "null"]},
        "action": { "enum": [e.value for e in enums.BlockAction]},
        "afterMessage": {"type": "string"}
    },
    "required": ["text", "action", "afterMessage", "blockToGoID"],
    "additionalProperties": False
}



FileUpload = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "action": {"enum": [e.value for e in enums.BlockAction]},
        "fileTypes": {"type": "array", "items": {"type": "string", "enum": [t for t in BaseConfig.ALLOWED_EXTENSIONS]}},
        "blockToGoID": { "type": [ "integer", "null" ] },
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
        "action": { "enum": [e.value for e in enums.BlockAction]},
        "blockToGoID": { "type": [ "number",  "null" ] },
        "afterMessage": {"type": "string"}

    },
    "required": ["showTop", "action", "afterMessage", "blockToGoID"],
    "additionalProperties": False
}