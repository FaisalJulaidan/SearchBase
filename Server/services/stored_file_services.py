import os

import boto3
from botocore.exceptions import ClientError
from sqlalchemy.orm import joinedload

from typing import List
from models import db, Callback, StoredFile, Conversation, StoredFileInfo
from utilities import helpers, enums

PUBLIC_URL = "https://tsb.ams3.digitaloceanspaces.com/"
UPLOAD_FOLDER = os.environ['FLASK_ENV']
COMPANY_LOGOS_PATH = '/company_logos'
USER_FILES_PATH = '/user_files'
BUCKET = 'tsb'


# NEEDS TO BE CONVERTED
def getByID(id) -> StoredFile or None:
    try:
        if id:
            # Get result and check if None then raise exception
            result: StoredFile = db.session.query(StoredFile).options(joinedload("StoredFileInfo")).get(id)
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


def createRef(file, model, identifier, value, storedFileID, key: enums.FileAssetType = None, realFileName: str = None) -> StoredFile or None:
    try:
        if not file: raise Exception;
        obj = db.session.query(model).filter(getattr(model, identifier) == value).first()
        if obj is None:
            return Callback(False, 'Model not found')
        elif not hasattr(obj, 'StoredFileID'):
            return Callback(False,'Provided model does not have StoredFileID Attribute')


        key = key if key else enums.FileAssetType.NoType
        filename = realFileName or file.filename
        file : StoredFileInfo = StoredFileInfo(StoredFileID=storedFileID, Key=key, FilePath=filename)
        obj.StoredFileID = storedFileID

        db.session.add(file)
        db.session.commit()

        return Callback(True, "Stored files reference was created successfully.",
                        helpers.getDictFromSQLAlchemyObj(file))

    except Exception as exc:
        helpers.logError("stored_file_services.createRef(): " + str(exc))
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


def uploadFile(file, filename, public=False, **kwargs):
    try:
        if 'model' in kwargs:
            #files, model, identifier, value, storedFileID, keys: List = None
            dbRef_callback: Callback = createRef(file, kwargs['model'], kwargs['identifier'], kwargs['identifier_value'], kwargs['stored_file_id'] , kwargs['key'], realFileName=filename)

            if not dbRef_callback.Success:
                raise Exception(dbRef_callback.Message)

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
            s3.upload_fileobj(file, BUCKET, UPLOAD_FOLDER + '/' + filename,
                              ExtraArgs=ExtraArgs)

        except ClientError as e:
            raise Exception("DigitalOcean Error")


        return Callback(True, "File uploaded successfully",  PUBLIC_URL + UPLOAD_FOLDER + '/' + filename)

    except Exception as exc:
        helpers.logError("stored_file_services.uploadFile() FileName: " + filename + "\n" + str(exc))
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
        file = s3.Object(BUCKET, UPLOAD_FOLDER + "/" + filename)

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
                                                'Key': UPLOAD_FOLDER + '/' + filename
                                            })
        except ClientError as e:
            raise Exception("---> DigitalOcean Error" + str(e))

        return Callback(True, "File downloaded successfully", url)

    except Exception as exc:
        helpers.logError("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "File is corrupted", None)


def deleteFile(filename, storedFile: StoredFile):
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
            s3.Object(BUCKET, UPLOAD_FOLDER + '/' + filename).delete()
        except ClientError as e:
            raise Exception("DigitalOcean Error")

        db.session.delete(storedFile)
        db.session.commit()

        return Callback(True, "File deleted successfully")

    except Exception as exc:
        helpers.logError("stored_file_services.deleteFile(): " + str(exc) + " >>> File Name:" + filename)
        return Callback(False, "Couldn't delete file")
