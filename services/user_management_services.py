import random
import string

from models import Callback, db, User
from services import user_services, role_services, mail_services
import logging


def addAdditionalUser(name, email, role, adminUser):
    try:
        # removed empty spaces around the strings and split the full name into first name and surname
        names = name.strip().split(" ")
        email = email.strip()
        firstname = names[0]
        surname = names[-1]

        # Check if email is already used
        test_callback: Callback = user_services.getByEmail(email)
        if test_callback.Success:
            return Callback(False, 'Email is already on use.')

        # Get the role to be assigned for the user
        role_callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.CompanyID)
        if not role_callback.Success:
            return Callback(False, role_callback.Message)

        # create random generated password
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))

        # Create the new user for the company
        create_callback: Callback = user_services.create(firstname, surname, email, password, "00000000000", adminUser.Company,
                                           role_callback.Data, verified=True)
        if not create_callback.Success:
            return Callback(False, create_callback.Message)

        email_callback: Callback = mail_services.addedNewUserEmail(adminUser.Email, email, password)
        if not email_callback.Success:
            remove_callback: Callback = user_services.removeByID(create_callback.Data.ID)
            if not remove_callback.Success:
                raise Exception(remove_callback.Message)
            return Callback(False, "Failed to send email with password to user. Addition has been aborted")

        return Callback(True, 'User has been created successfully!')

    except Exception as exc:
        print("user_services.addAdditionalUser ERROR: " + str(exc))
        logging.error("user_services.addAdditionalUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')


def updateAsOwner(userID, firstname, surname, email, role) -> Callback:
    try:
        user_callback: Callback = user_services.getByID(userID)
        if not user_callback.Success:
            return Callback(False, "Could not find user's records")
        user: User = user_callback.Data

        # Get the role to be assigned for the userToUpdate
        role_callback: Callback = role_services.getByNameAndCompanyID(role.strip(), user.CompanyID)
        if not role_callback.Success:
            return Callback(False, role_callback.Message)

        # Update user
        user.Firstname = firstname.strip()
        user.Surname = surname.strip()
        user.Email = email.strip().lower()
        user.Role = role_callback.Data

        db.session.commit()
        return Callback(True, 'User has been edited successfully!')

    except Exception as exc:
        print(exc)
        logging.error("user_services.updateAsOwner(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')