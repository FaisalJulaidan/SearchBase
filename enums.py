from enum import Enum, unique

# ===============================================================================================
# IMPORTANT: before making any changes to this file please ask Faisal Julaidan.
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
    # ===============================================================================================
    # IMPORTANT: make sure when you edit or add new DataType to change the JSON schemas accordingly.
    # also don't forget to  migrate ChatbotSession table's records
    # You know just ask Faisal Julaidan before making any changes.
    # ===============================================================================================
    NoType = {'name': 'No Type', 'validation': ValidationType.Ignore.value,
              'userTypes': []}

    FullName = {'name': 'Full Name', 'validation': ValidationType.Name.value,
             'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Email = {'name': 'Email', 'validation': ValidationType.Email.value,
             'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Telephone = {'name': 'Telephone', 'validation': ValidationType.Telephone.value,
                 'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    Resume = {'name': 'Resume', 'validation': ValidationType.Ignore.value,
              'userTypes': [UserType.Candidate.value]}

    ContactTime = {'name': 'Contact Time', 'validation': ValidationType.Email.value,
                   'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    DesiredSalary = {'name': 'Desired Salary', 'validation': ValidationType.Number.value,
                     'userTypes': [UserType.Candidate.value]}

    Availability = {'name': 'Availability', 'validation': ValidationType.Ignore.value,
                    'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    DesiredPosition = {'name': 'Desired Position', 'validation': ValidationType.Ignore.value,
                       'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    DesiredPositionYearsExp = {'name': 'Desired Position Years Exp', 'validation': ValidationType.Ignore.value,
                               'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    TopSkill = {'name': 'Top Skill', 'validation': ValidationType.Ignore.value,
                'userTypes': [UserType.Candidate.value]}

    TopSkillYearsExp = {'name': 'Top Skill Years Exp', 'validation': ValidationType.Ignore.value,
                        'userTypes': [UserType.Candidate.value]}

    LinkdinURL = {'name': 'Linkdin URL', 'validation': ValidationType.URL.value,
                  'userTypes': [UserType.Candidate.value, UserType.Client.value]}

    DesiredLocation = {'name': 'Desired Location', 'validation': ValidationType.Ignore.value,
                       'userTypes': [UserType.Candidate.value]}

    EmploymentType = {'name': 'Employment Type', 'validation': ValidationType.Ignore.value,
                      'userTypes': [UserType.Candidate.value]}

    DesiredHourlyRate = {'name': 'Desired Hourly Rate', 'validation': ValidationType.Ignore.value,
                         'userTypes': [UserType.Candidate.value]}


