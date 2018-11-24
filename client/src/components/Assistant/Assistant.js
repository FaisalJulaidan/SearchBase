import React, {Component} from 'react';
import "./Assistant.less"

import {Card, Icon, Tooltip} from 'antd';

const {Meta} = Card;

class Assistant extends Component {
    state = {};

    render() {
        return (
            <Card style={{width: 200, margin: 15, float: 'left'}}
                  cover={<img alt="example"
                              src="https://assets.wired.com/photos/w_1164/wp-content/uploads/2016/04/chat_bot-01.jpg"/>}
                  actions={[
                      <Tooltip title="Setting">
                          <Icon type="setting"/>
                      </Tooltip>,

                      <Tooltip title="Edit">
                          <Icon type="edit"/>
                      </Tooltip>,

                      <Tooltip title="Integration">
                          <Icon type="sync"/>
                      </Tooltip>,
                  ]}
            >
                <Meta
                    title={`Bot ${this.props.index + 1}`}
                    description="This is the Bot 1"
                />
            </Card>

        );
    }
}

export default Assistant;
