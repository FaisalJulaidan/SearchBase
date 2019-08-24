import os

import boto3
from botocore.exceptions import ClientError
from sqlalchemy.orm import joinedload

from typing import List
from models import db, Callback, StoredFile, Conversation, StoredFileInfo
from utilities import helpers

PUBLIC_URL = "https://tsb.ams3.digitaloceanspaces.com/"
UPLOAD_FOLDER = os.environ['FLASK_ENV']
COMPANY_LOGOS_PATH = '/company_logos'
USER_FILES_PATH = '/user_files'
BUCKET= 'tsb'


# NEEDS TO BE CONVERTED
def getByID(id) -> StoredFile or None:
    try:
        if id:
            # Get result and check if None then raise exception
            result : StoredFile = db.session.query(StoredFile).options(joinedload("StoredFileInfo")).get(id)
            if not result: raise Exception

            return Callback(True,
                            'StoredFile with ID ' + str(id) + ' was successfully retrieved',
                            result)
        else:
            raise Exception
    except Exception as exc:
        db.session.rollback()
        helpers.logError("stored_file_services.getByID(): " + str(exc))
        return Callback(False,
                        'Stored file with ID ' + str(id) + ' does not exist')


def getByConversation(conversation: Conversation) -> StoredFile or None:
    try:
        result = db.session.query(StoredFile).filter(conversation.StoredFileID == StoredFile.ID).first()
        if not result: return Callback(False, '')
        return Callback(True, 'StoredFile was successfully retrieved', result)

    except Exception as exc:
        helpers.logError("stored_file_services.getBySession(): " + str(exc))
        return Callback(False, 'StoredFile with ID ' + str(id) + ' does not exist')


def getAll():
    try:
        # Get result and check if None then raise exception
        result = db.session.query(StoredFile).all()
        return Callback(True, 'StoredFiles were successfully retrieved', result)

    except Exception as exc:
        helpers.logError("stored_file_services.getAll(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'StoredFiles could not be retrieved/empty')


def createRef(files, conversation, storedFileID, keys: List=None) -> StoredFile or None:
    try:
        if not files: raise Exception;
        conversation : Conversation = db.session.query(Conversation).filter(Conversation.ID == conversation.ID).first()
        newFiles = []
        for idx, file in enumerate(files):
            key =  keys[idx] + idx if keys.count(keys[idx]) > 1 else keys[idx] if keys else None
            newFiles.append(StoredFileInfo(StoredFileID=storedFileID, Key=key, FilePath=file.realFileName))

        conversation.StoredFileID = storedFileID
        db.session.add_all(newFiles)
        db.session.commit()
        return Callback(True, "Stored files reference was created successfully.", helpers.getListFromSQLAlchemyList(newFiles))

    except Exception as exc:
        helpers.logError("stored_file_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't create a storedFile entity.")


def removeByID(id):
    try:
        db.session.query(StoredFile).filter(StoredFile.ID == id).first().delete()
        db.session.commit()

        return Callback(True, "StoredFile has been deleted")
    except Exception as exc:
        helpers.logError("stored_file_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, "StoredFile cold not be deleted")


def uploadFile(file, filename, public=False):
    try:
        # Set config arguments
        ExtraArgs = {}
        if public: ExtraArgs['ACL'] = 'public-read'

        try:
            # Connect to DigitalOcean Space
            session = boto3.session.Session()
            s3 = session.client('s3',
                                region_name='ams3',
                                endpoint_url=os.environ['SPACES_SERVER_URI'],
                                aws_access_key_id=os.environ['SPACES_PUBLIC_KEY'],
                                aws_secret_access_key=os.environ['SPACES_SECRET_KEY'])

            # Upload file
            print(filename)
            s3.upload_fileobj(file, BUCKET, filename,
                              ExtraArgs=ExtraArgs)

        except ClientError as e:
            raise Exception("DigitalOcean Error")



        return Callback(True, "File uploaded successfully")

    except Exception as exc:
        helpers.logError("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "Couldn't upload file")



def downloadFile(filename):
    try:
        # Connect to DigitalOcean Space
        session = boto3.session.Session()
        s3 = session.resource('s3',
                              region_name='ams3',
                              endpoint_url=os.environ['SPACES_SERVER_URI'],
                              aws_access_key_id=os.environ['SPACES_PUBLIC_KEY'],
                              aws_secret_access_key=os.environ['SPACES_SECRET_KEY'])
        file = s3.Object(BUCKET, filename)

        # Check if file exists
        try:
            file.load()
        except ClientError as e:
            return Callback(False, "File not found")

        return Callback(True, "File downloaded successfully", file)

    except Exception as exc:
        helpers.logError("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "Couldn't upload file")


def genPresigendURL(filename, expireIn=None):
    try:
        # Connect to DigitalOcean Space
        print(filename)
        session = boto3.session.Session()
        s3 = session.client('s3',
                            region_name='ams3',
                            endpoint_url=os.environ['SPACES_SERVER_URI'],
                            aws_access_key_id=os.environ['SPACES_PUBLIC_KEY'],
                            aws_secret_access_key=os.environ['SPACES_SECRET_KEY'])

        try:
            url = s3.generate_presigned_url('get_object',
                                                 Params={
                                                    'Bucket': BUCKET,
                                                    'Key': filename
                                                 })
        except ClientError as e:
            print('error')
            raise Exception("---> DigitalOcean Error" + str(e))

        return Callback(True, "File downloaded successfully", url)

    except Exception as exc:
        helpers.logError("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "File is corrupted", None)

def genURL(path):
    logo = PUBLIC_URL + UPLOAD_FOLDER + COMPANY_LOGOS_PATH + "/" + (
        path or "")
    return logo if path else None

def deleteFile(filename):
    try:
        # Connect to DigitalOcean Space
        try:
            session = boto3.session.Session()
            s3 = session.resource('s3',
                                  region_name='ams3',
                                  endpoint_url=os.environ['SPACES_SERVER_URI'],
                                  aws_access_key_id=os.environ['SPACES_PUBLIC_KEY'],
                                  aws_secret_access_key=os.environ['SPACES_SECRET_KEY'])
            # Delete file
            s3.Object(BUCKET, filename).delete()
        except ClientError as e:
            raise Exception("DigitalOcean Error")

        return Callback(True, "File deleted successfully")

    except Exception as exc:
        helpers.logError("stored_file_services.deleteFile(): " + str(exc) + " >>> File Name:" + filename)
        return Callback(False, "Couldn't delete file")

def getUnusedFiles():
    try:
        files: List[StoredFileInfo] = db.session.query(StoredFileInfo).filter(StoredFileInfo.StoredFileID == None).all()

        if len(files) == 0 or files is None:
            return Callback(False, "No files to delete", None)
        return Callback(True, "Files found to delete", files)
    except Exception as exc:
        helpers.logError("stored_file_services.getUnusedFiles(): " + str(exc))
        return Callback(False, "Couldn't find files to delete")

