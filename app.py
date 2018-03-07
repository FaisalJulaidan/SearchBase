import os
import sqlite3
from json import dumps
from flask_mail import Mail, Message
from flask import Flask, redirect, request,render_template, jsonify, make_response, send_from_directory
from flask.ext.bcrypt import Bcrypt

COMPUTERDATABASE = "computers.db"
DATABASE = "users.db"

app = Flask(__name__)
mail = Mail(app)
flask_bcrypt = Bcrypt(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config.update(
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'thesearchbase@gmail.com',
	MAIL_PASSWORD = 'pilbvnczzdgxkyzy'
	)
mail = Mail(app)

@app.route("/", methods = ['GET'])
def indexpage():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/test", methods = ['GET', 'POST'])
def test():
	if request.method == "GET":
		return render_template("admin-addQandA.html")

@app.route("/demo", methods = ['GET'])
def aboutpage():
    if request.method == "GET":
        return render_template("demo.html")

@app.route("/about", methods = ['GET'])
def demopage():
    if request.method == "GET":
        return render_template("about.html")

@app.route("/features", methods = ['GET'])
def featurespage():
    if request.method == "GET":
        return render_template("features.html")

@app.route("/pricing", methods = ['GET'])
def pricingpage():
    if request.method == "GET":
        return render_template("Pricing.html")

@app.route("/contact", methods = ['GET'])
def contactpage():
    if request.method == "GET":
        return render_template("contact.html")

@app.route("/login", methods = ['GET', 'POST'])
def loginpage():
    if request.method == "GET":
        return render_template("Login.html")
    if request.method == 'POST':
        email = request.form.get("email", default="Error")
        password = request.form.get("pass", default="Error")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT ContactEmail FROM Users;")
        data = cur.fetchall()
        i = 0
        for c in data:
            i += 1
            if(email == c[0]):
                break
            else:
                if(i == len(data)):
                    return render_template('login.html', data = "User not found!")
        try:
            cur.execute("SELECT Password FROM Users WHERE ContactEmail=?;", [email])
            data = cur.fetchall()
            if(flask_bcrypt.check_password_hash(data[0][0], password)):
                return render_template("admin-main.html")
            else:
                print("Password does not match!")
                return render_template('Login.html', data = "User name and password does not match!")
        except:
            print("Error in trying to find user")
            conn.rollback()
        finally:
            conn.close()


@app.route("/signupform", methods = ['GET', 'POST'])
def signpage():
    if request.method == "GET":
        return render_template("Signup.html")
    if request.method == 'POST':
        userTitle = request.form.get("title", default="Error")
        userFirstname = request.form.get("firstname", default="Error")
        userSecondname = request.form.get("surname", default="Error")
        userCompanyName = request.form.get("companyName", default="Error")
        userPositionCompany = request.form.get("userPosition", default="Error")
        userCompanyAddress = request.form.get("companyAddress", default="Error")
        userEmail = request.form.get("contactEmail", default="Error")
        userContactNumber = request.form.get("contactNumber", default="Error")
        userCountry = request.form.get("country", default="Error")
        userPassword = request.form.get("pass", default="Error")
        pass_hashed = flask_bcrypt.generate_password_hash(userPassword).decode("utf-8")

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO Users ('Title', 'Firstname', 'Surname', 'CompanyName', 'UserPosition', 'CompanyAddress', 'ContactEmail', 'ContactNumber', 'Country', 'Password')\
                    VALUES (?,?,?,?,?,?,?,?,?,?)", (userTitle, userFirstname, userSecondname, userCompanyName, userPositionCompany, userCompanyAddress, userEmail, userContactNumber, userCountry, pass_hashed))

        conn.commit()
        print("User details added!")
        conn.close()
    return render_template("index.html")


# Admin pages

@app.route("/admin/homepage", methods = ['GET'])
def adminHomePage():
    if request.method == "GET":
        return render_template("admin-main.html")

@app.route("/admin/addQuestion", methods = ['GET'])
def adminAddQuestion():
    if request.method == "GET":
        return render_template("admin-form.html")

@app.route("/admin/addProduct", methods = ['GET'])
def adminAddProduct():
    if request.method == "GET":
        return render_template("admin-form-wizards.html")

@app.route("/admin/pricing", methods = ['GET'])
def adminPricing():
    if request.method == "GET":
        return render_template("admin-pricing-tables.html")

@app.route("/admin/profile", methods = ['GET'])
def adminProfile():
    if request.method == "GET":
        return render_template("admin-profile.html")

@app.route("/admin/indexAll", methods = ['GET'])
def adminDisplayAll():
    if request.method == "GET":
        return render_template("admin-tables.html")







@app.route("/send/mail", methods=['GET', 'POST'])
def sendEmail():
	if request.method == "GET":
		return render_template("index.html")
	if request.method == "POST":
		mailFirstname = request.form.get("sendingName", default="Error")
		mailUserEmail = request.form.get("sendingEmail", default="Error")
		mailUserMessage = request.form.get("sendMessage", default="Error")

		msg = Message(mailFirstname,
		sender=mailUserEmail,
		recipients=["thesearchbase@gmail.com"])
		msg.body = mailUserMessage
		mail.send(msg)
		return render_template("index.html")






# Route for the computer search

@app.route("/GetComputers", methods = ['POST'])
def getcomputers():
    if request.method == 'POST':
        computerUse = request.form["compuse"]
        minBudget = request.form["minbudget"]
        maxBudget = request.form["maxbudget"]
        portable = request.form["portable"]
        battery = request.form["battery"]
        keyfeatures = request.form["keyfeatures"]
        print(portable)
        conn = sqlite3.connect(COMPUTERDATABASE)
        cur = conn.cursor()
        print(keyfeatures)
        print("Looking for: ", computerUse, " ", minBudget, " ", maxBudget, " ", portable, " ", battery, " ", keyfeatures)
        try:
            if (portable=="null"):
                print("Search without portable setting")
                cur.execute("SELECT * FROM computers WHERE (Use1=? OR Use2=?) \
                AND Price>=? AND Price<=? AND BatteryLife>=? \
                ", [computerUse, computerUse, minBudget, maxBudget, battery])
            else:
                print("Search for ", portable)
                cur.execute("SELECT * FROM computers WHERE (Use1=? OR Use2=?) \
                AND Price>=? AND Price<=? AND Type=? AND BatteryLife>=? \
                ", [computerUse, computerUse, minBudget, maxBudget, portable, battery])
            data = cur.fetchall()
            print(data)
        except:
            print("ERROR IN RETRIEVING COMPUTERS")
        finally:
            conn.close()
        # filter for keyfeatures
        if(keyfeatures != ""):
            print("before keyfeatures: ", data)
            print(type(keyfeatures))
            if(keyfeatures is not list):
                print("Convert keyfeatures to list")
                keyfeatures = [keyfeatures]
            print(type(keyfeatures))
            print(keyfeatures)
            for t in keyfeatures:
                for c in data:
                    print(len(data))
                    print("Checking :", c)
                    init = False
                    for i in c:
                        if i == t:
                            init = True
                    if init == False:
                        data.remove(c)
                        print(t, " ", c, "removed")
                for c in data:
                    print(len(data))
                    print("Checking :", c)
                    init = False
                    for i in c:
                        if i == t:
                            init = True
                    if init == False:
                        data.remove(c)
                        print(t, " ", c, "removed")
            print("after keyfeatures: ", data)
        if not data:
            return "We could not find Computers that matched your seach. Please try different filter options."
        datastring = ""
        for i in data:
            for c in i:
                datastring+=str(c) + "|"
            datastring = datastring[:-1]
            datastring += ","
        print(datastring)
        return jsonify(datastring)

# Sitemap route

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Terms and conditions page route
@app.route("/termsandconditions", methods = ['GET'])
def termsPage():
    if request.method == "GET":
        return render_template("terms.html")

# Terms and conditions page route
@app.route("/privacy", methods = ['GET'])
def PrivacyPage():
    if request.method == "GET":
        return render_template("privacy-policy.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
