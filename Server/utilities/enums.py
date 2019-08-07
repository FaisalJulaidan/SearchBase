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


@unique
class Period(Enum):
    Annually = 'Annually'
    Monthly = 'Monthly'
    Weekly = 'Weekly'
    Daily = 'Daily'


@unique
class EmploymentType(Enum):
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
                    userTypes: List[UserType]):
    return {'name': name,
            'enumName': enumName,
            'validation': validation.value,
            'dataTypeSection': section.value,
            'userTypes': [ut.value for ut in userTypes],
            # 'blockTypes': ,
            }


@unique
class DataType(Enum):
    NoType = dataTypeCreator(
        'No Type',
        'NoType',
        ValidationType.Ignore,
        DataTypeSection.NoType, [
            UserType.Unknown])

    # Candidate
    CandidateName = dataTypeCreator(
        'Candidate Name',
        'CandidateName',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateEmail = dataTypeCreator(
        'Candidate Email',
        'CandidateEmail',
        ValidationType.Email,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateMobile = dataTypeCreator(
        'Candidate Mobile',
        'CandidateMobile',
        ValidationType.Telephone,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateLinkdinURL = dataTypeCreator(
        'Candidate Linkdin URL',
        'CandidateLinkdinURL',
        ValidationType.URL,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateCV = dataTypeCreator(
        'Candidate CV',
        'CandidateCV',
        ValidationType.Ignore,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateAvailability = dataTypeCreator(
        'Candidate Availability',
        'CandidateAvailability',
        ValidationType.DateTime,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateLocation = dataTypeCreator(
        'Candidate Location',
        'CandidateLocation',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateSkills = dataTypeCreator(
        'Candidate Skills',
        'CandidateSkills',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateJobTitle = dataTypeCreator(
        'Candidate Job Title',
        'CandidateJobTitle',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateEducation = dataTypeCreator(
        'Candidate Education',
        'CandidateEducation',
        ValidationType.String,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateYearsExperience = dataTypeCreator(
        'Candidate Years Experience',
        'CandidateYearsExperience',
        ValidationType.Number,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    # CandidateEmploymentPreference = dataTypeCreator(
    #     'Candidate Employment Preference',
    #     'CandidateEmploymentPreference',
    #     ValidationType.String,
    #     DataTypeSection.Candidate,
    #     [UserType.Candidate])

    # Example: Less Than 5000 GBP Annually
    CandidateDailyDesiredSalary = dataTypeCreator(
        'Candidate Daily Desired Salary',
        'CandidateDailyDesiredSalary',
        ValidationType.Salary,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CandidateAnnualDesiredSalary = dataTypeCreator(
        'Candidate Annual Desired Salary',
        'CandidateAnnualDesiredSalary',
        ValidationType.Salary,
        DataTypeSection.Candidate,
        [UserType.Candidate])

    CompanyName = dataTypeCreator(
        'Company Name',
        'CompanyName',
        ValidationType.String,
        DataTypeSection.Company,
        [UserType.Client, UserType.Candidate])

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
        [UserType.Client] * 6)

    ClientEmail = dataTypeCreator(
        'Client Email',
        'ClientEmail',
        ValidationType.Email,
        DataTypeSection.Client,
        [UserType.Client] * 6)

    ClientTelephone = dataTypeCreator(
        'Client Telephone',
        'ClientTelephone',
        ValidationType.Telephone,
        DataTypeSection.Client,
        [UserType.Client] * 6)

    ClientLocation = dataTypeCreator(
        'Client Location',
        'ClientLocation',
        ValidationType.String,
        DataTypeSection.Client,
        [UserType.Client] * 6)

    ClientAvailability = dataTypeCreator(
        'Client Availability',
        'ClientAvailability',
        ValidationType.DateTime,
        DataTypeSection.Client,
        [UserType.Client] * 6)

    # ======================================================================
    # Job

    JobTitle = dataTypeCreator(
        'Job Title',
        'JobTitle',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobLocation = dataTypeCreator(
        'Job Location',
        'JobLocation',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobType = dataTypeCreator(
        'Job Type',
        'JobType',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobAnnualSalary = dataTypeCreator(
        'Job Annual Salary',
        'JobAnnualSalary',
        ValidationType.Salary,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobDayRate = dataTypeCreator(
        'Job Day Rate',
        'JobDayRate',
        ValidationType.Salary,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobEssentialSkills = dataTypeCreator(
        'Job Essential Skills',
        'JobEssentialSkills',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobLinkURL = dataTypeCreator(
        'Job Link URL',
        'JobLinkURL',
        ValidationType.URL,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobEndDate = dataTypeCreator(
        'Job End Date',
        'JobEndDate',
        ValidationType.DateTime,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobStartDate = dataTypeCreator(
        'Job Start Date',
        'JobStartDate',
        ValidationType.DateTime,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobYearsRequired = dataTypeCreator(
        'Job Years Required',
        'JobYearsRequired',
        ValidationType.Number,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])
