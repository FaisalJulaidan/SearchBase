import sqlalchemy.exc

from services import company_services, admin_services, user_services
from models import Callback, User, Company, db
from flask import Blueprint, request, redirect, session


def getUserAndCompany(email):
    try:
        user_callback: Callback = user_services.getByEmail(email.lower())
        if not user_callback.Success:
            print("Profile GET Request: Email not found")
            return Callback(False, "Profile GET Request: Email not found")

        company_callback: Callback = company_services.getByCompanyID(user_callback.Data.CompanyID)
        if not company_callback.Success:
            print("Profile GET Request: Company not found")
            return Callback(False, "Profile GET Request: Company not found")

        user = admin_services.convertForJinja(user_callback.Data, User)
        company = admin_services.convertForJinja(company_callback.Data, Company)
        if not user.Success or not company.Success:
            print("Profile GET Request: Could not convert User or Company Data for Jinja")
            return Callback(False, "Profile GET Request: Could not convert User or Company Data for Jinja")

        return Callback(True, "Profile GET Request: Success", {"user": user.Data[0], "company": company.Data[0]})
    except Exception as exc:
        print("profile_services.getUserAndCompany() ERROR: ", )
        db.session.rollback()
        return Callback(False, "Error in loooking for user and company")

    # finally:
    # db.session.close()


def updateUser(firstname, secondname, newEmail, userID):
    try:
        user_callback: Callback = user_services.getByID(userID)
        if not user_callback: return Callback(False, "Could not find user")

        user_callback.Data.Firstname = firstname
        user_callback.Data.Surname = secondname
        user_callback.Data.Email = newEmail

        db.session.commit()

        return Callback(True, "User has been updated")
    except Exception as exc:
        print("profile_services.updateUser() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "User could not be updated")

    # finally:
    # db.session.close()


def updateCompany(companyName, companyID):
    try:
        company_callback: Callback = company_services.getByCompanyID(companyID)
        if not company_callback: return Callback(False, "Could not find company")

        company_callback.Data.Name = companyName

        db.session.commit()

        return Callback(True, "Company has been updated")
    except Exception as exc:
        print("profile_services.updateCompany() ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Company cold not be updated")

    # finally:
    # db.session.close()
