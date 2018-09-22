import os
from config import BaseConfig
from datetime import timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory
from flask import Blueprint, render_template, request, session, redirect, url_for, json
from flask_api import status
from utilties import helpers
from models import Callback, Assistant, Solution, db, ChatbotSession
from itsdangerous import URLSafeTimedSerializer
from services import user_services, company_services, db_services, auth_services, mail_services,\
    assistant_services, bot_services, chatbot_services, solutions_services,analytics_services
from models import secret_key
from werkzeug.utils import secure_filename
import uuid
from flask_cors import CORS

public_router = Blueprint('public_router', __name__, template_folder="../templates")

verificationSigner = URLSafeTimedSerializer(b'\xb7\xa8j\xfc\x1d\xb2S\\\xd9/\xa6y\xe0\xefC{\xb6k\xab\xa0\xcb\xdd\xdbV')


@public_router.route("/test", methods=['GET'])
def t():
    if request.method == "GET":
        return render_template("test-chatbot.html")


@public_router.route("/chatbottemplate/<assistantID>", methods=['GET'])
def test_chatbot_page(assistantID):
    if request.method == "GET":
        return render_template("chatbot-template.html")


@public_router.route("/assistant/<int:assistantID>/chatbot", methods=['GET', 'POST'])
def chatbot(assistantID):
    # For all type of requests, get the assistant
    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    if request.method == "GET":
        assistant: Assistant = callback.Data
        # Get blocks for the chatbot to use
        data: dict = bot_services.getChatbot(assistant)
        return helpers.jsonResponse(True, 200, "No Message", data)

    if request.method == "POST":
        data = request.get_json(silent=True)

        s_callback = solutions_services.getBasedOnKeywords(assistant, data['keywords'])
        if not s_callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message)

        solutions = []
        for s in s_callback.Data:
            solutions.append(s.to_dict())

        ch_callback: Callback = chatbot_services.processData(assistant, data, len(solutions))

        if not ch_callback.Success:
            return helpers.jsonResponse(False, 400, ch_callback.Message, ch_callback.Data)

        return helpers.jsonResponse(True, 200, "Solution list is here!", {'sessionID': ch_callback.Data.ID, 'solutions':solutions})

@public_router.route("/userdownloads/<path:path>", methods=['GET'])
def assistant_userdownloads(path):
    if request.method == "GET":
        print("trying to return file")
        return send_from_directory('static/user_downloads/', path)

@public_router.route("/getpopupsettings/<assistantID>", methods=['GET'])
def get_pop_settings(assistantID):
    if request.method == "GET":
        assistant_callback: Callback = assistant_services.getByID(assistantID)
        if not assistant_callback.Success:
            return helpers.jsonResponse(False, 404, "Assistant not found.", None)

        data = {"SecondsUntilPopUp": assistant_callback.Data.SecondsUntilPopup}
        return helpers.jsonResponse(True, 200, "Pop up settings retrieved", data)

@public_router.route("/assistant/<int:sessionID>/file", methods=['POST'])
def chatbot_upload_files(sessionID):
    callback: Callback = chatbot_services.getBySessionID(sessionID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Session not found.", None)
    userInput: ChatbotSession = callback.Data

    if request.method == "POST":
        data = request.get_json(silent=True)
        if request.method == 'POST':

            try:
                # check if the post request has the file part
                if 'file' not in request.files:
                    return helpers.jsonResponse(False, 404, "No file part")
                file = request.files['file']

                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    return helpers.jsonResponse(False, 404, "No selected file")

                filename = str(uuid.uuid4()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
                file.save(os.path.join(BaseConfig.USER_FILES, filename))
                userInput.FilePath = filename

            except Exception as exc:
                return helpers.jsonResponse(False, 404, "Couldn't save the file")


            # if file and allowed_file(file.filename):
            #     filename = secure_filename(file.filename)
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #     return redirect(url_for('uploaded_file',
            #                             filename=filename))

            db.session.commit()
            return helpers.jsonResponse(True, 200, "file uploaded successfully!!")



@public_router.route("/", methods=['GET'])
def indexpage():
    if request.method == "GET":
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



# Sitemap route
@public_router.route('/robots.txt')
@public_router.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# Terms and conditions page route
@public_router.route("/termsandconditions", methods=['GET'])
def terms_and_conditions():
    if request.method == "GET":
        return render_template("terms.html")


@public_router.route("/privacy", methods=['GET'])
def privacy():
    if request.method == "GET":
        return render_template("privacy-policy.html")


# Affiliate page route
@public_router.route("/affiliate", methods=['GET'])
def affiliate():
    if request.method == "GET":
        abort(status.HTTP_501_NOT_IMPLEMENTED, "Affiliate program coming soon")
        # return render_template("affiliate.html")


@public_router.route("/send/mail", methods=['GET', 'POST'])
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


@public_router.route("/setencryptionkey<key>", methods=["GET"])
def testing(key):
    if "debug" in key:
        serverRoute = "http://127.0.0.1:5000"
        if "gT5-f" in key:
            key = key.split("gT5-f")[1] + key.split("gT5-f")[0]
            key = key.replace("gT5-f", "").replace("Pa-", "5o_n").replace("uF-r", "UbwF").replace("debug", "")
    else:
        serverRoute = "https://www.thesearchbase.com"
    page = urllib.request.urlopen(serverRoute + "/static/js/sortTable.js")
    text = page.read().decode("utf8")
    part1 = text.split("FD-Y%%$VfdsaGSdsHB-%$-DFmrcStFa-S")[1].split("FEAewSvj-JGvbhKJQz-xsWEKc3-WRxjhT")[0].replace('La', 'H-q').replace('TrE', 'gb')
    page = urllib.request.urlopen(serverRoute + "/static/js/Chart.bundle.js")
    text = page.read().decode("utf8")
    part2 = text.split("GFoiWS$344wf43-cWzHOp")[1].split("Ye3Sv-FE-vWaIt3xWkbE6bsd7-jS")[0].replace('8B', '3J')
    page = urllib.request.urlopen(serverRoute + "/static/css/admin.css")
    text = page.read().decode("utf8")
    part3 = text.split(".tic")[1].split("Icon")[0]
    page = urllib.request.urlopen(serverRoute + "/static/css/themify-icons.css")
    text = page.read().decode("utf8")
    part4 = text.split("YbfEas-fUh")[1].split("TbCO")[0].replace('P-', '-G')
    if not app.debug:
        page = urllib.request.urlopen("https://bjhbcjvrawpiuqwyrzwxcksndmwpeo.herokuapp.com/static/skajhefjwehfiuwheifhxckjbachowejfhnkjfnlwgifnwoihfuwbkjcnkjfil.html")
        text = page.read().decode("utf8")
        part5 = text.split("gTb2I-6BasRb41BVr6fg-heWpB0-")[1].split("-PoWb5qEc-sMpAp-4BaOln")[0].replace('-9yR', '_nU')
    else:
        part5 = ""
    enckey = part1+part2+part3+part4+part5
    enckey = (enckey+key).replace(" ", "")
    secret_key = enckey
    return "Done"

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
    session.pop('UserID', None)
    session.pop('UserEmail', None)
    session.pop('UserPlan', None)
    session.pop('CompanyID', None)
    session.pop('Logged_in', False)
    session.clear()


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
        # size = request.form.get("companySize", default=None)
        url = request.form.get("websiteURL", default=None)
        phone = request.form.get("phoneNumber", default=None)

        if not (fullname and email and password
                and name and url):
            print("Signup Error .1")
            return helpers.redirectWithMessage("signup", "Error in getting all input information.")

        # Split fullname
        firstname = fullname.strip().split(" ")[0]
        surname = fullname.strip().split(" ")[1]

        # Signup new user
        signup_callback: Callback = auth_services.signup(email.lower(), firstname, surname, password, name, phone, url)
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

        return helpers.redirectWithMessage("login", "We have sent you a verification email. Please use it to complete the sign up process.")

@public_router.route("/account/verify/<payload>", methods=['GET'])
def verify_account(payload):
    if request.method == "GET":
        try:
            data = verificationSigner.loads(payload)
            email = data.split(";")[0]
            print("email: ", email)
            user_callback : Callback = user_services.verifyByEmail(email)
            if not user_callback.Success: raise Exception(user_callback.Message)

            return helpers.redirectWithMessage("login", "Your email has been verified. You can now access your account.")

        except Exception as e:

            print(e)
            return helpers.redirectWithMessage("login", "Email verification link failed. Please contact Customer Support in order to resolve this.")


    
## Error Handlers ##
@public_router.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/400.html', error=e.description), status.HTTP_400_BAD_REQUEST
    except:
        print("Error without description")
        return render_template('errors/400.html'), status.HTTP_400_BAD_REQUEST


@public_router.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/404.html', error= e.description), status.HTTP_404_NOT_FOUND
    except:
        print("Error without description")
        return render_template('errors/404.html'), status.HTTP_404_NOT_FOUND


@public_router.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def unsupported_media(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/415.html', error=e.description), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    except:
        print("Error without description")
        return render_template('errors/415.html'), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@public_router.errorhandler(418)
def im_a_teapot(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/418.html', error=e.description), 418
    except:
        print("Error without description")
        return render_template('errors/418.html'), 418


@public_router.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/500.html', error=e.description), status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        print("Error without description")
        return render_template('errors/500.html'), status.HTTP_500_INTERNAL_SERVER_ERROR


@public_router.errorhandler(status.HTTP_501_NOT_IMPLEMENTED)
def not_implemented(e):
    try:
        print("Error Handler:" + e.description)
        return render_template('errors/501.html', error=e.description), status.HTTP_501_NOT_IMPLEMENTED
    except:
        print("Error without description")
        return render_template('errors/501.html'), status.HTTP_501_NOT_IMPLEMENTED
