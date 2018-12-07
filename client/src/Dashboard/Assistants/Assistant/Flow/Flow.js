import React, {Component} from 'react';
import "./Flow.less"

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "./Header/Header";
import {flowActions} from "../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import {message} from "antd";

/*
*
* Todo:
*   2- design card for each tab type
* */

class Flow extends Component {

    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.fetchFlowRequest(assistant.ID))
    }

    addGroup = (newGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.addGroupRequest({ID: assistant.ID, newGroup: newGroup}));
        message.loading(`Adding ${newGroup.name} group`, 0);
    };

    editGroup = (editedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.editGroupRequest({ID: assistant.ID, editedGroup: editedGroup}));
        message.loading(`Editing ${editedGroup.name} group`, 0);
    };

    deleteGroup = (deletedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.deleteGroupRequest({ID: assistant.ID, deletedGroup: deletedGroup}));
        message.loading(`Deleting ${deletedGroup.name} group`, 0);
    };

    componentDidUpdate(prevProps) {

        if (!this.props.isAddingGroup && prevProps.successMsg !== this.props.successMsg) {
            message.destroy();
            message.success(this.props.successMsg);
        }

        if (!this.props.isEditingGroup && prevProps.successMsg !== this.props.successMsg) {
            message.destroy();
            message.success(this.props.successMsg);
        }

        if (!this.props.isDeletingGroup && prevProps.successMsg !== this.props.successMsg) {
            message.destroy();
            message.success(this.props.successMsg);
        }
    }

    render() {
        const {assistant} = this.props.location.state;

        return (
            <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header assistantName={assistant.Name}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '30%'}}>

                        <Groups isLoading={this.props.isLoading}
                                groupsList={this.props.blockGroups}
                                addGroup={this.addGroup}
                                editGroup={this.editGroup}
                                deleteGroup={this.deleteGroup}/>

                    </div>

                    <div style={{margin: 5, width: '70%'}}>
                        <Blocks/>
                    </div>
                </div>
            </div>
        );
    }

}


function mapStateToProps(state) {
    return {
        blockGroups: state.flow.blockGroups,
        isLoading: state.flow.isLoading,

        successMsg: state.flow.successMsg,

        isAddingGroup: state.flow.isAddingGroup,
        isEditingGroup: state.flow.isEditingGroup,
        isDeletingGroup: state.flow.isDeletingGroup
    };
}

export default connect(mapStateToProps)(Flow);


