from enum import Enum, unique
from typing import List

# ===============================================================================================
# IMPORTANT: don't forget to  migrate database tables where necessary e.g. ChatbotSession, Block
# You know just ask Faisal Julaidan before making any changes.
# STEPS TO FOLLOW
# 1. Change the Enum
# 2. Migrate the Database accordingly
# ===============================================================================================

# TODO What should be stored in the json is the enum name not value this will need a new parsing system for flow and
# TODO Chatbot session. but is important before the lunch as it will have significant benefits to the system


class BlockType(Enum):
    UserInput = 'User Input'
    Question = 'Question'
    FileUpload = 'File Upload'
    Solutions = 'Solutions'
    RawText = 'Raw Text'


class BlockAction(Enum):

    GoToNextBlock = 'Go To Next Block'
    GoToSpecificBlock = 'Go To Specific Block'
    GoToGroup = 'Go To Group'
    EndChat = 'End Chat'


class UserType(Enum):
    Unknown = 'Unknown'
    Candidate = 'Candidate'
    Client = 'Client'


class DatabaseType(Enum):
    # multiplying userTypes by 3 will help detect the user type in the chatbot
    Candidates = {'enumName': 'Candidates', 'name': 'Candidates', 'userTypes':[UserType.Client.value] * 5}
    Jobs = {'enumName': 'Candidates', 'name': 'Jobs', 'userTypes':[UserType.Candidate.value] * 5}


@unique
class DataTypeSection(Enum):
    NoType = 'No Type'
    Client = 'Client'
    Candidate = 'Candidate'
    Job = 'Job'

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

# === Data Types Stuff === #
def dataTypeCreator(name: str, enumName: str , validation: ValidationType, section: DataTypeSection, userTypes: List[UserType]):
    return {'name': name,
            'enumName': enumName,
            'validation': validation.value,
            'dataTypeSection': section.value,
            'userTypes': [ut.value for ut in userTypes],
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
        [UserType.Client])

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

    CandidateDesiredSalary = dataTypeCreator(
        'Candidate Desired Salary',
        'CandidateDesiredSalary',
        ValidationType.Number,
        DataTypeSection.Candidate,
        [UserType.Candidate])

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

    JobSalary = dataTypeCreator(
        'Job Salary',
        'JobSalary',
        ValidationType.Number,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobEssentialSkills = dataTypeCreator(
        'Job Essential Skills',
        'Job Essential Skills',
        ValidationType.String,
        DataTypeSection.Job,
        [UserType.Candidate, UserType.Client])

    JobDesiredSkills = dataTypeCreator(
        'Job Desired Skills',
        'JobDesiredSkills',
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

    # ======================================================================
    # Client
    # The chances of asking a question with a client data type is very low. however when is it asked it means most of
    # the time that this user type is a client. For that reason we multiplied Client UserType by 5 to increase
    # the probability of the userType being a Client at the end :)

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