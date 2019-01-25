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
    NoType = {'name': 'No Type', 'validation': ValidationType.Ignore.value}
    Email = {'name': 'Email', 'validation': ValidationType.Email.value}
    Telephone = {'name': 'Telephone', 'validation': ValidationType.Telephone.value}
    ContactTime = {'name': 'Contact Time', 'validation': ValidationType.Email.value}
    DesiredSalary = {'name': 'Desired Salary', 'validation': ValidationType.Number.value}
    Availability = {'name': 'Availability', 'validation': ValidationType.Ignore.value}
    DesiredPosition = {'name': 'Desired Position', 'validation': ValidationType.Ignore.value}
    DesiredPositionYearsExp = {'name': 'Desired Position Years Exp', 'validation': ValidationType.Ignore.value}
    TopSkill = {'name': 'Top Skill', 'validation': ValidationType.Ignore.value}
    TopSkillYearsExp = {'name': 'Top Skill Years Exp', 'validation': ValidationType.Ignore.value}
    Resume = {'name': 'Resume', 'validation': ValidationType.Ignore.value}
    LinkdinURL = {'name': 'Linkdin URL', 'validation': ValidationType.URL.value}
    DesiredLocation = {'name': 'Desired Location', 'validation': ValidationType.Ignore.value}
    EmploymentType = {'name': 'Employment Type', 'validation': ValidationType.Ignore.value}
    DesiredHourlyRate = {'name': 'Desired Hourly Rate', 'validation': ValidationType.Ignore.value}


class UserType(Enum):
    Unknown = 'Unknown'
    Candidate = 'Candidate'
    Client = 'Client'