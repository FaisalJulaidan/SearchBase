import enums
from config import BaseConfig

flow = {
    "type": "object",
    "properties": {
        "blocks": {"type": "array", "items": {
            "type": "object",
            "properties":{
                "id": {"type": "integer"},
                "groupID": {"type": "integer"},

                "dataType": {"type": "object",
                             "properties": {
                                 "name": {"enum": [e.value['name'] for e in enums.DataType]},
                                 "validation": {"enum": [e.value for e in enums.ValidationType]}
                             },
                             "required": ["name", "validation"],
                             "additionalProperties": True
                             },

                "type": {"enum": [e.value for e in enums.BlockType]},
                "order": {"type": "integer", "minimum": 1},
                "storeInDB": {"type": "boolean"},
                "isSkippable": { "type": "boolean" },
                "content": {"type": "object"}
            },
            "required": ["id", "groupID", "dataType", "type", "order", "storeInDB", "isSkippable", "content"],
            "additionalProperties": False
        }
                   }
    },
    "required": ["blocks"],
    "additionalProperties": False
}


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


new_block = {
    "type": "object",
    "properties": {
        "block": {
            "type": "object",
            "properties": {
                "type": { "enum": [e.value for e in enums.BlockType]},
                "groupID": {"type": "integer"},
                "dataType": {"type": "object",
                                 "properties": {
                                     "name": {"enum": [e.value['name'] for e in enums.DataType]},
                                     "validation": {"enum": [e.value for e in enums.ValidationType]}
                                 },
                                 "required": ["name", "validation"],
                                 "additionalProperties": True
                             },
                "storeInDB": { "type": "boolean" },
                "isSkippable": { "type": "boolean" },
                "content": { "type": "object" } # Depends on BlockType, see below schemas for content
            },
            "required": ["type","groupID", "dataType", "storeInDB", "content"],
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