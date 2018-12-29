import React, {Component} from 'react';
import "./Flow.less"

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "../../../../../components/Header/Header";
import {flowActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import styles from "./Flow.module.less"
class Flow extends Component {

    state = {
        currentGroup: {blocks: []}
    };

    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.fetchFlowRequest(assistant.ID))
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.blockGroups !== this.props.blockGroups)
            nextProps.blockGroups.map((group) => {
                if (group.id === this.state.currentGroup.id)
                    this.setState({currentGroup: group})
            })
    }

    selectGroup = (currentGroup) => this.setState({currentGroup});


    // GROUPS
    addGroup = (newGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.addGroupRequest({ID: assistant.ID, newGroup: newGroup}));
    };

    editGroup = (editedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.editGroupRequest({ID: assistant.ID, editedGroup: editedGroup}));
    };

    deleteGroup = (deletedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.deleteGroupRequest({assistantID: assistant.ID, deletedGroup: deletedGroup}));
    };


    // BLOCKS
    addBlock = (newBlock, groupID) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.addBlockRequest({newBlock, groupID, assistantID: assistant.ID}));
    };

    editBlock = (edittedBlock, groupID) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.editBlockRequest({edittedBlock, groupID, assistantID: assistant.ID}));
    };

    deleteBlock = (deletedBlock, groupID) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.deleteBlockRequest({deletedBlock, groupID, assistantID: assistant.ID}));
    };

    reorderBlocks = (newBlocksOrder, groupID) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.updateBlocksOrderRequest({newBlocksOrder, groupID, assistantID: assistant.ID}));
    };

    render() {
        const {assistant} = this.props.location.state;

        return (
            <div style={{height: '100%'}}>
                <Header display={assistant.Name}/>

                <div className={styles.Panel_Body_Only}>
                    <div style={{margin: '0 5px 0 0', width: '30%'}}>
                        <Groups selectGroup={this.selectGroup}
                                isLoading={this.props.isLoading}
                                groupsList={this.props.blockGroups}
                                addGroup={this.addGroup}
                                editGroup={this.editGroup}
                                deleteGroup={this.deleteGroup}/>
                    </div>
                    <div style={{margin: '0 0 0 5px', width: '70%'}}>
                        <Blocks addBlock={this.addBlock}
                                editBlock={this.editBlock}
                                deleteBlock={this.deleteBlock}
                                reorderBlocks={this.reorderBlocks}
                                currentGroup={this.state.currentGroup}
                                allGroups={this.props.blockGroups}/>
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
        isDeletingGroup: state.flow.isDeletingGroup,

        isAddingBlock: state.flow.isAddingBlock,

    };
}


export default connect(mapStateToProps)(Flow);
