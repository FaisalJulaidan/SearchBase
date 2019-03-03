import React, {Component} from 'react';

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "../../../../../components/Header/Header";
import {assistantActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import styles from "./Flow.module.less"
import {Modal, Spin} from "antd";
import shortid from 'shortid';
import { Prompt } from "react-router-dom";
import {destroyMessage, successMessage} from "../../../../../helpers";

const confirm = Modal.confirm;

class Flow extends Component {

    savedClicked = false; // Important for solving the saving flow bug

    state = {
        currentGroup: {blocks: []},
        assistant: {Flow: {groups:[]}},
        isSaved: true
    };

    componentWillReceiveProps(nextProps, nextContext) {
        if (nextProps.successMsg && this.savedClicked){
            this.savedClicked = false;
            this.setState({isSaved: true});
        }
    }

    componentDidUpdate = () => {
        if (!this.state.isSaved) {
            console.log('reload?');
            window.onbeforeunload = () => true
        } else {
            window.onbeforeunload = undefined
        }
    };


    componentDidMount() {
        console.log('componentDidMount');
        const {assistantList, match} = this.props;
        this.setState({assistant: assistantList.find(assistant => assistant.ID === +match.params.id)},
            () => console.log(this.state.assistant)
        )
    }

    getUpdatableState = () => {
        const {assistant, currentGroup} = this.state;
        let updatedAssistant = JSON.parse(JSON.stringify(assistant));
        let updatedGroup = updatedAssistant.Flow?.groups[updatedAssistant.Flow.groups.findIndex(group => group.id === currentGroup.id)];
        return {updatedAssistant, updatedGroup}
    };

    selectGroup = currentGroup => this.setState({currentGroup});


    // GROUPS
    addGroup = newGroup => {
        const {updatedAssistant} = this.getUpdatableState();
        if(!updatedAssistant.Flow)
            updatedAssistant.Flow = {groups: []};
        updatedAssistant.Flow.groups.push({
            id: shortid.generate(),
            name: newGroup.name,
            description: newGroup.description,
            blocks: []
        });

        this.setState({
            assistant: updatedAssistant,
            isSaved: false
        })
        destroyMessage();
        successMessage('Group added!');
    };

    editGroup = editedGroup => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();

        updatedGroup.name = editedGroup.name;
        updatedGroup.description = editedGroup.description;
        this.selectGroup(updatedGroup);

        this.setState({
            assistant: updatedAssistant,
            isSaved: false
        });
        destroyMessage();
        successMessage('Group updated!');
    };

    deleteGroup = deletedGroup => {
        const {updatedAssistant} = this.getUpdatableState();
        updatedAssistant.Flow.groups = updatedAssistant.Flow.groups.filter(group => group.id !== deletedGroup.id);
        this.setState({
            assistant: updatedAssistant,
            currentGroup: {blocks: []},
            isSaved: false
        });
        destroyMessage();
        successMessage('Group deleted!');
        // Todo: run the blocksRelation checker function
    };


    // BLOCKS
    addBlock = (newBlock) => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();

        const ID = shortid.generate();
        newBlock.ID = ID;

        if (updatedGroup.blocks.length > 0) {
            const lastBlock = updatedGroup.blocks[updatedGroup.blocks.length - 1];
            if (lastBlock.Content.action === "Go To Next Block")
                lastBlock.Content.blockToGoID = ID;
        }

        updatedGroup.blocks.push(newBlock);

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup,
            isSaved: false
        })
        destroyMessage();
        successMessage('Block added!');
    };

    editBlock = (edittedBlock) => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();
        const nextBlock = updatedGroup.blocks[updatedGroup.blocks.findIndex(b => b.ID === edittedBlock.ID) + 1];

        if (edittedBlock.Content.action === "Go To Next Block")
            if (nextBlock?.ID)
                edittedBlock.Content.blockToGoID = nextBlock.ID;
            else
                edittedBlock.Content.blockToGoID = null;

        updatedGroup.blocks[updatedGroup.blocks.findIndex(b => b.ID === edittedBlock.ID)] = edittedBlock;

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup,
            isSaved: false
        })
        destroyMessage();
        successMessage('Block updated!');
    };

    deleteBlock = (deletedBlock) => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();
        let counter = 0;
        updatedAssistant.Flow.groups.forEach((group) => {
            group.blocks.map((block) => {
                if (block.Content.blockToGoID === deletedBlock.ID) {
                    block.Content.blockToGoID = null;
                    counter++;
                }
                return block;
            })
        });

        confirm({
            title: `Delete block with type: ${deletedBlock.Type}`,
            content: <p>If you click OK, this block will be deleted forever and will affect <b>{counter}</b> blocks</p>,
            onOk: () => {
                updatedGroup.blocks = updatedGroup.blocks.filter((block) => block.ID !== deletedBlock.ID);

                this.setState({
                    assistant: updatedAssistant,
                    currentGroup: updatedGroup,
                    isSaved: false
                });
                destroyMessage();
                successMessage('Block deleted!');
            }
        });
    };

    reorderBlocks = (newBlocksOrder) => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();
        newBlocksOrder.map((block, index, array) => {
            if (block.Content.action === "Go To Next Block")
                if (array[index + 1]?.ID)
                    block.Content.blockToGoID = array[index + 1].ID;
                else
                    block.Content.blockToGoID = null;
            return block
        });

        updatedGroup.blocks = newBlocksOrder;

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup,
            isSaved: false
        })
    };

    saveFlow = () => {
        this.savedClicked = true;
        this.props.dispatch(assistantActions.updateFlow(this.state.assistant));
        this.props.location.state.assistant = this.state.assistant;
    };

    render() {
        const {assistant} = this.state;
        const {Flow} = assistant;

        return (
            <Spin spinning={!(!!assistant)} style={{height: '100%'}}>

                <div style={{height: '100%'}}>
                    <Header display={assistant.Name}
                            button={{
                                icon: "save",
                                onClick: this.saveFlow,
                                text: 'Save Flow',
                                disabled: this.state.isSaved,
                                loading: this.props.isUpdatingFlow
                            }}/>

                    <div className={styles.Panel_Body_Only}>
                        <div style={{margin: '0 5px 0 0', width: '27%'}}>
                            {
                                assistant && <Groups selectGroup={this.selectGroup}
                                                isLoading={this.props.isLoading}
                                                groupsList={Flow?.groups}
                                                currentGroup={this.state.currentGroup}
                                                addGroup={this.addGroup}
                                                editGroup={this.editGroup}
                                                deleteGroup={this.deleteGroup}/>
                            }
                        </div>

                        <div style={{margin: '0 0 0 5px', width: '73%'}}>
                            {
                                assistant && <Blocks addBlock={this.addBlock}
                                                editBlock={this.editBlock}
                                                deleteBlock={this.deleteBlock}
                                                reorderBlocks={this.reorderBlocks}
                                                currentGroup={this.state.currentGroup}
                                                allGroups={Flow?.groups}
                                                options={this.props.options}/>
                            }
                        </div>

                    </div>
                </div>

                <Prompt
                    when={!this.state.isSaved}
                    message={location =>
                        `Your flow is not saved are you sure you want leave without saving it?`
                    }
                />


            </Spin>

        );
    }

}

function mapStateToProps(state) {
    return {
        options: state.options.options,
        assistantList: state.assistant.assistantList,
        successMsg: state.assistant.updateFlowSuccessMsg,
        isUpdatingFlow: state.assistant.isUpdatingFlow,
    };
}


export default connect(mapStateToProps)(Flow);
