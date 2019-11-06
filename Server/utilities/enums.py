from enum import Enum, unique
from typing import List


# ===============================================================================================
# IMPORTANT: when making changes to enums don't forget to  migrate database tables
# where necessary e.g. Conversation, Block. You know just ask Faisal Julaidan before making any changes.
# STEPS TO FOLLOW
# 1. Change the Enum
# 2. Migrate the Database accordingly
# ===============================================================================================

@unique
class CRM(Enum):
    Adapt = 'Adapt'
    Bullhorn = 'Bullhorn'
    Vincere = 'Vincere'
    Greenhouse = 'Greenhouse'
    Jobscience = 'Jobscience'
    Mercury = 'Mercury'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class Calendar(Enum):
    Google = 'Google'
    Outlook = 'Outlook'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

@unique
class FileAssetType(Enum):
    NoType = 'No Type'
    CandidateCV = 'Candidate CV'
    Passport = 'Passport'
    DrivingLicense = 'Driving License'
    DrugTest = 'Drug Test'
    Logo = 'Logo'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class Messenger(Enum):
    Twilio = 'Twilio'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class Status(Enum):
    Pending = 'Pending'
    Accepted = 'Accepted'
    Rejected = 'Rejected'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
                
def planCreator(planID: str, assistants: int = 0, campaigns: int = 0, autopilot: int = 0, databases: int = 0, appointments: int = 0):
    return {
      'planID': planID,
      'accessAssistants': assistants,
      'accessCampaigns': campaigns,
      'accessAutopilot': autopilot,
      'accessDatabases': databases,
      'accessAppointments'  : appointments }

@unique
class Plan(Enum):
    Essential = planCreator("plan_D3lp2yVtTotk2f", 1, 0, 0, 1, 0)
    Pro = planCreator("plan_G7SuTtSoBxJ7aS", 1, 1, 0, 1, 1)
    Premium = planCreator("plan_G7SuT5aJA1OFJU", 1, 1, 1, 1, 1)

    @classmethod
    def get_plan(cls, value):
        for item in cls:
            if(value == item.value['planID']):
                return item
        return None


@unique
class Period(Enum):
    Annually = 'Annually'
    Monthly = 'Monthly'
    Weekly = 'Weekly'
    Daily = 'Daily'


@unique
class JobType(Enum):  
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Contract = 'Contract'
    # Any = 'Any'


@unique
class BlockType(Enum):
    UserInput = 'User Input'
    Question = 'Question'
    FileUpload = 'File Upload'
    Solutions = 'Solutions'
    RawText = 'Raw Text'
    SalaryPicker = 'Salary Picker'
    UserType = 'User Type'
    JobType = 'Job Type'
    DatePicker = 'Date Picker'
    NoType = 'No Type'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class BlockAction(Enum):
    GoToNextBlock = 'Go To Next Block'
    GoToSpecificBlock = 'Go To Specific Block'
    GoToGroup = 'Go To Group'
    EndChat = 'End Chat'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class UserType(Enum):
    Unknown = 'Unknown'
    Candidate = 'Candidate'
    Client = 'Client'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class Webhooks(Enum):
    Conversations = 'Conversations'
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class DatabaseType(Enum):
    # multiplying userTypes by x will help detect the user type in the chatbot
    Candidates = {'enumName': 'Candidates', 'name': 'Candidates', 'userTypes': [UserType.Client.value] * 5}
    Jobs = {'enumName': 'Jobs', 'name': 'Jobs', 'userTypes': [UserType.Candidate.value] * 5}

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

@unique
class DataTypeSection(Enum):
    NoType = 'No Type'
    Client = 'Client'
    Company = 'Company'
    Candidate = 'Candidate'
    Job = 'Job'
    User = 'User'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class ValidationType(Enum):
    Ignore = 'Ignore'
    Email = 'Email'
    Telephone = 'Telephone'
    Number = 'Number'
    String = 'String'
    URL = 'URL'
    Time = 'Time'
    Date = 'Date'
    DateTime = 'DateTime'
    Salary = 'Salary' # Ex: 1000-5000 GBP Annual

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


# === Data Types Stuff === #
def dataTypeCreator(name: str, enumName: str, validation: ValidationType, section: DataTypeSection,
                    userTypes: List[UserType], blockTypes: List[BlockType]):
    return {'name': name,
            'enumName': enumName,
            'validation': validation.value,
            'dataTypeSection': section.value,
            'userTypes': [ut.value for ut in userTypes],
            'blockTypes': [bt.value for bt in blockTypes],
            }
            

@unique
class DataType(Enum):
    NoType = dataTypeCreator(
        'No Type',
        'NoType',
        ValidationType.Ignore,
        DataTypeSection.NoType,
        [UserType.Unknown],
        [BlockType.UserInput, BlockType.Question, BlockType.FileUpload, BlockType.UserType])

    CandidateAvailability =  dataTypeCreator(
        'Candidate Availability',
        'CandidateAvailability',
        ValidationType.DateTime,
        DataTypeSection.Candidate,
        [UserType.Candidate, UserType.Client],
        [BlockType.DatePicker])


    # Candidate
    CandidateName = dataTypeCreator(
        'Candidate Name',
        'CandidateName',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateEmail = dataTypeCreator(
        'Candidate Email',
        'CandidateEmail',
        ValidationType.Email,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateMobile = dataTypeCreator(
        'Candidate Mobile',
        'CandidateMobile',
        ValidationType.Telephone,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateLinkdinURL = dataTypeCreator(
        'Candidate Linkdin URL',
        'CandidateLinkdinURL',
        ValidationType.URL,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateCV = dataTypeCreator(
        'Candidate CV',
        'CandidateCV',
        ValidationType.Ignore,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.FileUpload])

    CandidateLocation = dataTypeCreator(
        'Candidate Location',
        'CandidateLocation',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput, BlockType.Question])

    CandidateSkills = dataTypeCreator(
        'Candidate Skills',
        'CandidateSkills',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput, BlockType.Question])

    CandidateEducation = dataTypeCreator(
        'Candidate Education',
        'CandidateEducation',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput, BlockType.Question])

    CandidateYearsExperience = dataTypeCreator(
        'Candidate Years Experience',
        'CandidateYearsExperience',
        ValidationType.Number,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    # Example: Less Than 5000 GBP Annually/Daily
    CandidateDesiredSalary = dataTypeCreator(
        'Candidate Desired Salary',
        'CandidateDesiredSalary',
        ValidationType.Salary,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.SalaryPicker])

    CandidateVisa = dataTypeCreator(
        'Candidate Visa',
        'CandidateVisa',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.FileUpload])

    CandidatePassport = dataTypeCreator(
        'Candidate Passport',
        'CandidatePassport',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.FileUpload])

    CandidateWorkEligibility = dataTypeCreator(
        'Candidate Work Eligibility',
        'CandidateWorkEligibility',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateCriminalConvictions = dataTypeCreator(
        'Candidate Criminal Convictions',
        'CandidateCriminalConvictions',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    CandidateDrivingLicense = dataTypeCreator(
        'Candidate Driving License',
        'CandidateDrivingLicense',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.FileUpload])

    CandidateDrugsTest = dataTypeCreator(
        'Candidate Drugs Test',
        'CandidateDrugsTest',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.FileUpload])

    CandidateOver18 = dataTypeCreator(
        'Candidate Over 18',
        'CandidateOver18',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.NoType])

    CandidateOptIn = dataTypeCreator(
        'CandidateOptIn',
        'Candidate OptIn',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.NoType])

    CandidateConsultantName = dataTypeCreator(
        'Candidate Consultant Name',
        'CandidateConsultantName',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate],
        [BlockType.UserInput])

    # Company
    CompanyName = dataTypeCreator(
        'Company Name',
        'CompanyName',
        ValidationType.String,
        DataTypeSection.Company,
        [UserType.Client, UserType.Candidate],
        [BlockType.UserInput])

    # ======================================================================
    # Client
    # The chances of asking a question with a client data type is very low; however when asked it means most of
    # the time that this user type is a client. For that reason we multiplied Client UserType by 6 to increase
    # the probability of the userType being a Client when the chatbot tries to detect the user type :)

    ClientName = dataTypeCreator(
        'Client Name',
        'ClientName',
        ValidationType.String,
        DataTypeSection.Client,
        [UserType.Client] * 6,
        [BlockType.UserInput])

    ClientOptIn = dataTypeCreator(
        'ClientOptIn',
        'ClientOptIn',
        ValidationType.String,
        DataTypeSection.Client,
        [UserType.Client] * 6,
        [BlockType.NoType])

    ClientEmail = dataTypeCreator(
        'Client Email',
        'ClientEmail',
        ValidationType.Email,
        DataTypeSection.Client,
        [UserType.Client] * 6,
        [BlockType.UserInput])

    ClientTelephone = dataTypeCreator(
        'Client Telephone',
        'ClientTelephone',
        ValidationType.Telephone,
        DataTypeSection.Client,
        [UserType.Client] * 6,
        [BlockType.UserInput])

    ClientLocation = dataTypeCreator(
        'Client Location',
        'ClientLocation',
        ValidationType.String,
        DataTypeSection.Client,
        [UserType.Client] * 6,
        [BlockType.UserInput])

    ClientAvailability =  dataTypeCreator(
        'Client Availability',
        'ClientAvailability',
        ValidationType.DateTime,
        DataTypeSection.Client,
        [UserType.Client],
        [BlockType.DatePicker])


    # ======================================================================
    # Job

    JobTitle = dataTypeCreator(
        'Job Title',
        'JobTitle',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput, BlockType.Question])

    JobLocation = dataTypeCreator(
        'Job Location',
        'JobLocation',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput, BlockType.Question])

    JobType = dataTypeCreator(
        'Job Type',
        'JobType',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.JobType])

    JobCategory = dataTypeCreator(
        'Job Category',
        'JobCategory',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput, BlockType.Question])

    JobSalary = dataTypeCreator(
        'Job Salary',
        'JobSalary',
        ValidationType.Salary,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.SalaryPicker])

    JobEssentialSkills = dataTypeCreator(
        'Job Essential Skills',
        'JobEssentialSkills',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput, BlockType.Question])

    JobLinkURL = dataTypeCreator(
        'Job Link URL',
        'JobLinkURL',
        ValidationType.URL,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput])

    JobEndDate = dataTypeCreator(
        'Job End Date',
        'JobEndDate',
        ValidationType.DateTime,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.DatePicker])

    JobStartDate = dataTypeCreator(
        'Job Start Date',
        'JobStartDate',
        ValidationType.DateTime,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.DatePicker])

    JobYearsRequired = dataTypeCreator(
        'Job Years Required',
        'JobYearsRequired',
        ValidationType.Number,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserInput])

    # Warning: this should aways be the last dateType to avoid recursion with UserType Enum class
    UserType = dataTypeCreator(
        'User Type',
        'UserType',
        ValidationType.String,
        DataTypeSection.NoType,
        [UserType.Candidate, UserType.Client],
        [BlockType.UserType])