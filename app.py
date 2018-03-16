import os
import sqlite3
from json import dumps
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import Flask, redirect, request,render_template, jsonify, make_response, send_from_directory, send_file
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash


COMPUTERDATABASE = "computers.db"
USERDATABASE = "users.db"
QUESTIONDATABASE = "questions.db"
PRODUCTDATABASE = "products.db"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PRODUCT_IMAGES = os.path.join(APP_ROOT,'static/file_uploads/product_images')


app = Flask(__name__)
mail = Mail(app)

app.config['PRODUCT_IMAGES'] = PRODUCT_IMAGES
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

salt = generate_random_salt()

app.config.update(
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'thesearchbase@gmail.com',
	MAIL_PASSWORD = 'pilbvnczzdgxkyzy'
	)
mail = Mail(app)

#code to ensure user is loged in
@app.before_request
def before_request():
	theurl = str(request.url_rule)
	if ("admin" not in theurl):
		print("Ignore before request for: ", theurl)
		return None
	if(request.cookies.get("UserEmail") == None):
		print("User not logged in")
		return redirect("/login", code=302)
	print("Before request checking: ", theurl, " ep: ", request.endpoint)
	if(request.cookies.get("UserEmail") == 'None') and request.endpoint != 'login':
		return render_template("userlogin.html", msg = "Please log in first!")
	return None

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
        conn = sqlite3.connect(USERDATABASE)
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
            datapass = data[0][0]
            cur.execute("SELECT PSalt FROM Users WHERE ContactEmail=?;", [email])
            data = cur.fetchall()
            datasalt = data[0][0]
            if(check_password_hash(password, datapass, datasalt)):
                return render_template("admin-main.html", msg= email)
            else:
                print(password, data[0][0])
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
		pass_hashed = generate_password_hash(userPassword, salt)

		conn = sqlite3.connect(USERDATABASE)
		cur = conn.cursor()
		cur.execute("SELECT ContactEmail FROM Users WHERE ContactEmail=?", [userEmail])
		demail = cur.fetchall()
		if demail:
			return render_template("Signup.html", msg="Email already exists")
		cur.execute("INSERT INTO Users ('Title', 'Firstname', 'Surname', 'CompanyName', 'UserPosition', 'CompanyAddress', 'ContactEmail', 'ContactNumber', 'Country', 'Password', 'PSalt')\
						VALUES (?,?,?,?,?,?,?,?,?,?,?)", (userTitle, userFirstname, userSecondname, userCompanyName, userPositionCompany, userCompanyAddress, userEmail, userContactNumber, userCountry, pass_hashed, salt))
		conn.commit()
		print("User details added!")
		conn.close()
		return render_template("Login.html")


# Admin pages

@app.route("/admin/homepage", methods = ['GET'])
def adminHomePage():
    if request.method == "GET":
        return render_template("admin-main.html")

@app.route("/admin/addQuestion", methods = ['GET', 'POST'])
def adminAddQuestion():
	if request.method == "GET":
		return render_template("admin-form-add-question.html")
	if request.method == "POST":
		questions= []
		for i in range(1, 11):
			if(request.form.get("question" + str(i)) != None):
				questions.append(request.form.get("question" + str(i)))
		conn = sqlite3.connect(QUESTIONDATABASE)
		cur = conn.cursor()
		umail = request.cookies.get("UserEmail")
		cur.execute("CREATE TABLE IF NOT EXISTS \'" + umail + "\' (\
		Question text NOT NULL, 'Answer1' text, 'Answer2' text, 'Answer3' text, 'Answer4' text,\
		 'Answer5' text, 'Answer6' text, 'Answer7' text, 'Answer8' text, 'Answer9' text, 'Answer10' text,\
		  'Answer11' text, 'Answer12' text)")
		conn.commit()
		cur.execute("DELETE FROM \'" + umail + "\'")
		for q in questions:
			cur.execute("INSERT INTO \'" + umail + "\'('Question') VALUES (?)", (q,))
			conn.commit()
		return render_template("index.html", msg="Questions have been saved")

@app.route("/admin/addProduct", methods = ['GET', 'POST'])
def adminAddProduct():
	if request.method == "GET":
		return render_template("admin-form-add-product.html")
	if request.method == 'POST':
		def allowed_file(filename):
			ext = filename.rsplit('.',1)[1]
			print(ext)
			return '.' in filename and ext in ALLOWED_EXTENSIONS
		filePath = 'no file upload so far'
		msg = ''
		if request.method == 'POST':
			i = 0;
			pid = []
			name = []
			brand = []
			model = []
			price = []
			features = []
			keywords = []
			discount = []
			url = []
			fp = []
			try:
				while(True):
					i+=1
					pid.append(request.form.get("product_ID"+str(i), default="Error"))
					name.append(request.form.get("product_Name"+str(i), default="Error"))
					brand.append(request.form.get("product_Brand"+str(i), default="Error"))
					model.append(request.form.get("product_Model"+str(i), default="Error"))
					price.append(request.form.get("product_Price"+str(i), default="Error"))
					features.append(request.form.get("product_Features"+str(i), default="Error"))
					keywords.append(request.form.get("product_Keywords"+str(i), default="Error"))
					discount.append(request.form.get("product_Discount"+str(i), default="Error"))
					url.append(request.form.get("product_URL"+str(i), default="Error"))
					if 'file' not in request.files:
						msg = 'no file given'
					else:
						file = request.files['product_image'+str(i)]
						if file.filename == '':
							msg = 'No file name'
						elif file and allowed_file(file.filename):
							filename = secure_filename(file.filename)
							filePath = os.path.join(app.config['PRODUCT_IMAGES'], filename)
						file.save(filePath)
						fp.append(filePath)
			except:
				print("Error in Products Taken - Assume its ok")
			conn = sqlite3.connect(PRODUCTDATABASE)
			cur = conn.cursor()
			umail = request.cookies.get("UserEmail")
			cur.execute("CREATE TABLE IF NOT EXISTS \'" + umail + "\' (\
			ProductID text, ProductName text, ProductBrand text, ProductModel text, ProductPrice text\
			ProductFeatures text, ProductKeywords text, ProductDiscount text, ProductURL text, ProductImage text)")
			conn.commit()
			cur.execute("DELETE FROM \'" + umail + "\'")
			for q in range(1, i+1):
				cur.execute("INSERT INTO \'" + umail + "\'('ProductID', 'ProductName', 'ProductBrand', 'ProductModel', \
				'ProductPrice', 'ProductFeatures', 'ProductKeywords', 'ProductDiscount', 'ProductURL', 'ProductImage') \
				VALUES (?,?,?,?,?,?,?,?,?,?)", (pid[q],name[q],brand[q],model[q],price[q],features[q],keywords[q],discount[q],url[q],fp[q],))
				conn.commit()
			return render_template("index.html", msg="Questions have been saved")


@app.route("/admin/editProduct", methods = ['GET'])
def adminEditProduct():
    if request.method == "GET":
        return render_template("admin-form-wizards.html")

@app.route("/admin/deleteProduct", methods = ['GET'])
def adminDeleteProduct():
    if request.method == "GET":
        return render_template("admin-form-delete-product.html")


@app.route("/admin/displayQuestions", methods = ['GET'])
def adminDisplayQuestions():
    if request.method == "GET":
        return render_template("admin-table-questions.html")

@app.route("/admin/displayAnswers", methods = ['GET'])
def adminDisplayAnswers():
    if request.method == "GET":
        return render_template("admin-table-answers.html")



@app.route("/admin/pricing", methods = ['GET'])
def adminPricing():
    if request.method == "GET":
        return render_template("admin-pricing-tables.html")

@app.route("/admin/profile", methods = ['GET'])
def adminProfile():
    if request.method == "GET":
        return render_template("admin-profile.html")


@app.route("/admin/supportGeneral", methods = ['GET'])
def adminGeneralSupport():
    if request.method == "GET":
        return render_template("admin-general-support.html")

@app.route("/admin/supportDocs", methods = ['GET'])
def adminDocsSupport():
    if request.method == "GET":
        return render_template("admin-docs.html")

@app.route("/admin/supportSetup", methods = ['GET'])
def adminSetupSupport():
    if request.method == "GET":
        return render_template("admin-getting-setup.html")

@app.route("/admin/supportIntergartion", methods = ['GET'])
def adminIntergrationSupport():
    if request.method == "GET":
        return render_template("admin-intergation-tutorial.html")

@app.route("/admin/supportBilling", methods = ['GET'])
def adminBillingSupport():
    if request.method == "GET":
        return render_template("admin-billing-support.html")

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


@app.route("/send/mailtop", methods=['GET', 'POST'])
def sendMarketingEmail():
	if request.method == "GET":
		return render_template("index.html")
	if request.method == "POST":
		userEmail = request.form.get("user_email", default="Error")
		msg = Message(userEmail + " Has sent you mail!",
		sender=userEmail,
		recipients=["thesearchbase@gmail.com"])
		msg.body = userEmail + " Has registerd their Interest for your product"
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
