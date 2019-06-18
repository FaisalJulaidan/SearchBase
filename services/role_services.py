from models import Callback, db, Role, Company, User
from sqlalchemy import and_
from utilities import helpers
from services import user_services



def isAuthorised(operation, userID) -> bool:
    try:

        # Get editor user to check his permissions
        security_callback: Callback = user_services.getByID(userID)
        if not security_callback.Success:
            raise Exception('user cannot be found')
        editorUser: User = security_callback.Data

        # Check editor user permission
        if operation == 'editUsers':
            if not editorUser.Role.EditUsers:
                raise Exception("You are not authorised to edit users")

        if operation == 'deleteUsers':
            if not editorUser.Role.DeleteUsers:
                raise Exception("You are not authorised to edit users")

        if operation == 'editChatbot':
            if not editorUser.Role.EditChatbots:
                raise Exception("You are not authorised to edit chatbot script")

        if operation == 'accessBilling':
            if not editorUser.Role.AccessBilling:
                raise Exception("You are not authorised to access billing")

        # reaching to thing point means user is authorised to do such an operation
        return True

    except Exception as exc:
        helpers.logError("user_management_services.__isAuthorised(): ####### " + str(exc) + " ####### ")
        db.session.rollback()
        return False


def create(name, editChatbots: bool, addUsers: bool, editUsers: bool, deleteUsers: bool, accessBilling: bool, companyID: int) -> Callback:
    try:
        newRole = Role(Name=name, EditChatbots=editChatbots, AddUsers=addUsers, EditUsers=editUsers,
                    DeleteUsers=deleteUsers, AccessBilling=accessBilling, CompanyID=companyID)
        db.session.add(newRole)

        db.session.commit()
        return Callback(True, 'Role has been created successfully!', newRole)

    except Exception as exc:
        helpers.logError("role_service.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the role.')


def getByIDAndCompanyID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(and_(Role.CompanyID == companyID, Role.ID == id)).first()
        if not result: raise Exception

        return Callback(True,'Role was successfully retrieved.', result)

    except Exception as exc:
        helpers.logError("role_service.getByIDAndCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role could not be retrieved.')


def getByNameAndCompanyID(name: str, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(and_(Role.CompanyID == companyID, Role.Name == name)).first()
        if not result: raise Exception

        return Callback(True,
                        'Role was successfully retrieved.',
                        result)
    except Exception as exc:
        helpers.logError("role_service.getByNameAndCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role could not be retrieved.')


def getAllByCompanyID(companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(Role.CompanyID == companyID).all()

        return Callback(True, 'Roles retrieved successfully.',result)
    except Exception as exc:
        helpers.logError("role_service.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Roles cannot be retrieved.')


def removeAllByCompany(company: Company) -> Callback:
    try:
     db.session.query(Role).filter(Role.Company == company).delete()
     db.session.commit()
     return Callback(True, 'Role has been removed successfully.')

    except Exception as exc:
        helpers.logError("role_service.removeAllByCompany(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role could not be removed.')


def getByID(id) -> Role or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).get(id)
        if not result: raise Exception
        return Callback(True, 'Role does exist.', result)

    except Exception as exc:
        helpers.logError("role_service.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role does not exist')



def getByName(name) -> Role or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(Role.Name == name).first()
        if not result: raise Exception
        return Callback(True, 'Role does exist.', result)

    except Exception as exc:
        helpers.logError("role_service.getByName(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role does not exist')
