from models import Callback
from services import assistant_services, databases_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.CRM.crm_services import searchCandidatesCustom
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.Messenger.messenger_servicess import sendMessage
from utilities import helpers
from utilities.enums import CRM


def sendCampaign(campaign_details, companyID):
    try:

        assistant_callback: Callback = assistant_services.getByID(campaign_details.get("assistant_id"), companyID)
        if not assistant_callback.Success:
            raise Exception("Assistant not found.")

        crm_callback: Callback = crm_services.getByID(campaign_details.get("crm_id"), companyID)
        if not crm_callback.Success:
            raise Exception("CRM not found.")

        messenger_callback: Callback = messenger_servicess.getByID(campaign_details.get("messenger_id"), companyID)
        if not messenger_callback.Success:
            raise Exception("Messenger not found.")

        assistant = assistant_callback.Data
        crm = crm_callback.Data
        messenger = messenger_callback.Data
        text = campaign_details.get("text")

        campaign_details["location"] = campaign_details.get("location").split(",")[0]

        if not text:
            raise Exception("Message text is missing")

        if campaign_details.get("use_crm"):
            candidates_callback: Callback = searchCandidatesCustom(crm, companyID, campaign_details, True)
        else:
            session = {
                "showTop": 200,
                "keywordsByDataType": {
                    "Candidate Location": [campaign_details.get("location")],
                    # "Job Annual Salary": ["1000-5000 GBP Annually"],
                    "Candidate Job Title": [campaign_details.get("jobTitle")],
                },
                "databaseType": "Jobs"
            }
            candidates_callback: Callback = databases_services.scan(session, helpers.encodeID(assistant.ID))

        if not candidates_callback.Success:
            raise Exception(candidates_callback.Message)

        for candidate in candidates_callback.Data:
            if campaign_details.get("use_crm") or crm.Type is CRM.Bullhorn:
                candidate_phone = candidate.get("CandidateMobile")
            else:
                raise Exception("CRM is not supported for this operation")

            if not candidate_phone:
                continue

            sendMessage(messenger.Type, candidate_phone, text, messenger.Auth)

        return Callback(True, '')

    except Exception as exc:
        helpers.logError("campaign_service.sendCampaign(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')
