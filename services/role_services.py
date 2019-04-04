from models import Callback, db, Role, Company
from sqlalchemy import and_
import logging


def create(name, editChatbots: bool, editUsers: bool, deleteUsers: bool, accessBilling: bool, company: Company) -> Callback:
    try:
        newRole = Role(Name=name, EditChatbots=editChatbots, EditUsers=editUsers,
                    DeleteUsers=deleteUsers, AccessBilling=accessBilling, Company=company)
        db.session.add(newRole)

        db.session.commit()
        return Callback(True, 'Role has been created successfully!', newRole)

    except Exception as exc:
        print(exc)
        logging.error("role_service.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the role.', )


def getByNameAndCompanyID(name: str, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(and_(Role.CompanyID == companyID, Role.Name == name)).first()
        if not result: raise Exception

        return Callback(True,
                        'Role was successfully retrieved.',
                        result)
    except Exception as exc:
        db.session.rollback()
        logging.error("role_service.getByNameAndCompanyID(): " + str(exc))
        return Callback(False,
                        'Role could not be retrieved.')


def getAllByCompanyID(companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(Role.CompanyID == companyID).all()
        if not result: raise Exception

        return Callback(True,
                        'Roles with company ID ' + str(companyID) + ' were successfully retrieved.',
                        result)
    except Exception as exc:
        logging.error("role_service.getAllByCompanyID(): " + str(exc))
        db.session.rollback()
        return Callback(False,
                        'Roles with company ID ' + str(companyID) + ' could not be retrieved.')


def removeAllByCompany(company: Company) -> Callback:
    try:
     db.session.query(Role).filter(Role.Company == company).delete()
     db.session.commit()
     return Callback(True, 'Role has been removed successfully.')

    except Exception as exc:
        print(exc)
        logging.error("role_service.removeAllByCompany(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role could not be removed.')


def getByID(id) -> Role or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).get(id)
        if not result: raise Exception
        return Callback(True, 'Role does exist.', result)
    except Exception as exc:
        logging.error("role_service.getByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role with id ' + str(id) + ' does not exist')



def getByName(name) -> Role or None:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Role).filter(Role.Name == name).first()
        if not result: raise Exception
        return Callback(True, 'Role does exist.', result)
    except Exception as exc:
        logging.error("role_service.getByName(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Role ' + str(name) + ' does not exist')
