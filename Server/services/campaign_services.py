from models import Callback
from services import assistant_services, databases_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.Messenger import messenger_servicess
from services.Marketplace.Messenger.messenger_servicess import sendMessage
from utilities import helpers
from utilities.enums import CRM


def sendCampaign(campaign_details, companyID):
    try:
        messenger_callback: Callback = messenger_servicess.getByID(campaign_details.get("messenger_id"), companyID)
        if not messenger_callback.Success:
            raise Exception("Messenger not found.")

        hashedAssistantID = helpers.encodeID(campaign_details.get("assistant_id"))
        messenger = messenger_callback.Data
        crm = None
        source = "crm" if campaign_details.get("use_crm") else "database"
        text = campaign_details.get("text") + "\n\n" + helpers.getDomain() + "/chatbot_direct_link/" + \
               hashedAssistantID + "?source=" + source + "&source_id=" + \
               str(campaign_details.get("crm_id", campaign_details.get("database_id")))

        campaign_details["location"] = campaign_details.get("location").split(",")[0]

        if not text:
            raise Exception("Message text is missing")

        if campaign_details.get("use_crm"):
            crm_callback: Callback = crm_services.getByID(campaign_details.get("crm_id"), companyID)
            if not crm_callback.Success:
                raise Exception("CRM not found.")

            crm = crm_callback.Data

            candidates_callback: Callback = crm_services.searchCandidatesCustom(crm, companyID, campaign_details, True)
        else:
            session = {
                "showTop": 200,
                "keywordsByDataType": {
                    "Candidate Location": [campaign_details.get("location")],
                    # "Job Annual Salary": ["1000-5000 GBP Annually"],
                    "Candidate Job Title": [campaign_details.get("jobTitle")],
                },
                "databaseType": "Candidates"
            }
            candidates_callback: Callback = databases_services.scan(session, hashedAssistantID, True,
                                                                    campaign_details.get("database_id"))

        if not candidates_callback.Success:
            raise Exception(candidates_callback.Message)

        for candidate in candidates_callback.Data:
            if campaign_details.get("use_crm") and crm:
                if crm.Type is CRM.Bullhorn:
                    candidate_phone = candidate.get("CandidateMobile")
                else:
                    raise Exception("CRM is not supported for this operation")
            else:
                candidate_phone = candidate.get("CandidateMobile")

            if not candidate_phone:
                continue

            # insert candidate details in text
            text = text.replace("{candidate.name}", candidate.get("CandidateName"))

            # insert chatbot link
            text = text.split("&id")[0]
            text += "&id=" + str(candidate.get("ID"))
            print("TEXT: ", text)
            sendMessage(messenger.Type, candidate_phone, text, messenger.Auth)

        return Callback(True, '')

    except Exception as exc:
        helpers.logError("campaign_service.sendCampaign(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')
