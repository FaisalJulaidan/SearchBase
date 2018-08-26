from datetime import timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for
from utilties import helpers
from models import User, Company, Role, Callback
from itsdangerous import URLSafeTimedSerializer
from services import user_services, company_services, db_services, auth_services, mail_services

public_router = Blueprint('public_router', __name__, template_folder="../templates")

verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')


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

        # company = Company(Name='companyName', Size=12, PhoneNumber='4344423', URL='ff.com')
        # role = Role.query.filter(Role.Name == "Admin").first()
        # user = User(irstname='firstname', Surname='lastname', Email='email', Password=helpers.hashPass('123'), Company=company, Role=role)
        # company_services.addCompany("companyName", 12, "4344423", "ff.com" )
        # user_services.createUser(firstname='firstname', surname='lastname', email='email', password='123', company=company, role=role)

        return render_template("index.html")


@public_router.route("/features", methods=['GET'])
def features():
    if request.method == "GET":
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
    if request.method == "GET":
        msg = helpers.checkForMessage()
        return render_template("login.html", msg=msg)

    elif request.method == "POST":
        session.permanent = True

        email: str = request.form.get("email", default=None)
        password_to_check :str = request.form.get("password", default=None)

        callback: Callback = auth_services.login(email,password_to_check)

        if callback.Success:
            return redirect("/admin/dashboard", code=302)
        else:
            return helpers.redirectWithMessage("login", callback.Message)


@public_router.route('/logout',  methods=['GET'])
def logout():

    # Will clear out the session.
    session.pop('userID', None)
    session.pop('userEmail', None)
    session.pop('UserPlan', None)
    session.pop('Logged_in', False)

    return redirect(url_for('public_router.login'))


# TODO improve verification
@public_router.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == "GET":
        msg = helpers.checkForMessage()
        return render_template("signup.html", msg=msg)

    elif request.method == "POST":

        # User info
        email = request.form.get("email", default=None)
        fullname = request.form.get("fullname", default=None)
        password = request.form.get("password", default=None)

        # Company info
        name = request.form.get("companyName", default=None)
        size = request.form.get("companySize", default=None)
        url = request.form.get("websiteURL", default=None)
        phone = request.form.get("phoneNumber", default=None)

        if not (fullname and email and password
                and name and url and phone):
            print("Signup Error .1")
            return helpers.redirectWithMessage("signup", "Error in getting all input information.")

        # Split fullname
        firstname = fullname.strip().split(" ")[0]
        surname = fullname.strip().split(" ")[1]

        # Signup new user
        signup_callback: Callback = auth_services.signup(email.lower(), firstname, surname, password,
                                                         name, size, phone, url)
        print(signup_callback.Success, signup_callback.Message)
        if not signup_callback.Success:
            print(signup_callback.Message)
            return helpers.redirectWithMessage("signup", signup_callback.Message)

        # Send verification email
        mail_callback: Callback = mail_services.sendVerificationEmail(email, name, fullname)
        print(mail_callback.Message)

        # If error while sending verification email
        if not mail_callback.Success:
            helpers.redirectWithMessage('signup', 'Signed up successfully but > ' + mail_callback.Message
                                        + '. Please contact TheSearchBaseStaff to activate your account.')

        return render_template('errors/verification.html',
                               msg="Please check your email and follow instructions to verify account and get started.")
