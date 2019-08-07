from flask import Blueprint, request
from models import Callback
from services import company_services
from utilities import helpers

staff_router = Blueprint('staff_router', __name__)

@staff_router.route("/activate_company/<payload>", methods=['GET'])  # TODO
def activate_company(payload):
    if request.method == "GET":
        try:
            print("ACTIVATE COMAPNY")
            data = helpers.verificationSigner.loads(payload, salt='company-activate-key')
            callback: Callback = company_services.activateCompany(data['companyID'])
            print(data)
            if not callback.Success:
                raise Exception("Failed to activate company account (id: " + str(data['companyID']) + ")")

            return "Company account activated successfully :)"

        except Exception as exc:
            print(exc)
            return str(exc)