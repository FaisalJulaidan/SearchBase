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
    Name = 'Name'
    URL = 'URL'
    PostCode = 'Post Code'


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



# === Data Types Stuff === #
def dataTypeCreator(name: str, validation: ValidationType, userTypes: List[UserType]):
    return {'name': name,
            'validation': validation.value,
            'userTypes': [ut.value for ut in userTypes]}

@unique
class DataType(Enum):

    # Common
    NoType = dataTypeCreator('No Type', ValidationType.Ignore, [])

    Name = dataTypeCreator('Name', ValidationType.Name, [UserType.Candidate, UserType.Client])

    Email = dataTypeCreator('Email', ValidationType.Email, [UserType.Candidate, UserType.Client])

    Telephone = dataTypeCreator('Telephone', ValidationType.Telephone, [UserType.Candidate, UserType.Client])

    LinkdinURL = dataTypeCreator('Linkdin URL', ValidationType.URL, [UserType.Candidate, UserType.Client])

    PostCode = dataTypeCreator('Post Code', ValidationType.PostCode, [UserType.Candidate, UserType.Client])

    # Candidate
    Gender = dataTypeCreator('Gender', ValidationType.Ignore, [UserType.Candidate])

    Degree = dataTypeCreator('Degree', ValidationType.Ignore, [UserType.Candidate])

    Resume = dataTypeCreator('Resume', ValidationType.Ignore, [UserType.Candidate])

    ContactTime = dataTypeCreator('Contact Time', ValidationType.Ignore, [UserType.Candidate])

    Availability = dataTypeCreator('Availability', ValidationType.Ignore, [UserType.Candidate])

    CurrentSalary = dataTypeCreator('Current Salary', ValidationType.Number, [UserType.Candidate])

    CurrentRole = dataTypeCreator('Current Role', ValidationType.Ignore, [UserType.Candidate])

    JobTitle = dataTypeCreator('Job Title', ValidationType.Ignore, [UserType.Candidate])

    CurrentEmployer = dataTypeCreator('Current Employer', ValidationType.Ignore, [UserType.Candidate])

    CurrentEmploymentType = dataTypeCreator('Current Employment Type', ValidationType.Ignore, [UserType.Candidate])

    DesiredSalary = dataTypeCreator('Desired Salary', ValidationType.Number, [UserType.Candidate])

    DesiredPosition = dataTypeCreator('Desired Position', ValidationType.Ignore, [UserType.Candidate])

    CandidateSkills = dataTypeCreator('Candidate Skills', ValidationType.Ignore, [UserType.Candidate])

    YearsExp = dataTypeCreator('Years Exp', ValidationType.Number, [UserType.Candidate])

    PreferredLocation = dataTypeCreator('Preferred Location', ValidationType.Ignore, [UserType.Candidate])

    PreferredEmploymentType = dataTypeCreator('Desired Employment Type', ValidationType.Ignore, [UserType.Candidate])

    DesiredHourlyRate = dataTypeCreator('Desired Hourly Rate', ValidationType.Number, [UserType.Candidate])

# Client
    Location = dataTypeCreator('Location', ValidationType.Ignore, [UserType.Client])

    NearbyStation = dataTypeCreator('Nearby Station', ValidationType.Ignore, [UserType.Client])

    JobSalaryOffered = dataTypeCreator('Job Salary Offered', ValidationType.Number, [UserType.Client])

    EmploymentTypeOffered = dataTypeCreator('Employment Type Offered', ValidationType.Ignore, [UserType.Client])

    CandidatesNeeded = dataTypeCreator('Candidates Needed', ValidationType.Number, [UserType.Client])

    EssentialSkills = dataTypeCreator('Essential Skills', ValidationType.Ignore, [UserType.Client])

    EssentialYearsExp = dataTypeCreator('Essential Years Exp', ValidationType.Number, [UserType.Client])

    ContractRate = dataTypeCreator('Contract Rate', ValidationType.Number,[UserType.Client])

    JobDescription = dataTypeCreator('Job Description', ValidationType.Ignore, [UserType.Client])

    JobAvailability = dataTypeCreator('Job Availability', ValidationType.Ignore, [UserType.Client])



