import os
import sqlite3
import stripe
from json import dumps
from flask_mail import Mail, Message
from werkzeug import secure_filename
from flask import Flask, redirect, request,render_template, jsonify, make_response, send_from_directory, send_file, url_for
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash


COMPUTERDATABASE = "computers.db"
USERDATABASE = "users.db"
QUESTIONDATABASE = "questions.db"
PRODUCTDATABASE = "products.db"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PRODUCT_IMAGES = os.path.join(APP_ROOT,'static/file_uploads/product_images')

pub_key = 'pk_test_e4Tq89P7ma1K8dAjdjQbGHmR'
secret_key = 'sk_test_Kwsicnv4HaXaKJI37XBjv1Od'

stripe.api_key = secret_key

# stripe_keys = {
#   'secret_key': os.environ['SECRET_KEY'],
#   'publishable_key': os.environ['PUBLISHABLE_KEY']
# }

# stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, static_folder='static')
mail = Mail(app)

app.config['PRODUCT_IMAGES'] = PRODUCT_IMAGES
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])

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
	print(request.cookies.get("UserEmail"))
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
	print("Before Request checks out")
	return None

@app.route("/", methods = ['GET'])
def indexpage():
    if request.method == "GET":
        return render_template("index.html")

conn = sqlite3.connect(USERDATABASE)
cur = conn.cursor()
cur.execute("SELECT * FROM Users;")
cns = cur.fetchall()
@app.route("/<route>")
def getTemplate(route):
	for record in cns:
		if route == record[4]:
			conn = sqlite3.connect(QUESTIONDATABASE)
			cur = conn.cursor()
			user_mail = request.cookies.get("UserEmail")
			cur.execute("SELECT * FROM \""+record[7]+"\"")
			data = cur.fetchall()
			conn.close()
			return render_template("dynamic-template.html", data=data)


@app.route("/demo", methods = ['GET'])
def demopage():
    if request.method == "GET":
        return render_template("demo.html")

@app.route("/demo/construction", methods = ['GET'])
def demopageconstruction():
    if request.method == "GET":
        return render_template("demo-construction.html")

@app.route("/demo/education", methods = ['GET'])
def demopageeducation():
    if request.method == "GET":
        return render_template("demo-education.html")

@app.route("/demo/fashion", methods = ['GET'])
def demopagefashion():
    if request.method == "GET":
        return render_template("demo-fashion.html")

@app.route("/demo/industrial", methods = ['GET'])
def demopageIndustrial():
    if request.method == "GET":
        return render_template("demo-industrial.html")

@app.route("/demo/pharmaceutical", methods = ['GET'])
def demopagepharmaceutical():
    if request.method == "GET":
        return render_template("demo-pharmaceutical.html")

@app.route("/demo/technology", methods = ['GET'])
def demopagetechnology():
    if request.method == "GET":
        return render_template("demo-technology.html")



@app.route("/about", methods = ['GET'])
def aboutpage():
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
		# Checking to see if the email exists in the database
		for c in data:
			i += 1
			if(email == c[0]):
				break
			else:
				if(i == len(data)):
					return render_template('login.html', data = "User not found!")
		try:
			# selecting the password from the database
			cur.execute("SELECT Password FROM Users WHERE ContactEmail=?;", [email])
			data = cur.fetchall()
			datapass = data[0][0]
			# loading the salt from the database
			cur.execute("SELECT PSalt FROM Users WHERE ContactEmail=?;", [email])
			data = cur.fetchall()
			datasalt = data[0][0]
			# checking if the password and the salt match
			if(check_password_hash(password, datapass, datasalt)):
				return render_template("admin-main.html", msg= email)
			else:
				# else denying the login
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

		# collecting the text data from the front end
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

		# injecting the text data into the database
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

		# sending registration confirmation email to the user.
		msg = Message("Thank you for registering, " + userFirstname,
		sender="thesearchbase@gmail.com",
		recipients=[userEmail])
		msg.body = "We appriciate you registering with TheSaerchBase. A whole new world of possibilities is ahead of you."
		mail.send(msg)

		# sending the regstration confirmation email to us
		msg = Message("A new user has signed up!",
		sender="thesearchbase@gmail.com",
		recipients=["thesearchbase@gmail.com"])
		msg.body = "Title: " + userTitle + "Name: " + userFirstname + userSecondname + "Email: " + userEmail + "Number: " + userContactNumber
		mail.send(msg)

		return render_template("Login.html")




# Admin pages

@app.route("/admin/homepage", methods = ['GET'])
def adminHomePage():
    if request.method == "GET":
        return render_template("admin-main.html")

def allowed_file(filename):
	ext = filename.rsplit('.',1)[1]
	print(ext)
	return '.' in filename and ext in ALLOWED_EXTENSIONS

tempData = []

@app.route("/admin/addQuestion", methods = ['GET', 'POST'])
def adminAddQuestion():
	if request.method == "GET":
		conn = sqlite3.connect(QUESTIONDATABASE)
		cur = conn.cursor()
		user_mail = request.cookies.get("UserEmail")
		cur.execute("SELECT * FROM \""+user_mail+"\"")
		mes = cur.fetchall()
		tempData = mes
		conn.close()
		return render_template("admin-form-add-question.html", data=mes)
	if request.method == "POST":
		questions= []
		for i in range(1, 11):
			if(request.form.get("question" + str(i)) != None):
				questions.append(request.form.get("question" + str(i)))
		conn = sqlite3.connect(QUESTIONDATABASE)
		cur = conn.cursor()
		user_mail = request.cookies.get("UserEmail")
		cur.execute("CREATE TABLE IF NOT EXISTS \'" + user_mail + "\' (\
		Question text NOT NULL, 'Answer1' text, 'Answer2' text, 'Answer3' text, 'Answer4' text,\
		 'Answer5' text, 'Answer6' text, 'Answer7' text, 'Answer8' text, 'Answer9' text, 'Answer10' text,\
		  'Answer11' text, 'Answer12' text)")
		conn.commit()
		i = -1
		for q in questions:
			i+= 1
			try:
				if(tempData[i][0] != None):
					cur.execute("UPDATE \""+user_mail+"\" SET Question = \""+q+"\" WHERE Question = \""+tempData[i][0]+"\"")
			except:
				cur.execute("INSERT INTO \'" + user_mail + "\'('Question') VALUES (?)", (q,))
			conn.commit()
		if(i + 1 < len(tempData)+1):
			for b in range(i+1,len(tempData)+1):
				cur.execute("DELETE FROM \""+user_mail+"\" WHERE Question = \""+tempData[i+1][0]+"\"")
		conn.commit()
		conn.close()
		return render_template("index.html", msg="Questions have been saved")

@app.route("/admin/Answers", methods = ['GET', 'POST'])
def adminAnswers():
	if request.method == "GET":
		conn = sqlite3.connect(QUESTIONDATABASE)
		cur = conn.cursor()
		user_mail = request.cookies.get("UserEmail")
		cur.execute("SELECT * FROM \""+user_mail+"\"")
		mes = cur.fetchall()
		conn.close()
		return render_template("admin-form-add-answer.html", msg=mes)
	if request.method == "POST":
		conn = sqlite3.connect(QUESTIONDATABASE)
		cur = conn.cursor()
		answers= []
		selected_question = request.form.get("question")
		user_mail = request.cookies.get("UserEmail")
		for i in range(1, 13):
			print("pname" + str(i))
			if(request.form.get("pname" + str(i)) != None):
				if (request.files['file'+str(i)].filename == ""):
					print('no file given')
					if(request.form.get("delPic" + str(i)) != "yes"):
						cur.execute("SELECT Answer"+str(i)+" FROM \""+user_mail+"\" WHERE Question=\""+selected_question+"\"")
						data = cur.fetchall()
						print(data, user_mail, selected_question)
						link = data[0][0].split(";")[2]
						answers.append(request.form.get("pname" + str(i))+";"+request.form.get("keywords" + str(i))+";"+link)
					else:
						answers.append(request.form.get("pname" + str(i))+";"+request.form.get("keywords" + str(i))+";../static/img/core-img/android-icon-72x72.png")
				else:
					file = request.files['file'+str(i)]
					if file.filename == '':
						print('No file name')
					elif file and allowed_file(file.filename):
						filename = secure_filename(file.filename)
						filePath = os.path.join(app.config['PRODUCT_IMAGES'], filename)
					file.save(filePath)
					filePath = filePath.split("TheSearchBase")[len(filePath.split("TheSearchBase")) - 1]
					# temporay string
					tempList = list(filePath)
					tempString = ""
					for char in tempList:
						if(char == "\\"):
							char = "/"
						tempString += char
					filePath = tempString
					# tempString = filePath.split("\\")
					# filePath = tempString[0] + "/" + tempString[1]
					answers.append(request.form.get("pname" + str(i))+";"+request.form.get("keywords" + str(i))+";.."+filePath)
		c=0
		for a in answers:
			c+=1
			cur.execute("UPDATE \""+user_mail+"\" SET Answer"+str(c)+" = \""+a+"\" WHERE Question = \""+selected_question+"\"")
			conn.commit()
		for b in range(c+1, 13):
			cur.execute("UPDATE \""+user_mail+"\" SET Answer"+str(b)+" = \"\" WHERE Question = \""+selected_question+"\"")
			conn.commit()
		conn.close()
		return redirect("/admin/Answers", code=302)

@app.route("/admin/addProduct", methods = ['GET', 'POST'])
def adminAddProduct():
	if request.method == "GET":
		conn = sqlite3.connect(PRODUCTDATABASE)
		cur = conn.cursor()
		user_mail = request.cookies.get("UserEmail")
		cur.execute("SELECT * FROM \""+user_mail+"\"")
		mes = cur.fetchall()
		conn.close()
		return render_template("admin-form-add-product.html", data=mes)
	if request.method == 'POST':
		filePath = 'no file upload so far'
		msg = ''
		if request.method == 'POST':
			i = 0;
			product_id = []
			name = []
			brand = []
			model = []
			price = []
			keywords = []
			discount = []
			url = []
			file_path = []
			while(True):
				i+=1
				if(request.form.get("product_ID"+str(i), default="Error") == "Error"):
					break
				product_id.append(request.form.get("product_ID"+str(i), default="Error"))
				name.append(request.form.get("product_Name"+str(i), default="Error"))
				brand.append(request.form.get("product_Brand"+str(i), default="Error"))
				model.append(request.form.get("product_Model"+str(i), default="Error"))
				price.append(request.form.get("product_Price"+str(i), default="Error"))
				keywords.append(request.form.get("product_Keywords"+str(i), default="Error"))
				discount.append(request.form.get("product_Discount"+str(i), default="Error"))
				url.append(request.form.get("product_URL"+str(i), default="Error"))
				if (request.files['product_image'+str(i)].filename == ""):
					print('no file given')
				else:
					file = request.files['product_image'+str(i)]
					if file.filename == '':
						print('No file name')
					elif file and allowed_file(file.filename):
						filename = secure_filename(file.filename)
						filePath = os.path.join(app.config['PRODUCT_IMAGES'], filename)
					file.save(filePath)
					filePath = filePath.split("TheSearchBase")[len(filePath.split("TheSearchBase")) - 1]
					tempList = list(filePath)
					tempString = ""
					for char in tempList:
						if(char == "\\"):
							char = "/"
						tempString += char
					filePath = tempString
					filePath = ".." + filePath
					file_path.append(filePath)
			try:
				conn = sqlite3.connect(PRODUCTDATABASE)
				cur = conn.cursor()
				user_mail = request.cookies.get("UserEmail")
				cur.execute("CREATE TABLE IF NOT EXISTS \'" + user_mail + "\' (\
				ProductID text, ProductName text, ProductBrand text, ProductModel text, ProductPrice text\
				ProductKeywords text, ProductDiscount text, ProductURL text, ProductImage text)")
				cur.execute("DELETE FROM \'" + user_mail + "\'")
				for q in range(0, i-1):

					# injecting database with sql with product
					cur.execute("INSERT INTO \'" + user_mail + "\'('ProductID', 'ProductName', 'ProductBrand', 'ProductModel', \
					'ProductPrice', 'ProductKeywords', 'ProductDiscount', 'ProductURL', 'ProductImage') \
					VALUES (?,?,?,?,?,?,?,?,?)", (product_id[q],name[q],brand[q],model[q],price[q],keywords[q],discount[q],url[q],file_path[q],))
					conn.commit()
			except:
				print("Error in editing the database")
				conn.rollback()
				conn.close()
			return render_template("index.html", msg="Questions have been saved")


@app.route("/admin/displayQuestions", methods = ['GET'])
def adminDisplayQuestions():
    if request.method == "GET":
        return render_template("admin-table-questions.html")

@app.route("/admin/displayAnswers", methods = ['GET'])
def adminDisplayAnswers():
    if request.method == "GET":
        return render_template("admin-table-answers.html")

@app.route("/admin/pricing")
def adminPricing():
	return render_template("admin-pricing-tables.html", pub_key=pub_key)

@app.route('/admin/thanks')
def thanks():
    return render_template('admin-thank-you.html')

@app.route("/admin/pay", methods=['GET','POST'])
def chargeUser():
	if request.method == 'GET':
		return render_template("admin-pay.html")


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

		msg = Message(mailFirstname + " from " + mailUserEmail + " has sent you a message.",
		sender=mailUserEmail,
		recipients=["thesearchbase@gmail.com"])
		msg.body = mailFirstname + " said: " + mailUserMessage + " their email is: " + mailUserEmail
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

@app.route('/robots.txt')
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

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
	app.run(debug=True)
