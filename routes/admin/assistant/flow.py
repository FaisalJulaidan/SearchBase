from flask import Blueprint, request
from services import assistant_services, flow_services, user_services
from models import Callback, Assistant, User, BlockGroup
from utilities import helpers
from flask_jwt_extended import jwt_required, get_jwt_identity


flow_router: Blueprint = Blueprint('flow_router', __name__, template_folder="../../templates")


@flow_router.route("/assistant/<int:assistantID>/flow", methods=['GET', 'PUT'])
@jwt_required
def flow(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, security_callback.Data, security_callback.Message, None)
    assistant: Assistant = security_callback.Data

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Get the assistant's flow including (groups & blocks)
    if request.method == "GET":
        callback: Callback = flow_services.getFlow(assistant)

    # Update the blocks
    if request.method == "PUT":
        data = request.json
        callback: Callback = flow_services.updateFlow(data, assistant)


    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Add, Update and Delete blocks group, We ask for assistant ID for security purposes
@flow_router.route("/assistant/<int:assistantID>/flow/group", methods=['POST', 'PUT', 'DELETE'])
@jwt_required
def group(assistantID):

    # Authenticate
    user = get_jwt_identity()['user']
    # For all type of requests methods, get the assistant
    security_callback: Callback = assistant_services.getByID(assistantID, user['companyID'])
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Assistant not found.", None)
    assistant: Assistant = security_callback.Data


    #############
    callback: Callback = Callback(False, 'Error!', None)
    data = request.json
    if not data:
        return helpers.jsonResponse(False, 400, "Data missing")

    # Add a group
    if request.method == "POST":
        # Get the new group data from the request's body
        callback: Callback = flow_services.addGroup(data, assistant)

    # Update the group
    if request.method == "PUT":
        # Get new blocks data from the request's body
        callback: Callback = flow_services.updateGroup(data, assistant)

    # Delete the blocks' group
    if request.method == "DELETE":
        # Get new block data from the request's body
        callback: Callback = flow_services.deleteGroupByID(data.get('id', None), assistant)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


# Add and Delete a single block, We ask for group ID for security purposes
@flow_router.route("/assistant/flow/group/<int:groupID>/block", methods=['POST', 'DELETE'])
@jwt_required
def block(groupID):

    # Authenticate
    user = get_jwt_identity()['user']

    # For all type of requests methods, get the assistant
    security_callback: Callback = flow_services.getGroupByID(groupID)
    if not security_callback.Success:
        return helpers.jsonResponse(False, 404, "Group not found.", None)
    group: BlockGroup = security_callback.Data

    # Check if this user has access to this group
    if group.Assistant.CompanyID != user['companyID']:
        return helpers.jsonResponse(False, 401, "Unauthorised!")

    #############
    callback: Callback = Callback(False, 'Error!', None)
    # Add a block
    if request.method == "POST":
        # Get the new block data from the request's body
        data = request.json
        callback: Callback = flow_services.addBlock(data, group)

    # Delete the block
    if request.method == "DELETE":
        # Get new block data from the request's body
        data = request.json
        callback: Callback = flow_services.deleteBlockByID(data.get('id', None), group)

    # Return response
    if not callback.Success:
        return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
    return helpers.jsonResponse(True, 200, callback.Message, callback.Data)


@flow_router.route("/assistant/flow/options", methods=['GET'])
@jwt_required
def get_flowOptions():

    if request.method == "GET":
        callback: Callback = flow_services.getOptions()
        # Return response
        if not callback.Success:
            return helpers.jsonResponse(False, 400, callback.Message, callback.Data)
        return helpers.jsonResponse(True, 200, "These are the options the flow provides.", callback.Data)
