import React, {Component} from 'react';

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "../../../../../components/Header/Header";
import {flowActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import styles from "./Flow.module.less"
import {Spin} from "antd";
import shortid from 'shortid';
class Flow extends Component {

    state = {
        currentGroup: {blocks: []},
        assistant: {}
    };


    componentDidMount() {
        this.setState({
                assistant: this.props.location.state.assistant
            },
            () => console.log(this.state.assistant)
        )
    }

    selectGroup = (currentGroup) => this.setState({currentGroup});


    // GROUPS
    addGroup = (newGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.addGroupRequest({assistantID: assistant.ID, newGroup: newGroup}));
    };

    editGroup = (editedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.editGroupRequest({assistantID: assistant.ID, editedGroup: editedGroup}));
    };

    deleteGroup = (deletedGroup) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.deleteGroupRequest({assistantID: assistant.ID, deletedGroup: deletedGroup}));
        this.setState({currentGroup: {blocks: []}});
    };


    // BLOCKS
    addBlock = (newBlock) => {
        const {assistant, currentGroup} = this.state;
        let updatedAssistant = {...assistant};
        let updatedGroup = updatedAssistant.Flow.groups[updatedAssistant.Flow.groups.findIndex(group => group.ID === currentGroup.ID)];

        const ID = shortid.generate();
        newBlock.ID = ID;

        if (updatedGroup.blocks.length > 0) {
            const lastBlock = updatedGroup.blocks[updatedGroup.blocks.length - 1];
            if (lastBlock.Content.action === "Go To Next Block")
                lastBlock.Content.blockToGoID = ID;
        }

        updatedGroup.blocks.push(newBlock);

        console.log(updatedAssistant, updatedGroup);
        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup
        })
    };

    editBlock = (edittedBlock, groupID) => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(flowActions.editBlockRequest({
            edittedBlock,
            groupID,
            assistantID: assistant.ID,
            currentBlocks: [...this.state.currentGroup.blocks]
        }));
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
        const {assistant} = this.state;
        const {Flow} = assistant;
        return (
            <Spin spinning={!(!!Flow)} style={{height: '100%'}}>

                <div style={{height: '100%'}}>
                    <Header display={assistant.Name}/>
                    <div className={styles.Panel_Body_Only}>
                        <div style={{margin: '0 5px 0 0', width: '30%'}}>
                            {
                                Flow && <Groups selectGroup={this.selectGroup}
                                                isLoading={this.props.isLoading}
                                                groupsList={Flow.groups}
                                                addGroup={this.addGroup}
                                                editGroup={this.editGroup}
                                                deleteGroup={this.deleteGroup}/>
                            }
                        </div>

                        <div style={{margin: '0 0 0 5px', width: '70%'}}>
                            {
                                Flow && <Blocks addBlock={this.addBlock}
                                                editBlock={this.editBlock}
                                                deleteBlock={this.deleteBlock}
                                                reorderBlocks={this.reorderBlocks}
                                                currentGroup={this.state.currentGroup}
                                                allGroups={Flow.groups}
                                                options={this.props.options}/>
                            }
                        </div>

                    </div>
                </div>
            </Spin>

        );
    }

}

function mapStateToProps(state) {
    return {
        options: state.options.options,
        // blockGroups: state.flow.blockGroups,
        // isLoading: state.flow.isLoading,

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
