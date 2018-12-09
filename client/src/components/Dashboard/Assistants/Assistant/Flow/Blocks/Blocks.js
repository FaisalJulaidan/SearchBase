import React, {Component} from 'react';

import "./Blocks.less"
import styles from "../Flow.module.less";
import {Button, Drawer, Form} from "antd";

import BlocksDrawer from "./BlocksDrawer/BlocksDrawer";
import Block from "./Block/Block";
import {DragDropContext, Droppable, Draggable} from 'react-beautiful-dnd';

// a little function to help us with reordering the result
const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

const getItemStyle = draggableStyle => ({margin: `0 0 8px 0`, ...draggableStyle});

class Blocks extends Component {

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


    state = {
        visible: false,
        blocks: []
    };

    componentWillReceiveProps(nextProps) {
        if (nextProps.currentGroup !== this.state.currentGroup && nextProps.currentGroup.blocks)
            this.setState({blocks: nextProps.currentGroup.blocks})
    }


    showDrawer = () => {
        this.setState({
            visible: true,
        });
    };

    onClose = () => {
        this.setState({
            visible: false,
        });
    };


    render() {
        console.log(this.props.currentGroup)
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div>
                        <h3>{this.props.currentGroup.name} Blocks</h3>
                    </div>
                    <div>
                        <Button className={styles.PanelButton} type="primary" icon="plus"
                                onClick={this.showDrawer} disabled={!this.props.currentGroup.id}>
                            Add Block
                        </Button>
                    </div>
                </div>

                <div className={styles.Body}>
                    <div style={{height: "100%", width: '100%', overflowY: 'auto'}}>
                        {/*<SortableList blocks={this.state.blocks}*/}
                        {/*onSortEnd={this.onSortEnd}/>*/}

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
                                                        <Block block={block}/>
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

                <Drawer title="Configure Block"
                        placement="right" mask={false}
                        onClose={this.onClose}
                        visible={this.state.visible}
                        width={'45%'}>
                    <BlocksDrawer onClose={this.onClose}/>
                </Drawer>
            </div>
        );
    }
}

export default Form.create()(Blocks);
