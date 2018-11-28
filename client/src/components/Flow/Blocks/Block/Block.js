import React, {Component} from 'react';
import {Card, Collapse} from "antd";

const Panel = Collapse.Panel;

class Block extends Component {

    render() {
        return (
            <Collapse bordered={true}>
                <Panel header={this.props.value} key={this.props.key}>
                    <Card title={this.props.value} style={{width: '100%'}}>
                        {this.props.value}
                    </Card>
                </Panel>
            </Collapse>
        );
    }

}

export default Block;

