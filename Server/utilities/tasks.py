import copy
import json
import os
from os.path import join

from jsonschema import validate

from config import BaseConfig
from models import db, Assistant, Conversation, StoredFileInfo
from services import stored_file_services
from utilities import json_schemas, enums
from sqlalchemy.orm import joinedload
from typing import List
import boto3
from botocore.exceptions import ClientError

salaryPicker = {
    "min": 100,
    "max": 200,
    "period": "Annually",
    "currency": "GBP",
}

jobType = {
    "types": [
        {
            "value": "Permanent",
            "text": "Permanent",
        },
        {
            "value": "Contract",
            "text": "Contract",
        }
    ]
}

datePicker = {
    "type": "Range",
}

userType = {
    "text": "User Type",
    "types": [
        {
            "value": "Candidate",
            "text": "Candidate",
        },
        {
            "value": "Client",
            "text": "Client",
        }
    ]
}


# NOTE: Make sure to take a backup of the database before running these functions
# =============================================================================

def cleanStoredFiles():
    try:
        files: List[StoredFileInfo] = db.session.query(StoredFileInfo).filter(StoredFileInfo.StoredFileID == None).all()

        if len(files) == 0 or files is None:
            return "No files to delete..."

        for file in files:
            key = file.FilePath
            try:
                session = boto3.session.Session()
                s3 = session.client('s3',
                                    region_name='ams3',
                                    endpoint_url=os.environ['SPACES_SERVER_URI'],
                                    aws_access_key_id=os.environ['SPACES_PUBLIC_KEY'],
                                    aws_secret_access_key=os.environ['SPACES_SECRET_KEY'])
                # Delete file
                response = s3.delete_object(
                    Bucket=stored_file_services.BUCKET,
                    Key=key
                )

                db.session.delete(file)
            except ClientError as e:
                raise Exception("DigitalOcean Error")

        db.session.commit()
        print("Files found to delete")
    except Exception as exc:
        return print("Couldn't find files to delete")


def migrateConversations():
    try:
        for conversation in db.session.query(Conversation).options(
                joinedload('StoredFile').joinedload("StoredFileInfo")).all():
            counter = 0
            storedFile = conversation.StoredFile
            if storedFile:
                # print(storedFile.StoredFileInfo)
                newData = copy.deepcopy(conversation.Data)  # deep clone is IMPORTANT
                for cd in newData['collectedData']:
                    if cd['input'] == "&FILE_UPLOAD&":
                        cd["fileName"] = storedFile.StoredFileInfo[counter].FilePath
                        counter += 1
                conversation.Data = newData

        # Save all changes
        db.session.commit()
        print("Conversation migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("migrateConversation failed :(")


def migrateFlows():
    try:
        for assistant in db.session.query(Assistant).all():
            if assistant.Flow:
                # Update flow
                newFlow = __migrateFlow(assistant.Flow)
                if not newFlow:
                    raise Exception(assistant.ID + ' failed')

                # Update in database only if there are 0 errors
                assistant.Flow = newFlow

        # Save all changes
        db.session.commit()
        print("Flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        db.session.rollback()
        print("migrateFlows failed :(")


def migrateFlowTemplates():
    try:
        directory = join(BaseConfig.APP_ROOT, 'static/assistant_templates')
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                jsonFile = open(directory + '/' + filename, 'r')  # Open the JSON file for reading
                flow = json.load(jsonFile)  # Read the JSON into the buffer
                jsonFile.close()  # Close the JSON file

                # Migrate
                newFlow = __migrateFlow(flow)
                if not newFlow:
                    raise Exception(filename + ' failed')

                ## Save our changes to JSON file
                jsonFile = open(directory + '/' + filename, "w+")
                jsonFile.write(json.dumps(newFlow))
                jsonFile.close()
                continue
            else:
                continue

        print("Templates flow migration done successfully :)")

    except Exception as exc:
        print(exc.args)
        print("migrateFlowTemplates failed :(")


def __migrateFlow(flow):
    try:
        newFlow = copy.deepcopy(flow)  # deep clone is IMPORTANT
        for group in newFlow['groups']:  # loop groups
            for block in group['blocks']:  # loop blocks

                if block['DataType'] in ["CandidateAvailableFrom", "CandidateAvailableTo"]:
                    pass

                if block['Type'] == enums.BlockType.Question.value:
                    pass
                    # for answer in block['Content']['answers']:

                if block['Type'] == enums.BlockType.UserInput.value:
                    pass
                    # block['Content']['keywords']= []

                if block['Type'] == enums.BlockType.Solutions.value:
                    pass

                if block['Type'] == enums.BlockType.FileUpload.value:
                    pass

                # validate block content based on block type
                validate(block.get('Content'), getattr(json_schemas, str(enums.BlockType(block.get('Type')).name)))

        # validate whole flow then update
        validate(newFlow, json_schemas.flow)

        return newFlow

    except Exception as exc:
        print(exc.args)
        print("Flow migration failed :(")
        return None
