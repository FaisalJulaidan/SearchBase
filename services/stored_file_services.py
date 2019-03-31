from models import db, Callback, StoredFile, ChatbotSession
import logging

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


def getBySession(session: ChatbotSession) -> StoredFile or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(StoredFile).filter(StoredFile.ChatbotSession == session).first()
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
        if not result: raise Exception
        return Callback(True, 'StoredFiles were successfully retrieved', result)
    
    except Exception as exc:
        print("stored_file_services.getAll() ERROR: ", exc)
        logging.error("stored_file_services.getAll(): " + str(exc))
        db.session.rollback()
        return Callback(False,'StoredFiles could not be retrieved/empty')


def create(filePath, chatbotSession) -> StoredFile or None:

    try:
        newStoredFile = StoredFile(FilePath=filePath, ChatbotSession=chatbotSession)
        db.session.add(newStoredFile)

        db.session.commit()
        return Callback(True, "StoredFile uas been created successfully.", newStoredFile)

    except Exception as exc:
        print("stored_file_services.create() ERROR: ", exc)
        logging.error("stored_file_services.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't create a storedFile entity.")
    

def updateStoredFile(id, filePath, chatbotSession):
    try:
        callback: Callback = getByID(id)
        if not callback.Success: return callback
        callback.Data.FilePath = filePath
        if chatbotSession:
            callback.Data.ChatbotSession = chatbotSession
        db.session.commit()

        return Callback(True, "StoredFile has been updated")
    except Exception as exc:
        print("stored_file_services.updateStoredFile() ERROR: ", exc)
        logging.error("stored_file_services.updateStoredFile(): " + str(exc))
        db.session.rollback()
        return Callback(False, "StoredFile cold not be updated")
    

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