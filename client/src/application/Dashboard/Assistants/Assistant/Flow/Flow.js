import React, {Component} from 'react';

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "../../../../../components/Header/Header";
import {assistantActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import styles from "./Flow.module.less"
import {Modal, Spin} from "antd";
import shortid from 'shortid';

const confirm = Modal.confirm;

class Flow extends Component {

    state = {
        currentGroup: {blocks: []},
        assistant: {},
        isSaved: true
    };

    getUpdatableState = () => {
        const {assistant, currentGroup} = this.state;
        let updatedAssistant = JSON.parse(JSON.stringify(assistant));
        let updatedGroup = updatedAssistant.Flow.groups[updatedAssistant.Flow.groups.findIndex(group => group.id === currentGroup.id)];
        return {updatedAssistant, updatedGroup}
    };

    componentDidMount() {
        this.setState({
                assistant: this.props.location.state.assistant
            },
            () => console.log(this.state.assistant)
        )
    }


    selectGroup = currentGroup => this.setState({currentGroup});


    // GROUPS
    addGroup = newGroup => {
        const {updatedAssistant} = this.getUpdatableState();
        updatedAssistant.Flow.groups.push({
            id: shortid.generate(),
            name: newGroup.name,
            description: newGroup.description,
            blocks: []
        });
        this.setState({assistant: updatedAssistant, isSaved: false})
    };

    editGroup = editedGroup => {
        const {updatedAssistant, updatedGroup} = this.getUpdatableState();
        updatedGroup.name = editedGroup.name;
        updatedGroup.description = editedGroup.description;
        this.setState({assistant: updatedAssistant, isSaved: false});
    };

    deleteGroup = deletedGroup => {
        const {updatedAssistant} = this.getUpdatableState();
        updatedAssistant.Flow.groups = updatedAssistant.Flow.groups.filter(group => group.id !== deletedGroup.id);
        this.setState({
            assistant: updatedAssistant,
            currentGroup: {blocks: []},
            isSaved: false
        });
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
    };

    editBlock = (edittedBlock, groupID) => {

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
                this.setState({assistant: updatedAssistant, currentGroup: updatedGroup, isSaved: false})
            }
        });
    };

    reorderBlocks = (newBlocksOrder, groupID) => {

    };

    saveFlow = () => {
        // if i got the assistans.js then i click on flow
        this.props.dispatch(assistantActions.updateFlow(this.state.assistant));
        // this when i refresh the page beacause the props.llcati.stat kj fasdis sdfsdf stuck and need to
        // be clicked again from the alst page
        this.props.location.state.assistant = this.state.assistant;

        if (this.props.successMsg)
            this.setState({isSaved: true});
    };

    render() {
        const {assistant} = this.state;
        const {Flow} = assistant;

        return (
            <Spin spinning={!(!!Flow)} style={{height: '100%'}}>

                <div style={{height: '100%'}}>
                    <Header display={assistant.Name}
                            button={{
                                icon: "save",
                                onClick: this.saveFlow,
                                text: 'Save Flow',
                                disabled: this.state.isSaved
                            }}/>

                    <div className={styles.Panel_Body_Only}>
                        <div style={{margin: '0 5px 0 0', width: '27%'}}>
                            {
                                Flow && <Groups selectGroup={this.selectGroup}
                                                isLoading={this.props.isLoading}
                                                groupsList={Flow.groups}
                                                currentGroup={this.state.currentGroup}
                                                addGroup={this.addGroup}
                                                editGroup={this.editGroup}
                                                deleteGroup={this.deleteGroup}/>
                            }
                        </div>

                        <div style={{margin: '0 0 0 5px', width: '73%'}}>
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
        successMsg: state.assistant.updateFlowSuccessMsg,
    };
}


export default connect(mapStateToProps)(Flow);
