from datetime import timedelta

from flask import Blueprint, render_template, request, session
from utilties import helpers
from services import user_services, company_services, db_services, auth_services
from models import User, Company, Role, Callback
from utilties import helpers

public_router = Blueprint('public_router', __name__, template_folder="../templates")

@public_router.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
        # db_services.addCompanyAndUserAndRole(db_services)
        # print(CompanyServices.getByID(1).Users)
        # callback: Callback = db_services.addCompany()
        # print(callback.Success, callback.Message)
        #
        # callback: Callback = db_services.addUser()
        # print(callback.Success, callback.Message)

        company = Company(Name='companyName', Size=12, PhoneNumber='4344423', URL='ff.com')
        role = Role.query.filter(Role.Name == "Admin").first()
        # user = User(irstname='firstname', Surname='lastname', Email='email', Password=helpers.hashPass('123'), Company=company, Role=role)
        # company_services.addCompany("companyName", 12, "4344423", "ff.com" )
        user_services.createUser(firstname='firstname', surname='lastname', email='email', password='123', company=company, role=role)

        return render_template("index.html")


@public_router.route("/features", methods=['GET'])
def features():
    if request.method == "GET":
        company_services.removeByName('companyName')
        # users_services.deleteByEmail('email')
        return render_template("features.html")


@public_router.route("/dataRetrieval", methods=['GET'])
def data_retrieval():
    if request.method == "GET":
        return render_template("retrieval.html")


@public_router.route("/dataCollection", methods=['GET'])
def data_collection():
    if request.method == "GET":
        return render_template("collection.html")


@public_router.route("/pricing", methods=['GET'])
def pricing():
    if request.method == "GET":
        return render_template("pricing.html")


@public_router.route("/about", methods=['GET'])
def about():
    if request.method == "GET":
        return render_template("about.html")


@public_router.route("/contact", methods=['GET'])
def contactpage():
    if request.method == "GET":
        return render_template("contact.html")


@public_router.route("/login", methods=['GET', 'POST'])
def login():
    # if request.method == "GET":
    msg = helpers.checkForMessage()
    #     return render_template("login.html", msg=msg)
    #
    # elif request.method == "POST":
    if request.method == "POST" or request.method == "GET":
        session.permanent = True

        email :str = request.form.get("email", default="Error")
        password_to_check :str = request.form.get("password", default="Error")

        callback: Callback = auth_services.login(email,password_to_check)

        # if not callback.Success:
        #     return helpers.redirectWithMessage("login", callback.Message)


        return render_template("login.html", msg=msg)

        # else:

            # users = query_db("SELECT * FROM Users")

            # users = db_services
            # If user exists
            # for user in users:
            #     if user["Email"] == email:
            #         password = user['Password']
            #         if hash_password(password_to_check, password) == password:
            #
            #             verified = user['Verified']
            #
            #             # If credentials are correct and users' account is verified
            #             if verified == "True":
            #
            #                 messages = dumps({"email": escape(email)})
            #
            #                 # Set the session for the logged in user
            #                 session['User'] = user
            #                 session['Logged_in'] = True
            #
            #                 # Store user assistants if they exist, in the session
            #                 assistants = query_db("SELECT * FROM Assistants WHERE CompanyID=?;",
            #                                     [user['CompanyID']])
            #
            #                 #Store users access permisions
            #                 session['UserAssistants'] =  assistants
            #                 permissionsDic = {}
            #                 permissions = query_db("SELECT * FROM UserSettings WHERE CompanyID=?", [session.get('User')['CompanyID']])[0]
            #                 if "Owner" in session.get('User')['AccessLevel']:
            #                     permissions = permissions["AdminPermissions"].split(";")
            #                     for perm in permissions:
            #                         if perm:
            #                             permissionsDic[perm.split(":")[0]] = True
            #                 else:
            #                     permissions = permissions[session.get('User')['AccessLevel']+"Permissions"].split(";")
            #                     for perm in permissions:
            #                         if perm:
            #                             if "True" in perm.split(":")[1]:
            #                                 permBool = True
            #                             else:
            #                                 permBool = False
            #                             permissionsDic[perm.split(":")[0]] = permBool
            #                 session['Permissions'] = dict(permissionsDic)
            #
            #                 # Set user plan e.g. (Basic, Ultimate...)
            #                 session['UserPlan'] = {}
            #                 session['UserPlan']['Nickname'] =  getPlanNickname(user['SubID'])
            #                 if getPlanNickname(user['SubID']) is None:
            #                     session['UserPlan']['Settings'] = NoPlan
            #                 elif "Basic" in getPlanNickname(user['SubID']):
            #                     session['UserPlan']['Settings'] = BasicPlan
            #                 elif "Advanced" in getPlanNickname(user['SubID']):
            #                     session['UserPlan']['Settings'] = AdvancedPlan
            #                 elif "Ultimate" in getPlanNickname(user['SubID']):
            #                     session['UserPlan']['Settings'] = UltimatePlan
            #
            #                 # Test session specific values
            #                 print(session)
            #
            #                 return redirect("/admin/homepage", code=302)
            #
            #             else:
            #                 return redirectWithMessage("login", "Please verify your account before you log in.")
            # return redirectWithMessage("login", "You entered an incorrect username or password.")
#

# @public_router.route('/logout')
# def logout():
#
#     # Will clear out the session.
#     session.pop('User', None)
#     session.pop('UserAssistants', None)
#     session.pop('Logged_in', False)
#
#     return redirect(url_for('login'))


# TODO improve verification
@public_router.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        msg = helpers.checkForMessage()
        return render_template("signup.html", msg=msg)


    # elif request.method == "POST":
    #
    #     email = request.form.get("email", default="Error").lower()
    #
    #     fullname = request.form.get("fullname", default="Error")
    #     accessLevel = "Owner"
    #     password = request.form.get("password", default="Error")
    #
    #     companyName = request.form.get("companyName", default="Error")
    #     companySize = request.form.get("companySize", default="0")
    #     companyPhoneNumber = request.form.get("phoneNumber", default="Error")
    #     websiteURL = request.form.get("websiteURL", default="Error")
    #
    #     if fullname == "Error" or accessLevel == "Error" or email == "Error" or password == "Error" \
    #             or companyName == "Error" or websiteURL == "Error":
    #         print("Invalid request")
    #         return redirectWithMessage("signup", "Error in getting all input information")
    #
    #
    #     else:
    #         users = query_db("SELECT * FROM Users")
    #         # If user exists
    #         for user in users:
    #             if user["Email"] == email:
    #                 print("Email is already in use!")
    #                 return redirectWithMessage("signup", "Email already in use.")
    #         try:
    #             firstname = fullname.strip().split(" ")[0]
    #             surname = fullname.strip().split(" ")[1]
    #
    #             # debug
    #             print(firstname)
    #             print(surname)
    #
    #         except IndexError as e:
    #             return redirectWithMessage("signup", "Error in handling names")
    #
    #         newUser = None
    #         newCompany = None
    #         newCustomer = None
    #
    #         # Create a Stripe customer for the new company.
    #         newCustomer = stripe.Customer.create(
    #             email=email
    #         )
    #
    #         # debug
    #         # print(newCustomer)
    #
    #         hashed_password = hash_password(password)
    #         if app.debug:
    #             verified = "True"
    #         else:
    #             verified = "False"
    #
    #         # Create a company record for the new user
    #         # ENCRYPTION
    #         insertCompanyResponse = insert_into_database_table(
    #             "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (
    #             encryptVar(companyName), encryptVar(companySize), encryptVar(websiteURL),
    #             encryptVar(companyPhoneNumber)))
    #         # insertCompanyResponse = insert_into_database_table(
    #         #   "INSERT INTO Companies('Name','Size', 'URL', 'PhoneNumber') VALUES (?,?,?,?);", (companyName, companySize, websiteURL, companyPhoneNumber))
    #
    #         newCompany = get_last_row_from_table("Companies")
    #         # print(newCompany)
    #
    #         createUserSettings = insert_into_database_table("INSERT INTO UserSettings('CompanyID') VALUES (?);",
    #                                                         (newCompany['ID'],))
    #         # TODO validate insertCompanyResponse and createUserSettings
    #
    #         try:
    #
    #             # Subscribe to the Basic plan with a trial of 14 days
    #             sub = stripe.Subscription.create(
    #                 customer=newCustomer['id'],
    #                 items=[{'plan': 'plan_D3lp2yVtTotk2f'}],
    #                 trial_period_days=14,
    #             )
    #
    #             print(sub['items']['data'][0]['plan']['nickname'])
    #             # print(sub)
    #
    #             # Create a user account and link it with the new created company record above
    #             # ENCRYPTION
    #             newUser = insert_db("Users", (
    #             'CompanyID', 'Firstname', 'Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified',
    #             'SubID'),
    #                                 (newCompany['ID'], encryptVar(firstname), encryptVar(surname), accessLevel,
    #                                  encryptVar(email), hashed_password, newCustomer['id'],
    #                                  str(verified), sub['id'])
    #                                 )
    #             # newUser = insert_db("Users", ('CompanyID', 'Firstname','Surname', 'AccessLevel', 'Email', 'Password', 'StripeID', 'Verified', 'SubID'),
    #             #           (newCompany['ID'], firstname, surname, accessLevel, email, hashed_password, newCustomer['id'],
    #             #          str(verified), sub['id'])
    #             #         )
    #
    #
    #
    #         except Exception as e:
    #             # Clear out when exception
    #             if newUser is not None:
    #                 query_db("DELETE FROM Users WHERE ID=?", [newUser['ID']])
    #                 print("Delete new user")
    #
    #             if newCompany is not None:
    #                 query_db("DELETE FROM Companies WHERE ID=?", [newCompany['ID']])
    #                 print("Delete new company")
    #
    #             print("Delete new user' stripe account")
    #             if newCustomer is not None:
    #                 cus = stripe.Customer.retrieve(newCustomer['id'])
    #                 cus.delete()
    #
    #             print(e)
    #             return redirectWithMessage("signup", "An error occurred and could not subscribe. Please try again!.")
    #             # TODO check subscription for errors https://stripe.com/docs/api#errors
    #
    #         # TODO this needs improving
            msg = Message("Account verification",
                          sender="thesearchbase@gmail.com",
                          recipients=[email])
            payload = email + ";" + companyName
            link = "https://www.thesearchbase.com/account/verify/" + verificationSigner.dumps(payload)
            msg.html = "<img src='https://thesearchbase.com/static/email_images/verify_email.png'><br /><h4>Hi,</h4> <p>Thank you for registering with TheSearchbase.</p> <br />  There is just one small step left, visit \
                        <a href='" + link + "'> this link </a> to verify your account. \
                        In case the link above doesn't work you can click on the link below. <br /> <br /> " + link + " <br />  <br /> \
                        We look forward to you, using our platform. <br /> <br />\
                        Regards, <br /> TheSearchBase Team <br />\
                        <img src='https://thesearchbase.com/static/email_images/footer_image.png'>"
            mail.send(msg)

            # sending the registration confirmation email to us
            msg = Message("A new company has signed up!",
                          sender="thesearchbase@gmail.com",
                          recipients=["thesearchbase@gmail.com"])
            msg.html = "<p>Company name: " + companyName + " has signed up. <br>The admin's details are: <br>Name: " + fullname + " <br>Email: " + email + ".</p>"
            mail.send(msg)
    #
    #         return render_template('errors/verification.html',
    #                                msg="Please check your email and follow instructions to verify account and get started.")
    #
