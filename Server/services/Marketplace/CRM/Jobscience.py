import json
import logging
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, db, StoredFileInfo
from services import databases_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services

from utilities import helpers
from utilities.enums import CRM

# USE Jobscience SANDBOX or PROD environment:

if os.environ['FLASK_ENV'] == 'development':
    os.environ['JS_CLIENT_ID'] = os.environ['JOBSCIENCE_SANDBOX_CLIENT_ID']
    os.environ['JS_URL'] = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/oauth2/authorize?"
    CLIENT_ID = os.environ['JOBSCIENCE_SANDBOX_CLIENT_ID']
    CLIENT_SECRET = os.environ['JOBSCIENCE_SANDBOX_CLIENT_SECRET']
    BASE_URL = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v46.0/"
    BASE_URL_LOGIN = "https://test.salesforce.com/services/oauth2/"

    logging.info("Using sandbox Jobscience app instance")

else:
    CLIENT_ID = os.environ['JOBSCIENCE_CLIENT_ID']
    CLIENT_SECRET = os.environ['JOBSCIENCE_CLIENT_SECRET']
    BASE_URL = "https://prsjobs.cs83.my.salesforce.com/services/data/v46.0/"
    BASE_URL_LOGIN = "https://login.salesforce.com/services/oauth2/"

    logging.info("Using production Jobscience app instance")


# Load Synonyms:
# SYNONYMS: dict = marketplace_helpers.loadSynonyms(construction=True)


def testConnection(auth, companyID):
    try:

        if auth.get("refresh_token"):

            if isValidToken(auth, companyID):
                return Callback(True, 'Logged in successfully', auth)

            else:
                callback: Callback = refreshToken(auth, companyID)

        else:
            callback: Callback = login(auth)

        if not callback.Success:
            raise Exception("Connection test failed")

        return Callback(True, 'Logged in successfully', callback.Data)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


def isValidToken(auth, companyID):
    url = BASE_URL
    method = "GET"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth.get('access_token'),
        'cache-control': 'no-cache',
        'Cookie': 'inst=APP_3X'
    }
    response = marketplace_helpers.sendRequest(url, method, headers, {})
    if response.ok:
        return True
    else:
        return False


def refreshToken(auth, companyID):
    # get new access token:
    try:

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            'Cookie': "inst=APP_3X",
            'cache-control': "no-cache"
        }

        body = {
            'grant_type': "refresh_token",
            'client_id': "3MVG9I5UQ_0k_hTlh64o5U2MnkGkPmYj_xkMpFkEi0tIJXl_CGhXpux_w5khN6pvnNd.IH6Yvo82ZAcRystWE",
            'client_secret': "972A46C725406EE38D971409A1509EF164B100A9B8B42CA4C39AB3952B65A215",
            'refresh_token': auth.get('refresh_token')
        }

        resp = json.loads(
            requests.request("POST", (BASE_URL_LOGIN + "token?"), headers=headers,
                             data=body).text)
        auth['access_token'] = resp.get('access_token')

        saveAuth_callback: Callback = crm_services.updateByType(CRM.Jobscience, auth, companyID)
        if not saveAuth_callback.Success:
            raise Exception(saveAuth_callback.Message)

        return Callback(True, 'New access token', {
            "access_token": auth.get("access_token"),
            "refresh_token": auth.get("refresh_token")
        })

    except Exception as exc:
        db.session.rollback()
        helpers.logError("Marketplace.CRM.Bullhorn.retrieveRestToken() ERROR: " + str(exc))
        return Callback(False, "Failed to retrieve CRM tokens. Please check login information")


# NOTE: For production, we need to change the domain name (currently it is pointing to sandbox)

def login(auth):
    try:

        authCopy = dict(auth)

        headers = {'Content-Type': 'application/json'}

        access_token_url = (BASE_URL_LOGIN + "token?") + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=" + helpers.getDomain(3000) + "/dashboard/marketplace/Jobscience" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + authCopy.get("code")

        # get the access token and refresh token
        response = requests.post(access_token_url, headers=headers)

        # if response.status_code == 200:
        #     print("Login to Jobscience Successful")
        # else:
        #     print("Login to Jobscience Unsuccessful")

        if not response.ok:
            raise Exception(response.text)

        result_body = json.loads(response.text)

        return Callback(True, 'Logged in successfully', {"access_token": result_body.get('access_token'),
                                                         "refresh_token": result_body.get("refresh_token")})

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(auth, companyID):  # QUESTION: Purpose of companyID param?
    try:
        # Attempt logout
        logout_url = BASE_URL_LOGIN + "revoke?token=" + auth.get("access_token")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + auth.get("access_token"),
            'cache-control': "no-cache"
        }

        response = marketplace_helpers.sendRequest(logout_url, "get", headers, {})
        # if response.status_code == 200:
        #     print("Disconnect from Jobscience Successful")
        # else:
        #     print("Disconnect from Jobscience Unsuccessful")

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.logout() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCandidateSkills(access_token, conversation: Conversation, contactID) -> Callback:
    try:
        skills = conversation.get("skills")

        entries = []
        counter = 0

        for skill in skills:
            entry = {
                "attributes": {"type": "ts2__Skill__c", "referenceId": "ref" + str(counter + 5)},  # Add unique ID
                "ts2__Contact__c": contactID,
                "ts2__Skill_Name__c": skill
            }
            entries.append(entry)
            counter = counter + 1

        body = {
            "records": entries  # Add entries to request body
        }

        # Send query
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "composite/tree/ts2__Skill__c/")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertCandidateSkills() ERROR: " + str(exc))
        return Callback(False, str(exc))


# BUG: Education not showing, may need to add to EDU object [~]

def convertDate(date: str):
    if date is None:
        return ""
    return datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")


def insertCandidate(access_token, conversation: Conversation) -> Callback:
    try:
        if conversation.get("owner") is None:
            owner_name = "Anonymous"
        else:
            owner_name = conversation.get("owner").Firstname

        name = (conversation.get("name") or " ").split(" ")
        body = {
            "FirstName": helpers.getListValue(name, 0, "") or "FIRST_DEFAULT",
            "LastName": helpers.getListValue(name, 1, "") or "LAST_DEFAULT",  # LastName is only required field
            "Title": conversation.get("preferredJobTitle"),
            "MobilePhone": conversation.get('mobile') or " ",
            "MailingCity": conversation.get("city") or "",
            "email": conversation.get("email") or " ",
            "ts2__Date_Available__c": convertDate(conversation.get("availability")),  # TODO CHECK
            "ts2__Education__c": "",  # Needs to be in a separate post request
            "ts2__Desired_Salary__c": conversation.get("annualSalary"),
            "ts2__Desired_Hourly__c": conversation.get("dayRate"),
            "ts2__LinkedIn_Profile__c": conversation.get("CandidateLinkdinURL"),
            "Attributes__c": conversation.get("skills"),
            "ts2__Job_Type__c": conversation.get("preferredJobType"),
            # "ts2__Text_Resume__c": "", # TODO: Link this with File upload
            "Internal_Notes__c": "Owner: " + owner_name + ",  Last Updated: " + datetime.now().strftime("%I:%M%p on %B %d, %Y"),
            "RecordTypeId": "0120O000000tJIAQA2"
        }

        # Send query
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "sobjects/Contact/")

        # Will need returned ID for adding skills

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)
        return_body = json.loads(sendQuery_callback.Data.text)

        # Insert candidate skills
        if conversation.get("skills") is not None:
            insertCandidateSkills_callback: Callback = insertCandidateSkills(
                access_token, conversation, return_body.get("id"))

            if not insertCandidateSkills_callback.Success:  # Needs to  fetch the Account ID
                raise Exception(insertCandidateSkills_callback.Message)
        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def updateCandidate(auth, conversation: Conversation, companyID) -> Callback:
    try:

        # Compose body keywords:

        body = {
            "Title": conversation.get("preferredJobTitle"),
            "MobilePhone": conversation.get('mobile'),
            "MailingCity": conversation.get("city"),
            "email": conversation.get("email"),
            "ts2__Date_Available__c": convertDate(conversation.get("availability")),  # TODO CHECK
            "ts2__Education__c": "",  # Needs to be in a separate post request
            "ts2__Desired_Salary__c": conversation.get("annualSalary"),
            "ts2__Desired_Hourly__c": conversation.get("dayRate"),
            "ts2__LinkedIn_Profile__c": conversation.get("CandidateLinkdinURL"),
            "Attributes__c": conversation.get("skills"),
            "ts2__Job_Type__c": conversation.get("preferredJobType"),
            "Internal_Notes__c": crm_services.additionalCandidateNotesBuilder(
                {
                    "preferredJobTitle": conversation.get("preferredJobTitle"),
                    "preferredJobType": conversation.get("preferredJobType"),
                    "yearsExperience": conversation.get("yearsExperience"),
                    "skills": conversation.get("skills")
                }, conversation.get("selectedSolutions")
            ),
        }

        # Note: So that we dont replace existing data will nothing
        filtered_body = {}
        for propertyKey, propertyValue in body.items():
            if propertyValue is not None:
                if type(propertyValue) is str and str(propertyValue).strip():
                    filtered_body[propertyKey] = propertyValue
                elif type(propertyValue) is int and propertyValue != 0:
                    filtered_body[propertyKey] = propertyValue

        # print("Updating Candidate: {}".format(filtered_body))
        logging.info("Updating Candidate: {}".format(filtered_body))

        # send query
        sendQuery_callback: Callback = sendQuery(auth, "patch", filtered_body,
                                                 "sobjects/Contact/" + str(conversation.get("id")))

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.updateCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClient(auth, conversation: Conversation) -> Callback:
    try:
        # Insert client company
        insertCompany_callback: Callback = insertCompany(auth, conversation)
        if not insertCompany_callback.Success:
            raise Exception(insertCompany_callback.Message)

        # Insert client account
        insertClient_callback: Callback = insertClientContact(auth, conversation,
                                                              insertCompany_callback.Data.get("id"))
        if not insertClient_callback.Success:  # Needs to  fetch the Account ID
            raise Exception(insertClient_callback.Message)

        return Callback(True, insertClient_callback.Message)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(access_token, conversation: Conversation, prsCompanyID) -> Callback:
    try:
        # New client contact details

        if conversation.get("firstName") == "":
            conversation["firstName"] = "DEFAULT_FIRST"
        if conversation.get("lastName") == "":
            conversation["lastName"] = "DEFAULT_LAST"

        body = {
            "FirstName": conversation.get("firstName"),  # TODO: Decide on default values
            "LastName": conversation.get("lastName"),
            "MobilePhone": conversation.get("mobile", ""),
            "MailingCity": conversation.get("city"),
            # check number of emails and submit them
            "email": conversation.get("email"),
            "AccountId": prsCompanyID
        }

        # Perform insert
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "sobjects/Contact/")
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCompany(auth, conversation: Conversation) -> Callback:
    try:

        body = {
            "Name": conversation.get("companyName")
        }

        sendQuery_callback: Callback = sendQuery(auth, "post", body, "sobjects/Account/")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


def fetchSkillsForCandidateSearch(list_of_contactIDs: list, list_of_skills, access_token, test=None):
    records_to_return = []
    for i in range(0, len(list_of_contactIDs), 500):
        # Need set of contact ID's returned from searchCandidates()
        if i + 500 <= len(list_of_contactIDs):
            query_segment = ",".join(list_of_contactIDs[i:i + 500])
        else:
            query_segment = ",".join(list_of_contactIDs[i:len(list_of_contactIDs)])
        # Add LIKE statements:
        like_string = ""
        for skill in list_of_skills:

            like_string += "+AND+("

            # TODO: Generate synonyms:
            synonyms = (skill,)
            for synonym in synonyms:
                like_string += "ts2__Skill_Name__c+LIKE+" + "'%" + synonym + "%'+or+"

            # Remove final or:
            if len(synonyms) > 0:
                like_string = like_string[:-4]

            like_string += ")"
        if test:
            # Note: This assumes at least one skill is given
            sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                     "SELECT+ts2__Skill_Name__c,ts2__Last_Used__c,ts2__Contact__c" +
                                                     "+FROM+ts2__Skill__c+WHERE+" +
                                                     "ts2__Contact__c+IN+(" + query_segment + ")" + "+LIMIT+1000")

        else:
            # Note: This assumes at least one skill is given
            sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                 "SELECT+ts2__Skill_Name__c,ts2__Last_Used__c,ts2__Contact__c" +
                                                 "+FROM+ts2__Skill__c+WHERE+" +
                                                 "ts2__Contact__c+IN+(" + query_segment + ")" + like_string + "+LIMIT+1000")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        candidate_skills_fetch = json.loads(sendQuery_callback.Data.text)
        records_to_return += candidate_skills_fetch['records']

    # print("CURRENT LENGTH IS: {}".format(len(records_to_return)))
    return records_to_return


def getShortLists(access_token) -> Callback:
    # TODO: Fetch all short list links
    # https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v37.0/query/?q=SELECT+name,ts2__r_contact__c,ts2__Status__c+from+ts2__s_UserListLink__c

    sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                             "SELECT+name+from+ts2__s_UserList__c")

    if not sendQuery_callback.Success:
        raise Exception(sendQuery_callback.Message)

    shortlist_fetch = json.loads(sendQuery_callback.Data.text)
    shortlists = shortlist_fetch['records']
    shortlist_entries = []
    for shortlist in shortlists:
        # print("The shortlist is {}".format(shortlist))
        shortlist_entries.append({"name": shortlist.get("Name"),
                                  "url": shortlist.get("attributes").get("url")})

    return Callback(True, sendQuery_callback.Message, shortlist_entries)


def searchCandidatesByShortlist(access_token, conversation) -> Callback:
    # print(conversation)
    #
    # print("THIS HAS BEEN CALLED...")
    # exit(0)
    # TODO: Fetch all short list links
    # https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v37.0/query/?q=SELECT+name,ts2__r_contact__c,ts2__Status__c+from+ts2__s_UserListLink__c

    sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                             "SELECT+name,ts2__r_contact__c,ts2__Status__c,ts2__r_user_list__c+from+ts2__s_UserListLink__c+WHERE+ts2__r_user_list__c+=+"+ "'" + conversation.get("shortlist_id").replace('/services/data/v46.0/sobjects/ts2__s_UserList__c/', '') + "'")

    if not sendQuery_callback.Success:
        raise Exception(sendQuery_callback.Message)

    shortlist_fetch = json.loads(sendQuery_callback.Data.text)
    shortlists = shortlist_fetch['records']

    contact_ids = []
    result = []
    records = []
    for shortlist_link in shortlists:
        if "/services/data/v46.0/sobjects/ts2__s_UserList__c/" + shortlist_link.get("ts2__r_user_list__c") == conversation.get("shortlist_id"):
            # print("Shortlist: {}".format(shortlist_link))
            contact_ids.append("'" + shortlist_link.get('ts2__r_contact__c') + "'")
    # print("Number of matches: {}".format(len(contact_ids)))
    # print("Exiting...")
    # #exit(0)
    # print("Number of contacts to retrieve: {}".format(len(contact_ids)))

    for i in range(0, len(contact_ids), 500):
        # Need set of contact ID's returned from searchCandidates()
        if i + 500 <= len(contact_ids):
            query_segment = ",".join(contact_ids[i:i + 500])
        else:
            query_segment = ",".join(contact_ids[i:len(contact_ids)])

        query = "WHERE+X18_Digit_ID__c+IN+(" + query_segment + ")"
        # print(query)
        # TODO: Fetch associated candidate object
        # https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v37.0/sobjects/Contact/0030O0000232s7FQAQ
        # print("Should be fetching contacts...")
        sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                             "SELECT+X18_Digit_ID__c,ID,Name,Title,email,MobilePhone,MailingCity," +
                                             "ts2__Desired_Salary__c,ts2__Date_Available__c,ts2__Years_of_Experience__c,ts2__Desired_Hourly__c,Min_Basic__c," +
                                             "ts2__EduDegreeName1__c,ts2__Education__c+from+Contact+" + query)  # Limit set to 10 TODO: Customize

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        records += json.loads(sendQuery_callback.Data.text)['records']
        # print("Number of records retrieved: {}".format(len(records)))

    list_of_contactIDs = []

    # <-- CALL SKILLS SEARCH -->
    for record in records:
        # print(record)
        list_of_contactIDs.append("'" + record.get("Id") + "'")

        # Fetch associated candidate skills
    skills = conversation.get("skills")

    if type(skills) != list:
        skills = []

    candidate_skills = []
    if len(records) > 0:
        candidate_skills = fetchSkillsForCandidateSearch(list_of_contactIDs, skills, access_token, test=True)

    # <-- CALL SKILLS SEARCH -->
    # print("Number of records: {}".format(len(records)))
    for record_num, record in enumerate(records):
        has_skills: bool = False

        skills_string = ""
        counter = 0
        for skill in candidate_skills:
            # Cap skills at 5:

            if skill.get("ts2__Contact__c") == record.get("Id") and counter < 5:
                counter += 1
                has_skills = True

                skills_string += skill.get("ts2__Skill_Name__c")
                if skill.get("ts2__Last_Used__c") is not None:
                    skills_string += "(" + skill.get("ts2__Last_Used__c") + "), "  # Display year of use
                else:
                    skills_string += ""

        if has_skills:
            result.append(databases_services.createPandaCandidate(id=record.get("X18_Digit_ID__c", str(record_num)),
                                                                      name=record.get("Name"),
                                                                      email=record.get("Email"),
                                                                      mobile=record.get("MobilePhone"),
                                                                      location=record.get("MailingCity"),
                                                                      skills=skills_string,
                                                                      linkdinURL=None,
                                                                      availability=record.get(
                                                                          "ts2__Date_Available__c") or
                                                                                   "Not Specified",
                                                                      currentJobTitle=record.get("Title"),
                                                                      education=record.get('ts2__EduDegreeName1__c'),
                                                                      yearsExperience=record.get(
                                                                          'ts2__Years_of_Experience__c'),
                                                                      desiredSalary=record.get(
                                                                          'ts2__Desired_Salary__c') or
                                                                                    record.get(
                                                                                        'ts2__Desired_Hourly__c') or
                                                                                    record.get('Min_Basic__c', 0),
                                                                      currency=Currency("GBP"),
                                                                      source="Jobscience"))

    return Callback(True, sendQuery_callback.Message, result)


# Need to make it so that if only skill is provided, a search can still be done.
def searchCandidates(access_token, conversation) -> Callback:
    list_of_contactIDs = []

    try:

        # Create filter:

        # Fetch contacts who are candidates and are active"
        query = "WHERE+RecordType.Name+IN+('Candidate')+AND+ts2__People_Status__c+IN+('Active', 'Live')+AND+"

        # Filter on location:
        if conversation.get('location') is not None:
            query += populateFilter(conversation.get('location'), "MailingCity", quote_wrap=True, SOQL_type="=")

        # Filter on job title:
        if conversation.get('preferredJotTitle') is not None:
            query += populateFilter("%" + conversation.get('preferredJotTitle') + "%", "Title", quote_wrap=True,
                                    SOQL_type="+LIKE+")
        else:
            # Set job title to skills value:
            # query += populateFilter("%" + conversation.get('skills').split(" ")[0] + "%", "Title", quote_wrap=True,
            #                         SOQL_type="+LIKE+")
            pass

        # Filter on desired salary:
        if conversation.get('desiredSalary') is not None:
            query += populateFilter(conversation.get("desiredSalary", 0), "ts2__Desired_Salary__c", quote_wrap=True,
                                    SOQL_type="=")

        # Filter on Job Type:
        # Need to map permanent -> Perm and temporary -> Temp
        if conversation.get('jobType'):
            job_type = "Perm" if conversation.get("jobType") == "permanent" else "Temp"
            query += populateFilter(job_type, "Employment_Type__c", quote_wrap=True,
                                    SOQL_type="=")

        query = query[:-5]

        # TODO: Differentiate between hourly and salary
        sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                 "SELECT+X18_Digit_ID__c,ID,Name,Title,email,MobilePhone,MailingCity," +
                                                 "ts2__Desired_Salary__c,ts2__Date_Available__c,ts2__Years_of_Experience__c,ts2__Desired_Hourly__c,Min_Basic__c," +
                                                 "ts2__EduDegreeName1__c,ts2__Education__c+from+Contact+" + query +
                                                 "+LIMIT+500")  # Limit set to 10 TODO: Customize

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        candidate_fetch = json.loads(sendQuery_callback.Data.text)
        records = candidate_fetch['records']

        # Iterate through candidates
        result = []

        #  Iterative generalisation:
        while len(records) < 500:
            # send query
            sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                     "SELECT+X18_Digit_ID__c,ID,Name,Title,email,MobilePhone,MailingCity," +
                                                     "ts2__Desired_Salary__c,ts2__Date_Available__c,ts2__Years_of_Experience__c,ts2__Desired_Hourly__c,Min_Basic__c," +
                                                     "ts2__EduDegreeName1__c,ts2__Education__c+from+Contact+" + query +
                                                     "+LIMIT+500")  # Limit set to 10 TODO: Customize
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            # get query result
            return_body = json.loads(sendQuery_callback.Data.text)

            # TODO: Call skills fetch here
            if return_body["records"]:

                # add the candidates to the records
                records = records + list(return_body["records"])

                # remove duplicate records
                seen = set()
                new_l = []
                for d in records:
                    t = tuple(d.items())
                    if str(t) not in seen:
                        seen.add(str(t))
                        new_l.append(d)

                records = []
                for l in new_l:
                    records.append(dict(l))

            # remove the last (least important filter)
            query = "AND".join(query.split("AND")[:-1])

            # if no filters left then stop
            if not query:
                break

        # <-- CALL SKILLS SEARCH -->
        for record in records:
            list_of_contactIDs.append("'" + record.get("Id") + "'")

        # Fetch associated candidate skills
        skills = conversation.get("skills")

        if type(skills) != list:
            skills = skills.split(" ")

        candidate_skills = []
        if len(candidate_fetch['records']) > 0:
            candidate_skills = fetchSkillsForCandidateSearch(list_of_contactIDs, skills, access_token)

        # <-- CALL SKILLS SEARCH -->
        # print("Number of records: {}".format(len(records)))
        for record_num, record in enumerate(records):
            has_skills: bool = False

            skills_string = ""
            counter = 0
            for skill in candidate_skills:
                # Cap skills at 5:

                if skill.get("ts2__Contact__c") == record.get("Id") and counter < 5:
                    counter += 1
                    has_skills = True

                    skills_string += skill.get("ts2__Skill_Name__c")
                    if skill.get("ts2__Last_Used__c") is not None:
                        skills_string += "(" + skill.get("ts2__Last_Used__c") + "), "  # Display year of use
                    else:
                        skills_string += ""

            if has_skills:
                result.append(databases_services.createPandaCandidate(id=record.get("X18_Digit_ID__c", str(record_num)),
                                                                      name=record.get("Name"),
                                                                      email=record.get("Email"),
                                                                      mobile=record.get("MobilePhone"),
                                                                      location=record.get("MailingCity"),
                                                                      skills=skills_string,
                                                                      linkdinURL=None,
                                                                      availability=record.get(
                                                                          "ts2__Date_Available__c") or
                                                                                   "Not Specified",
                                                                      preferredJobTitle=record.get("Title"),
                                                                      education=record.get('ts2__EduDegreeName1__c'),
                                                                      yearsExperience=record.get(
                                                                          'ts2__Years_of_Experience__c'),
                                                                      desiredSalary=record.get(
                                                                          'ts2__Desired_Salary__c') or
                                                                                    record.get(
                                                                                        'ts2__Desired_Hourly__c') or
                                                                                    record.get('Min_Basic__c', 0),
                                                                      currency=Currency("GBP"),
                                                                      source="Jobscience"))

        return Callback(True, sendQuery_callback.Message, result)
    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def populateFilter(value, string, quote_wrap, SOQL_type: str):
    if value:
        if quote_wrap:
            value = "'" + value + "'"
            return string + SOQL_type + value + "+AND+"
        else:
            # Convert date format:
            new_date = datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
        return string + SOQL_type + new_date + "+AND+"

    return ""


def searchJobs(access_token, conversation) -> Callback:
    try:
        query = "WHERE+"

        # Job must be open:
        query += populateFilter("Open", "ts2__Status__c", quote_wrap=True, SOQL_type="=")
        # Add (%) for LIKE operator...
        query += populateFilter("%" + conversation.get('preferredJobTitle') + "%", "Name", quote_wrap=True, SOQL_type="+LIKE+")

        query += populateFilter(conversation.get('city'), "ts2__Location__c", quote_wrap=True, SOQL_type="=")

        # query += populateFilter(conversation.get('employmentType'),
        #                         "ts2__Employment_Type__c", quote_wrap=True, SOQL_type="=")

        query += populateFilter(conversation.get('skills'), "ts2__Job_Tag__c", quote_wrap=True, SOQL_type="+LIKE+")

        # NOTE: Have these changed

        query += populateFilter(conversation.get('JobStartDate'), "ts2__Estimated_Start_Date__c", quote_wrap=False,
                                SOQL_type=">")

        # query += populateFilter(DT.JobEndDate, "ts2__Estimated_End_Date__c", quote_wrap=False)

        query = query[:-5]  # To remove final +AND

        # NOTE: Properties to return must be stated, no [*] operator
        sendQuery_callback: Callback = sendQuery(
            access_token, "get", {},
            "SELECT+Name,ts2__Employment_Type__c,RecordType.Name,Rate_Type__c,ts2__Text_Description__c," +
            "ts2__Max_Salary__c,ts2__Max_Pay_Rate__c,ts2__Min_Pay_Rate__c,ts2__Location__c,ts2__Job_Tag__c," +
            "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c+" +
            query + "+LIMIT+500")  # Return 500 records at most
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        job_fetch = json.loads(sendQuery_callback.Data.text)
        records = job_fetch['records']
        #  Iterative generalisation:
        while len(job_fetch['records']) < 200:
            # send query
            sendQuery_callback: Callback = sendQuery(
                access_token, "get", {},
                "SELECT+Name,ts2__Employment_Type__c,RecordType.Name,Rate_Type__c,ts2__Text_Description__c," +
                "ts2__Max_Salary__c,ts2__Max_Pay_Rate__c,ts2__Min_Pay_Rate__c,ts2__Location__c,ts2__Job_Tag__c," +
                "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c+" +
                query + "+LIMIT+100")  # Return 500 records at most
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            # get query result
            return_body = json.loads(sendQuery_callback.Data.text)

            # TODO: Call skills fetch here
            if return_body["records"]:

                # Add the candidates to the records
                records = records + list(return_body["records"])

                # remove duplicate records
                seen = set()
                new_l = []
                for d in records:
                    t = tuple(d.items())
                    if str(t) not in seen:
                        seen.add(str(t))
                        new_l.append(d)

                records = []
                for l in new_l:
                    records.append(dict(l))

            # remove the last (least important filter)
            query = "AND".join(query.split("AND")[:-1])

            # if no filters left - stop
            if not query:
                break

        # Iterate through jobs
        result = []
        for record in records:
            # Add jobs to database
            result.append(databases_services.createPandaJob(id=record.get('id'),
                                                            title=record.get('Name'),
                                                            desc=record.get('ts2__Text_Description__c'),
                                                            location=record.get('ts2__Location__c'),
                                                            type=record.get('RecordType').get('Name'),
                                                            salary=record.get('ts2__Max_Salary__c') or
                                                                   record.get('ts2__Max_Pay_Rate__c') or
                                                                   record.get('ts2__Min_Pay_Rate__c') or 0,
                                                            essentialSkills=record.get('ts2__Job_Tag__c'),
                                                            yearsRequired=0,
                                                            startDate=record.get('ts2__Estimated_Start_Date__c'),
                                                            endDate=record.get('ts2__Estimated_End_Date__c'),
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            source="Jobscience"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobsCustomQuery(access_token, companyID, query, fields=None) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(
            access_token, "get", "{}", "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                                       "ts2__Max_Salary__c,ts2__Location__c,ts2__Job_Tag__c," +
                                       "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c" +
                                       "+WHERE+ts2__Max_Salary__c+NOt+IN+(NULL)+LIMIT+500")  # Limit set to 500
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


# TODO: Match to Bullhorn and trigger from chatbot

def getAllCandidates(access_token, companyID, fields=None) -> Callback:
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(access_token, "get", "{}", "SELECT+Name,email,MobilePhone+from+Contact+" +
                                                 "WHERE+RecordType.Name+IN+('Candidate')+LIMIT+10")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def getAllJobs(access_token, companyID, fields=None) -> Callback:  # TODO: See this triggered.
    try:

        sendQuery_callback: Callback = sendQuery(
            access_token, "get", "{}", "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                                       "ts2__Max_Salary__c,ts2__Location__c,ts2__Job_Tag__c," +
                                       "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c" +
                                       "+WHERE+ts2__Max_Salary__c+NOt+IN+(NULL)+LIMIT+10")
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


# TODO: Clean up this sendquery and enacpsulate refresh token logic:
def sendQuery(auth, method, body, query, simple=False, c_id=None):
    try:

        url = buildUrl(query, method)

        # set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth.get('access_token'),
            'cache-control': 'no-cache',
            'Cookie': 'inst=APP_3X'
        }

        response = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))

        if response.status_code == 401:  # wrong rest token

            refreshToken(auth, None)
            headers['Authorization'] = "Bearer " + auth.get('access_token')

            # Try again
            response = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))

        if not response.ok:
            raise Exception(response.text + ". Query could not be sent")

        return Callback(True, "Query was successful", response)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(query, method, simple=False, c_id=None):
    url = BASE_URL
    if method == "post":
        url = url + query  # Append object to be edited
    elif method == "get":
        if simple:
            url = url + "/sobjects/Contact/" + c_id
        else:
            url = url + "query/?q=" + query  # Append SOQL query
    elif method == 'patch':
        url = url + query
    return url


# TODO
def uploadFile(auth, storedFileInfo: StoredFileInfo):
    pass
