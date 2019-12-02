from datetime import datetime, timedelta

from sqlalchemy_utils import Currency

from models import db, Role, Company, Assistant, Conversation, Database, Candidate, CRM, Appointment, Job, Messenger
from services import user_services, flow_services, auto_pilot_services, appointment_services
from utilities import helpers, enums


# Generates dummy data for testing
def generate():
    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com', StripeID='cus_00000000000000', SubID='sub_00000000000000',
                           Active=True, AccessAssistants=True, AccessCampaigns=True, AccessAutoPilot=True,
                           AccessDatabases=True, AccessAppointments=True))

    db.session.add(Company(Name='Sabic', URL='ff.com', StripeID='cus_DbgKupMRLNYXly', Active=True,
                           AccessAssistants=True, AccessCampaigns=True, AccessAutoPilot=True,
                           AccessDatabases=True, AccessAppointments=True))

    # Get Companies
    aramco: Company = Company.query.filter(Company.Name == "Aramco").first()
    sabic: Company = Company.query.filter(Company.Name == "Sabic").first()

    config = {
        "restrictedCountries": [],
        "chatbotPosition": "Right"
    }

    # Create and validate a flow for an assistant
    # Create Assistants for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there",
                         TopBarText="Aramco Bot", SecondsUntilPopup=1,
                         Config=config, Active=True, Company=aramco)

    flow = {
        "groups": [
            {
                "blocks": [
                    {
                        "Content": {
                            "answers": [
                                {
                                    "action": "Go To Next Block",
                                    "afterMessage": "",
                                    "blockToGoID": "1Nto4DL8B",
                                    "id": "WZXp26mdL",
                                    "keywords": [
                                        "python"
                                    ],
                                    "score": 2,
                                    "text": "low"
                                },
                                {
                                    "action": "Go To Next Block",
                                    "afterMessage": "",
                                    "blockToGoID": "1Nto4DL8B",
                                    "id": "godj9rom5",
                                    "keywords": [],
                                    "score": 5,
                                    "text": "medium"
                                },
                                {
                                    "action": "Go To Next Block",
                                    "afterMessage": "",
                                    "blockToGoID": "1Nto4DL8B",
                                    "id": "E6phkGY5u",
                                    "keywords": [],
                                    "score": 8,
                                    "text": "high"
                                }
                            ],
                            "text": "what?"
                        },
                        "DataType": enums.DataType.CandidateSkills.name,
                        "ID": "8EDEBiDHa",
                        "SkipAction": "End Chat",
                        "SkipBlockToGoID": None,
                        "SkipText": "Skip!",
                        "Skippable": False,
                        "StoreInDB": True,
                        "Type": "Question"
                    },
                    {
                        "Type": "Solutions",
                        "StoreInDB": False,
                        "Skippable": True,
                        "SkipText": "Not found what you're looking for?",
                        "SkipAction": "Go To Next Block",
                        "SkipBlockToGoID": None,
                        "DataType": enums.DataType.NoType.name,
                        "Content": {
                            "showTop": 5,
                            "action": "Go To Next Block",
                            "blockToGoID": None,
                            "afterMessage": "123",
                            "databaseType": "Candidates"
                        },
                        "ID": "1Nto4DL8B"
                    }
                ],
                "description": "The best group",
                "id": "tisd83f4",
                "name": "group 1"
            }
        ]
    }

    # Insert candidate flow
    candidate_insert_flow = {
        "groups": [
            {
                "blocks": [
                    # Candidate NAME
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateName.name,
                     "Content": {"text": "Can you please provide us with your name?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the name",
                                 "keywords": []},
                     "ID": "001"},
                    # Candidate EMAIL
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateEmail.name,
                     "Content": {"text": "Can you please provide us with email?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the email",
                                 "keywords": []},
                     "ID": "002"},
                    # Candidate LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateCity.name,
                     "Content": {"text": "What city are you in?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "003"},
                    # Candidate PHONE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateMobile.name,
                     "Content": {"text": "What is your phone number?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the phone number",
                                 "keywords": []},
                     "ID": "004"},
                    # Candidate EDUCATION
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'None', "DataType": "CandidateEducation",
                    #  "Content": {"text": "What is your education?", "blockToGoID": "006",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                    #              "keywords": []},
                    #  "ID": "005"},
                    # # Candidate SALARY
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'None', "DataType": "CandidateDesiredSalary",
                    #  "Content": {"text": "What is your annual desired salary?", "blockToGoID": "007",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the salary",
                    #              "keywords": []},
                    #  "ID": "006"},
                    # # Candidate JOB TITLE
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'None', "DataType": "JobTitle",
                    #  "Content": {"text": "What job title are you looking for?", "blockToGoID": "008",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the title",
                    #              "keywords": []},
                    #  "ID": "007"},
                    # # Candidate LINKDIN URL
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'None', "DataType": "CandidateLinkdinURL",
                    #  "Content": {"text": "Linkdin URL?", "blockToGoID": "009",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the URL",
                    #              "keywords": []},
                    #  "ID": "008"},
                    # # Candidate SKILLS
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'None', "DataType": "CandidateSkills",
                    #  "Content": {"text": "What are your skills?", "blockToGoID": None,
                    #              "action": "End Chat", "afterMessage": "Thank you for the skills",
                    #              "keywords": ["SQL", "Python"]},
                    #  "ID": "009"},
                ],
                "description": "To search candidates",
                "id": "tisd83f4",
                "name": "Search Candidates Group"
            }
        ]
    }

    # Search candidate flow
    candidate_search_flow = {
        "groups": [
            {
                "blocks": [

                    # Candidate LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateCity.name,
                     "Content": {"text": "What city are you in?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "001"},

                    # Candidate EDUCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateEducation.name,
                     "Content": {"text": "What is your education?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                                 "keywords": []},
                     "ID": "002"},
                    # Candidate JOB TITLE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobTitle.name,
                     "Content": {"text": "What job title are you looking for?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the title",
                                 "keywords": []},
                     "ID": "004"},
                    # Candidate SKILLS
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CandidateSkills.name,
                     "Content": {"text": "What are your skills?", "blockToGoID": "007",
                                 "action": "Go To Next Block", "afterMessage": "skills will be searched",
                                 "keywords": ["SQL", "Python"]},
                     "ID": "006"},
                    # Candidate SEARCH
                    {"Content": {"action": "End Chat", "afterMessage": "", "blockToGoID": None,
                                 "databaseType": "Candidates", "showTop": 5}, "DataType": enums.DataType.NoType.name, "ID": "007",
                     "SkipAction": "End Chat", "SkipBlockToGoID": None,
                     "SkipText": "I didn't find what I was looking for.", "Skippable": True, "StoreInDB": True,
                     "Type": "Solutions"}
                ],
                "description": "To search candidates",
                "id": "tisd83f4",
                "name": "Search Candidates Group"
            }
        ]
    }

    # Search jobs flow
    # NOTE: Search params -> title, location, years required, skills, employment type
    job_search_flow = {
        "groups": [
            {
                "blocks": [

                    # Job TITLE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobTitle.name,
                     "Content": {"text": "Title of job?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "thanks",
                                 "keywords": []},
                     "ID": "001"},

                    # Job LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobCity.name,
                     "Content": {"text": "Job location?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "thanks",
                                 "keywords": []},
                     "ID": "002"},
                    # job SALARY
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobSalary.name,
                     "Content": {"text": "Job salary?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the salary",
                                 "keywords": []},
                     "ID": "003"},
                    # Job START DATE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobStartDate.name,
                     "Content": {"text": "Start date of job?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the start date",
                                 "keywords": []},
                     "ID": "004"},
                    # Job END DATE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobEndDate.name,
                     "Content": {"text": "End date of job?", "blockToGoID": "006",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the end date",
                                 "keywords": []},
                     "ID": "005"},
                    # Job SKILLS
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.JobEssentialSkills.name,
                     "Content": {"text": "Skills of job?", "blockToGoID": "007",
                                 "action": "Go To Next Block", "afterMessage": "thanks for the skills",
                                 "keywords": ["SQL", "Python"]},
                     "ID": "006"},
                    # Job SEARCH
                    {"Content": {"action": "End Chat", "afterMessage": "", "blockToGoID": None,
                                 "databaseType": "Jobs", "showTop": 10}, "DataType": enums.DataType.NoType.name, "ID": "007",
                     "SkipAction": "End Chat", "SkipBlockToGoID": None,
                     "SkipText": "I didn't find what I was looking for.", "Skippable": True, "StoreInDB": True,
                     "Type": "Solutions"}
                ],
                "description": "To search candidates",
                "id": "tisd83f4",
                "name": "Search Candidates Group"
            }
        ]
    }

    # Client insert flow
    client_insert_flow = {
        "groups": [
            {
                "blocks": [

                    # CLIENT LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.ClientLocation.name,
                     "Content": {"text": "What city are you in?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "001"},

                    # COMPANY NAME
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.CompanyName.name,
                     "Content": {"text": "What is your name?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                                 "keywords": []},
                     "ID": "002"},

                    # CLIENT PHONE NUMBER
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'None', "DataType": enums.DataType.ClientTelephone.name,
                     "Content": {"text": "What is your phone number?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the number",
                                 "keywords": []},
                     "ID": "003"},
                ],
                "description": "To search candidates",
                "id": "tisd83f4",
                "name": "Search Candidates Group"
            }
        ]
    }

    test = {
        "groups": [{"id": "u0Q88uPGM", "name": "Main", "blocks": [{"ID": "aReFwax_N", "Type": "Raw Text", "Content": {
            "text": "Before we can process your application we need to ask you a few questions to further qualify you. ",
            "action": "Go To Next Block", "blockToGoID": "l931XnlT1"}, "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": False,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "l931XnlT1", "Type": "User Input",
                                                                   "Content": {"text": "What is your name?",
                                                                               "action": "Go To Next Block",
                                                                               "keywords": [],
                                                                               "blockToGoID": "57u9dl6YO",
                                                                               "afterMessage": ""},
                                                                   "DataType": enums.DataType.CandidateName.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "57u9dl6YO", "Type": "User Input", "Content": {
                                                                      "text": "What is the best mobile number we can reach you on?",
                                                                      "action": "Go To Next Block", "keywords": [],
                                                                      "blockToGoID": "N-lHcLlze", "afterMessage": ""},
                                                                   "DataType": enums.DataType.CandidateMobile.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "N-lHcLlze", "Type": "Question",
                                                                   "Content": {"text": "Are you over the age of 18? ",
                                                                               "answers": [
                                                                                   {"id": "Na12wF9Z4", "text": "Yes",
                                                                                    "score": 10,
                                                                                    "action": "Go To Next Block",
                                                                                    "keywords": [],
                                                                                    "blockToGoID": "KBZ_QivPh",
                                                                                    "afterMessage": "Great"},
                                                                                   {"id": "wl2JC3GdS", "text": "No",
                                                                                    "score": -999, "action": "End Chat",
                                                                                    "keywords": [], "blockToGoID": None,
                                                                                    "afterMessage": "Unfortunately we will not be able to process your application you are older than 18 years old."}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "KBZ_QivPh", "Type": "Question", "Content": {
                                                                      "text": "Have you previously worked in a factory? ",
                                                                      "answers": [
                                                                          {"id": "ATqZwA9eO", "text": "Yes", "score": 5,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "AYjTC7dt-",
                                                                           "afterMessage": "Very good"},
                                                                          {"id": "arxgdOu3W", "text": "No", "score": 0,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "AYjTC7dt-",
                                                                           "afterMessage": "Okay, that's not a problem"}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "AYjTC7dt-", "Type": "Question", "Content": {
                                                                      "text": "Are you legible to work in the UK?",
                                                                      "answers": [
                                                                          {"id": "wCNV3L3Qv", "text": "Yes",
                                                                           "score": 10,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "qo5i9AOn9",
                                                                           "afterMessage": "Cool"},
                                                                          {"id": "1ijkqdIyo", "text": "No",
                                                                           "score": -999,
                                                                           "action": "End Chat", "keywords": [],
                                                                           "blockToGoID": None,
                                                                           "afterMessage": "Unfortunately, for any role that we have advertised, you will need to be eligible to work in the United Kingdom"}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "qo5i9AOn9", "Type": "User Input", "Content": {
                                                                      "text": "Enter below what documents you can provide us? ",
                                                                      "action": "Go To Next Block", "keywords": [],
                                                                      "blockToGoID": "oyDNWmdnE",
                                                                      "afterMessage": "Great, thanks for your input"},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "oyDNWmdnE", "Type": "Question", "Content": {
                                                                      "text": "Do you have any unspent criminal convictions?",
                                                                      "answers": [
                                                                          {"id": "NLj1Q4ZJ0", "text": "Yes",
                                                                           "score": -999,
                                                                           "action": "End Chat", "keywords": [],
                                                                           "blockToGoID": None,
                                                                           "afterMessage": "Unfortunately you cannot proceed if you have any unspent criminal convictions."},
                                                                          {"id": "AGPOnFfz2", "text": "No", "score": 10,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "Bu1AH28Eg",
                                                                           "afterMessage": "Ok"}]},
                                                                   "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": True, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "Bu1AH28Eg", "Type": "Question", "Content": {
                                                                      "text": "Will you pass a Drug and Alcohol test?",
                                                                      "answers": [
                                                                          {"id": "Du1jlagy9", "text": "Yes",
                                                                           "score": 10,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "9RVd_x2tv",
                                                                           "afterMessage": "Okay, you qualify very well for the job."},
                                                                          {"id": "DOndgOo9B", "text": "No",
                                                                           "score": -999,
                                                                           "action": "End Chat", "keywords": [],
                                                                           "blockToGoID": None,
                                                                           "afterMessage": "Unfortunately we canot progress further if you cannot pass a Drugs and Alcohol test."}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "9RVd_x2tv", "Type": "Question", "Content": {
                                                                      "text": "Fantastic, so before I book you in for the registration, I'm going to go through the job role and benefits, is that ok?",
                                                                      "answers": [
                                                                          {"id": "FI_Lmlrtx", "text": "Let's do it",
                                                                           "score": 0, "action": "Go To Next Block",
                                                                           "keywords": [], "blockToGoID": "a-6xv2ksf",
                                                                           "afterMessage": "Great"}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "a-6xv2ksf", "Type": "Question", "Content": {
                                                                      "text": "You will be picking and packing products in our factory. You will be working with poultry. Are you okay with this?",
                                                                      "answers": [
                                                                          {"id": "KYLkQ0wbP", "text": "Yes",
                                                                           "score": 10,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "dW6pjcEVe",
                                                                           "afterMessage": "Great"},
                                                                          {"id": "7mCmnc6Dv", "text": "No", "score": 0,
                                                                           "action": "End Chat", "keywords": [],
                                                                           "blockToGoID": None,
                                                                           "afterMessage": "Unfortunately as the role is very physically demanding, you will not be fit for this job."}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "dW6pjcEVe", "Type": "Raw Text", "Content": {
                                                                      "text": "Pay rates (Days = £9.50PH - Plus £1.71 for late hours premium",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "U34o91ZXH"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "U34o91ZXH", "Type": "Raw Text", "Content": {
                                                                      "text": "Regular overtime available (Between 41 - 50 hours = time and a half - Plus £1.71 for late hours premium) (50 plus hours = double pay - Plus £1.71 for late hours premium) ",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "ExmDcwN5Y"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "ExmDcwN5Y", "Type": "Raw Text", "Content": {
                                                                      "text": "Shift are based on a 4 on 3 off pattern",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "eaOW-wjsb"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "eaOW-wjsb", "Type": "Raw Text", "Content": {
                                                                      "text": "Public transport links are fantastic (except on Sunday)",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "QTNAVyAHG"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "QTNAVyAHG", "Type": "Raw Text", "Content": {
                                                                      "text": "And finally, we provide full training ",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "z_wmNJ6av"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "z_wmNJ6av", "Type": "Question", "Content": {
                                                                      "text": "Are you happy with everything so far?",
                                                                      "answers": [
                                                                          {"id": "P7sV_VvCW", "text": "Yes", "score": 0,
                                                                           "action": "Go To Next Block", "keywords": [],
                                                                           "blockToGoID": "ncMzXBZkw",
                                                                           "afterMessage": "Fantastic. Let's run you over the benefits as well"}]},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": True,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "ncMzXBZkw", "Type": "Raw Text", "Content": {
                                                                      "text": "Subsidised canteen serving hot and cold food (cash or contactless)",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "lro-HEL6-"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "lro-HEL6-", "Type": "Raw Text",
                                                                   "Content": {"text": "Free hot drinks machine",
                                                                               "action": "Go To Next Block",
                                                                               "blockToGoID": "bnPPP397f"},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": False,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "bnPPP397f", "Type": "Raw Text",
                                                                   "Content": {"text": "2 snack machines",
                                                                               "action": "Go To Next Block",
                                                                               "blockToGoID": "VJnJiDoS0"},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": False,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "VJnJiDoS0", "Type": "Raw Text",
                                                                   "Content": {"text": "2 x 30 minute breaks",
                                                                               "action": "Go To Next Block",
                                                                               "blockToGoID": "FRI-Ytaox"},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": False,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None},
                                                                  {"ID": "FRI-Ytaox", "Type": "Raw Text", "Content": {
                                                                      "text": "Arcade machine, ping pong table and pool table",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "jKfIB7nJZ"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "jKfIB7nJZ", "Type": "Raw Text", "Content": {
                                                                      "text": "Music playing throughout the warehouse",
                                                                      "action": "Go To Next Block",
                                                                      "blockToGoID": "XrekYSlv1"}, "DataType": enums.DataType.NoType.name,
                                                                   "SkipText": "Skip!", "Skippable": False,
                                                                   "StoreInDB": False, "SkipAction": "End Chat",
                                                                   "SkipBlockToGoID": None},
                                                                  {"ID": "XrekYSlv1", "Type": "Raw Text", "Content": {
                                                                      "text": "Thank you for running through our chatbot. We will be in touch with you very soon to confirm your appointment with the location and start date",
                                                                      "action": "End Chat", "blockToGoID": None},
                                                                   "DataType": enums.DataType.NoType.name, "SkipText": "Skip!",
                                                                   "Skippable": False, "StoreInDB": False,
                                                                   "SkipAction": "End Chat", "SkipBlockToGoID": None}],
                    "description": "Chat"}]}

    flow_services.updateFlow(flow, reader_a)

    helper_a = Assistant(Name="Candidate Insert Bot", Message="Test candidate insert", TopBarText="Insert Candidate",
                         Config=config, SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(candidate_insert_flow, helper_a)
    helper_b = Assistant(Name="Candidate Search Bot", Message="Test candidate search", TopBarText="Search Candidates",
                         Config=config, SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(candidate_search_flow, helper_b)
    helper_c = Assistant(Name="Job Search Bot", Message="Test job search", TopBarText="Search Jobs",
                         Config=config, SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(job_search_flow, helper_c)
    helper_d = Assistant(Name="Client Insert Bot", Message="Test client insert", TopBarText="Insert Client",
                         Config=config, SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(client_insert_flow, helper_d)

    flow_services.updateFlow(flow, reader_a)

    helper_e = Assistant(Name="TEST BOT", Message="TEST", TopBarText="TEST",
                         Config=config, SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(test, helper_e)

    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", Config=config,
                         SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", Config=config, SecondsUntilPopup=1,
                         Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", Config=config, SecondsUntilPopup=1,
                         Active=True, Company=sabic)

    helpers.seed()

    db.session.add(
        Role(Name="Admin", Company=aramco, AddUsers=True, EditChatbots=True, EditUsers=True, DeleteUsers=True,
             AccessBilling=True))
    db.session.add(
        Role(Name="User", Company=aramco, AddUsers=False, EditChatbots=True, EditUsers=False, DeleteUsers=False,
             AccessBilling=False))

    db.session.add(Role(Name="Admin", Company=sabic, AddUsers=True, EditChatbots=True, EditUsers=True, DeleteUsers=True,
                        AccessBilling=True))
    db.session.add(
        Role(Name="User", Company=sabic, AddUsers=False, EditChatbots=True, EditUsers=False, DeleteUsers=False,
             AccessBilling=False))

    # Get Roles
    ownerRole = Role.query.filter(Role.Name == "Owner").first()

    admin_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Admin").first()
    user_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "User").first()

    admin_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Admin").first()
    user_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "User").first()

    user_services.create(firstname='Sylvester', surname='Stallone', email='aa@aa.com', password='123',
                         phone='43444236456',
                         companyID=aramco.ID, roleID=ownerRole.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='Evg', surname='Test', email='evgeniy67@abv.bg', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123',
                         phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123',
                         phone='43444236456',
                         companyID=aramco.ID, roleID=user_aramco.ID, verified=True, timeZone="Europe/London")

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='43444236456',
                         companyID=sabic.ID, roleID=ownerRole.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123',
                         phone='43444236456',
                         companyID=sabic.ID, roleID=admin_sabic.ID, verified=True, timeZone="Europe/London")

    # Chatbot Conversations
    data = {
        "collectedData": [
            {
                "blockID": 1,
                "questionText": "What is your email?",
                "dataType": 'Email',
                "input": "faisal@gmail.com",
                "keywords": ['faisal', 'developer', 'email']
            },
            {
                "blockID": 2,
                "questionText": "How are you doing?",
                "dataType": 'No Type',
                "input": "I am fine thank you",
                "keywords": []
            },
            {
                "blockID": 3,
                "questionText": "When are you available?",
                "dataType": 'Availability',
                "input": "Only weekend days",
                "keywords": []
            },
            {
                "blockID": 4,
                "questionText": "What is your friend's email?",
                "dataType": "Email",
                "input": "friend@hotmail.com",
                "keywords": []
            }
        ],
        "selectedSolutions": None,
        "keywordsByDataType": {"Email": ["faisal@gmail.com", "friend@hotmail.com"],
                               "Availability": ["Only weekend days"],
                               "No Type": ["I am fine thank you"]}
    }
    conversation1 = Conversation(Data=data, DateTime=datetime.now(),
                                 TimeSpent=55, SolutionsReturned=2, QuestionsAnswered=3,
                                 UserType=enums.UserType.Candidate, Score=1,
                                 ApplicationStatus=enums.Status.Accepted, Assistant=reader_a)
    db.session.add(conversation1)
    db.session.add(Conversation(Data=data, DateTime=datetime.now(),
                                TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                UserType=enums.UserType.Client, Score=0.05, Completed=False,
                                ApplicationStatus=enums.Status.Rejected, Assistant=reader_a))

    # add chatbot session in bulk
    for i in range(50):
        db.session.add(Conversation(Data=data, DateTime=datetime.now() - timedelta(days=i),
                                    TimeSpent=i + 40, SolutionsReturned=i + 3, QuestionsAnswered=i + 4,
                                    UserType=enums.UserType.Candidate, Score=0.45, Assistant=reader_a))

    db1: Database = Database(Name='db1', Type=enums.DatabaseType.Candidates, Company=aramco)
    db2: Database = Database(Name='db2', Type=enums.DatabaseType.Candidates, Company=aramco)

    db3: Database = Database(Name='db3', Type=enums.DatabaseType.Jobs, Company=aramco)

    db.session.add(db1)
    db.session.add(db2)
    db.session.add(db3)

    db.session.add(addCandidate(db1, 'Faisal', 2000, "Software Engineer", "python, java, javascript, SQL",
                                5, "London"))

    db.session.add(addCandidate(db1, 'Mohammed', 4000, "Software Engineer", "python, SQL",
                                10, "Cardiff"))

    db.session.add(addCandidate(db2, 'Ahmed', 1500, "Web Developer", "html,css, javascript",
                                2, "Cardiff"))

    db.session.add(
        addJob(db3, 'Python Developer', 'a job for someone who is good at python', 1500, 'London', Currency('USD')))
    db.session.add(addJob(db3, 'Python Developer', None, None, 'London', Currency('GBP')))

    for i in list(range(120)):
        db.session.add(addCandidate(db1, 'Ahmed', 1500, "Web Developer", "html,css, javascript",
                                    2, "Cardiff"))

    # Add CRM connection for aramco company
    # Adapt
    db.session.add(CRM(Type=enums.CRM.Adapt, Company=aramco, Auth={
        "domain": "PartnerDomain9",
        "username": "SD9USR8",
        "password": "P@55word",
        "profile": "CoreProfile",
        "locale": "en_GB",
        "timezone": "GMT",
        "dateFormat": 0,
        "timeFormat": 0}))

    # Bullhorn
    db.session.add(CRM(Type=enums.CRM.Bullhorn, CompanyID=1, Auth={
        "access_token": "91:184cd487-b4b0-4114-be56-67f70f50d358",
        "refresh_token": "91:91aa0af7-67f8-4cac-a4bf-016413b51b4a"
    }))

    # Twilio
    db.session.add(Messenger(Type=enums.Messenger.Twilio, CompanyID=1, Auth={
        "account_sid": "AC7326ee584c07bf56782b1392df33bc50",
        "auth_token": "34f86f89ee6f67deede6725bb6e7c9af",
        "phone_number": "441143032341"
    }))

    # Create an AutoPilot for a Company
    reader_a.AutoPilot = auto_pilot_services.create('First Pilot',
                                                    "First pilot to automate the acceptance and rejection of candidates application",
                                                    aramco.ID).Data

    auto_pilot_services.create('Second Pilot', '', aramco.ID)

    appointment_services.dummyCreateAppointmentAllocationTime("Test Times", aramco.ID)

    # Add Appointment
    a = Appointment(DateTime=datetime.now() + timedelta(days=5), Conversation=conversation1,
                    UserTimeZone="Europe/London")

    db.session.add(a)
    db.session.commit()


def addCandidate(db, name, desiredSalary, jobTitle, skills, exp, city):
    return Candidate(Database=db,
                     CandidateName=name,
                     CandidateDesiredSalary=desiredSalary,
                     CandidateJobTitle=jobTitle,
                     CandidateSkills=skills,
                     CandidateYearsExperience=exp,
                     CandidateCity=city,
                     Currency=Currency('USD'))


def addJob(db, title, description, salary, location, currency: Currency or None):
    return Job(Database=db,
               JobTitle=title,
               JobDescription=description,
               JobCity=location,
               JobSalary=salary,
               Currency=currency)
