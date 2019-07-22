import requests

from utilities.enums import Calendar as Calendar_Enum, CRM as CRM_Enum
from models import Callback
from services.Marketplace.CRM import crm_services
from services.Marketplace.Calendar import calendar_services
from utilities import helpers


# process the redirect from the auth callback
def connect(type, auth, companyID):
    try:

        # find the type and redirect to its service
        if CRM_Enum.has_value(type):
            return crm_services.connect(type, auth, companyID)
        elif Calendar_Enum.has_value(type):
            return calendar_services.connect(type, auth, companyID)
        else:
            return Callback(False, "The Marketplace object did not match any on the system")

    except Exception as exc:
        helpers.logError("Marketplace.marketplace_helpers.processRedirect() ERROR: " + str(exc))
        return Callback(False, str(exc))


# Test marketplace item connection (e.g. CRM, Calendar...)
def testConnection(type, companyID):
    try:

        # find the type and redirect to its service
        if CRM_Enum.has_value(type):

            # Check if connection exist
            exist_callback: Callback = crm_services.getCRMByType(type, companyID)
            if not exist_callback.Success:
                return Callback(True, "", {"Status": "NOT_CONNECTED"})

            # If yes test connection
            return Callback(True, "",
                            {"Status":
                                "CONNECTED" if crm_services
                                .testConnection(type, exist_callback.Data.Auth, companyID).Success else "FAILED"
                            })

        elif Calendar_Enum.has_value(type):

            # Check if connection exist
            exist_callback: Callback = calendar_services.getCalendarByType(type, companyID)
            if not exist_callback.Success:
                return Callback(True, "", {"Status": "NOT_CONNECTED"})

            # If yes test connection
            return Callback(True, "",
                            {"Status":
                                 "CONNECTED" if calendar_services
                                 .testConnection(type, exist_callback.Data.Auth, companyID).Success else "FAILED"
                             })

        else:
            callback = Callback(False, "The Marketplace object did not match any on the system")

        return callback

    except Exception as exc:
        helpers.logError("Marketplace.marketplace_helpers.processRedirect() ERROR: " + str(exc))
        return Callback(False, str(exc))


# d marketplace item connection (e.g. CRM, Calendar...)
def disconnect(type, companyID):
    try:

        # find the type and redirect to its service
        if CRM_Enum.has_value(type):
            return crm_services.disconnectByType(type, companyID)
        elif Calendar_Enum.has_value(type):
            return calendar_services.disconnectByType(type, companyID)
        else:
            return Callback(False, "The Marketplace object did not match any on the system")

    except Exception as exc:
        helpers.logError("Marketplace.marketplace_helpers.processRedirect() ERROR: " + str(exc))
        return Callback(False, str(exc))



# send request with dynamic method
def sendRequest(url, method, headers, data=None):
    request = None
    if method is "put":
        request = requests.put(url, headers=headers, data=data)
    elif method is "post":
        request = requests.post(url, headers=headers, data=data)
    elif method is "get":
        request = requests.get(url, headers=headers, data=data)
    return request


def convertSkillsToString(skills):
    if skills:
        if type(skills) is list:  # list
            if type(skills[0]) is str:  # list of strings
                skills = ", ".join(skills)

            elif type(skills[0]) is dict:  # list of dicts
                temp = ""
                for skill in skills:
                    temp += skill["name"] + ", "
                    skills = temp[:-2]

    return skills
