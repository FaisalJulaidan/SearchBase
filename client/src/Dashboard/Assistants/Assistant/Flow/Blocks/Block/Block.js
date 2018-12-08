import React, {Component} from 'react';
import {Button, Card, Collapse} from "antd";

const Panel = Collapse.Panel;

class Block extends Component {

    render() {
        const {block} = this.props;
        return (
            <Collapse bordered={true}>
                <Panel header={block.content.text} key={this.props.key}>
                    <Card title={block.content.text} style={{width: '100%'}} extra={<Button icon={'edit'}/>}>
                        <h4>{block.type}</h4>
                    </Card>
                </Panel>
            </Collapse>
        );
    }

}

export default Block;

