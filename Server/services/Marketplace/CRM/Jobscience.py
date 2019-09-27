import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, StoredFile, StoredFileInfo
from services import databases_services, stored_file_services
from services.Marketplace import marketplace_helpers
from utilities import helpers
from services.Marketplace.CRM import crm_services

CLIENT_ID = os.environ['JOBSCIENCE_CLIENT_ID']
CLIENT_SECRET = os.environ['JOBSCIENCE_CLIENT_SECRET']


# TODO CHECKLIST:
# [1] SearchJobs [DATA RETURNED]
# [2] SearchCandidates [DATA RETURNED]
# [3] Complete iterative generalisation for candidate search[CHECK]
# [4] Complete iterative generalisation for job search[CHECK]
# [4.5] Fix and check insert functions [CHECK]

# --- URGENT ----
# [4.6] Add job type (perm or temp) []
# [4.7] Get primitive file upload working []
# --- URGENT ---

# [5] Clean & refactor []
# [6] TEST []
# [7] IMPROVE []
# [8] TRY WITH PROD SALESFORCE []


def testConnection(auth, companyID):
    try:
        callback: Callback = login(auth)

        if not callback.Success:
            raise Exception("Testing failed")

        return Callback(True, 'Logged in successfully', callback.Data)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


# NOTE: For production, we need to change the domain name (currently it is pointing to sandbox)

def login(auth):
    try:

        authCopy = dict(auth)

        headers = {'Content-Type': 'application/json'}

        access_token_url = "https://login.salesforce.com/services/oauth2/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=" + helpers.getDomain(3000) + "/dashboard/marketplace/Jobscience" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + authCopy.get("code")

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)
        print(access_token_request.status_code)
        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)
        print(result_body)

        return Callback(True, 'Logged in successfully', result_body.get('access_token'))  # No refresh token currently

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(access_token, companyID):  # QUESTION: Purpose of companyID param?
    try:
        # Attempt logout
        logout_url = "https://salesforce.com/services/oauth2/revoke?token=" + access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache"
        }

        response = marketplace_helpers.sendRequest(logout_url, "get", headers, {})

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

        # NOTE: Should require on front-end that a full name is provided --> reduce data inconsistency
        name = (conversation.get("name") or " ").split(" ")
        body = {
            "FirstName": helpers.getListValue(name, 0, "") or "FIRST_DEFAULT",
            "LastName": helpers.getListValue(name, 1, "") or "LAST_DEFAULT",  # LastName is only required field
            "Title": conversation.get("preferredJobTitle"),
            "phone": conversation.get('mobile') or " ",
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
            "sirenum__General_Comments__c": crm_services.additionalCandidateNotesBuilder(
                {
                    "preferredJobTitle": conversation.get("preferredJobTitle"),
                    "preferredJobType": conversation.get("preferredJobType"),
                    "yearsExperience": conversation.get("yearsExperience"),
                    "skills": conversation.get("skills")
                }, conversation.get("selectedSolutions")
            ),
            "RecordTypeId": "0120O000000tJIAQA2"  # ID for a candidate person record type
        }

        # Send query
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "sobjects/Contact/")

        # Will need returned ID for adding skills

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)
        return_body = json.loads(sendQuery_callback.Data.text)

        # Insert candidate skills
        print("THE CANDIDATE SKILLS:")
        print(conversation.get("skills"))
        if conversation.get("skills") is not None:
            insertCandidateSkills_callback: Callback = insertCandidateSkills(
                access_token, conversation, return_body.get("id"))

            if not insertCandidateSkills_callback.Success:  # Needs to  fetch the Account ID
                raise Exception(insertCandidateSkills_callback.Message)
        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))


def uploadFile(auth, storedFile: StoredFile):  # ISSUE: NO CURRENT API OPTION FOR RESUME UPLOAD
    print("UPLOAD FILE NOT SUPORTED")


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
        print(conversation)

        body = {
            "FirstName": conversation.get("firstName"),  # TODO: Decide on default values
            "LastName": conversation.get("lastName"),
            "phone": conversation.get("mobile", ""),
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


def fetchSkillsForCandidateSearch(list_of_contactIDs: list, list_of_skills, access_token):
    # Need set of contact ID's returned from searchCandidates()
    query_segment = ",".join(list_of_contactIDs)
    skills = str((', '.join("'" + skill + "'" for skill in list_of_skills)))

    sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                             "SELECT+ts2__Skill_Name__c,ts2__Contact__c+FROM+ts2__Skill__c+WHERE+" +
                                             "ts2__Contact__c+IN+(" + query_segment + ")+LIMIT+200")

    if not sendQuery_callback.Success:
        raise Exception(sendQuery_callback.Message)

    candidate_skills_fetch = json.loads(sendQuery_callback.Data.text)
    print(candidate_skills_fetch)
    return candidate_skills_fetch['records']


# Need to make it so that if only skill is provided, a search can still be done.
def searchCandidates(access_token, conversation) -> Callback:
    # Should add employment type (permanent or temporary)
    list_of_contactIDs = []

    try:

        # Create filter:
        query = "WHERE+RecordType.Name+IN+('Candidate')+AND+"  # Fetch contacts who are candidates"
        query += populateFilter(conversation.get('location'), "MailingCity", quote_wrap=True, SOQL_type="=")
        query += populateFilter("%" + conversation.get('preferredJotTitle') + "%", "Title", quote_wrap=True,
                                SOQL_type="+LIKE+")
        query += populateFilter(conversation.get("desiredSalary", 0), "ts2__Desired_Salary__c", quote_wrap=True,
                                SOQL_type="=")

        query = query[:-5]

        print("Query is:")
        print(query)
        # print("Exiting...")
        # exit(0)

        # TODO: Differentiate between hourly and salary
        sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                 "SELECT+X18_Digit_ID__c,ID,Name,Title,email,phone,MailingCity," +
                                                 "ts2__Desired_Salary__c,ts2__Desired_Hourly__c," +
                                                 "ts2__EduDegreeName1__c,ts2__Education__c,Attributes__c+from+Contact+" + query +
                                                 "+LIMIT+200")  # Limit set to 10 TODO: Customize

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)
        print("QUERY HAS BEEN SENT")
        candidate_fetch = json.loads(sendQuery_callback.Data.text)
        records = candidate_fetch['records']
        # Iterate through candidates
        result = []
        # TODO: Fetch job title
        print("NUMBER OF RECORDS RETRIEVED: ", len(candidate_fetch['records']))

        # <-- CALL SKILLS SEARCH -->
        # for record in candidate_fetch['records']:
        #     list_of_contactIDs.append("'" + record.get("Id") + "'")
        #
        # # Fetch associated candidate skills
        # skills = conversation.get("skills")
        # candidate_skills = []
        # if len(candidate_fetch['records']) > 0:
        #     candidate_skills = fetchSkillsForCandidateSearch(list_of_contactIDs, skills.split(","), access_token)
        # <-- CALL SKILLS SEARCH -->

        #  Iterative generalisation:
        while len(candidate_fetch['records']) < 20:
            # send query
            sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                     "SELECT+X18_Digit_ID__c,ID,Name,Title,email,phone,MailingCity," +
                                                     "ts2__Desired_Salary__c,ts2__Desired_Hourly__c," +
                                                     "ts2__EduDegreeName1__c,ts2__Education__c,Attributes__c+from+Contact+" + query +
                                                     "+LIMIT+200")  # Limit set to 10 TODO: Customize
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            # get query result
            return_body = json.loads(sendQuery_callback.Data.text)

            # TODO: Call skills fetch here
            if return_body["records"]:
                print("Records length:", str(len(records)))
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
            print("QUERY IS: ", query)

            # if no filters left - stop
            if not query:
                break

        # <-- CALL SKILLS SEARCH -->
        for record in records:
            list_of_contactIDs.append("'" + record.get("Id") + "'")

        # Fetch associated candidate skills
        skills = conversation.get("skills")
        candidate_skills = []
        if len(candidate_fetch['records']) > 0:
            candidate_skills = fetchSkillsForCandidateSearch(list_of_contactIDs, skills.split(","), access_token)
        # <-- CALL SKILLS SEARCH -->

        for record in records:
            print("SALARY FOUND: ", record.get('ts2__Desired_Salary__c'))
            print("SALARY FOUND: ", record.get('ts2__Desired_Hourly__c'))
            skills_string = ""
            for skill in candidate_skills:
                print(skill.get("ts2__Skill_Name__c"))
                if skill.get("ts2__Contact__c") == record.get("Id"):
                    skills_string += skill.get("ts2__Skill_Name__c") + ", "
            skills_string += record.get("Attributes__c", "")  # Merging skills and job title together...
            # Ignoring skills string for now

            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("Name"),
                                                                  email=record.get("Email"),
                                                                  mobile=record.get("Phone"),
                                                                  location=record.get("MailingCity"),
                                                                  skills=skills_string,
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=record.get("Title"),
                                                                  education=record.get('ts2__EduDegreeName1__c'),
                                                                  yearsExperience=0,  # When 0 -> No skills displayed
                                                                  desiredSalary=record.get('ts2__Desired_Salary__c') or
                                                                                record.get('ts2__Desired_Hourly__c', 0),
                                                                  currency=Currency("GBP"),
                                                                  source="Jobscience"))
        print("RETURNING RECORDS ...")
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

        # Add (%) for LIKE operator...
        query += populateFilter("%" + conversation.get('jobTitle') + "%", "Name", quote_wrap=True, SOQL_type="+LIKE+")

        query += populateFilter(conversation.get('city'), "ts2__Location__c", quote_wrap=True, SOQL_type="=")

        # query += populateFilter(conversation.get('employmentType'),
        #                         "ts2__Employment_Type__c", quote_wrap=True, SOQL_type="=")

        query += populateFilter(conversation.get('skills'), "ts2__Job_Tag__c", quote_wrap=True, SOQL_type="+LIKE+")

        # NOTE: Have these changed

        query += populateFilter(conversation.get('JobStartDate'), "ts2__Estimated_Start_Date__c", quote_wrap=False,
                                SOQL_type=">")

        # query += populateFilter(DT.JobEndDate, "ts2__Estimated_End_Date__c", quote_wrap=False)

        query = query[:-5]  # To remove final +AND
        print("QUERY IS: ", query)

        # NOTE: Properties to return must be stated, no [*] operator
        sendQuery_callback: Callback = sendQuery(
            access_token, "get", {}, "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
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
                access_token, "get", {}, "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                                         "ts2__Max_Salary__c,ts2__Max_Pay_Rate__c,ts2__Min_Pay_Rate__c,ts2__Location__c,ts2__Job_Tag__c," +
                                         "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c+" +
                                         query + "+LIMIT+100")  # Return 500 records at most
            if not sendQuery_callback.Success:
                raise Exception(sendQuery_callback.Message)

            # get query result
            return_body = json.loads(sendQuery_callback.Data.text)

            # TODO: Call skills fetch here
            if return_body["records"]:
                print("Records length:", str(len(records)))
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
            print("QUERY IS: ", query)

            # if no filters left - stop
            if not query:
                break

        # Iterate through jobs
        result = []
        for record in records:
            print("NEW JOB RECORD")
            print(record.get('Name'))
            print(record.get('ts2__Max_Pay_Rate__c'))
            print(record.get('ts2__Min_Pay_Rate__c'))
            # Add jobs to database
            result.append(databases_services.createPandaJob(id=record.get('id'),
                                                            title=record.get('Name'),
                                                            desc=record.get('ts2__Text_Description__c'),
                                                            location=record.get('ts2__Location__c'),
                                                            type=record.get('ts2__Job_Tag__c'),
                                                            salary=record.get('ts2__Max_Salary__c') or
                                                                   record.get('ts2__Max_Pay_Rate__c') or
                                                                   record.get('ts2__Min_Pay_Rate__c'),

                                                            essentialSkills=record.get('ts2__Job_Tag__c'),
                                                            yearsRequired=0,
                                                            startDate=record.get('ts2__Estimated_Start_Date__c'),
                                                            endDate=record.get('ts2__Estimated_End_Date__c'),
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            source="Jobscience"))
        print("FINISHED")

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
        sendQuery_callback: Callback = sendQuery(access_token, "get", "{}", "SELECT+Name,email,phone+from+Contact+" +
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


def sendQuery(access_token, method, body, query):
    try:
        url = buildUrl(query, method)

        # set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache",
            'Cookie': 'inst=APP_3X'
        }
        print("URL OF THE SEND QUERY")
        print(url)
        print("HEADERS OF SEND QUERY")
        print(headers)
        response = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
        if not response.ok:
            raise Exception(response.text + ". Query could not be sent")

        elif not response.ok:
            raise Exception("Rest url for query is incorrect")

        return Callback(True, "Query was successful", response)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(query, method):

    url = "https://prsjobs.cs83.my.salesforce.com/services/data/v46.0/"
    if method == "post":
        url = url + query  # Append object to be edited
    elif method == "get":
        url = url + "query/?q=" + query  # Append SOQL query
    return url


# TODO
def uploadFile(auth, storedFileInfo: StoredFileInfo):
    print("ATTEMPT FILE UPLOAD")
