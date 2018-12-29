import React, {Component} from 'react';
import "./Assistant.less"
import {Card, Dropdown, Icon, Menu, Switch} from 'antd';
import {Link} from "react-router-dom";
import AssistantSettings from "./AssistantSettings/AssistantSettings";

const {Meta} = Card;


const menu = (assistant) => (
    <Menu>
        <Menu.Item key="1">
            <Link to={{
                      pathname: `assistants/${assistant.ID}/solutions`,
                      state: {assistant: assistant}
                  }}>
                <Icon type="database"/> Solutions
            </Link>
        </Menu.Item>
        <Menu.Item key="2">
            <Link to={{
                      pathname: `assistants/${assistant.ID}/userInput`,
                      state: {assistant: assistant}
                  }}>
                <Icon type="code"/> User Input
            </Link>
        </Menu.Item>
        <Menu.Item key="3">
            <Link to={{
                      pathname: `assistants/${assistant.ID}/analytics`,
                      state: {assistant: assistant}
                  }}>
                <Icon type="line-chart"/> Analytics
            </Link>
        </Menu.Item>
        <Menu.Divider/>
        <Menu.Item key="4">
            <Link to={{
                      pathname: `assistants/${assistant.ID}/integration`,
                      state: {assistant: assistant}
                  }}>
                <Icon type="sync"/> Integration
            </Link>
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

    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    hideModal = () => {
        this.setState({
            visible: false,
        });
    };

    onActiveChanged = () => {

    }

    render() {
        const {assistant} = this.props;
        return (
            <>
                <Card loading={this.props.isLoading} style={{width: 300, margin: 15, float: 'left', height: 369}}
                      cover={
                          <img alt="example"
                               height={200}
                               width="100%"
                               src={covers[Math.floor(Math.random() * covers.length)]}/>
                      }
                      title={assistant.Name}
                      extra={<Switch defaultChecked={assistant.Active} onChange={this.onActiveChanged}/>}
                      actions={[
                          <div onClick={this.showModal}>
                              <Icon type="setting"/>
                              <span> Settings</span>
                          </div>,

                          <div>
                              <Link
                                  to={{
                                      pathname: `assistants/${assistant.ID}/flow`,
                                      state: {assistant: assistant}
                                  }}>
                                  <Icon type="build"/>
                                  <span> Flow</span>
                              </Link>
                          </div>,

                          <Dropdown overlay={menu(assistant)} trigger={['click']}>
                              <a className="ant-dropdown-link">
                                  ...
                              </a>
                          </Dropdown>]}>
                    <Meta description={assistant.TopBarText}/>
                </Card>

                <AssistantSettings assistant={assistant}
                                   hideModal={this.hideModal}
                                   visible={this.state.visible}/>

            </>
        )
    }
}

export default Assistant;
