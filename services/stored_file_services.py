from models import db, Callback, StoredFile, Conversation
import logging, boto3, botocore, os

PUBLIC_URL = "https://tsb.ams3.digitaloceanspaces.com/"
UPLOAD_FOLDER = os.environ['FLASK_ENV']
COMPANY_LOGOS_PATH = '/company_logos'
USER_FILES_PATH = '/user_files'

def getByID(id) -> StoredFile or None:
    try:
        if id:
            # Get result and check if None then raise exception
            result = db.session.query(StoredFile).get(id)
            if not result: raise Exception

            return Callback(True,
                            'StoredFile with ID ' + str(id) + ' was successfully retrieved',
                            result)
        else:
            raise Exception
    except Exception as exc:
        db.session.rollback()
        logging.error("stored_file_services.getByID(): " + str(exc))
        return Callback(False,
                        'Stored file with ID ' + str(id) + ' does not exist')


def getByConversation(conversation: Conversation) -> StoredFile or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(StoredFile).filter(StoredFile.Conversation == conversation).first()
        if not result: return Callback(False, '')
        return Callback(True, 'StoredFile was successfully retrieved', result)

    except Exception as exc:
        print("stored_file_services.getBySession() ERROR: ", exc)
        logging.error("stored_file_services.getBySession(): " + str(exc))
        return Callback(False,'StoredFile with ID ' + str(id) + ' does not exist')


def getAll():
    try:
        # Get result and check if None then raise exception
        result = db.session.query(StoredFile).all()
        return Callback(True, 'StoredFiles were successfully retrieved', result)
    
    except Exception as exc:
        print("stored_file_services.getAll() ERROR: ", exc)
        logging.error("stored_file_services.getAll(): " + str(exc))
        db.session.rollback()
        return Callback(False,'StoredFiles could not be retrieved/empty')


def createRef(filePath, conversation) -> StoredFile or None:

    try:
        if not filePath: raise Exception;
        newStoredFile = StoredFile(FilePath=filePath, Conversation=conversation)
        db.session.add(newStoredFile)
        db.session.commit()
        return Callback(True, "Stored files reference was created successfully.", newStoredFile)

    except Exception as exc:
        print("stored_file_services.create() ERROR: ", exc)
        logging.error("stored_file_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't create a storedFile entity.")
    

def removeByID(id):
    try:
        db.session.query(StoredFile).filter(StoredFile.ID == id).first().delete()
        db.session.commit()
        
        return Callback(True, "StoredFile has been deleted")
    except Exception as exc:
        print("stored_file_services.removeByID() ERROR: ", exc)
        logging.error("stored_file_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, "StoredFile cold not be deleted")


def uploadFile(file, filename, path, public=False):

    try:
        # Set config arguments
        ExtraArgs = {}
        if public: ExtraArgs['ACL'] = 'public-read'

        # Connect to DigitalOcean Space
        session = boto3.session.Session()
        s3 = session.client('s3',
                            region_name='ams3',
                            endpoint_url= os.environ['SERVER_SPACES'],
                            aws_access_key_id= os.environ['PUBLIC_KEY_SPACES'],
                            aws_secret_access_key= os.environ['SECRET_KEY_SPACES'])

        # Upload file
        s3.upload_fileobj(file, 'tsb', UPLOAD_FOLDER + path + '/' + filename,
                          ExtraArgs=ExtraArgs)
        return Callback(True, "File uploaded successfully")

    except Exception as exc:
        print("stored_file_services.uploadFile() ERROR: ", exc)
        logging.error("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "Couldn't upload file")


def downloadFile(filename, path):
    try:
        # Connect to DigitalOcean Space
        session = boto3.session.Session()
        s3 = session.resource('s3',
                                region_name='ams3',
                                endpoint_url= os.environ['SERVER_SPACES'],
                                aws_access_key_id= os.environ['PUBLIC_KEY_SPACES'],
                                aws_secret_access_key= os.environ['SECRET_KEY_SPACES'])
        file = s3.Object('tsb', UPLOAD_FOLDER + path + '/' + filename)

        # Check if file exists
        try:
            file.load()
        except botocore.exceptions.ClientError as e:
            return Callback(False, "File not found")


        return Callback(True, "File downloaded successfully", file)


    except Exception as exc:
        print("stored_file_services.downloadFile() ERROR: ", exc)
        logging.error("stored_file_services.uploadFile(): " + str(exc))
        return Callback(False, "Couldn't upload file")


def deleteFile(filename, path):

    try:
        # Connect to DigitalOcean Space
        session = boto3.session.Session()
        s3 = session.resource('s3',
                            region_name='ams3',
                            endpoint_url='https://ams3.digitaloceanspaces.com',
                            aws_access_key_id= os.environ['PUBLIC_KEY_SPACES'],
                            aws_secret_access_key= os.environ['SECRET_KEY_SPACES'])
        # Delete file
        s3.Object('tsb', UPLOAD_FOLDER + path + '/' + filename).delete()

        return Callback(True, "File deleted successfully")

    except Exception as exc:
        print("stored_file_services.deleteFile() ERROR: ", exc)
        logging.error("stored_file_services.deleteFile(): " + str(exc) + " >>> File Name: " + path + '/' + filename)
        return Callback(False, "Couldn't delete file")