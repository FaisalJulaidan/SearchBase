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

@unique
class DataType(Enum):
    # ===============================================================================================
    # IMPORTANT: make sure when you edit or add new DataType to change the JSON schemas accordingly.
    # You know just ask Faisal Julaidan before making any changes.
    # ===============================================================================================
    NoType = {'name': 'None', 'validation': None}
    Email = {'name': 'Email', 'validation': ValidationType.Email.value}
    Telephone = {'name': 'Telephone', 'validation': ValidationType.Telephone.value}
    ContactTime = {'name': 'Contact Time', 'validation': ValidationType.Email.value}
    DesiredSalary = {'name': 'Desired Salary', 'validation': ValidationType.Number.value}
    Availability = {'name': 'Availability', 'validation': None}
    DesiredPosition = {'name': 'Desired Position', 'validation': None}
    DesiredPositionYearsExp = {'name': 'Desired Position Years Exp', 'validation': None}
    TopSkill = {'name': 'Top Skill', 'validation': None}
    TopSkillYearsExp = {'name': 'Top Skill Years Exp', 'validation': None}
    Resume = {'name': 'Resume', 'validation': None}
    LinkdinURL = {'name': 'Linkdin URL', 'validation': ValidationType.URL.value}
    DesiredLocation = {'name': 'Desired Location', 'validation': None}
    EmploymentType = {'name': 'Employment Type', 'validation': None}
    DesiredHourlyRate = {'name': 'Desired Hourly Rate', 'validation': None}


class UserType(Enum):
    Unknown = 'Unknown'
    Candidate = 'Candidate'
    Client = 'Client'