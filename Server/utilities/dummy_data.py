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

    # Create and validate a flow for an assistant

    # job = scheduler_services.scheduler.add_job(func=scheduler_services.printSomething, trigger='interval', seconds=5, id="3559a1946b52419899e8841d4317d194", replace_existing=True)
    # scheduler_services.scheduler.start()

    # Create Assistants for Aramco and Sabic companies
    reader_a = Assistant(Name="Reader", Message="Hey there",
                         TopBarText="Aramco Bot", SecondsUntilPopup=1,
                         Active=True, Company=aramco)

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
                        "DataType": enums.DataType.CandidateSkills.value['enumName'],
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
                        "DataType": enums.DataType.NoType.value['enumName'],
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
                        "DataType": enums.DataType.CandidateSkills.value['enumName'],
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
                        "DataType": enums.DataType.NoType.value['enumName'],
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
                        "DataType": enums.DataType.CandidateSkills.value['enumName'],
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
                        "DataType": enums.DataType.NoType.value['enumName'],
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
                     "SkipBlockToGoID": 'null', "DataType": "CandidateName",
                     "Content": {"text": "Can you please provide us with your name?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the name",
                                 "keywords": []},
                     "ID": "001"},
                    # Candidate EMAIL
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateEmail",
                     "Content": {"text": "Can you please provide us with email?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the email",
                                 "keywords": []},
                     "ID": "002"},
                    # Candidate LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateLocation",
                     "Content": {"text": "What city are you in?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "003"},
                    # Candidate PHONE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateMobile",
                     "Content": {"text": "What is your phone number?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the phone number",
                                 "keywords": []},
                     "ID": "004"},
                    # Candidate EDUCATION
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'null', "DataType": "CandidateEducation",
                    #  "Content": {"text": "What is your education?", "blockToGoID": "006",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                    #              "keywords": []},
                    #  "ID": "005"},
                    # # Candidate SALARY
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'null', "DataType": "CandidateAnnualDesiredSalary",
                    #  "Content": {"text": "What is your annual desired salary?", "blockToGoID": "007",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the salary",
                    #              "keywords": []},
                    #  "ID": "006"},
                    # # Candidate JOB TITLE
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'null', "DataType": "CandidateJobTitle",
                    #  "Content": {"text": "What job title are you looking for?", "blockToGoID": "008",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the title",
                    #              "keywords": []},
                    #  "ID": "007"},
                    # # Candidate LINKDIN URL
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'null', "DataType": "CandidateLinkdinURL",
                    #  "Content": {"text": "Linkdin URL?", "blockToGoID": "009",
                    #              "action": "Go To Next Block", "afterMessage": "Thank you for the URL",
                    #              "keywords": []},
                    #  "ID": "008"},
                    # # Candidate SKILLS
                    # {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                    #  "SkipAction": "End Chat",
                    #  "SkipBlockToGoID": 'null', "DataType": "CandidateSkills",
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
                     "SkipBlockToGoID": 'null', "DataType": "CandidateLocation",
                     "Content": {"text": "What city are you in?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "001"},

                    # Candidate EDUCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateEducation",
                     "Content": {"text": "What is your education?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                                 "keywords": []},
                     "ID": "002"},
                    # Candidate SALARY
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateAnnualDesiredSalary",
                     "Content": {"text": "What is your annual desired salary?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the salary",
                                 "keywords": []},
                     "ID": "003"},
                    # Candidate JOB TITLE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateJobTitle",
                     "Content": {"text": "What job title are you looking for?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the title",
                                 "keywords": []},
                     "ID": "004"},
                    # Candidate AVAILABILITY
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateAvailability",
                     "Content": {"text": "Required availability of candidate?", "blockToGoID": "006",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the availability",
                                 "keywords": []},
                     "ID": "005"},
                    # Candidate SKILLS
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CandidateSkills",
                     "Content": {"text": "What are your skills?", "blockToGoID": "007",
                                 "action": "Go To Next Block", "afterMessage": "skills will be searched",
                                 "keywords": ["SQL", "Python"]},
                     "ID": "006"},
                    # Candidate SEARCH
                    {"Content": {"action": "End Chat", "afterMessage": "", "blockToGoID": None,
                                 "databaseType": "Candidates", "showTop": 5}, "DataType": "NoType", "ID": "007",
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
                     "SkipBlockToGoID": 'null', "DataType": "JobTitle",
                     "Content": {"text": "Title of job?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "thanks",
                                 "keywords": []},
                     "ID": "001"},

                    # Job LOCATION
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "JobLocation",
                     "Content": {"text": "Job location?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "thanks",
                                 "keywords": []},
                     "ID": "002"},
                    # job SALARY
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "JobAnnualSalary",
                     "Content": {"text": "Job salary?", "blockToGoID": "004",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the salary",
                                 "keywords": []},
                     "ID": "003"},
                    # Job START DATE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "JobStartDate",
                     "Content": {"text": "Start date of job?", "blockToGoID": "005",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the start date",
                                 "keywords": []},
                     "ID": "004"},
                    # Job END DATE
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "JobEndDate",
                     "Content": {"text": "End date of job?", "blockToGoID": "006",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the end date",
                                 "keywords": []},
                     "ID": "005"},
                    # Job SKILLS
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "JobEssentialSkills",
                     "Content": {"text": "Skills of job?", "blockToGoID": "007",
                                 "action": "Go To Next Block", "afterMessage": "thanks for the skills",
                                 "keywords": ["SQL", "Python"]},
                     "ID": "006"},
                    # Job SEARCH
                    {"Content": {"action": "End Chat", "afterMessage": "", "blockToGoID": None,
                                 "databaseType": "Jobs", "showTop": 10}, "DataType": "NoType", "ID": "007",
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
                     "SkipBlockToGoID": 'null', "DataType": "ClientLocation",
                     "Content": {"text": "What city are you in?", "blockToGoID": "002",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the city",
                                 "keywords": []},
                     "ID": "001"},

                    # COMPANY NAME
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "CompanyName",
                     "Content": {"text": "What is your name?", "blockToGoID": "003",
                                 "action": "Go To Next Block", "afterMessage": "Thank you for the edcuation",
                                 "keywords": []},
                     "ID": "002"},

                    # CLIENT PHONE NUMBER
                    {"Type": "User Input", "StoreInDB": True, "Skippable": False, "SkipText": "Skip!",
                     "SkipAction": "End Chat",
                     "SkipBlockToGoID": 'null', "DataType": "ClientTelephone",
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

    flow_services.updateFlow(flow, reader_a)

    helper_a = Assistant(Name="Candidate Insert Bot", Message="Test candidate insert", TopBarText="Insert Candidate",
                         SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(candidate_insert_flow, helper_a)
    helper_b = Assistant(Name="Candidate Search Bot", Message="Test candidate search", TopBarText="Search Candidates",
                         SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(candidate_search_flow, helper_b)
    helper_c = Assistant(Name="Job Search Bot", Message="Test job search", TopBarText="Search Jobs",
                         SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(job_search_flow, helper_c)
    helper_d = Assistant(Name="Client Insert Bot", Message="Test client insert", TopBarText="Insert Client",
                         SecondsUntilPopup=1, Active=True, Company=aramco)
    flow_services.updateFlow(client_insert_flow, helper_d)

    flow_services.updateFlow(flow, reader_a)

    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)

    helpers.seed()

    db.session.add(Role(Name="Admin", Company= aramco, AddUsers=True, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= aramco, AddUsers=False, EditChatbots=True, EditUsers=False, DeleteUsers=False, AccessBilling=False))

    db.session.add(Role(Name="Admin", Company= sabic, AddUsers=True, EditChatbots=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="User", Company= sabic, AddUsers=False, EditChatbots=True, EditUsers=False, DeleteUsers=False, AccessBilling=False))


    # Get Roles
    ownerRole = Role.query.filter(Role.Name == "Owner").first()

    admin_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "Admin").first()
    user_aramco = Role.query.filter(Role.Company == aramco).filter(Role.Name == "User").first()

    admin_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "Admin").first()
    user_sabic = Role.query.filter(Role.Company == sabic).filter(Role.Name == "User").first()

    user_services.create(firstname='Sylvester', surname='Stallone', email='aa@aa.com', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=ownerRole.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='Evg', surname='Test', email='evgeniy67@abv.bg', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=user_aramco.ID, verified=True, timeZone="Europe/London")

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='43444236456',
                         companyID=sabic.ID, roleID=ownerRole.ID, verified=True, timeZone="Europe/London")
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', phone='43444236456',
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
                                 UserType=enums.UserType.Candidate, Score= 1,
                                 ApplicationStatus=enums.Status.Accepted, Assistant=reader_a)
    db.session.add(conversation1)
    db.session.add(Conversation(Data=data, DateTime=datetime.now(),
                                TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                UserType=enums.UserType.Client, Score= 0.05, Completed=False,
                                ApplicationStatus=enums.Status.Rejected, Assistant=reader_a))

    # add chatbot session in bulk
    for i in range(50):
        db.session.add(Conversation(Data=data, DateTime=datetime.now() - timedelta(days=i),
                                    TimeSpent=i+40, SolutionsReturned=i+3, QuestionsAnswered=i+4,
                                    UserType=enums.UserType.Candidate, Score= 0.45, Assistant=reader_a))


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

    db.session.add(addJob(db3, 'Python Developer', 'a job for someone who is good at python', 1500, 'London', Currency('USD')))
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
    a = Appointment(DateTime=datetime.now() + timedelta(days=5), Conversation=conversation1, UserTimeZone="Europe/London")

    db.session.add(a)
    db.session.commit()



def addCandidate(db, name, desiredSalary, jobTitle, skills, exp, location):
    return Candidate(Database=db,
                     CandidateName=name,
                     CandidateDesiredSalary=desiredSalary,
                     CandidateJobTitle=jobTitle,
                     CandidateSkills =skills,
                     CandidateYearsExperience = exp,
                     CandidateLocation = location,
                     Currency= Currency('USD'))


def addJob(db, title, description, salary, location, currency: Currency or None):
    return Job(Database=db,
               JobTitle=title,
               JobDescription=description,
               JobLocation=location,
               JobSalary=salary,
               Currency= currency)