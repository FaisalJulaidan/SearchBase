from models import Callback
from services import assistant_services
from services.Marketplace.CRM.crm_services import searchCandidatesCustom
from services.Marketplace.Messenger.mesenger_services import sendMessage
from utilities import helpers
from utilities.enums import CRM


def sendCampaign(campaign_details, companyID):
    try:

        assistant_callback: Callback = assistant_services.getByID(campaign_details.get("assistant_id"), companyID)
        if not assistant_callback.Success:
            raise Exception("Assistant not found.")

        assistant = assistant_callback.Data
        crm_type = assistant.CRM.Type
        messenger = assistant.Messenger
        text = campaign_details.get("text")

        if not text:
            raise Exception("Message text is missing")

        candidates_callback: Callback = searchCandidatesCustom(assistant, campaign_details, True)
        if not candidates_callback.Success:
            raise Exception(candidates_callback.Message)

        for candidate in candidates_callback.Data:
            if crm_type is CRM.Bullhorn:
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
