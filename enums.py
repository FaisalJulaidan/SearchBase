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

    DesiredSalary = {'name': 'Desired Salary', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

    DesiredPosition = {'name': 'Desired Position', 'validation': ValidationType.Ignore.value,
                       'userTypes': [UserType.Candidate.value]}

    # DesiredPositionYearsExp = {'name': 'Desired Position Years Exp', 'validation': ValidationType.Ignore.value,
    #                            'userTypes': [UserType.Candidate.value]}

    TopSkills = {'name': 'Top Skills', 'validation': ValidationType.Ignore.value,
                'userTypes': [UserType.Candidate.value]}

    YearsExp = {'name': 'Years Exp', 'validation': ValidationType.Ignore.value,
                        'userTypes': [UserType.Candidate.value]}


    DesiredLocation = {'name': 'Desired Location', 'validation': ValidationType.Ignore.value,
                       'userTypes': [UserType.Candidate.value]}

    DesiredEmploymentType = {'name': 'Desired Employment Type', 'validation': ValidationType.Ignore.value,
                      'userTypes': [UserType.Candidate.value]}

    DesiredHourlyRate = {'name': 'Desired Hourly Rate', 'validation': ValidationType.Number.value,
                         'userTypes': [UserType.Candidate.value]}


    # Client

    ClientName = {'name': 'Name of the Client\'s company', 'validation': ValidationType.Name.value,
            'userTypes': [UserType.Client.value]}

    ClientEmail = {'name': 'Email', 'validation': ValidationType.Email.value,
             'userTypes': [UserType.Client.value]}

    ClientTelephone = {'name': 'Telephone', 'validation': ValidationType.Telephone.value,
                 'userTypes': [UserType.Client.value]}

    Location = {'name': 'Location', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    NearbyStation = {'name': 'Nearby Station', 'validation': ValidationType.Ignore.value,
                'userTypes': [UserType.Client.value]}

    OfferingSalary = {'name': 'Offering Salary', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Client.value]}

    OfferingEmploymentType = {'name': 'Offering Employment Type', 'validation': ValidationType.Ignore.value,
                      'userTypes': [UserType.Client.value]}

    EssentialSkills = {'name': 'Essential Skills', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    EssentialYearsExperience = {'name': 'Essential years of experience', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    JobType = {'name': 'Type of Job (Perm/Contract)', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    JobSalary = {'name': 'Salary being offered', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

    JobRate = {'name': 'Contract Rate', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}


    JobAvailability = {'name': 'Availability Of the Job', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}


    DesiredSkills = {'name': 'Desired Skills', 'validation': ValidationType.Ignore.value,
                     'userTypes': [UserType.Client.value]}

