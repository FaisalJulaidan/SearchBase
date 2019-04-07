from enums import CRM, UserType
from models import ChatbotSession, Assistant
from services.CRM import Adapt

# First Step
def processSession (session: ChatbotSession, assistant: Assistant):
    if session.UserType is UserType.Candidate:
        print("processSession insert Candidate")
        return insertCandidate("PartnerDomain9", "SD9USR7", "P@55word", session, CRM.Adapt)
    if session.UserType is UserType.Client:
        print("processSession insert Client")
        return insertClient("PartnerDomain9", "SD9USR7", "P@55word", session, CRM.Adapt)


def insertCandidate(domain, username, password, session: ChatbotSession, crm: CRM):
   if crm is CRM.Adapt:
       return Adapt.insertCandidate(domain, username, password, session)

def insertClient(domain, username, password, session: ChatbotSession, crm: CRM):
    if crm is CRM.Adapt:
        return Adapt.insertClient(domain, username, password, session)