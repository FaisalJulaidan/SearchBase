from services import user_services, admin_services
from models import Callback, User
from flask import Blueprint, request, redirect, session
from utilties import helpers

users_router: Blueprint = Blueprint('users_router', __name__ ,template_folder="../../templates")


# Method for the users
@users_router.route("/admin/users", methods=['GET'])
def admin_users():
    if request.method == "GET":
        callback: Callback = user_services.getAllByCompanyID(session.get('CompanyID', 0))
        users = []
        if callback.Success:
            users = callback.Data

        print(users)

        return admin_services.render("admin/users.html", users=users)


@users_router.route("/admin/users/add", methods=['POST'])
def admin_users_add():
    if request.method == "POST":
        numberOfCompanyUsers = count_db("Users", " WHERE CompanyID=?", [session.get('User')['CompanyID'], ])
        if numberOfCompanyUsers >= session['UserPlan']['Settings']['AdditionalUsersCap'] + 1:
            return redirectWithMessage("admin_users", "You have reached the max amount of additional Users - " + str(
                session['UserPlan']['Settings']['AdditionalUsersCap']) + ".")
        email = session.get('User')['Email']
        companyID = session.get('User')['CompanyID']
        fullname = request.form.get("fullname", default="Error")
        accessLevel = request.form.get("accessLevel", default="Error")
        newEmail = request.form.get("email", default="Error")
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(9))
        # Generates a random password

        if fullname == "Error" or accessLevel == "Error" or newEmail == "Error":
            return redirectWithMessage("admin_users", "Error in retrieving all textbox inputs.")
        else:
            newEmail = newEmail.lower()
            users = query_db("SELECT * FROM Users")
            # If user exists
            for record in users:
                if record["Email"] == newEmail:
                    return redirectWithMessage("admin_users", "Email is already in use!")
            try:
                firstname = fullname.split(" ")[0]
                surname = fullname.split(" ")[1]
            except IndexError as e:
                return redirectWithMessage("admin_users", "Error in retrieving both names.")
            hashed_password = hash_password(password)

            # ENCRYPTION
            insertUserResponse = insert_into_database_table(
                "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
                (companyID, encryptVar(firstname), encryptVar(surname), accessLevel, encryptVar(newEmail),
                 hashed_password, "False"))
            # insertUserResponse = insert_into_database_table(
            #   "INSERT INTO Users ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'Verified') VALUES (?,?,?,?,?,?,?);",
            #  (companyID, firstname, surname, accessLevel, newEmail, hashed_password, "True"))
            if "added" not in insertUserResponse:
                return redirectWithMessage("admin_users", "Error in adding user to our records.")
            else:
                # if not app.debug:

                # sending email to the new user.
                # TODO this needs improving
                link = "https://www.thesearchbase.com/admin/changepassword"
                msg = Message("Account verification, " + firstname + " " + surname,
                              sender="thesearchbase@gmail.com",
                              recipients=[newEmail])
                msg.html = "<h4>Hi, <h4> <br /> <p>You have been registered with TheSearchBase by an admin at your company.<br> \
                            To get access to the platform, we have generated a temporary password for you to access the platform.</p> <br /> \
                            <h4>Your temporary password is: " + password + ".<h4><br />\
                            Please visit <a href='" + link + "'>this link</a> to sign in and to set the password for your account.<p><br /> If you feel this is a mistake please contact " + email + ". <br /> <br / > Regards, TheSearchBase Team"
                mail.send(msg)
                return redirectWithMessage("admin_users",
                                           "User has been added. A temporary password has been emailed to them.")


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