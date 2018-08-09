
from flask import Blueprint, request, redirect

profile_router: Blueprint = Blueprint('profile', __name__ ,template_folder="../../templates")
@profile_router.route("/admin/profile", methods=['GET', 'POST'])
def profilePage():
    if request.method == "GET":
        message = checkForMessage()
        email = session.get('User')['Email']
        users = query_db("SELECT * FROM Users")
        user = "Error"
        # If user exists
        for record in users:
            if record["Email"] == email:
                user = record
        if "Error" in user:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error in finding user!")
        company = query_db("SELECT * FROM Companies WHERE ID=?;", [user["CompanyID"]])
        if company is None or company is "None" or company is "Error":
            company="Error in finding company"
        print(company)
        print(user)
        print(email)
        return render_template("admin/profile.html", user=user, email=email, company=company[0], message=message)

    elif request.method == "POST":
        curEmail = session.get('User')['Email']
        names = request.form.get("names", default="Error")
        newEmail = request.form.get("email", default="error").lower()
        companyName = request.form.get("companyName", default="Error")
        companyURL = request.form.get("companyURL", default="error").lower()
        if names != "Error" and newEmail != "error" and companyURL != "error" and companyName != "Error":
            names = names.split(" ")
            name1 = names[0]
            name2 = names[1]
            users = query_db("SELECT * FROM Users")
            # If user exists
            for user in users:
                if user["Email"] == curEmail:
                    #TODO check if they worked
                    #ENCRYPTION
                    updateUser = update_table("UPDATE Users SET Firstname=?, Surname=?, Email=? WHERE ID=?;", [encryptVar(name1),encryptVar(name2),encryptVar(newEmail),user["ID"]])
                    #updateUser = update_table("UPDATE Users SET Firstname=?, Surname=?, Email=? WHERE ID=?;", [name1,name2,newEmail,user["ID"]])
                    companyID = select_from_database_table("SELECT CompanyID FROM Users WHERE ID=?;", [user["ID"]])
                    updateCompany = update_table("UPDATE Companies SET Name=?, URL=? WHERE ID=?;", [encryptVar(companyName),encryptVar(companyURL),companyID[0]])
                    #updateCompany = update_table("UPDATE Companies SET Name=?, URL=? WHERE ID=?;", [companyName,companyURL,companyID[0]])
                    users = query_db("SELECT * FROM Users")
                    user = "Error"
                    for record in users:
                        if record["Email"] == newEmail:
                            user = record
                    if "Error" in user:
                        print("Error in updating Company or Profile Data")
                        return redirect("/admin/profile", code=302)
                    session['User'] = user
                    return redirect("/admin/profile", code=302)
        print("Error in updating Company or Profile Data")
        return redirect("/admin/profile", code=302)
