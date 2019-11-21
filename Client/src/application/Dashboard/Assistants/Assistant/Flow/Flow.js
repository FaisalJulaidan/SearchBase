import React, { Component } from 'react';

import Groups from './Groups/Groups';
import Blocks from './Blocks/Blocks';
import AssistantToolsModal from './Tools/AssistantToolsModal';
import { assistantActions } from 'store/actions';
import connect from 'react-redux/es/connect/connect';
import styles from './Flow.module.less';
import { Button, Modal, Spin } from 'antd';
import shortid from 'shortid';
import { deepClone, successMessage } from 'helpers';

const confirm = Modal.confirm;

class Flow extends Component {


    state = {
        currentGroup: { blocks: [] },
        assistant: { Flow: { groups: [] } },
        assistantToolsBlockVisible: false
    };


    componentDidMount() {
        const { assistant } = this.props;
        this.setState({ assistant }, () => {
            if (this.state.assistant?.Flow?.groups.length)
                this.selectGroup(this.state.assistant.Flow.groups[0]);
        });
    }

    getUpdatableState = () => {
        const { assistant, currentGroup } = this.state;
        let updatedAssistant = deepClone(assistant);
        let updatedGroup = updatedAssistant.Flow?.groups[updatedAssistant.Flow.groups.findIndex(group => group.id === currentGroup.id)];
        return { updatedAssistant, updatedGroup };
    };

    selectGroup = currentGroup => this.setState({ currentGroup });


    // GROUPS
    addGroup = newGroup => {
        const { updatedAssistant } = this.getUpdatableState();
        if (!updatedAssistant.Flow)
            updatedAssistant.Flow = { groups: [] };

        newGroup = {
            id: shortid.generate(),
            name: newGroup.name,
            description: newGroup.description,
            blocks: []
        };

        updatedAssistant.Flow.groups.push(newGroup);

        this.setState({
            assistant: updatedAssistant,
            currentGroup: newGroup
        });

        this.props.setIsFlowSaved(false);
        successMessage('Group added!');
    };

    editGroup = editedGroup => {
        const { updatedAssistant, updatedGroup } = this.getUpdatableState();

        updatedGroup.name = editedGroup.name;
        updatedGroup.description = editedGroup.description;
        this.selectGroup(updatedGroup);

        this.setState({
            assistant: updatedAssistant
        });
        this.props.setIsFlowSaved(false);
        successMessage('Group updated!');
    };

    deleteGroup = deletedGroup => {
        const { updatedAssistant } = this.getUpdatableState();
        updatedAssistant.Flow.groups = updatedAssistant.Flow.groups.filter(group => group.id !== deletedGroup.id);
        this.setState({
            assistant: updatedAssistant,
            currentGroup: { blocks: [] }
        });
        this.props.setIsFlowSaved(false);
        successMessage('Group deleted');
        // TODO: Check the related blocks to this group
    };


    // BLOCKS
    addBlock = (newBlock) => {
        const { updatedAssistant, updatedGroup } = this.getUpdatableState();

        const ID = shortid.generate();
        newBlock.ID = ID;

        if (updatedGroup.blocks.length > 0) {
            const lastBlock = updatedGroup.blocks[updatedGroup.blocks.length - 1];

            // update if last block is question || User Type || Job Type each answer should point to newBlock.ID
            switch (lastBlock.Type) {
                case 'Question':
                    lastBlock.Content.answers.map((answer) => {
                        if (answer.action === 'Go To Next Block')
                            answer.blockToGoID = newBlock.ID;
                        return answer;
                    });
                    break;
                case 'User Type':
                case 'Job Type':
                    lastBlock.Content.types.map((type) => {
                        if (type.action === 'Go To Next Block')
                            type.blockToGoID = newBlock.ID;
                        return type;
                    });
                    break;
            }


            if (lastBlock.Content.action === 'Go To Next Block')
                lastBlock.Content.blockToGoID = newBlock.ID;

            if (lastBlock.SkipAction === 'Go To Next Block')
                lastBlock.SkipBlockToGoID = newBlock.ID;
        }
        updatedGroup.blocks.push(newBlock);

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup
        });
        this.props.setIsFlowSaved(false);
        successMessage('Block added');
    };

    editBlock = (edittedBlock) => {
        const { updatedAssistant, updatedGroup } = this.getUpdatableState();
        const nextBlock = updatedGroup.blocks[updatedGroup.blocks.findIndex(b => b.ID === edittedBlock.ID) + 1];

        switch (edittedBlock.Type) {
            case 'Question':
                edittedBlock.Content.answers.map((answer) => {
                    if (answer.action === 'Go To Next Block')
                        if (nextBlock?.ID)
                            answer.blockToGoID = nextBlock.ID;
                        else
                            answer.blockToGoID = null;
                    return answer;
                });
                break;
            case 'User Type':
            case 'Job Type':
                edittedBlock.Content.types.map((type) => {
                    if (type.action === 'Go To Next Block')
                        if (nextBlock?.ID)
                            type.blockToGoID = nextBlock.ID;
                        else
                            type.blockToGoID = null;
                    return type;
                });
                break;
        }

        if (edittedBlock.Content.action === 'Go To Next Block')
            if (nextBlock?.ID)
                edittedBlock.Content.blockToGoID = nextBlock.ID;
            else
                edittedBlock.Content.blockToGoID = null;

        if (edittedBlock.SkipAction === 'Go To Next Block')
            if (nextBlock?.ID)
                edittedBlock.SkipBlockToGoID = nextBlock.ID;
            else
                edittedBlock.Content.blockToGoID = null;

        updatedGroup.blocks[updatedGroup.blocks.findIndex(b => b.ID === edittedBlock.ID)] = edittedBlock;

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup
        });
        this.props.setIsFlowSaved(false);
        successMessage('Block updated!');
    };

    deleteBlock = (deletedBlock, closeModalCallback) => {
        const { updatedAssistant, updatedGroup } = this.getUpdatableState();
        let counter = 0;
        updatedAssistant.Flow.groups.forEach((group) => {
            group.blocks.map((block) => {
                switch (block.Type) {
                    case 'Question':
                        block.Content.answers.map((answer) => {
                            if (answer.blockToGoID === deletedBlock.ID) {
                                answer.blockToGoID = null;
                                counter++;
                            }
                            return answer;
                        });
                        break;
                    case 'User Type':
                    case 'Job Type':
                        block.Content.types.map((type) => {
                            if (type.blockToGoID === deletedBlock.ID) {
                                type.blockToGoID = null;
                                counter++;
                            }
                            return type;
                        });
                        break;
                }

                let shallIncreament = false;
                if (block.Content.blockToGoID === deletedBlock.ID) {
                    shallIncreament = true;
                    block.Content.blockToGoID = null;
                }

                if (block.SkipBlockToGoID === deletedBlock.ID) {
                    shallIncreament = true;
                    block.SkipBlockToGoID = null;
                }

                if (shallIncreament) counter++;

                return block;
            });
        });


        confirm({
            title: `Delete block with type: ${deletedBlock.Type}`,
            content: <p>If you click OK, this block will be deleted forever and will affect <b>{counter}</b> blocks</p>,
            onOk: () => {
                updatedGroup.blocks = updatedGroup.blocks.filter((block) => block.ID !== deletedBlock.ID);

                this.setState({
                    assistant: updatedAssistant,
                    currentGroup: updatedGroup
                });
                this.props.setIsFlowSaved(false);
                successMessage('Block deleted!');
                closeModalCallback();
            }
        });
    };

    reorderBlocks = (newBlocksOrder) => {
        const { updatedAssistant, updatedGroup } = this.getUpdatableState();
        newBlocksOrder.map((block, index, array) => {

            switch (block.Type) {
                case 'Question':
                    block.Content.answers.map((answer) => {
                        if (answer.action === 'Go To Next Block')
                            if (array[index + 1]?.ID)
                                answer.blockToGoID = array[index + 1].ID;
                            else
                                answer.blockToGoID = null;
                        return answer;
                    });
                    break;
                case 'User Type':
                case 'Job Type':
                    block.Content.types.map((type) => {
                        if (type.action === 'Go To Next Block')
                            if (array[index + 1]?.ID)
                                type.blockToGoID = array[index + 1].ID;
                            else
                                type.blockToGoID = null;
                        return type;
                    });
                    break;
            }

            if (block.Content.action === 'Go To Next Block')
                if (array[index + 1]?.ID)
                    block.Content.blockToGoID = array[index + 1].ID;
                else
                    block.Content.blockToGoID = null;

            if (block.SkipAction === 'Go To Next Block')
                if (array[index + 1]?.ID)
                    block.SkipBlockToGoID = array[index + 1].ID;
                else
                    block.SkipBlockToGoID = null;

            return block;
        });

        updatedGroup.blocks = newBlocksOrder;

        this.setState({
            assistant: updatedAssistant,
            currentGroup: updatedGroup
        });
        this.props.setIsFlowSaved(false);
    };

    saveFlow = () => {
        this.props.dispatch(assistantActions.updateFlow(this.state.assistant))
            .then(() => {
                this.props.setIsFlowSaved(true);
            });
    };

    // ASSISTANT TOOLS MODAL
    showAssistantToolsModal = () => this.setState({ assistantToolsBlockVisible: true });
    closeAssistantToolsModal = () => this.setState({ assistantToolsBlockVisible: false });


    render() {
        const { assistant } = this.state;
        const { Flow } = assistant;

        return (
            !assistant ?
                <Spin/>
                : <>

                    <div className={styles.Header}>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="tool"
                                onClick={this.showAssistantToolsModal}>
                            Tools
                        </Button>
                        <Button type={'primary'}
                                icon={'save'}
                                onClick={this.saveFlow}
                                disabled={this.props.isFlowSaved}
                                loading={this.props.isUpdatingFlow}>
                            Save Script
                        </Button>
                    </div>

                    <div style={{ marginBottom: 15 }}>
                        {
                            assistant &&
                            <Groups selectGroup={this.selectGroup}
                                    isLoading={this.props.isLoading}
                                    groupsList={Flow?.groups}
                                    currentGroup={this.state.currentGroup}
                                    addGroup={this.addGroup}
                                    editGroup={this.editGroup}
                                    deleteGroup={this.deleteGroup}/>
                        }
                    </div>

                    <div>
                        {
                            assistant &&
                            <Blocks addBlock={this.addBlock}
                                    editBlock={this.editBlock}
                                    deleteBlock={this.deleteBlock}
                                    reorderBlocks={this.reorderBlocks}
                                    currentGroup={this.state.currentGroup}
                                    allGroups={Flow?.groups}
                                    options={this.props.options}/>
                        }
                    </div>

                    <AssistantToolsModal visible={this.state.assistantToolsBlockVisible}
                                         closeModal={this.closeAssistantToolsModal}/>


                </>
        );
    }

}

function mapStateToProps(state) {
    return {
        options: state.options.options,
        successMsg: state.assistant.updateFlowSuccessMsg,
        isUpdatingFlow: state.assistant.isUpdatingFlow
    };
}


export default connect(mapStateToProps)(Flow);
