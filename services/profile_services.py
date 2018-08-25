import sqlalchemy.exc

from services import company_services, admin_services, user_services
from models import Callback, User, Company
from flask import Blueprint, request, redirect, session

def getUserAndCompany(email):
    user_callback: Callback = user_services.getByEmail(email.lower())
    if not user_callback.Success:
        print("Profile GET Request: Email not found")
        return Callback(False, "Profile GET Request: Email not found")

    company_callback : Callback = company_services.getByCompanyID(session.get('companyID', None))
    if not company_callback.Success:
        print("Profile GET Request: Company not found")
        return Callback(False, "Profile GET Request: Company not found")

    user = admin_services.convertForJinja(user_callback.Data, User)
    company = admin_services.convertForJinja(company_callback.Data, Company)
    if not user.Success or not company.Success:
        print("Profile GET Request: Could not convert User or Company Data for Jinja")
        return Callback(False, "Profile GET Request: Could not convert User or Company Data for Jinja")

    return Callback(True, "Profile GET Request: Success", {"user" : user.Data[0], "company" : company.Data[0]})

def updateUser(firstname, secondname, newEmail, userID):

