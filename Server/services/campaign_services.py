from sqlalchemy import and_

from models import Callback, db, Campaign
from services import assistant_services, databases_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.Messenger import messenger_servicess
from utilities import helpers
from utilities.enums import CRM


def getByID(campaign_id: int, companyID: int):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Campaign) \
            .filter(and_(Campaign.ID == campaign_id, Campaign.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got campaign successfully.", result)

    except Exception as exc:
        helpers.logError("campaign_services.getByID(): " + str(exc))
        return Callback(False, 'Could not get the campaign.')


def getAll(companyID) -> Callback:
    try:
        if not companyID:
            raise Exception("Company ID have not been provided")

        result = db.session.query(Campaign) \
            .filter(Campaign.CompanyID == companyID).all()

        if len(result) == 0:
            return Callback(True, "No campaigns found", [])

        return Callback(True, "Campaigns have been retrieved", result)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("campaign_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get campaigns.')


def save(campaign_details, companyID, campaignID=None):
    try:
        if campaignID:
            campaign_callback = getByID(campaignID, companyID)
            if not campaign_callback.Success:
                raise Exception(campaign_callback.Message)

            campaign = campaign_callback.Data
        else:
            campaign = Campaign()

        campaign.Name = campaign_details.get("name")
        campaign.JobTitle = campaign_details.get("jobTitle")
        campaign.Skills = str(campaign_details.get("skills"))
        campaign.Location = campaign_details.get("location")
        campaign.Message = campaign_details.get("message")
        campaign.UseCRM = campaign_details.get("use_crm")
        campaign.CompanyID = companyID
        campaign.AssistantID = campaign_details.get("assistant_id")
        campaign.MessengerID = campaign_details.get("messenger_id")
        campaign.DatabaseID = campaign_details.get("database_id")
        campaign.CRMID = campaign_details.get("crm_id")

        if not campaignID:
            db.session.add(campaign)
        db.session.commit()

        return Callback(True, 'Campaign Saved', campaign)

    except Exception as exc:
        helpers.logError("campaign_services.save(): " + str(exc))
        return Callback(False, 'Error while saving the campaign!')


def removeByID(campaignID, companyID) -> Callback:
    try:
        db.session.query(Campaign).filter(and_(Campaign.ID == campaignID, Campaign.CompanyID == companyID)).delete()
        db.session.commit()
        return Callback(True, 'Campaign has been deleted.')

    except Exception as exc:
        helpers.logError("assistant_services.removeByID(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Error in deleting campaign.')


def getCampaignOptions(companyID):
    try:

        # fetch Assistants
        assistants_callback: Callback = assistant_services.getAll(companyID)
        if not assistants_callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Assistants")

        # fetch CRMs
        crms_callback: Callback = crm_services.getAll(companyID)
        if not crms_callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch CRMs")

        # fetch Messengers
        messengers_callback: Callback = messenger_servicess.getAll(companyID)
        if not messengers_callback.Success:
            return helpers.jsonResponse(False, 404, "Cannot fetch Messengers")

        # fetch Databases
        databases_callback: Callback = databases_services.getDatabasesList(companyID)
        if not databases_callback.Success:
            return helpers.jsonResponse(False, 400, "Cannot fetch Databases")

        return Callback(True, "Information has been retrieved", {
            "assistants": helpers.getListFromLimitedQuery(['ID',
                                                           'Name',
                                                           'Description',
                                                           'Message',
                                                           'TopBarText',
                                                           'Active'],
                                                          assistants_callback.Data),
            "crms": helpers.getListFromSQLAlchemyList(
                crms_callback.Data),
            "messengers": helpers.getListFromSQLAlchemyList(
                messengers_callback.Data),
            "databases": helpers.getListFromSQLAlchemyList(
                databases_callback.Data)
        })

    except Exception as exc:
        helpers.logError("campaign_services.getCampaignOptions(): " + str(exc))
        return Callback(False, 'Error while searching the information!')


def prepareCampaign(campaign_details, companyID):
    try:
        hashedAssistantID = helpers.encodeID(campaign_details.get("assistant_id"))
        campaign_details["location"] = campaign_details.get("location").split(",")[0]

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
        print(candidates_callback.Message)
        print(candidates_callback.Data)
        if not candidates_callback.Success:
            raise Exception(candidates_callback.Message)
        for candidate in candidates_callback.Data:
            if candidate.get("Currency"):
                candidate["Currency"] = ""

        campaign_details["candidate_list"] = candidates_callback.Data

        return Callback(True, 'Campaign Ready', campaign_details)

    except Exception as exc:
        helpers.logError("campaign_services.prepareCampaign(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')


def sendCampaign(campaign_details, companyID):
    try:
        messenger_callback: Callback = messenger_servicess.getByID(campaign_details.get("messenger_id"), companyID)
        if not messenger_callback.Success:
            raise Exception("Messenger not found.")

        messenger = messenger_callback.Data
        crm = None
        hashedAssistantID = helpers.encodeID(campaign_details.get("assistant_id"))
        source = "crm" if campaign_details.get("use_crm") else "database"
        text = campaign_details.get("text") + "\n\n" + helpers.getDomain() + "/chatbot_direct_link/" + \
               hashedAssistantID + "?source=" + source + "&source_id=" + \
               str(campaign_details.get("crm_id", campaign_details.get("database_id")))

        if not text:
            raise Exception("Message text is missing")

        for candidate in campaign_details.get("candidate_list"):
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
            # insert candidate id in link
            text = text.split("&id")[0]
            text += "&id=" + str(candidate.get("ID"))

            messenger_servicess.sendMessage(messenger.Type, candidate_phone, text, messenger.Auth)

        return Callback(True, '')

    except Exception as exc:
        helpers.logError("campaign_services.sendCampaign(): " + str(exc))
        return Callback(False, 'Error while search the database for matches!')
