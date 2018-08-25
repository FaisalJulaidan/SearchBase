from flask import Blueprint, request, redirect, flash, session
from services import solutions_services, admin_services, assistant_services, sub_services
from models import Callback, Product
from utilties import helpers

products_router: Blueprint = Blueprint('products_router', __name__, template_folder="../../templates")

@products_router.route("/admin/assistant/<assistantID>/solutions", methods=['GET', 'POST'])
def admin_connect(assistantID):
    checkAssistantID(assistantID)
    assistant = query_db("SELECT * FROM Assistants WHERE ID=?;", [assistantID], True)
    return render("admin/connect.html", companyID=assistant["CompanyID"], assistantID=assistantID)