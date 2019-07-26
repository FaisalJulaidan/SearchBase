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

        # Logged in successfully

        # <-- TESTING QUERIES -->
        # GENERIC QUERY: sendQuery(result_body.get("access_token"), "get", "SELECT+name+from+Account")
        # FETCH ALL JOBS:
        # getAllJobs(result_body.get("access_token"), None, None)
        # FETCH ALL CANDIDATES: getAllCandidates(result_body.get("access_token"), None, None)
        # SEARCH ALL JOBS: searchJobs(result_body.get("access_token"), None, None, None)
        # SEARCH ALL CANDIDATES: searchCandidates(result_body.get("access_token"), None, None, None)
        # INSERT A CANDIDATE:
        # insertCandidate(result_body.get("access_token"), None)
        return Callback(True, 'Logged in successfully', {"refresh_token": ""})  # No refresh token currently

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prmjobs.login() ERROR: " + str(exc))
        return Callback(False, str(exc))


def logout(access_token, companyID):

    try:
        print("LOGOUT") # TODO
        # Attempt logout
        logout_url = "https://test.salesforce.com/services/oauth2/revoke?token=" + access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache"
        }

        r = marketplace_helpers.sendRequest(logout_url, "get", headers, {})

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.logout() ERROR: " + str(exc))
        return Callback(False, str(exc))



def insertCandidate(access_token, conversation: Conversation) -> Callback:
    # Attempt Dummy Insert:
    print("<-- INSERT CANDIDATE -->")

    # Populate JSON fields:
    # 1 convert fields
    # 2 Add record type as candidate
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + access_token,
        'accept-encoding': "gzip, deflate",
        'content-length': "35",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    payload = "{\n\t\"LastName\": \"ANOTHER_TEST\"\n\t\n}"
    url = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v36.0/sobjects/Contact/"
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    # TODO:
    # (1) print in JSON format
    # (2) Link to sendquery
    # (3) Add fields
    # Insert record
    #sendQuery(access_token, "post", body, "sobjects/Contact/")


def uploadFile(auth, storedFile: StoredFile):
    print("UPLOAD FILE")


def insertClient(auth, conversation: Conversation) -> Callback:
    print("INSERT CLIENT")


def insertClientContact(auth, conversation: Conversation, bhCompanyID) -> Callback:
    print("INSERT CONTACT FOR CLIENT")


def insertCompany(auth, conversation: Conversation) -> Callback:
    print("INSERT COMPANY")



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
        candidate_fetch = sendQuery(access_token, "get", "{}", "SELECT+Name,email,phone,MailingAddress,ts2__Desired_Salary__c" +
                                    ",ts2__Desired_Hourly__c,ts2__EduDegreeName1__c,ts2__Education__c+from+Contact" +
                                    "+WHERE+RecordType.Name+IN+('Candidate')+LIMIT+10") # Limit set to 10 TODO: Customize
        print(candidate_fetch)

        result = []
        for record in candidate_fetch:
            print("<-- New Record -->")
            print("Name: " + str(record.get('Name')))
            print("Email:" + str(record.get('Email')))
            print("Phone: " + str(record.get('Phone')))
            print("Mailing Address: " + str(record.get('MailingAddress')))
            print("Education: " + str(record.get('ts2__EduDegreeName1__c')))
            print("Desired Salary: " + str(record.get('ts2__Desired_Salary__c')))

            result.append(databases_services.createPandaCandidate(id=record.get("id", ""),
                                                                  name=record.get("Name"),
                                                                  email=record.get("Email"),
                                                                  mobile=record.get("Phone"),
                                                                  location=record.get("MailingAddress"),
                                                                  skills="",
                                                                  linkdinURL=None,
                                                                  availability=record.get("status"),
                                                                  jobTitle=None,
                                                                  education=record.get('ts2__EduDegreeName1__c'),
                                                                  yearsExperience=0,
                                                                  desiredSalary=record.get('ts2__Desired_Salary__c'),
                                                                  currency=Currency("GBP"),
                                                                  payPeriod=Period("Annually"),
                                                                  source="prsjobs"))

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.searchCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobs(access_token, companyID, conversation, fields=None) -> Callback:
    # PLAN:
    # 1) Retrieve jobs
    # 2) Iterate through jobs
    # 3) Add jobs to database

    # Fields
    # ID, Title, Description, Address, Salary, Skills, Start date, end data
    try:
        # Retrieve jobs
        print("<-- SEARCH JOBS -->")
        job_fetch = sendQuery(access_token, "get", "{}", "SELECT+Name,Rate_Type__c,ts2__Text_Description__c," +
                              "ts2__Max_Salary__c,ts2__Location__c,ts2__Job_Tag__c," +
                              "ts2__Estimated_Start_Date__c,ts2__Estimated_End_Date__c+from+ts2__Job__c" +
                              "+WHERE+ts2__Max_Salary__c+NOt+IN+(NULL)+LIMIT+10")  # Limit set to 10 TODO: Customize
        print(job_fetch)

        # Iterate through jobs
        result = []
        for record in job_fetch:
            print("<-- New Record -->")
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


    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.searchJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def searchJobsCustomQuery(auth, companyID, query, fields=None) -> Callback:
    print("SEARCH JOBS CUSTOM QUERY")


def getAllCandidates(access_token, companyID, fields=None) -> Callback:

    try:
        # send query
        sendQuery(access_token, "get", "{}", "SELECT+Name,email,phone+from+Contact+" +
                  "WHERE%20RecordType.Name%20IN%20%28%27Candidate%27%29+LIMIT+10")  # Limit set to 10 TODO: Customize
        print("<-- GET ALL CANDIDATES -->")

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.getAllCandidates() ERROR: " + str(exc))
        return Callback(False, str(exc))




def getAllJobs(access_token, companyID, fields=None) -> Callback:
    try:
        # send query
        sendQuery(access_token, "get", "{}", "SELECT+Name+from+Contact+LIMIT+10")  # Limit set to 10 TODO: Customize
        print("<--- GET ALL JOBS --->")

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.getAllJobs() ERROR: " + str(exc))
        return Callback(False, str(exc))


def produceRecruiterValueReport(crm: CRM_Model, companyID) -> Callback:
    print("PRODUCE RECRUITER VALUE REPORT")


def sendQuery(access_token, method, body, query):
    try:
        # get url
        url = buildUrl(query, method)
        print("CONSTRUCTED URL IS: " + url)

        # set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + access_token,
            'cache-control': "no-cache"
        }

        # test query

        r = marketplace_helpers.sendRequest(url, method, headers, body)
        print("REQUEST STATUS: " + str(r))
        print(r.json().get("records"))
        if method == "get":
            return r.json().get("records")

    except Exception as exc:
        helpers.logError("Marketplace.CRM.prsjobs.sendQuery() ERROR: " + str(exc))
        return Callback(False, str(exc))


def buildUrl(query, method):
    url = "https://prsjobs--jsfull.cs83.my.salesforce.com/services/data/v46.0/"
    if method == "post":
        url += query  # Initial URL
    elif method == "get":
        url = url + "query/?q=" + query  # Add query
    return url
