import React, {Component} from 'react';

import "./Blocks.less"
import styles from "../Flow.module.less";
import {Button, Form} from "antd";

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

class Blocks extends Component {

    state = {
        addBlockVisible: false,
        editBlockVisible: false,
        blocks: [],
        edittedBlock: {}
    };

    constructor(props) {
        super(props);
        this.onDragEnd = this.onDragEnd.bind(this);
    }

    onDragEnd(result) {
        // dropped outside the list
        if (!result.destination) return;

        const blocks = reorder(this.state.blocks, result.source.index, result.destination.index);
        this.setState({blocks});
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

    handleAddBlock = (newBlock) => {
        const {addBlock, currentGroup} = this.props;
        console.log(newBlock);
        addBlock(newBlock, currentGroup.id)
    };

    // EDIT BLOCK MODAL CONFIGS

    // this called from block.js when you click on edit block button
    editBlock = (edittedBlock) => this.setState({edittedBlock, editBlockVisible: true});
    closeEditBlockModal = () => this.setState({edittedBlock: {}, editBlockVisible: false});

    handleEditBlock = (edittedBlock) => {
        const {editBlock, currentGroup} = this.props;
        editBlock(edittedBlock, currentGroup.id)
    };

    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div>
                        <h3>{this.props.currentGroup.name} Blocks</h3>
                    </div>
                    <div>
                        <Button className={styles.PanelButton} type="primary" icon="plus"
                                onClick={this.showAddBlockModal} disabled={!this.props.currentGroup.id}>
                            Add Block
                        </Button>
                    </div>
                </div>

                <div className={styles.Body}>
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
