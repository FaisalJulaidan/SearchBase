import React, {Component} from 'react';
import "./Assistant.less"

import {Card, Dropdown, Icon, Menu, Switch} from 'antd';

const {Meta} = Card;


const menu = (
    <Menu>
        <Menu.Item key="1">
            <Icon type="database"/> Solutions
        </Menu.Item>
        <Menu.Item key="2">
            <Icon type="code"/>User Input
        </Menu.Item>
        <Menu.Item key="3">
            <Icon type="line-chart"/>Analytics
        </Menu.Item>
        <Menu.Divider/>
        <Menu.Item key="4">
            <Icon type="sync"/> Integration
        </Menu.Item>
    </Menu>
);

const covers = [
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/active_support_6rwo.svg',
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg',
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/group_chat_v059.svg',
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/status_update_jjgk.svg',
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/messages1_9ah2.svg'
];

class Assistant extends Component {

    state = {};

    onChange(checked) {
        // Send request to disable the assistant
        console.log(`switch to ${checked}`);
    }


    render() {
        const {assistant} = this.props;
        return (
            <Card style={{width: 300, margin: 15, float: 'left', height:369}}
                  cover={
                      <img alt="example"
                           height={200}
                           width="100%"
                           src={covers[Math.floor(Math.random() * covers.length)]}/>
                  }
                  title={assistant.Name}
                  extra={<Switch defaultChecked={assistant.Active} onChange={this.onChange}/>}
                  actions={[
                      <div>
                          <Icon type="setting"/>
                          <span> Settings</span>
                      </div>,
                      <div>
                          <Icon type="build"/>
                          <span> Flow</span>
                      </div>,

                      <Dropdown overlay={menu} trigger={['click']}>
                          <a className="ant-dropdown-link">
                              ...
                          </a>
                      </Dropdown>]}>
                <Meta
                    description={assistant.TopBarText}
                />
            </Card>

        );
    }
}

export default Assistant;
