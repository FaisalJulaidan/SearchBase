import React, {Component} from 'react';

import "./Blocks.less"
import styles from "../Flow.module.less";
import {Button, Drawer, Form} from "antd";
import {arrayMove, SortableContainer, SortableElement} from "react-sortable-hoc";

import BlocksDrawer from "./BlocksDrawer/BlocksDrawer";
import Block from "./Block/Block";


const SortableItem = SortableElement(({value, key}) =>
    <Block value={value} key={key}/>
);

const SortableList = SortableContainer(({items}) => {
    return (
        <div>
            {items.map(
                (value, index) => (
                    <SortableItem key={`item-${index}`} index={index} value={value}/>
                )
            )}
        </div>
    );
});


class Blocks extends Component {

    state = {
        visible: false,
        items: ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6'],
    };

    onSortEnd = ({oldIndex, newIndex}) => {
        this.setState({
            items: arrayMove(this.state.items, oldIndex, newIndex),
        });
        console.log(this.state.items)
    };

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
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div>
                        <h3>Blocks</h3>
                    </div>
                    <div>
                        <Button className={styles.PanelButton} type="primary" icon="plus"
                                onClick={this.showDrawer}>
                            Add Block
                        </Button>
                    </div>
                </div>

                <div className={styles.Body}>
                    <div style={{height: "100%", width: '100%', overflowY: 'auto    '}}>
                        <SortableList items={this.state.items} onSortEnd={this.onSortEnd}/>
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
