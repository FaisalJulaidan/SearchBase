import React, {Component} from 'react';
import "./Flow.less"

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "./Header/Header";
import {flowActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import {message} from "antd";

/*
*
* Todo:
*   2- design card for each tab type
* */

class Flow extends Component {

    state = {
        currentGroup: {blocks: []}
    };

    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.fetchFlowRequest(assistant.ID))
    }

    selectGroup = (currentGroup) => this.setState({currentGroup});

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

        if (!this.props.isAddingGroup && prevProps.addSuccessMsg !== this.props.addSuccessMsg) {
            message.destroy();
            message.success(this.props.addSuccessMsg);
        }

        if (!this.props.isEditingGroup && prevProps.editSuccessMsg !== this.props.editSuccessMsg) {
            message.destroy();
            message.success(this.props.editSuccessMsg);
        }

        if (!this.props.isDeletingGroup && prevProps.deleteSuccessMsg !== this.props.deleteSuccessMsg) {
            message.destroy();
            message.success(this.props.deleteSuccessMsg);
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

                        <Groups selectGroup={this.selectGroup}
                                isLoading={this.props.isLoading}
                                groupsList={this.props.blockGroups}
                                addGroup={this.addGroup}
                                editGroup={this.editGroup}
                                deleteGroup={this.deleteGroup}/>

                    </div>

                    <div style={{margin: 5, width: '70%'}}>
                        <Blocks currentGroup={this.state.currentGroup}/>
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

        addSuccessMsg: state.flow.addSuccessMsg,
        editSuccessMsg: state.flow.editSuccessMsg,
        deleteSuccessMsg: state.flow.deleteSuccessMsg,

        isAddingGroup: state.flow.isAddingGroup,
        isEditingGroup: state.flow.isEditingGroup,
        isDeletingGroup: state.flow.isDeletingGroup
    };
}


export default connect(mapStateToProps)(Flow);


