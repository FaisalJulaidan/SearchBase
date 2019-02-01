from enum import Enum, unique

# ===============================================================================================
# IMPORTANT: make sure when you edit or add new Enums to change the JSON schemas accordingly.
# also don't forget to  migrate database tables where necessary e.g. ChatbotSession, Block
# You know just ask Faisal Julaidan before making any changes.
# STEP TO FOLLOW
# 1. Change the Enum
# 2. Make the change accordingly to the JSON Schema
# 3. Migrate the Database accordingly
# ===============================================================================================


class ValidationType(Enum):
    Ignore = 'Ignore'
    Email = 'Email'
    Telephone = 'Telephone'
    Number = 'Number'
    Name = 'Name'
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
    Client = 'Client'
    Candidate = 'Candidate'
    Job = 'Job'


@unique
class DataType(Enum):

    # Common
    NoType = {'name': 'No Type', 'validation': ValidationType.Ignore.value,
              'userTypes': []}

    Name = {'name': 'Name', 'validation': ValidationType.Name.value,
             'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Email = {'name': 'Email', 'validation': ValidationType.Email.value,
             'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Telephone = {'name': 'Telephone', 'validation': ValidationType.Telephone.value,
                 'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    LinkdinURL = {'name': 'Linkdin URL', 'validation': ValidationType.URL.value,
              'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    # Candidate
    Gender = {'name': 'Gender', 'validation': ValidationType.Ignore.value,
              'userTypes': [UserType.Candidate.value]}

    Degree = {'name': 'Degree', 'validation': ValidationType.Ignore.value,
              'userTypes': [UserType.Candidate.value]}

    Resume = {'name': 'Resume', 'validation': ValidationType.Ignore.value,
              'userTypes': [UserType.Candidate.value]}

    ContactTime = {'name': 'Contact Time', 'validation': ValidationType.Email.value,
                   'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Availability = {'name': 'Availability', 'validation': ValidationType.Ignore.value,
                    'userTypes': [UserType.Candidate.value]}

    CurrentSalary = {'name': 'Current Salary', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

    CurrentRole = {'name': 'Current Role', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

    DesiredPosition = {'name': 'Desired Position', 'validation': ValidationType.Ignore.value,
                       'userTypes': [UserType.Candidate.value]}

    DesiredSalary = {'name': 'Desired Salary', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

    CandidateSkills = {'name': 'Candidate Skills', 'validation': ValidationType.Ignore.value,
                'userTypes': [UserType.Candidate.value]}

    YearsExp = {'name': 'Years Exp', 'validation': ValidationType.Ignore.value,
                        'userTypes': [UserType.Candidate.value]}

    PreferredLocation = {'name': 'Preferred Location', 'validation': ValidationType.Ignore.value,
                         'userTypes': [UserType.Candidate.value]}

    PreferredEmploymentType = {'name': 'Desired Employment Type', 'validation': ValidationType.Ignore.value,
                               'userTypes': [UserType.Candidate.value]}

    DesiredHourlyRate = {'name': 'Desired Hourly Rate', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

# Client
    Location = {'name': 'Location', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    NearbyStation = {'name': 'Nearby Station', 'validation': ValidationType.Ignore.value,
                'userTypes': [UserType.Client.value]}

    JobSalaryOffered = {'name': 'Job Salary Offered', 'validation': ValidationType.Number.value,
                    'userTypes': [UserType.Client.value]}

    EmploymentTypeOffered = {'name': 'Employment Type Offered', 'validation': ValidationType.Ignore.value,
                              'userTypes': [UserType.Client.value]}

    CandidatesNeeded = {'name': 'Candidates Needed', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Client.value]}

    EssentialSkills = {'name': 'Essential Skills', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    EssentialYearsExp = {'name': 'Essential Years Exp', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    ContractRate = {'name': 'Contract Rate', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Client.value]}

    JobDescription = {'name': 'Job Description', 'validation': ValidationType.Ignore.value,
                      'userTypes': [UserType.Client.value]}

    JobAvailability = {'name': 'Job Availability', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}



