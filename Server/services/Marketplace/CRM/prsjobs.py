import base64
import json
import os
from datetime import datetime

import requests
from sqlalchemy_utils import Currency

from models import Callback, Conversation, db, CRM as CRM_Model, StoredFile
from services import databases_services, stored_file_services
from services.Marketplace import marketplace_helpers
from services.Marketplace.CRM import crm_services

from utilities import helpers
from utilities.enums import DataType as DT, Period, CRM

# TODO: 26/07/2019
# --> Match logout&login to Bullhorn [CHECK]
# --> Add remaining inserts [CHECK]
# --> Call functions from chatbot []
# --> Comment issues & unique features to prsjobs API []

CLIENT_ID = os.environ['PRSJOBS_CLIENT_ID']
CLIENT_SECRET = os.environ['PRSJOBS_CLIENT_SECRET']


def testConnection(auth, companyID):
    try:
        print("ATTEMPTING LOGIN")
        print("auth: ")
        print(auth)
        callback: Callback = login(auth)

        if not callback.Success:
            raise Exception("Testing failed")

        return Callback(True, 'Logged in successfully', callback.Data)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.testConnection() ERROR: " + str(exc))
        return Callback(False, str(exc))


def login(auth):
    try:
        authCopy = dict(auth)
        print("LOGGING IN HERE")
        headers = {'Content-Type': 'application/json'}

        access_token_url = "https://test.salesforce.com/services/oauth2/token?" + \
                           "&grant_type=authorization_code" + \
                           "&redirect_uri=" + helpers.getDomain() + "/dashboard/marketplace/PRSJobs" + \
                           "&client_id=" + CLIENT_ID + \
                           "&client_secret=" + CLIENT_SECRET + \
                           "&code=" + authCopy.get("code")

        # get the access token and refresh token
        access_token_request = requests.post(access_token_url, headers=headers)
        print(access_token_request)
        if not access_token_request.ok:
            raise Exception(access_token_request.text)

        result_body = json.loads(access_token_request.text)
        print("WHERE IS THE CODE?")
        print(result_body)

        # Logged in successfully

        # <-- TESTING QUERIES -->
        # GENERIC QUERY: sendQuery(result_body.get("access_token"), "get", "SELECT+name+from+Account")
        # FETCH ALL JOBS:
        # getAllJobs(result_body.get("access_token"), None, None)
        # FETCH ALL CANDIDATES: getAllCandidates(result_body.get("access_token"), None, None)
        # SEARCH ALL JOBS:
        # searchJobs(result_body.get("access_token"), None, None, None)
        # SEARCH ALL CANDIDATES:
        # searchCandidates(result_body.get("access_token"), None, None, None)
        # INSERT A CANDIDATE:
        # insertCandidate(result_body.get("access_token"), None)
        # INSERT A  CLIENT COMPANY:
        # insertCompany(result_body.get("access_token"), None);

        return Callback(True, 'Logged in successfully', result_body.get('access_token'))  # No refresh token currently

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prmjobs.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(access_token, companyID):  # QUESTION: Purpose of companyID param?
    print("<-- ATTEMTING TO LOGOUT -->")
    try:
        # Attempt logout
        logout_url = "https://test.salesforce.com/services/oauth2/revoke?token=" + access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache"
        }

        r = marketplace_helpers.sendRequest(logout_url, "get", headers, {})

        print(r.status_code)
    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.logout() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertCandidate(access_token, conversation: Conversation) -> Callback:
    print("Should be attempting candidate insert...")
    try:
        name = (conversation.Name or " ").split(" ")
        body = {
            "FirstName": "dummy", #helpers.getListValue(name, 0, " "),
            "LastName":  "dummy", #helpers.getListValue(name, 1, "NONE"), #  Requires last name entry (need agreed value for None)
            "phone": conversation.PhoneNumber or " ",
            "MailingCity": "TEMP_CITY",#"".join(conversation.Data.get('keywordsByDataType').get(DT.CandidateLocation.value['name'], [" "])),
            "email": conversation.Email or " ",
            "ts2__Education__c": "TEMP_EDUCATION", #conversation.Data.get('keywordsByDataType').get(DT.CandidateEducation.value['name'], [""]),
            "ts2__Desired_Salary__c": str(crm_services.getSalary(conversation, DT.CandidateDesiredSalary, Period.Annually)),
            "RecordTypeId": "0120O000000tJIAQA2"  # ID for a candidate person
            }

        print("BODY IS")
        print(body)
        # Attempt Dummy Insert:
        print("<-- INSERT CANDIDATE -->")
        sendQuery_callback: Callback = sendQuery(access_token, "post", body, "sobjects/Contact/")
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return Callback(True, sendQuery_callback.Data.text)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.Bullhorn.insertCandidate() ERROR: " + str(exc))
        return Callback(False, str(exc))

    # Populate JSON fields:
    # 1 convert fields
    # 2 Add record type as candidate
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': "Bearer " + access_token,
    #     'accept-encoding': "gzip, deflate",
    #     'content-length': "35",
    #     'Connection': "keep-alive",
    #     'cache-control': "no-cache"
    # }
    # payload = "{\n\t\"LastName\": \"ANOTHER_TEST\"\n\t\n}"
    # url = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v36.0/sobjects/Contact/"
    # response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.status_code)
    # # TODO:
    # # (1) print in JSON format
    # # (2) Link to sendquery
    # # (3) Add fields
    # # Insert record
    # #sendQuery(access_token, "post", body, "sobjects/Contact/")


def uploadFile(auth, storedFile: StoredFile): # TODO: NO CURRENT SOLUTION
    print("UPLOAD FILE")


def insertClient(auth, conversation: Conversation) -> Callback:
    try:
        print("<-- ATTEMPTING CLIENT INSERT -->")
        print("Auth passed in is: ")
        print(auth)
        # get query url
        insertCompany_callback: Callback = insertCompany(auth, conversation)
        if not insertCompany_callback.Success:
            raise Exception(insertCompany_callback.Message)
        print("STUFF RETURNED")
        print(insertCompany_callback.Message)
        print(insertCompany_callback.Data)
        insertClient_callback: Callback = insertClientContact(auth, conversation,
                                                              insertCompany_callback.Data.get("id"))
        if not insertClient_callback.Success:                  # Needs to  fetch the Account ID
            raise Exception(insertClient_callback.Message)

        return Callback(True, insertClient_callback.Message)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.insertClient() ERROR: " + str(exc))
        return Callback(False, str(exc))


def insertClientContact(access_token, conversation: Conversation, prsCompanyID) -> Callback:
    try:
        print("INSERT CONTACT FOR CLIENT")
        # New candidate details
        emails = conversation.Data.get('keywordsByDataType').get(DT.ClientEmail.value['name'], [" "])

        # TODO: Ensure name is split into first and last as required by API (no name option)
        body = {
            "FirstName": conversation.Name or " ",
            "LastName": "NoLastName",
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
        helpers.logError("Marketplace.CRM.PRSJobs.insertClientContact() ERROR: " + str(exc))
        return Callback(False, str(exc))



def insertCompany(auth, conversation: Conversation) -> Callback:
    try:
        print("INSERT COMPANY")

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
        helpers.logError("Marketplace.CRM.prsjobs.insertCompany() ERROR: " + str(exc))
        return Callback(False, str(exc))


# TODO: Add filters
def searchCandidates(access_token, companyID, conversation, fields=None) -> Callback:


    # PLAN:
    # 1) Retrieve candidates
    # 2) Iterate through candidates
    # 3) Add candidates to database

    # Fields
    # ID, Name, Email, Mobile, Address, Primary Skills, Status, Education, Day Rate, Salary
    try:

        # Retrieve candidates
        print("<-- SEARCH CANDIDATES -->")
        sendQuery_callback: Callback = sendQuery(access_token, "get", "{}", "SELECT+Name,email,phone,MailingCity,ts2__Desired_Salary__c" +
                                    ",ts2__Desired_Hourly__c,ts2__EduDegreeName1__c,ts2__Education__c+from+Contact" +
                                    "+WHERE+RecordType.Name+IN+('Candidate')+LIMIT+500") # Limit set to 10 TODO: Customize

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        candidate_fetch = json.loads(sendQuery_callback.Data.text)

        print(candidate_fetch['records'])


        result = []
        for record in candidate_fetch['records']:
            print("<-- New Record -->")
            print("Name: " + str(record.get('Name')))
            print("Email:" + str(record.get('Email')))
            print("Phone: " + str(record.get('Phone')))
            print("Mailing Address: " + str(record.get('MailingCity')))
            print("Education: " + str(record.get('ts2__EduDegreeName1__c')))
            print("Desired Salary: " + str(record.get('ts2__Desired_Salary__c')))

            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("Name"),
                                                                  email=record.get("Email"),
                                                                  mobile=record.get("Phone"),
                                                                  location=record.get("MailingCity"),
                                                                  skills="Engineering",  # Set temporarily to engineering
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education=record.get('ts2__EduDegreeName1__c'),
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get('ts2__Desired_Salary__c'),
                                                                  currency=Currency("GBP"),
                                                                  payPeriod=Period("Annually"),
                                                                  source="prsjobs"))
        return Callback(True, sendQuery_callback.Message, result)
    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))

# TODO: Add filters
def searchJobs(access_token, companyID, conversation, fields=None) -> Callback:
    print("Recieved search request: ")
    print("Conversation is:")
    print(conversation)
    # PLAN:
    # 1) Retrieve jobs with filters from conversation
    # 2) Iterate through jobs
    # 3) Add jobs to database

    # Fields
    # ID, Title, Description, Address, Salary, Skills, Start date, end data
    try:
        # Retrieve jobs
        print("<-- SEARCH JOBS -->")
        # send query (note that properties to return must be stated, no [*] operator)
        sendQuery_callback: Callback = sendQuery(
            access_token, "get", "{}", "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                                       "ts2__Max_Salary__c,ts2__Location__c,ts2__Job_Tag__c," +
                                       "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c" +
                                       "+WHERE+ts2__Max_Salary__c+NOt+IN+(NULL)+LIMIT+5")
        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        job_fetch = json.loads(sendQuery_callback.Data.text)

        print(job_fetch['records'])

        # Iterate through jobs
        result = []
        for record in job_fetch['records']:
            print("<-- New Record -->")
            print(record)
            print("Name: " + str(record.get('Name')))
            print("Description:" + str(record.get('ts2__Text_Description__c')))
            print("Salary: " + str(record.get('ts2__Max_Salary__c')))
            print("Rate of pay: " + str(record.get('Rate_Type__c')))
            print("Start Date: " + str(record.get('ts2__Estimated_Start_Date__c')))
            print("End Date: " + str(record.get('ts2__Estimated_End_Date__c')))
            print("Location " + str(record.get('ts2__Location__c')))
            print("Job Tag " + str(record.get('ts2__Job_Tag__c')))
            # Add jobs to database
            result.append(databases_services.createPandaJob(id=record.get('id'),
                                                            title=record.get('Name'),
                                                            desc=record.get('ts2__Text_Description__c'),
                                                            location=record.get('ts2__Location__c'),
                                                            type=record.get('ts2__Job_Tag__c'),
                                                            salary=record.get('ts2__Max_Salary__c'),
                                                            essentialSkills=record.get('Name'),
                                                            desiredSkills=None,
                                                            yearsRequired=0,
                                                            startDate=record.get('ts2__Estimated_Start_Date__c'),
                                                            endDate=record.get('ts2__Estimated_End_Date__c'),
                                                            linkURL=None,
                                                            currency=Currency("GBP"),
                                                            payPeriod=Period("Annually"),  # May need to derive this
                                                            source="prsjobs"))

        return Callback(True, sendQuery_callback.Message, result)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))

# TODO: Match to Bullhorn and trigger from chatbot
def searchJobsCustomQuery(auth, companyID, query, fields=None) -> Callback: # TODO
    print("SEARCH JOBS CUSTOM QUERY")

# TODO: Match to Bullhorn and trigger from chatbot


def getAllCandidates(access_token, companyID, fields=None) -> Callback:
    print("GET ALL CANDIDATES HAS BEEN TRIGGERED")
    try:
        # send query
        sendQuery_callback: Callback = sendQuery(access_token, "get", "{}", "SELECT+Name,email,phone+from+Contact+" +
                                                 "WHERE+RecordType.Name+IN+('Candidate')+LIMIT+10")

        if not sendQuery_callback.Success:
            raise Exception(sendQuery_callback.Message)

        return_body = json.loads(sendQuery_callback.Data.text)

        return Callback(True, sendQuery_callback.Message, return_body)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))

# TODO: Match to Bullhorn and trigger from chatbot


def getAllJobs(access_token, companyID, fields=None) -> Callback:  # TODO: See this triggered.
    print("GET ALL JOBS HAS BEEN TRIGGERED")
    try:

        # send query (note that properties to return must be stated, no [*] operator)
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
        helpers.logError("Marketplace.CRM.prsjobs.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def produceRecruiterValueReport(crm: CRM_Model, companyID) -> Callback: # TODO
    print("PRODUCE RECRUITER VALUE REPORT")


def sendQuery(access_token, method, body, query):
    try:
        # get url
        url = buildUrl(query, method)
        print(query)
        print(method)
        print(url)
        print(method)
        print("CONSTRUCTED URL IS: " + url)

        # set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache"
        }
        print(headers)

        # set headers
        #headers = {'Content-Type': 'application/json'}

        r = marketplace_helpers.sendRequest(url, method, headers, json.dumps(body))
        if not r.ok:
            raise Exception(r.text + ". Query could not be sent")

        elif not r.ok:
            raise Exception("Rest url for query is incorrect")

        return Callback(True, "Query was successful", r)

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(query, method):
    url = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v46.0/"
    if method == "post":
        url = url + query  # Append object to be edited
    elif method == "get":
        url = url + "query/?q=" + query  # Append SOQL query
    return url