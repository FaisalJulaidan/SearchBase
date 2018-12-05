from flask import Blueprint, request, session
from services import admin_services, assistant_services, flow_services, user_services, blockLabels_services
from models import Callback, Assistant, User, BlockLabel
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


flow_router: Blueprint = Blueprint('flow_router', __name__, template_folder="../../templates")


@flow_router.route("/assistant/<int:assistantID>/flow", methods=['GET', 'PUT'])
@jwt_required
def get_flow(assistantID):
    # Auth
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)

    # Get the assistant's flow including (groups & blocks)
    if request.method == "GET":
        assistant: Assistant = callback.Data
        data: dict = flow_services.getFlow(assistant)
        return helpers.jsonResponse(True, 200, "No Message", data)

    # Update the blocks
    if request.method == "PUT":
        data = request.get_json(silent=True)
        callback: Callback = flow_services.updateFlow(data, assistant)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Add new blocks group
@flow_router.route("/assistant/<int:assistantID>/group", methods=['POST'])
@jwt_required
def add_block(assistantID):
    # Auth
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)
    # Add a block
    if request.method == "POST":
        # Get new block data from the request's body
        data = request.get_json(silent=True)
        callback: Callback = flow_services.addBlock(data)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Update and delete blocks group, We ask for assistant ID for security purposes
@flow_router.route("/assistant/<int:assistantID>/group/<int:groupID>", methods=['PUT', 'DELETE'])
@jwt_required
def add_block(assistantID, groupID):
    # Auth
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    callback: Callback = assistant_services.getByID(assistantID)
    if not callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = callback.Data

    # Check if this user has access to this assistant
    if assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!", callback.Data)

    # Update the blocks' group
    if request.method == "PUT":
        # Get new block data from the request's body
        data = request.get_json(silent=True)
        callback: Callback = flow_services.addBlock(data)
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@flow_router.route("/assistant/flow/block/<int:blockID>", methods=['DELETE'])
@jwt_required
def delete_block(blockID):
    if request.method == "DELETE":
        user = get_jwt_identity()['user']
        # Get the user who is logged in and wants to delete.
        callback: Callback = user_services.getByID(user['companyID'])
        if not callback.Success:
            return helpers.jsonResponse(False, 400, "Sorry, your account doesn't exist. Try again please!")
        user: User = callback.Data

        # Check if this user is authorised for such an operation.
        if not user.Role.EditChatbots:
            return helpers.jsonResponse(False, 401, "Sorry, You're not authorised for deleting blocks.")

        # Delete the block
        callback: Callback = flow_services.deleteBlockByID(blockID)
        if not callback.Success:
            return helpers.jsonResponse(False, 404, callback.Message, None)
        return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@flow_router.route("/assistant/flow/options", methods=['GET'])
@jwt_required
def get_flowOptions():
    if request.method == "GET":
        return helpers.jsonResponse(True, 200, "These are the options the flow provides.", flow_services.getOptions())



