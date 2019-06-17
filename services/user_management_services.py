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
            raise Exception('You are not authorised to edit users')


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

    except Exception as exc:
        helpers.logError("user_management_services.editUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Couldn't update user.")


def addUser(firstname, surname, email, givenRoleID, editorUserID, editorCompanyID):
    try:

        if givenRoleID in [0,1]: # 0 = Staff, 1 = Owners
            raise Exception('Someone is trying to hack the system')

        # Check if editorUser is authorised to do such an operation (returns boolean)
        if not role_services.isAuthorised('addUsers', editorUserID):
            raise Exception('You are not authorised to add users')

        # Get and check if new role belongs to this company
        role_callback: Callback = role_services.getByIDAndCompanyID(givenRoleID, editorCompanyID)
        if not role_callback.Success:
            raise Exception('Role does not exist')
        givenRole: Role = role_callback.Data

        # Check if email of new user already exist
        callback: Callback = user_services.getByEmail(email)
        if callback.Success:
            return Callback(False, 'Email is already on use, maybe under your or another company')

        # Get company
        callback: Callback = company_services.getByID(editorCompanyID)
        if callback.Success:
            return Callback(False, 'Email is already on use, maybe under your or another company')
        company: Company = callback.Data

        # create random generated password
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))

        # Create the new user for the company
        db.session.add(User(Firstname=firstname,
                            Surname=surname,
                            Email='aa@aa.com',
                            Password=password,
                            PhoneNumber='',
                            CompanyID=editorCompanyID,
                            Role=givenRole.ID,
                            Verified=False))

        # Send email invitation to verify his account
        email_callback: Callback = \
            mail_services.send_email(email,
                                    'Account Invitation',
                                    '/emails/account_invitation.html',
                                    companyName=company.Name,
                                    logoPath=company.LogoPath,
                                    userName= firstname + ' ' + surname,
                                    password=password,
                                    accountVerifcationLink= helpers.getDomain() + "/verify_account/" + \
                                                            helpers.verificationSigner.dumps(email + ";" + str(company.ID),
                                                                                             salt='email-confirm-key')
                                    )

        if not email_callback.Success:
            return Callback(False, 'Could not send new user an invitation email; therefore, all operations are discarded')

        # Save changes
        db.session.commit()
        return Callback(True, 'User has been created successfully!')

    except Exception as exc:
        helpers.logError("user_services.addUser(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Sorry, Could not add the user.')



