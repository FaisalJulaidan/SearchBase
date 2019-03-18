from enum import Enum, unique
from typing import List

# ===============================================================================================
# IMPORTANT: don't forget to  migrate database tables where necessary e.g. ChatbotSession, Block
# You know just ask Faisal Julaidan before making any changes.
# STEPS TO FOLLOW
# 1. Change the Enum
# 2. Migrate the Database accordingly
# ===============================================================================================


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


class BlockType(Enum):
    UserInput = 'User Input'
    Question = 'Question'
    FileUpload = 'File Upload'
    Solutions = 'Solutions'


class BlockAction(Enum):

    GoToNextBlock = 'Go To Next Block'
    GoToSpecificBlock = 'Go To Specific Block'
    GoToGroup = 'Go To Group' # Will use Go To Specific Block
    EndChat = 'End Chat'


class UserType(Enum):
    Unknown = 'Unknown'
    Candidate = 'Candidate'
    Client = 'Client'


class DatabaseType(Enum):
    Candidates = {'name': 'Candidates'}
    Jobs = {'name': 'Jobs'}


@unique
class DataTypeSection(Enum):
    NoType = 'No Type'
    Client = 'Client'
    Candidate = 'Candidate'
    Job = 'Job'


# === Data Types Stuff === #
def dataTypeCreator(name: str, validation: ValidationType, section: DataTypeSection, userTypes: List[UserType]):
    return {'name': name,
            'validation': validation.value,
            'dataTypeSection': section.value,
            'userTypes': [ut.value for ut in userTypes],
            }

@unique
class DataType(Enum):

    # Candidate
    NoType = dataTypeCreator('No Type', ValidationType.Ignore, DataTypeSection.NoType, [UserType.Unknown])

    CandidateName = dataTypeCreator('Candidate Name',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateEmail = dataTypeCreator('Candidate Email',
                                    ValidationType.Email,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateMobile = dataTypeCreator('Candidate Mobile',
                                    ValidationType.Telephone,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateLinkdinURL = dataTypeCreator('Candidate Linkdin URL',
                                    ValidationType.URL,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateCV = dataTypeCreator('Candidate CV',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])


    CandidateAvailability = dataTypeCreator('Candidate Availability',
                                    ValidationType.DateTime,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateLocation = dataTypeCreator('Candidate Location',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateSkills = dataTypeCreator('Candidate Skills',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateJobTitle = dataTypeCreator('Candidate Job Title',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateEducation = dataTypeCreator('Candidate Education',
                                    ValidationType.String,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateYearsExperience = dataTypeCreator('Candidate Years Experience',
                                    ValidationType.Number,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    CandidateDesiredSalary = dataTypeCreator('Candidate Desired Salary',
                                    ValidationType.Number,
                                    DataTypeSection.Candidate,
                                    [UserType.Candidate])

    # ======================================================================
    # Job

    JobTitle = dataTypeCreator('Job Title',
                                ValidationType.String,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobLocation = dataTypeCreator('Job Location',
                                ValidationType.String,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobType = dataTypeCreator('Job Type',
                                ValidationType.String,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobSalary = dataTypeCreator('Job Salary',
                                ValidationType.String,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobEssentialSkills = dataTypeCreator('Job Essential Skills',
                                ValidationType.String,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobDesiredSkills = dataTypeCreator('Job Desired Skills',
                                         ValidationType.String,
                                         DataTypeSection.Job,
                                         [UserType.Candidate, UserType.Client])

    JobLinkURL = dataTypeCreator('Job Link URL',
                                ValidationType.URL,
                                DataTypeSection.Job,
                                [UserType.Candidate, UserType.Client])

    JobEndDate = dataTypeCreator('Job End Date',
                                 ValidationType.DateTime,
                                 DataTypeSection.Job,
                                 [UserType.Candidate, UserType.Client])

    JobStartDate = dataTypeCreator('Job Start Date',
                                    ValidationType.DateTime,
                                    DataTypeSection.Job,
                                    [UserType.Candidate, UserType.Client])

    # ======================================================================
    # Client

    ClientName = dataTypeCreator('Client Name',
                                  ValidationType.String,
                                  DataTypeSection.Client,
                                  [UserType.Client])

    ClientEmail = dataTypeCreator('Client Email',
                                  ValidationType.Email,
                                  DataTypeSection.Client,
                                  [UserType.Client])

    ClientTelephone = dataTypeCreator('Client Telephone',
                                    ValidationType.Telephone,
                                    DataTypeSection.Client,
                                    [UserType.Client])

    ClientLocation = dataTypeCreator('Client Location',
                                    ValidationType.String,
                                    DataTypeSection.Client,
                                    [UserType.Client])