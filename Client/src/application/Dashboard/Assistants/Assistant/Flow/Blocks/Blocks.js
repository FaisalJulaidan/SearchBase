import React, { Component } from 'react';

import styles from './Blocks.module.less';
import { Button, Empty, Form } from 'antd';

import Block from './Block/Block';
import { DragDropContext, Draggable, Droppable } from 'react-beautiful-dnd';
import NewBlockModal from './Modals/NewBlockModal';
import EditBlockModal from './Modals/EditBlockModal1';

// a little function to help us with reordering the result
const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

const getItemStyle = draggableStyle => ({margin: `0 0 8px 0`, ...draggableStyle});

class Blocks extends Component {

    state = {
        addBlockVisible: false,
        // addBlockVisible: true,
        editBlockVisible: false,
        deleteBlockVisible: false,
        blocks: [],
        edittedBlock: {},
        deletedBlock: {content: {}}
    };

    constructor(props) {
        super(props);
        this.onDragEnd = this.onDragEnd.bind(this);
    }

    onDragEnd(result) {
        // dropped outside the list
        if (!result.destination) return;

        let blocks = reorder(this.state.blocks, result.source.index, result.destination.index);
        this.setState({blocks});
        // send a request to the flow for logic
        this.props.reorderBlocks(blocks)
    }

    componentWillReceiveProps(nextProps) {
        // This handles when updating the selected group to show its blocks
        if (nextProps.currentGroup !== this.state.currentGroup && nextProps.currentGroup.blocks){
            this.setState({blocks: nextProps.currentGroup.blocks})
        }
    }


    ///////////////////////////////////////////////////

    // ADD BLOCK MODAL CONFIGS
    showAddBlockModal = () => this.setState({addBlockVisible: true});
    closeAddBlockModal = () => this.setState({addBlockVisible: false});
    handleAddBlock = (newBlock) => this.props.addBlock(newBlock, this.props.currentGroup.id);


    // EDIT BLOCK MODAL CONFIGS
    // this called from block.js when you click on edit block button
    editBlock = (edittedBlock) => this.setState({edittedBlock, editBlockVisible: true});
    closeEditBlockModal = () => this.setState({edittedBlock: {}, editBlockVisible: false});
    handleEditBlock = (edittedBlock) => this.props.editBlock(edittedBlock);

    // DELETE BLOCK MODAL CONFIGS
    // this called from block.js & editBlockModal when you click on delete block button
    handleDeleteBlock = deletedBlock => {
        this.props.deleteBlock(deletedBlock, this.closeEditBlockModal);

    };



    render() {

        return (
            <div className={styles.Panel}>
                <div className={styles.Panel_Header_With_Button}>
                    <div>
                        <h3>{this.props.currentGroup.name} Questions</h3>
                    </div>
                    <div>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                onClick={this.showAddBlockModal} disabled={!this.props.currentGroup.id}>
                            Add Question
                        </Button>
                    </div>
                </div>

                <div className={styles.Panel_Body}>
                    <div style={{height: "100%", width: '100%', overflowY: 'auto'}}>
                        <DragDropContext onDragEnd={this.onDragEnd}>
                            <Droppable droppableId="droppable">
                                {(provided) => (
                                    <div ref={provided.innerRef}>
                                        {
                                            this.state.blocks.length ?
                                            this.state.blocks.map((block, index) =>
                                                <Draggable key={block.ID} draggableId={block.ID} index={index}>
                                                    {(provided) => (
                                                        <div ref={provided.innerRef} {...provided.draggableProps}
                                                             {...provided.dragHandleProps}
                                                             style={getItemStyle(provided.draggableProps.style)}>
                                                            <Block block={block}
                                                                   editBlock={this.editBlock}
                                                                   deleteBlock={this.handleDeleteBlock}
                                                                   allGroups={this.props.allGroups}
                                                                   options={this.props.options}/>
                                                        </div>
                                                    )}
                                                </Draggable>
                                            ) :
                                            <Empty description={this.state.currentGroup ? 'No questions yet' : 'No groups yet'}
                                                   style={{marginTop: '5px'}}/>
                                        }


                                        {provided.placeholder}
                                    </div>
                                )}
                            </Droppable>
                        </DragDropContext>
                    </div>
                </div>

                <NewBlockModal visible={this.state.addBlockVisible}
                               handleAddBlock={this.handleAddBlock}
                               closeModal={this.closeAddBlockModal}

                               currentGroup={this.props.currentGroup}
                               allBlocks={this.state.blocks}
                               allGroups={this.props.allGroups}
                               options={this.props.options}/>

                <EditBlockModal visible={this.state.editBlockVisible}
                                handleEditBlock={this.handleEditBlock}
                                handleDeleteBlock={this.handleDeleteBlock}
                                closeModal={this.closeEditBlockModal}

                                block={this.state.edittedBlock}
                                currentGroup={this.props.currentGroup}
                                allBlocks={this.state.blocks}
                                allGroups={this.props.allGroups}
                                options={this.props.options}/>

            </div>
        );
    }
}

export default Form.create()(Blocks);
