import React, {Component} from 'react';

import "./Blocks.less"
import styles from "./Blocks.module.less";
import {Button, Form, Modal} from "antd";

import Block from "./Block/Block";
import {DragDropContext, Draggable, Droppable} from 'react-beautiful-dnd';
import NewBlockModal from "./NewBlockModal/NewBlockModal";
import EditBlockModal from "./EditBlockModal/EditBlockModal1";

// a little function to help us with reordering the result
const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

const getItemStyle = draggableStyle => ({margin: `0 0 8px 0`, ...draggableStyle});
const confirm = Modal.confirm;

class Blocks extends Component {

    state = {
        addBlockVisible: false,
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
        for (const i in blocks) blocks[i].order = Number(i) + 1;
        this.setState({blocks});
        // send a request to the server
        this.props.reorderBlocks(blocks, this.props.currentGroup.id)
    }

    componentWillReceiveProps(nextProps) {
        // This handles when updating the selected group to show its blocks
        if (nextProps.currentGroup !== this.state.currentGroup && nextProps.currentGroup.blocks)
            this.setState({blocks: nextProps.currentGroup.blocks})
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
    handleEditBlock = (edittedBlock) => this.props.editBlock(edittedBlock, this.props.currentGroup.id);

    // DELETE BLOCK MODAL CONFIGS
    // this called from block.js when you click on delete block button
    deleteBlock = (deletedBlock) => confirm({
        title: `Delete block with type: ${deletedBlock.type}`,
        content: `You can't get back to the deleted block after click ok`,
        onOk: () => this.handleDeleteBlock(deletedBlock)
    });
    handleDeleteBlock = (deletedBlock) => {
        this.props.deleteBlock(deletedBlock, this.props.currentGroup.id);

        // Remove the deletedBlock
        let blocks = this.state.blocks.filter((block) => block.id !== deletedBlock.id);
        // Update order
        for (const i in blocks) blocks[i].order = Number(i) + 1;
        this.setState({blocks});
        // send a request to the server
        this.props.reorderBlocks(blocks, this.props.currentGroup.id)
    };



    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Panel_Header}>
                    <div>
                        <h3>{this.props.currentGroup.name} Blocks</h3>
                    </div>
                    <div>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                onClick={this.showAddBlockModal} disabled={!this.props.currentGroup.id}>
                            Add Block
                        </Button>
                    </div>
                </div>

                <div className={styles.Panel_Body}>
                    <div style={{height: "100%", width: '100%', overflowY: 'auto'}}>

                        <DragDropContext onDragEnd={this.onDragEnd}>
                            <Droppable droppableId="droppable">
                                {(provided) => (
                                    <div ref={provided.innerRef}>
                                        {this.state.blocks.map((block, index) => (
                                            <Draggable key={block.id} draggableId={block.order} index={index}>
                                                {(provided) => (
                                                    <div ref={provided.innerRef} {...provided.draggableProps}
                                                         {...provided.dragHandleProps}
                                                         style={getItemStyle(provided.draggableProps.style)}>
                                                        <Block block={block}
                                                               editBlock={this.editBlock}
                                                               deleteBlock={this.deleteBlock}
                                                        />
                                                    </div>
                                                )}
                                            </Draggable>
                                        ))}
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

                               blocks={this.state.blocks}
                               currentGroup={this.props.currentGroup}
                               allGroups={this.props.allGroups}/>

                <EditBlockModal visible={this.state.editBlockVisible}
                                handleEditBlock={this.handleEditBlock}
                                closeModal={this.closeEditBlockModal}

                                block={this.state.edittedBlock}
                                blocks={this.state.blocks}
                                currentGroup={this.props.currentGroup}
                                allGroups={this.props.allGroups}/>
            </div>
        );
    }
}

export default Form.create()(Blocks);
