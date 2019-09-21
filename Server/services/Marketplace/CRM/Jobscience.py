import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, StoredFile
from services import databases_services
from services.Marketplace import marketplace_helpers
from utilities import helpers
from utilities.enums import DataType as DT, Period

CLIENT_ID = os.environ['JOBSCIENCE_CLIENT_ID']
CLIENT_SECRET = os.environ['JOBSCIENCE_CLIENT_SECRET']


# ISSUE: USING REFRESH TOKEN []
# Session timeout set to 24 hours
# 'If you use refresh tokens, your code should first try the regular API call, and if you get a 4xx result,
# try using the refresh token to get a new session token, and if that fails, then you've been kicked out,
# and the user needs to re-authenticate to continue. If you don't use refresh tokens,
# you can skip the middle step, obviously'.
# Will receive 401 for expired access token -> will then need to fetch new one using the refresh token
# Note: that skill may have to be added separately [CHECK]
# NOTE: Before use in dev or prod, the callback url must be changed both in items.js and on the Salesforce dashboard


# CHECKLIST
# [1] SearchJobs [DATA RETURNED]
# [2] SearchCandidates [DATA RETURNED]
# [3] Merge skills with title and validate [DATA RETURNED]
# [3] Clean & refactor []
# [4] TEST []
# [5] IMPROVE []
# [6] TRY WITH PROD SALESFORCE []


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

        access_token_url = "https://test.salesforce.com/services/oauth2/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=" + helpers.getDomain(3000) + "/dashboard/marketplace/Jobscience" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + authCopy.get("code")

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)

        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)

        return Callback(True, 'Logged in successfully', result_body.get('access_token'))  # No refresh token currently

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(access_token, companyID):  # QUESTION: Purpose of companyID param?
    try:
        # Attempt logout
        logout_url = "https://test.salesforce.com/services/oauth2/revoke?token=" + access_token
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
        skills = conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], [" "])

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

def insertCandidate(access_token, conversation: Conversation) -> Callback:
    try:
        salary = conversation.Data.get('keywordsByDataType').get(DT.CandidateAnnualDesiredSalary.value['name'], [""])
        avg_sal = 0
        if salary[0] != "":
            # NOTE: Splitting salary
            salary_splitted = salary[0].split(" ")
            low_and_high = salary_splitted[0].split("-")

            # print("MINIMAL DESIRED SALARY: ")
            min_sal = low_and_high[0]
            # print(min_sal)

            # print("MAX DESIRED SALARY: ")
            max_sal = low_and_high[1]
            # print(max_sal)

            # print("AVERAGE DESIRED SALARY: ")
            avg_sal = str(0.5 * (int(min_sal) + int(max_sal)))
            # print(avg_sal)

        # NOTE: Should require on front-end that a full name is provided --> reduce data inconsistency
        name = (conversation.Name or " ").split(" ")
        body = {
            "FirstName": helpers.getListValue(name, 0, "") or "FIRST_DEFAULT",
            "LastName": helpers.getListValue(name, 1, "") or "LAST_DEFAULT",  # LastName is only required field
            "Title": "".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateJobTitle.value['name'],
                                                                             [" "])),
            "phone": conversation.PhoneNumber or " ",
            "MailingCity": "".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'],
                                                                                   [""])),
            # "ts2__Desired_Salary__c": conversation.Data.get(DT.CandidateDailyDesiredSalary.value['name']),
            "email": conversation.Email or " ",
            "ts2__Education__c": "",  # Needs to be in a separate post request
            "ts2__Desired_Salary__c": avg_sal,
            "ts2__LinkedIn_Profile__c": "".join(conversation.Data.get('keywordsByDataType').get(
                DT.CandidateLinkdinURL.value['name'],
                [""])),
            "Attributes__c": "; ".join(
                conversation.Data.get('keywordsByDataType').get(DT.CandidateSkills.value['name'], [" "])),
            "RecordTypeId": "0120O000000tJIAQA2"  # ID for a candidate person record type
        }

        # Send query
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "sobjects/Contact/")

        # Will need returned ID for adding skills

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)
        return_body = json.loads(sendQuery_callback.Data.text)

        # Insert candidate skills
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
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])

        body = {
            "FirstName": conversation.Name or "FIRST_DEFAULT",  # TODO: Decide on default values
            "LastName": conversation.Name or "DEFAULT",
            "phone": conversation.PhoneNumber or " ",
            "MailingCity": "".join(conversation.Data.get('keywordsByDataType').get(
                DT.ClientLocation.value['name'], [" "])),
            # check number of emails and submit them
            "email": emails[0],
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
            "Name": " ".join(conversation.Data.get('keywordsByDataType').get(
                DT.CompanyName.value['name'],
                ["Undefined Company - TSB"]))
        }

        sendQuery_callback: Callback = sendQuery(auth, "post", body, "sobjects/Account/")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Jobscience.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


# TODO: First get other info, then get the skills and filter them - may be slow
# NOTE: JOB title may need to query CRM Skills field
# TODO: Check speed of this approach
# NOTE: This needs to be a query!
def fetchSkillsForCandidateSearch(list_of_contactIDs: list, list_of_skills, access_token):
    # [1] Need set of contact ID's returned from searchCandidates()
    # [2] Use a IN(CID1,CID2,...,CIDx) to retrieve all associated skills
    query_segment = ",".join(list_of_contactIDs)
    skills = str((', '.join("'" + skill + "'" for skill in list_of_skills)))
    # print(query_segment)
    sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                             "SELECT+ts2__Skill_Name__c,ts2__Contact__c+FROM+ts2__Skill__c+WHERE+" +
                                             "ts2__Contact__c+IN+(" + query_segment + ")+AND+ts2__Skill_Name__c+IN+(" +
                                             skills + ")+LIMIT+20")


    if not sendQuery_callback.Success:
        raise Exception(sendQuery_callback.Message)

    candidate_skills_fetch = json.loads(sendQuery_callback.Data.text)
    print(candidate_skills_fetch)
    return candidate_skills_fetch['records']

# jobtitle, location, category, experience
# NOTE: Bullhorn is using AND always
# Need to make it so that if only skill is provided, a search can still be done.
def searchCandidates(access_token, conversation) -> Callback:

    #########################################################
    print("HERE")
    print(conversation.get("skills"))
    print("-------------------------")
    #exit(0)
    #########################################################

    # Should add employment type (permanent or temporary)
    list_of_contactIDs = []

    try:
        # TODO: Add more filters, perhaps with a hierarchy of what to search on (maybe skills more important than
        # education) --> Could be set by user and sent with the conversation.
        # Note: Date will need to be reversed for comparison, also dates could be compared with a range rather than
        # requiring an exact match --> unrealistic
        query = "WHERE+"
        print("Search candidates got to here...")

        # populate filter

        # NOTE: Currently, closest thing to jobtype
        query += populateFilter(conversation.get('location'), "MailingCity", quote_wrap=True, SOQL_type="=")
        query += populateFilter("%"+conversation.get('preferredJotTitle')+"%",
                                "Title", quote_wrap=True, SOQL_type="+LIKE+")

        query = query[:-4]
        query += "+AND+RecordType.Name+IN+('Candidate')"  # Fetch contacts who are candidates

        print("Query is:")
        print(query)


        # TODO: Differentiate between hourly and salary
        sendQuery_callback: Callback = sendQuery(access_token, "get", {},
                                                 "SELECT+X18_Digit_ID__c,ID,Name,Title,email,phone,MailingCity," +
                                                 "ts2__Desired_Salary__c,ts2__Desired_Hourly__c," +
                                                 "ts2__EduDegreeName1__c,ts2__Education__c+from+Contact+" + query +
                                                 "+LIMIT+200")  # Limit set to 10 TODO: Customize

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)
        print("QUERY HAS BEEN SENT")
        candidate_fetch = json.loads(sendQuery_callback.Data.text)

        # Iterate through candidates
        result = []
        # TODO: Fetch job title
        for record in candidate_fetch['records']:
            list_of_contactIDs.append("'" + record.get("Id") + "'")

        # Fetch associated candidate skills
        skills = conversation.get("skills")

        candidate_skills = fetchSkillsForCandidateSearch(list_of_contactIDs, skills.split(","), access_token)

        # NOTE: Possibly add restriction on how many skills to show
        for record in candidate_fetch['records']:
            print("SALARY FOUND: ", record.get('ts2__Desired_Salary__c'))
            print("SALARY FOUND: ", record.get('ts2__Desired_Hourly__c'))
            skills_string = ""
            for skill in candidate_skills:
                if skill.get("ts2__Contact__c") == record.get("Id"):
                    skills_string += skill.get("ts2__Skill_Name__c") + ", "
            skills_string += record.get("Title")  # Merging skills and job title together...
            #skills_string = skills_string[:-1]
            # NOTE: Serious review of efficiency is needed also should try to find years experience field
            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("Name"),
                                                                  email=record.get("Email"),
                                                                  mobile=record.get("Phone"),
                                                                  location=record.get("MailingCity"),
                                                                  skills=skills_string,  # Need to fetch from skills
                                                                  # Set temporarily to engineering
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=record.get("Title"),
                                                                  education=record.get('ts2__EduDegreeName1__c'),
                                                                  yearsExperience=0,  # When 0 -> No skills displayed
                                                                  desiredSalary=record.get('ts2__Desired_Salary__c', 0),
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

def checkFilter(keywords, dataType: DT, string, quote_wrap, exact: bool):
    if keywords.get(dataType.value["name"]):
        altered_list = []
        for word in keywords[dataType.value["name"]]:  # NOTE: Wrap string types in single quotes
            if quote_wrap:
                word = "'" + word + "'"
                altered_list.append(word)
            else:
                # Convert date format:
                new_date = datetime.strptime(word, "%m/%d/%Y").strftime("%Y-%m-%d")
                altered_list.append(new_date)

        # TODO: Multi-values, AND instead of OR?
        # if exact:
        #     return string + "=" + "".join(altered_list) + "+and+"
        # else:
        return string + "=" + "".join(altered_list) + "+or+"
    return ""


# TODO: CONVERT TO BULLHORN STYLE:
def searchJobs(access_token, conversation) -> Callback:
    # print("CONVERSATION IS: ")
    # print(conversation)
    print(conversation)
    # keywords = conversation['keywordsByDataType']  # BUG: THIS HAS BEEN REMOVED
    # keywords = {'Job Location': ['London'], 'Job Title': ['chef'], 'Job Type': []}
    # print("keywords: ")
    # print(keywords)

    try:
        query = "WHERE+"

        # Add (%) for LIKE operator...
        query += populateFilter("%"+conversation.get('jobTitle')+"%", "Name", quote_wrap=True, SOQL_type="+LIKE+")

        query += populateFilter(conversation.get('city'), "ts2__Location__c", quote_wrap=True, SOQL_type="=")

        query += populateFilter(conversation.get('employmentType'),
                                "ts2__Employment_Type__c", quote_wrap=True, SOQL_type="LIKE")

        query += populateFilter(conversation.get('skills'), "ts2__Job_Tag__c", quote_wrap=True, SOQL_type="+LIKE+")

        # NOTE: Have these changed

        # query += populateFilter(DT.JobStartDate, "ts2__Estimated_Start_Date__c", quote_wrap=False)

        # query += populateFilter(DT.JobEndDate, "ts2__Estimated_End_Date__c", quote_wrap=False)

        query = query[:-5]  # To remove final +or
        print("QUERY IS: ")
        print(query)

        # NOTE: No years experience property available

        # send query NOTE: Properties to return must be stated, no [*] operator
        sendQuery_callback: Callback = sendQuery(
            access_token, "get", {}, "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                                       "ts2__Max_Salary__c,ts2__Location__c,ts2__Job_Tag__c," +
                                       "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c+" +
                                       query + "+LIMIT+500")  # Return 500 records at most
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        job_fetch = json.loads(sendQuery_callback.Data.text)

        # Iterate through jobs
        result = []
        for record in job_fetch['records']:
            # Add jobs to database
            result.append(databases_services.createPandaJob(id=record.get('id'),
                                                            title=record.get('Name'),
                                                            desc=record.get('ts2__Text_Description__c'),
                                                            location=record.get('ts2__Location__c'),
                                                            type=record.get('ts2__Job_Tag__c'),
                                                            salary=record.get('ts2__Max_Salary__c'),
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
            'cache-control': "no-cache"
        }
        print("BODY OF THE SEND QUERY")
        print(url)
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
    url = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v46.0/"
    if method == "post":
        url = url + query  # Append object to be edited
    elif method == "get":
        url = url + "query/?q=" + query  # Append SOQL query
    return url
