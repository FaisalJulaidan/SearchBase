from enum import Enum, unique
from typing import List

# ===============================================================================================
# IMPORTANT: make sure when you edit or add new Enums to change the JSON schemas accordingly.
# also don't forget to  migrate database tables where necessary e.g. ChatbotSession, Block
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
    JobSeeker = 'Job Seeker'
    CandidateSeeker = 'Candidate Seeker'


class DatabaseType(Enum):
    Candidates = {'name': 'Candidates', 'userType': UserType.CandidateSeeker }
    Jobs = {'name': 'Jobs', 'userType': UserType.JobSeeker }


# === Data Types Stuff === #
def dataTypeCreator(name: str, validation: ValidationType, userTypes: List[UserType]):
    return {'name': name,
            'validation': validation.value,
            'userTypes': [ut.value for ut in userTypes],
            }

@unique
class DataType(Enum):

    # Common
    NoType = dataTypeCreator('No Type', ValidationType.Ignore, [])

    Name = dataTypeCreator('Name',
                           ValidationType.String,
                           [UserType.JobSeeker, UserType.CandidateSeeker])

    Email = dataTypeCreator('Email',
                            ValidationType.Email,
                            [UserType.JobSeeker, UserType.CandidateSeeker])

    Telephone = dataTypeCreator('Telephone',
                                ValidationType.Telephone,
                                [UserType.JobSeeker, UserType.CandidateSeeker])

    LinkdinURL = dataTypeCreator('Linkdin URL',
                                 ValidationType.URL,
                                 [UserType.JobSeeker, UserType.CandidateSeeker])

    PostCode = dataTypeCreator('Post Code',
                               ValidationType.Ignore,
                               [UserType.JobSeeker, UserType.CandidateSeeker])

    # Candidate
    Gender = dataTypeCreator('Gender',
                             ValidationType.Ignore,
                             [UserType.JobSeeker])

    Degree = dataTypeCreator('Degree',
                             ValidationType.Ignore,
                             [UserType.JobSeeker])

    Resume = dataTypeCreator('Resume',
                             ValidationType.Ignore,
                             [UserType.JobSeeker])

    ContactTime = dataTypeCreator('Contact Time',
                                  ValidationType.Ignore,
                                  [UserType.JobSeeker])

    CurrentSalary = dataTypeCreator('Current Salary',
                                    ValidationType.Number,
                                    [UserType.JobSeeker])

    CurrentRole = dataTypeCreator('Current Role',
                                  ValidationType.Ignore,
                                  [UserType.JobSeeker])


    CurrentEmployer = dataTypeCreator('Current Employer',
                                      ValidationType.Ignore,
                                      [UserType.JobSeeker])

    CurrentEmploymentType = dataTypeCreator('Current Employment Type',
                                            ValidationType.Ignore,
                                            [UserType.JobSeeker])

    DesiredSalary = dataTypeCreator('Desired Salary',
                                    ValidationType.Number,
                                    [UserType.JobSeeker])

    DesiredPosition = dataTypeCreator('Desired Position',
                                      ValidationType.Ignore,
                                      [UserType.JobSeeker])

    CandidateSkills = dataTypeCreator('Candidate Skills',
                                      ValidationType.Ignore,
                                      [UserType.JobSeeker])

    YearsExp = dataTypeCreator('Years Exp',
                               ValidationType.Number,
                               [UserType.JobSeeker])

    PreferredLocation = dataTypeCreator('Preferred Location',
                                        ValidationType.Ignore,
                                        [UserType.JobSeeker])

    PreferredEmploymentType = dataTypeCreator('Desired Employment Type',
                                              ValidationType.Ignore,
                                              [UserType.JobSeeker])

    DesiredPayRate = dataTypeCreator('Desired Pay Rate',
                                     ValidationType.Number,
                                     [UserType.JobSeeker])

# Job

    OfferedJobTitle = dataTypeCreator('Offered Job Title',
                               ValidationType.Ignore,
                               [UserType.CandidateSeeker])

    JobAvailability = dataTypeCreator('Job Availability',
                                   ValidationType.Ignore,
                                   [UserType.CandidateSeeker])

