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
    Candidate = 'Candidate'
    Client = 'Client'


class DatabaseType(Enum):
    Candidates = 'Candidates'
    Jobs = 'Jobs'
    Clients = 'Clients' # Not supported yet




# === Data Types Stuff === #
def dataTypeCreator(name: str, validation: ValidationType, userTypes: List[UserType], databaseTypes: List[DatabaseType]):
    return {'name': name,
            'validation': validation.value,
            'userTypes': [ut.value for ut in userTypes],
            'databaseTypes': [dt.value for dt in databaseTypes]
            }

@unique
class DataType(Enum):

    # Common
    NoType = dataTypeCreator('No Type', ValidationType.Ignore, [], [])

    Name = dataTypeCreator('Name',
                           ValidationType.String,
                           [UserType.Candidate, UserType.Client],
                           [DatabaseType.Candidates, DatabaseType.Clients])

    Email = dataTypeCreator('Email',
                            ValidationType.Email,
                            [UserType.Candidate,
                             UserType.Client],
                            [DatabaseType.Candidates, DatabaseType.Clients])

    Telephone = dataTypeCreator('Telephone',
                                ValidationType.Telephone,
                                [UserType.Candidate, UserType.Client],
                                [DatabaseType.Candidates, DatabaseType.Clients])

    LinkdinURL = dataTypeCreator('Linkdin URL',
                                 ValidationType.URL,
                                 [UserType.Candidate, UserType.Client],
                                 [DatabaseType.Candidates, DatabaseType.Clients])

    PostCode = dataTypeCreator('Post Code',
                               ValidationType.Ignore,
                               [UserType.Candidate, UserType.Client],
                               [DatabaseType.Candidates, DatabaseType.Clients])

    # Candidate
    Gender = dataTypeCreator('Gender',
                             ValidationType.Ignore,
                             [UserType.Candidate],
                             [DatabaseType.Candidates])

    Degree = dataTypeCreator('Degree',
                             ValidationType.Ignore,
                             [UserType.Candidate],
                             [DatabaseType.Candidates])

    Resume = dataTypeCreator('Resume',
                             ValidationType.Ignore,
                             [UserType.Candidate],
                             [DatabaseType.Candidates])

    ContactTime = dataTypeCreator('Contact Time',
                                  ValidationType.Ignore,
                                  [UserType.Candidate],
                                  [DatabaseType.Candidates])

    Availability = dataTypeCreator('Availability',
                                   ValidationType.Ignore,
                                   [UserType.Candidate],
                                   [DatabaseType.Candidates])

    CurrentSalary = dataTypeCreator('Current Salary',
                                    ValidationType.Number,
                                    [UserType.Candidate],
                                    [DatabaseType.Candidates])

    CurrentRole = dataTypeCreator('Current Role',
                                  ValidationType.Ignore,
                                  [UserType.Candidate],
                                  [DatabaseType.Candidates])

    JobTitle = dataTypeCreator('Job Title',
                               ValidationType.Ignore,
                               [UserType.Candidate],
                               [DatabaseType.Candidates])

    CurrentEmployer = dataTypeCreator('Current Employer',
                                      ValidationType.Ignore,
                                      [UserType.Candidate],
                                      [DatabaseType.Candidates])

    CurrentEmploymentType = dataTypeCreator('Current Employment Type',
                                            ValidationType.Ignore,
                                            [UserType.Candidate],
                                            [DatabaseType.Candidates])

    DesiredSalary = dataTypeCreator('Desired Salary',
                                    ValidationType.Number,
                                    [UserType.Candidate],
                                    [DatabaseType.Candidates])

    DesiredPosition = dataTypeCreator('Desired Position',
                                      ValidationType.Ignore,
                                      [UserType.Candidate],
                                      [DatabaseType.Candidates])

    CandidateSkills = dataTypeCreator('Candidate Skills',
                                      ValidationType.Ignore,
                                      [UserType.Candidate],
                                      [DatabaseType.Candidates])

    YearsExp = dataTypeCreator('Years Exp',
                               ValidationType.Number,
                               [UserType.Candidate],
                               [DatabaseType.Candidates])

    PreferredLocation = dataTypeCreator('Preferred Location',
                                        ValidationType.Ignore,
                                        [UserType.Candidate],
                                        [DatabaseType.Candidates])

    PreferredEmploymentType = dataTypeCreator('Desired Employment Type',
                                              ValidationType.Ignore,
                                              [UserType.Candidate],
                                              [DatabaseType.Candidates])

    DesiredHourlyRate = dataTypeCreator('Desired Hourly Rate',
                                        ValidationType.Number,
                                        [UserType.Candidate],
                                        [DatabaseType.Candidates])

# Client
    Location = dataTypeCreator('Location',
                               ValidationType.Ignore,
                               [UserType.Client],
                               [DatabaseType.Clients])

    NearbyStation = dataTypeCreator('Nearby Station',
                                    ValidationType.Ignore,
                                    [UserType.Client],
                                    [DatabaseType.Clients])

    JobSalaryOffered = dataTypeCreator('Job Salary Offered',
                                       ValidationType.Number,
                                       [UserType.Client],
                                       [DatabaseType.Clients])

    EmploymentTypeOffered = dataTypeCreator('Employment Type Offered',
                                            ValidationType.Ignore,
                                            [UserType.Client],
                                            [DatabaseType.Clients])

    CandidatesNeeded = dataTypeCreator('Candidates Needed',
                                       ValidationType.Number,
                                       [UserType.Client],
                                       [DatabaseType.Clients])

    EssentialSkills = dataTypeCreator('Essential Skills',
                                      ValidationType.Ignore,
                                      [UserType.Client],
                                      [DatabaseType.Clients])

    EssentialYearsExp = dataTypeCreator('Essential Years Exp',
                                        ValidationType.Number,
                                        [UserType.Client],
                                        [DatabaseType.Clients])

    ContractRate = dataTypeCreator('Contract Rate',
                                   ValidationType.Number,
                                   [UserType.Client],
                                   [DatabaseType.Clients])

    JobDescription = dataTypeCreator('Job Description',
                                     ValidationType.Ignore,
                                     [UserType.Client],
                                     [DatabaseType.Clients])

    JobAvailability = dataTypeCreator('Job Availability',
                                      ValidationType.Ignore,
                                      [UserType.Client],
                                      [DatabaseType.Clients])


