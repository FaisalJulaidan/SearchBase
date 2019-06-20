from models import db, Role, Company, Assistant, Conversation, Database, Candidate, CRM, Appointment, Job
from services import user_services, flow_services, auto_pilot_services, assistant_services, scheduler_services
from datetime import datetime, timedelta, time
from utilities import helpers
from sqlalchemy_utils import Currency
import enums

# Generates dummy data for testing
def generate():

    # Companies creation
    db.session.add(Company(Name='Aramco', URL='ff.com', StripeID='cus_00000000000000', SubID='sub_00000000000000'))
    db.session.add(Company(Name='Sabic', URL='ff.com', StripeID='cus_DbgKupMRLNYXly'))

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
                "id": "tisd83f4",
                "name": "group 1",
                "description": "The best group",
                "blocks": [
                    {
                        "ID":"8EDEBiDHa",
                        "Type":"Question",
                        "StoreInDB":True,
                        "Skippable":False,
                        "SkipText":"Skip!",
                        "SkipAction":"End Chat",
                        "SkipBlockToGoID": None,
                        "DataType":"CandidateAvailability",
                        "Content":{
                            "text":"what?",
                            "answers":[
                                {
                                    "id":"WZXp26mdL",
                                    "text":"low",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 2
                                },
                                {
                                    "id":"godj9rom5",
                                    "text":"medium",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 5
                                },
                                {
                                    "id":"E6phkGY5u",
                                    "text":"high",
                                    "keywords":[],
                                    "blockToGoID": '834hf',
                                    "action":"Go To Next Block",
                                    "afterMessage":"",
                                    "score": 8
                                }
                            ]
                        },
                    },
                    {
                        "ID": "834hf",
                        "DataType": enums.DataType.CandidateSkills.name,
                        "Type": enums.BlockType.UserInput.value,
                        "StoreInDB": True,
                        "Skippable": True,
                        "SkipText": "Skip!",
                        "SkipAction": enums.BlockAction.EndChat.value,
                        "SkipBlockToGoID": None,
                        "Content": {
                            "action": "Go To Next Block",
                            "text": "What's are your skills?",
                            "blockToGoID": "by_GnLY-f",
                            "afterMessage": "Your input is being processed...",
                            "keywords": ['python', 'sql', 'java']
                        }
                    },
                    # {
                    #     "ID":"by_GnLY-f",
                    #     "Type": enums.BlockType.Solutions.value,
                    #     "StoreInDB":False,
                    #     "Skippable":True,
                    #     "SkipText": "Skip!",
                    #     "SkipAction": enums.BlockAction.EndChat.value,
                    #     "SkipBlockToGoID": None,
                    #     "DataType":enums.DataType.NoType.name,
                    #     "Content": {
                    #         "showTop": 3,
                    #         "action": "End Chat",
                    #         "blockToGoID": None,
                    #         "afterMessage": "We will contact you with this candidate",
                    #         "databaseType": enums.DatabaseType.Candidates.value['enumName']
                    #     },
                    # },
                    # {
                    #     "ID": "gje6D",
                    #     "DataType": enums.DataType.CandidateEmail.name,
                    #     "Type": "User Input",
                    #     "StoreInDB": True,
                    #     "Skippable": False,
                    #     "Content": {
                    #         "action": "End Chat",
                    #         "text": "What's your email",
                    #         "blockToGoID": None,
                    #         "afterMessage": "Your email is in good hands :) Bye!"
                    #     }
                    # },
                    # {
                    #     "ID": "hkwt845",
                    #     "DataType": enums.DataType.CandidateSkills.name,
                    #     "Type": "File Upload",
                    #     "StoreInDB": True,
                    #     "Skippable": True,
                    #     "Content": {
                    #         "action": "Go To Next Block",
                    #         "text": "Upload CV1",
                    #         "blockToGoID": "gjdfl34",
                    #         "afterMessage": "File processed!",
                    #         "fileTypes": ["docx", "txt", "png", "xml", "doc", "pdf", "jpg"]
                    #     }
                    # },
                    # {
                    #     "ID": "gjdfl34",
                    #     "DataType": enums.DataType.CandidateSkills.value,
                    #     "Type": "File Upload",
                    #     "StoreInDB": True,
                    #     "Skippable": True,
                    #     "Content": {
                    #         "action": "End Chat",
                    #         "text": "Upload CV2",
                    #         "blockToGoID": None,
                    #         "afterMessage": "File processed!",
                    #         "fileTypes": ["docx", "txt", "png", "xml", "doc", "pdf", "jpg"]
                    #     }
                    # },
                ]
            }
        ]
    }
    flow_services.updateFlow(flow, reader_a)

    helper_a = Assistant(Name="Helper", Message="Hey there", TopBarText="Aramco Bot", SecondsUntilPopup=1, Active=True, Company=aramco)

    reader_s = Assistant(Name="Reader", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)
    helper_s = Assistant(Name="Helper", Message="Hey there", TopBarText="Sabic Bot", SecondsUntilPopup=1, Active=True, Company=sabic)


    # Create Roles
    db.session.add(Role(Name="Staff", EditChatbots=True, AddUsers=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))
    db.session.add(Role(Name="Owner", EditChatbots=True, AddUsers=True, EditUsers=True, DeleteUsers=True, AccessBilling=True))

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
                         companyID=aramco.ID, roleID=ownerRole.ID, verified=True)
    user_services.create(firstname='Evg', surname='Test', email='evgeniy67@abv.bg', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e2@e.com', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=admin_aramco.ID, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e3@e.com', password='123', phone='43444236456',
                         companyID=aramco.ID, roleID=user_aramco.ID, verified=True)

    user_services.create(firstname='Ali', surname='Khalid', email='bb@bb.com', password='123', phone='43444236456',
                         companyID=sabic.ID, roleID=ownerRole.ID, verified=True)
    user_services.create(firstname='firstname', surname='lastname', email='e5@e.com', password='123', phone='43444236456',
                         companyID=sabic.ID, roleID=admin_sabic.ID, verified=True)



    # Chatbot Sessions
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
                                 ApplicationStatus=enums.ApplicationStatus.Accepted, Assistant=reader_a)
    db.session.add(conversation1)
    db.session.add(Conversation(Data=data, DateTime=datetime.now(),
                                TimeSpent=120, SolutionsReturned=20, QuestionsAnswered=7,
                                UserType=enums.UserType.Client, Score= 0.05, Completed=False,
                                ApplicationStatus=enums.ApplicationStatus.Rejected, Assistant=reader_a))

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
    db.session.add(CRM(Type=enums.CRM.Adapt, Company=aramco, Auth={
        "domain": "PartnerDomain9",
        "username": "SD9USR8",
        "password": "P@55word",
        "profile": "CoreProfile",
        "locale": "en_GB",
        "timezone": "GMT",
        "dateFormat": 0,
        "timeFormat": 0}))

    # Create an AutoPilot for a Company
    auto_pilot_services.create('First Pilot',
                               "First pilot to automate the acceptance and rejection of candidates application",
                               aramco.ID)
    auto_pilot_services.create('Second Pilot', '', aramco.ID)
    reader_a.AutoPilot = auto_pilot_services.getByID(1,1).Data

    # Add Appointment
    a = Appointment(DateTime=datetime.now() + timedelta(days=5),
                    Conversation=conversation1, Assistant=reader_a)

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