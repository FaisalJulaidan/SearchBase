from copy import deepcopy

from sqlalchemy import and_

from models import Callback, db, Campaign
from services import assistant_services, databases_services, mail_services, url_services, company_services
from services.Marketplace.CRM import crm_services
from services.Marketplace.Messenger import messenger_servicess
from utilities import helpers
from utilities.enums import CRM, DataType as DT, DatabaseType


def getByID(campaign_id: int, companyID: int):
    try:
        # Get result and check if None then raise exception
        result = db.session.query(Campaign) \
            .filter(and_(Campaign.ID == campaign_id, Campaign.CompanyID == companyID)).first()
        if not result: raise Exception
        # result.Skills = str(result.Skills).replace("[", "").replace("]", "").replace("'", "")
        # result.Skills = result.Skills.split(", ")
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

        # for r in result:
        # r.Skills = str(r.Skills).replace("[", "").replace("]", "").replace("'", "")
        # r.Skills = r.Skills.split(", ")

        return Callback(True, "Campaigns have been retrieved", result)

    except Exception as exc:
        db.session.rollback()
        helpers.logError("campaign_services.getAll(): " + str(exc))
        return Callback(False, 'Could not get campaigns.')


# save and update
def save(campaign_details, companyID, campaignID=None):
    try:
        if campaignID:
            campaign_callback = getByID(campaignID, companyID)
            if not campaign_callback.Success:
                raise Exception(campaign_callback.Message)

            campaign = campaign_callback.Data
        else:
            campaign = Campaign()

        # skills = campaign_details.get("skills")
        # if campaign_details.get("skills"):
        #     print(campaign_details.get("skills"))
        #     skills = ",".join(campaign_details.get("skills"))
        # else:
        #     skills = ""
        campaign.Name = campaign_details.get("name")
        campaign.PreferredJobTitle = campaign_details.get("preferredJobTitle")
        campaign.Skills = str(campaign_details.get("skills", "[]"))
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
                                                           'Active',
                                                           'UserID'],
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
        campaign_details["location"] = campaign_details.get("location", "").split(",")[0]

        if campaign_details.get("use_crm"):
            crm_callback: Callback = crm_services.getByID(campaign_details.get("crm_id"), companyID)
            if not crm_callback.Success:
                raise Exception("CRM not found.")

            candidates_callback: Callback = crm_services.searchCandidatesCustom(crm_callback.Data, companyID,
                                                                                campaign_details, True,
                                                                                perfect=campaign_details.get("perfect_match"),
                                                                                shortlist=campaign_details.get("shortlist"))
        else:
            session = {
                "showTop": 2000000,
                "keywordsByDataType": {
                    DT.CandidateCity.value['name']: [campaign_details.get("location")],
                    # DT.JobSalary.value['name']: ["1000-5000 GBP Annually"],
                    DT.PreferredJobTitle.value['name']: [campaign_details.get("preferredJobTitle")],
                    DT.CandidateSkills.value['name']: campaign_details.get("skills"),
                },
                "databaseType": DatabaseType.Candidates.name
            }
            candidates_callback: Callback = databases_services.scan(session, helpers.encodeID(
                                                                    campaign_details.get("assistant_id")),
                                                                    True, campaign_details.get("database_id"))

        if not candidates_callback.Success:
            raise Exception(candidates_callback.Message)

        if candidates_callback.Data:
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
        text = campaign_details.get("text")
        if not text:
            raise Exception("Message text is missing")

        outreach_type = campaign_details.get("outreach_type")
        messenger = None
        if outreach_type == "sms" or outreach_type == "whatsapp":
            messenger_callback: Callback = messenger_servicess.getByID(campaign_details.get("messenger_id"), companyID)
            if not messenger_callback.Success:
                raise Exception("Messenger not found.")

            messenger = messenger_callback.Data

        hashedAssistantID = helpers.encodeID(campaign_details.get("assistant_id"))
        source = 'crm' if campaign_details.get("use_crm") else 'db'
        sourceID = campaign_details.get("crm_id") if source == 'crm' else campaign_details.get("database_id")

        failedCandidates = 0
        totalCandidates = len(campaign_details.get("candidate_list"))

        for candidate in campaign_details.get("candidate_list"):
            candidate_phone = candidate.get("CandidateMobile")
            candidate_email = candidate.get("CandidateEmail")

            # check if phone or email is needed and present
            if (not candidate_phone and (outreach_type == "sms" or outreach_type == "whatsapp")) \
                    or (not candidate_email and outreach_type == "email"):
                failedCandidates += 1
                continue

            access = helpers.verificationSigner.dumps(
                {"candidateID": candidate.get("ID"), "source": source, "sourceID": sourceID}, salt='chatbot')

            url: Callback = url_services.createShortenedURL(helpers.getDomain(3000) + "/chatbot_direct_link/" + \
                                                            hashedAssistantID + "?candidate=" + str(access),
                                                            domain="recruitbot.ai")
            if not url.Success:
                failedCandidates += 1
                continue

            # insert assistant link and candidate details in text
            tempText = text \
                .replace("${assistantLink}$", url.Data) \
                .replace("${candidateName}$", candidate.get("CandidateName"))

            if outreach_type == "sms" or outreach_type == "whatsapp":
                whatsapp = True if outreach_type == "whatsapp" else False
                messenger_servicess.sendMessage(messenger.Type, candidate_phone, tempText, messenger.Auth, whatsapp)
            elif outreach_type == "email":
                mail_services.simpleSend(candidate_email, campaign_details.get("email_title"), tempText)

        if failedCandidates == totalCandidates:
            raise Exception("Campaign Failed due to 0 contact details or problem with URL shortening")

        return Callback(True, 'Campaign sent! ' + str(failedCandidates) + " out of " + str(totalCandidates) +
                        " candidates did not have contact details and were not contacted.")

    except Exception as exc:
        helpers.logError("campaign_services.sendCampaign(): " + str(exc))
        return Callback(False, 'Error while sending campaign!')


def updateStatus(campaignID, newStatus, companyID):
    try:

        if newStatus is None: raise Exception("Please provide the new status true/false")
        db.session.query(Campaign).filter(and_(Campaign.ID == campaignID, Campaign.CompanyID == companyID)) \
            .update({"Active": newStatus})

        db.session.commit()
        return Callback(True, 'Campaign status has been changed.')

    except Exception as exc:
        helpers.logError("campaign_services.updateStatus(): " + str(exc))
        db.session.rollback()
        return Callback(False, "Could not change the Campaign's status.")


def getShortlists(crm_id, companyID, listID=None):
    crm = None
    if crm_id:
        crm_callback: Callback = crm_services.getByID(crm_id, companyID)
        if not crm_callback.Success:
            raise Exception("CRM not found.")
        crm = crm_callback.Data

    return crm_services.getShortlists(crm.Auth, crm.Type, companyID, listID)
