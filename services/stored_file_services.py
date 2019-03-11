from models import db, Callback, StoredFile


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
        if exc:
            print("stored_file_services.getByID() ERROR: ", exc)
        return Callback(False,
                        'StoredFile with ID ' + str(id) + ' does not exist')


def getBySession(session) -> StoredFile or None:
    try:
        if session:
            # Get result and check if None then raise exception
            result = db.session.query(StoredFile).filter(StoredFile.ChatbotSession == session).first()
            if not result:
                raise Exception

            return Callback(True,
                            'StoredFile with ID ' + str(id) + ' was successfully retrieved',
                            result)
        else:
            raise Exception
    except Exception as exc:
        db.session.rollback()
        if exc:
            print("stored_file_services.getBySession() ERROR: ", exc)
        return Callback(False,
                        'StoredFile with ID ' + str(id) + ' does not exist')


def getAll():
    try:
        # Get result and check if None then raise exception
        result = db.session.query(StoredFile).all()
        if not result:
            raise Exception

        return Callback(True,
                        'StoredFiles were successfully retrieved',
                        result)
    
    except Exception as exc:
        db.session.rollback()
        print("stored_file_services.getAll() ERROR: ", exc)
        return Callback(False,
                        'StoredFiles could not be retrieved/empty')


def create(filePath, chatbotSession) -> StoredFile or None:

    try:
        newStoredFile = StoredFile(FilePath=filePath, ChatbotSession=chatbotSession)
        db.session.add(newStoredFile)

        db.session.commit()
        return Callback(True, "StoredFile uas been created successfully.", newStoredFile)

    except Exception as exc:
        print("stored_file_services.create() ERROR: ", exc)
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
        db.session.rollback()
        return Callback(False, "StoredFile cold not be updated")
    

def removeByID(id):

    try:
        db.session.query(StoredFile).filter(StoredFile.ID == id).first().delete()
        db.session.commit()
        
        return Callback(True, "StoredFile has been deleted")
    except Exception as exc:
        db.session.rollback()
        print("stored_file_services.removeByID() ERROR: ", exc)
        return Callback(False, "StoredFile cold not be deleted")