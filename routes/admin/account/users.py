from flask import jsonify, json
from services import user_services, admin_services, role_services, company_services
from models import Callback, User, Company
from flask import Blueprint, request, redirect, session
from utilties import helpers

users_router: Blueprint = Blueprint('users_router', __name__ ,template_folder="../../templates")


# Get all users for logged in company
@users_router.route("/admin/users", methods=['GET'])
def admin_users():
    if request.method == "GET":
        users_callback: Callback = user_services.getAllByCompanyID(session.get('CompanyID', 0))
        role_callback: Callback =  role_services.getAllByCompanyID(session.get('CompanyID', 0))

        roles = []
        userWithRoles = []
        if users_callback.Success and role_callback.Success:
            users = helpers.getListFromSQLAlchemyList(users_callback.Data)
            roles = helpers.getListFromSQLAlchemyList(role_callback.Data)
            userWithRoles = helpers.mergeRolesToUserLists(users, roles)

        return admin_services.render("admin/users.html", users=userWithRoles, roles=roles)


# Create a new user under the logged in user's company
@users_router.route("/admin/user", methods=['POST'])
def admin_users_add():
    if request.method == "POST":

        # Get the admin user who is logged in and wants to create a new user.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, error occurred. Try again please!"}), \
                   400, {'ContentType': 'application/json'}
        adminUser: User = callback.Data

        # Check if the admin user is authorised to create a new user.
        if not adminUser.Role.EditUsers:
            return json.dumps({'success': False, 'msg': "Sorry, You're not authorised to create a user"}), \
                   401, {'ContentType': 'application/json'}

        # If authorised then complete the process
        # Get submitted user info
        firstname = request.form.get("firstname", default='').strip()
        surname = request.form.get("surname", default='').strip()
        email = request.form.get("email", default='').strip()
        role = request.form.get("role", default='').strip()

        # Check if info valid
        if not helpers.isStringsLengthGreaterThanZero(firstname, surname, email, role):
            return json.dumps({'success': False, 'msg': "Please provide all required info for the new user."}), \
                   400, {'ContentType': 'application/json'}

        # Validate the given email
        if not helpers.isValidEmail(email):
            return json.dumps({'success': False, 'msg': "Please provide a valid email."}), \
                   400, {'ContentType': 'application/json'}

        # Check if email is already used
        user: User = user_services.getByEmail(email).Data
        if user:
            return json.dumps({'success': False, 'msg': 'Email is already on use.'}), \
                   400, {'ContentType': 'application/json'}

        # Get the role to be assigned for the user
        callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.Company.ID)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': role + " role does not exist."}), \
                   400, {'ContentType': 'application/json'}
        role = callback.Data

        # Create the new user for the company
        callback: Callback = user_services.create(firstname, surname, email, 'passwordToBeChanged',
                                                  adminUser.Company, role, verified=True)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': " Sorry couldn't create the user. Try again!"}), \
                   400, {'ContentType': 'application/json'}

        print('new user > success!')
        return json.dumps({'success': True, 'msg': " User has been created successfully!"}), \
                   200, {'ContentType': 'application/json'}


# Update user with id <userID>
@users_router.route("/admin/user/<userID>", methods=['PUT'])
def update_user(userID):
    if request.method == "PUT":

        # User info
        firstname = request.form.get("firstname", default='').strip()
        surname = request.form.get("surname", default='').strip()
        email = request.form.get("email", default='').strip()
        role = request.form.get("role", default='').strip()

        if not helpers.isStringsLengthGreaterThanZero(firstname, surname, email, role):
            return json.dumps({'success': False, 'msg': "Please provide all required info for the new user."}), \
                   400, {'ContentType': 'application/json'}

        # Validate the given email
        if not helpers.isValidEmail(email):
            return json.dumps({'success': False, 'msg': "Please provide a valid email."}), \
                   400, {'ContentType': 'application/json'}

        # Get the user to be updated.
        if not userID: userID = 0
        callback: Callback = user_services.getByID(userID)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, but this user doesn't exist"}),\
                   400, {'ContentType': 'application/json'}
        userToUpdate: User = callback.Data

        # Get the admin user who is logged in and wants to edit.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, you account doesn't exist. Try again please!"}), \
                   400, {'ContentType': 'application/json'}
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if (not adminUser.Role.EditUsers) or \
                userToUpdate.CompanyID != adminUser.CompanyID or \
                userToUpdate.Role.Name == adminUser.Role.Name or \
                userToUpdate.Role.Name == 'Owner':
            return json.dumps({'success': False, 'msg': "Sorry, You're not authorised"}), \
                   401, {'ContentType': 'application/json'}


        # Get the role to be assigned for the userToUpdate
        callback: Callback = role_services.getByNameAndCompanyID(role, adminUser.Company.ID)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': role + " role does not exist."}), \
                   400, {'ContentType': 'application/json'}
        role = callback.Data

        # Update the user (userToUpdate)
        callback: Callback = user_services.updateAsOwner(userToUpdate.ID, firstname, surname, email, role)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': " Sorry couldn't update the user. Please try again!"}), \
                   400, {'ContentType': 'application/json'}

        print("Success >> user updated")
        return json.dumps({'success':True, 'msg': "User updated successfully!"}),\
               200,\
               {'ContentType':'application/json'}


@users_router.route("/admin/user/<userID>", methods=['DELETE'])
def delete_user(userID):
    if request.method == "DELETE":

        # Get the user to be deleted.
        if not userID: userID = 0
        callback: Callback = user_services.getByID(userID)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, but this user doesn't exist"}),\
                   400, {'ContentType': 'application/json'}
        userToBeDeleted: User = callback.Data

        # Get the admin user who is logged in and wants to delete.
        callback: Callback = user_services.getByID(session.get('UserID', 0))
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, error occurred. Try again please!"}), \
                   400, {'ContentType': 'application/json'}
        adminUser: User = callback.Data

        # Check if the admin user is authorised for such an operation.
        if (not adminUser.Role.DeleteUsers) or\
                userToBeDeleted.CompanyID != adminUser.CompanyID or \
                userToBeDeleted.Role.Name == adminUser.Role.Name or \
                userToBeDeleted.Role.Name == 'Owner':
            return json.dumps({'success': False, 'msg': "Sorry, You're not authorised"}), \
                   401, {'ContentType': 'application/json'}

        # Delete the user
        callback: Callback = user_services.removeByID(userToBeDeleted.ID)
        if not callback.Success:
            return json.dumps({'success': False, 'msg': "Sorry, error occurred. Try again please!"}), \
               500, {'ContentType': 'application/json'}

        print("Success.  " + userID)

        return json.dumps({'success':True, 'msg': "User deleted successfully!"}),\
               200,\
               {'ContentType':'application/json'}


# @users_router.route("/admin/users/get", methods=['GET'])
# def admin_get_users():
#     if request.method == "GET":
#         callback: Callback = user_services.getAllByCompanyID(session.get('CompanyID', 0))
#         users = []
#         if callback.Success:
#             users = helpers.getListFromSQLAlchemyList(callback.Data)
#
#         print(users)
#     return jsonify(users)


@users_router.route("/admin/users/modify", methods=["POST"])
def admin_users_modify():
    if request.method == "POST":
        email = session.get('User')['Email']
        userID = request.form.get("userID", default="Error")
        newAccess = request.form.get("accessLevel", default="Error")
        if userID != "Error" and newAccess != "Error":
            updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE ID=?;", [newAccess, userID])
            if newAccess == "Owner":
                users = query_db("SELECT * FROM Users")
                recordID = "Error"
                # If user exists
                for record in users:
                    if record["Email"] == session.get('User')['Email']:
                        recordID = record["ID"]
                if "Error" in recordID:
                    return redirectWithMessage("admin_users", "Error in finding user.")
                updatedAccess = update_table("UPDATE Users SET AccessLevel=? WHERE ID=?;", ["Admin", recordID])
                return redirectWithMessage("admin_users", "User has been modified.")
        return redirectWithMessage("admin_users", "Error in retrieving all textbox inputs.")


@users_router.route("/admin/users/delete/<userID>", methods=["GET"])
def admin_users_delete(userID):
    if request.method == "GET":
        email = session.get('User')['Email']
        companyID = session.get('User')['CompanyID']

        users = query_db("SELECT * FROM Users")
        requestingUser = "Error"
        # If user exists
        for user in users:
            if user["Email"] == email:
                requestingUser = user
        if "Error" in requestingUser:
            return redirectWithMessage("admin_users", "Error in finding user.")
        targetUser = select_from_database_table("SELECT CompanyID FROM Users WHERE ID=?", [userID])[0]
        # Check that users are from the same company and operating user isnt 'User'
        if requestingUser["AccessLevel"] == "User" or requestingUser["CompanyID"] != targetUser:
            # TODO send feedback message
            return redirect("/admin/dashboard", code=302)
        delete_from_table("DELETE FROM Users WHERE ID=?;", [userID])
        return redirectWithMessage("admin_users", "User has been deleted.")


@users_router.route("/admin/users/permissions", methods=["POST"])
def admin_users_permissions():
    if request.method == "POST":
        adminPermissions = ""
        userPermissions = ""

        permissionTypes = ["EditChatbots", "EditUsers", "AccessBilling"]
        # try to get admin permissions
        for i in range(0, 3):
            permission = request.form.get("AdminPermission" + str(i + 1), default="Error")
            # look for Trues
            if "Error" not in permission:
                for pType in permissionTypes:
                    if pType in permission:
                        adminPermissions += (pType + ":True;")
                        permissionTypes.remove(pType)
        # look for Falses
        for pType in permissionTypes:
            adminPermissions += (pType + ":False;")

        permissionTypes = ["EditChatbots", "EditUsers", "AccessBilling"]
        # try to get user permissions
        for i in range(0, 3):
            permission = request.form.get("UserPermission" + str(i + 1), default="Error")
            # look for Trues
            if "Error" not in permission:
                for pType in permissionTypes:
                    if pType in permission:
                        userPermissions += (pType + ":True;")
                        permissionTypes.remove(pType)
        # look for Falses
        for pType in permissionTypes:
            userPermissions += (pType + ":False;")

        # update table
        # updatePermissions = query_db("UPDATE UserSettings SET AdminPermissions=?,UserPermissions=? WHERE CompanyID=?;", [adminPermissions, userPermissions, session.get('User')['CompanyID']])
        updatePermissions = update_table(
            "UPDATE UserSettings SET AdminPermissions=?,UserPermissions=? WHERE CompanyID=?;",
            [adminPermissions, userPermissions, session.get('User')['CompanyID']])

        # update current user's permisions
        permissionsDic = {}
        permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]
        if "Owner" in session.get('User')['AccessLevel']:
            permissions = permissions["AdminPermissions"].split(";")
            for perm in permissions:
                if perm:
                    permissionsDic[perm.split(":")[0]] = True
        else:
            permissions = permissions[session.get('User')['AccessLevel'] + "Permissions"].split(";")
            for perm in permissions:
                if perm:
                    if "True" in perm.split(":")[1]:
                        permBool = True
                    else:
                        permBool = False
                    permissionsDic[perm.split(":")[0]] = permBool
        session['Permissions'] = dict(permissionsDic)

        return redirect("/admin/users", code=302)