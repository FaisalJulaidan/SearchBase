from models import Callback, db, User, Role, Company
from services import user_services, role_services, mail_services, company_services
from utilities import helpers
import random, string


def editUser(userID, firstname, surname, phoneNumber, newRoleID, editorUserID, editorCompanyID):
    try:

        if newRoleID in [0,1]: # 0 = Staff, 1 = Owners
            raise Exception('Someone is trying to hack the system')

        # Check if editorUser is authorised to do such an operation (returns boolean)
        if not role_services.isAuthorised('editUsers', editorUserID):
            return Callback(False, 'You are not authorised to edit users')


        # Get and check if new role belongs to this company
        role_callback: Callback = role_services.getByIDAndCompanyID(newRoleID, editorCompanyID)
        if not role_callback.Success:
            raise Exception('Role does not exist')
        newRole: Role = role_callback.Data

        # Get user to be edited
        callback: Callback = user_services.getByIDAndCompanyID(userID, editorCompanyID)
        if not callback.Success:
            return Callback(False, "You are not authorised to edit this user")
        user: User = callback.Data

        user.Firstname = firstname
        user.Surname = surname
        user.PhoneNumber = phoneNumber
        user.Role = newRole

        db.session.commit()

        return Callback(True, 'User updated successfully', user)

    except Exception as exc:
        helpers.logError("user_management_services.editUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't update user.")


def deleteUser(userID, editorUserID, editorCompanyID):
    try:

        if userID == editorUserID:
            return Callback(False, "You cannot delete yourself")

        # Check if editorUser is authorised to do such an operation (returns boolean)
        if not role_services.isAuthorised('deleteUsers', editorUserID):
            return Callback(False, 'You are not authorised to delete users')

        # Get user to be edited
        callback: Callback = user_services.getByIDAndCompanyID(userID, editorCompanyID)
        if not callback.Success:
            return Callback(False, "You are not authorised to edit this user")
        user: User = callback.Data

        # Delete user and save changes
        db.session.delete(user)
        db.session.commit()

        return Callback(True, 'User deleted successfully')

    except Exception as exc:
        helpers.logError("user_management_services.deleteUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't delete user.")


def addUser(firstname, surname, email, phoneNumber,  givenRoleID, editorUserID, editorCompanyID):
    try:

        if givenRoleID in [0,1]: # 0 = Staff, 1 = Owners
            raise Exception('Someone is trying to hack the system')

        # Check if editorUser is authorised to do such an operation (returns boolean)
        if not role_services.isAuthorised('addUsers', editorUserID):
            return Callback(False, 'You are not authorised to add users')

        # Get and check if new role belongs to this company
        role_callback: Callback = role_services.getByIDAndCompanyID(givenRoleID, editorCompanyID)
        if not role_callback.Success:
            raise Exception('Role does not exist')
        givenRole: Role = role_callback.Data

        # Check if email of new user already exist
        callback: Callback = user_services.getByEmail(email)
        if callback.Success:
            return Callback(False, 'Email is already on use maybe under your or another company')

        # Get company
        callback: Callback = company_services.getByID(editorCompanyID, True)
        if not callback.Success:
            return Callback(False, 'Your company does not exist')
        company: Company = callback.Data

        # create random generated password
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))

        # Create the new user for the company
        newUser = User(Firstname=firstname,
                    Surname=surname,
                    Email=email,
                    Password=password,
                    PhoneNumber=phoneNumber,
                    CompanyID=editorCompanyID,
                    Role=givenRole,
                    Verified=False)
        db.session.add(newUser)

        # Send account invitation email to new user
        email_callback: Callback = mail_services.sendAccountInvitation(firstname, surname, email, password,
                                                                       company.Name, company.LogoPath, company.ID)


        if not email_callback.Success:
            return Callback(False, 'Could not send new user an invitation email. All operations are discarded')

        # Save changes
        db.session.commit()
        return Callback(True, 'User has been created successfully', newUser)

    except Exception as exc:
        helpers.logError("user_management_services.addUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could not add the user.')



