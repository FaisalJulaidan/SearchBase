from models import Callback, db, User
from services import user_services, role_services, mail_services
from utilities import helpers
import random, string, logging


def add_user_with_permission(name, email, role, admin_id):
    try:
        # Get the admin user who is logged in and wants to create a new user.
        user_callback: Callback = user_services.getByID(admin_id)
        if not user_callback.Success:
            return Callback(False, user_callback.Message)

        # check if the user can edit users, the email is valid and the role of the new user is valid
        if not user_callback.Data.Role.EditUsers \
                or (role != "Admin" and role != "User") \
                or not helpers.isValidEmail(email):
            return Callback(False, "Please make sure you entered all data correctly and have the necessary permission" +
                                   " to do this action")

        admin_user = user_callback.Data

        # removed empty spaces around the strings and split the full name into first name and surname
        names = name.strip().split(" ")
        email = email.strip()
        first_name = names[0]
        surname = names[-1]

        # Check if email is already used
        test_callback: Callback = user_services.getByEmail(email)
        if test_callback.Success:
            return Callback(False, 'Email is already on use.')

        # Get the role to be assigned for the user
        role_callback: Callback = role_services.getByNameAndCompanyID(role, admin_user.CompanyID)
        if not role_callback.Success:
            return Callback(False, role_callback.Message)

        # create random generated password
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))

        # Create the new user for the company
        create_callback: Callback = user_services.create(first_name, surname, email, password, "00000000000", 
                                                         admin_user.Company, role_callback.Data, verified=True)
        if not create_callback.Success:
            return Callback(False, create_callback.Message)

        email_callback: Callback = mail_services.addedNewUserEmail(admin_user.Email, email, password)
        if not email_callback.Success:
            remove_callback: Callback = user_services.removeByID(create_callback.Data.ID)
            if not remove_callback.Success:
                raise Exception(remove_callback.Message)
            return Callback(False, "Failed to send email with password to user. Addition has been aborted")

        return Callback(True, 'User has been created successfully!')

    except Exception as exc:
        helpers.logError("user_services.add_user_with_permission(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not create the user.')


def update_user_with_permission(user_id, first_name, surname, email, role, admin_id) -> Callback:
    try:
        # Get the admin user who is logged in and wants to edit.
        user_callback: Callback = user_services.getByID(admin_id)
        if not user_callback.Success:
            return Callback(False, user_callback.Message)

        # check if the email is valid and if the user has permission to edit users and if his new role is valid
        if not helpers.isValidEmail(email) or not user_callback.Data.Role.EditUsers \
                or (role != "Admin" and role != "User"):
            return Callback(False, "Please make sure you entered all data correctly and have the necessary permission" +
                                   " to do this action")

        user_callback: Callback = user_services.getByID(user_id)
        if not user_callback.Success:
            return Callback(False, "Could not find user's records")
        user: User = user_callback.Data

        # Get the role to be assigned for the userToUpdate
        role_callback: Callback = role_services.getByNameAndCompanyID(role, user.CompanyID)
        if not role_callback.Success:
            return Callback(False, role_callback.Message)

        # Update user
        user.Firstname = first_name.strip()
        user.Surname = surname.strip()
        user.Email = email.strip().lower()
        user.Role = role_callback.Data

        db.session.commit()
        return Callback(True, 'User has been edited successfully!')

    except Exception as exc:
        helpers.logError("user_services.update_user_with_permission(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not update the user.')


def delete_user_with_permission(user_id, admin_id):
    try:
        # Get the admin user who is logged in and wants to delete.
        user_callback: Callback = user_services.getByID(admin_id)
        if not user_callback.Success:
            return Callback(False, user_callback.Message)

        # Check if the admin user is authorised for such an operation.
        if not user_callback.Data.Role.DeleteUsers:
            return Callback(False, "You're not authorised to delete users")

        # Delete the user
        remove_callback: Callback = user_services.removeByID(user_id)
        if not remove_callback.Success:
            return Callback(False, remove_callback.Message)

        return Callback(True, 'User has been deleted successfully!')

    except Exception as exc:
        helpers.logError("user_services.delete_user_with_permission(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not delete the user.')
