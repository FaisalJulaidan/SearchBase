from flask import json
from config import BaseConfig
from os.path import join, dirname
from jsonschema import validate
import jsonref


def validateSchema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('static/json_schemas', filename)
    absolute_path = join(BaseConfig.APP_ROOT, relative_path)

    base_path = dirname(absolute_path)
    base_uri = 'file://{}/'.format(base_path)

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)


def jsonResponse(success: bool, http_code: int, msg: str, data):
    return json.dumps({'success': success, 'code': http_code, 'msg': msg, 'data': data}),\
            http_code, {'ContentType': 'application/json'}

