import React, {Component} from 'react';
import "./Assistant.less"
import styles from "./Assistant.modue.less"
import {Button, Card, Dropdown, Icon, Menu, Modal, Switch} from 'antd';
import {Link} from "react-router-dom";
import EditAssistant from "./EditAssistant/EditAssistant";

const {Meta} = Card;


const menu = (assistant) => (
    <Menu>
        <Menu.Item key="1">
            <Link to={`solutions/${assistant.ID}`}>
                <Icon type="database"/> Solutions
            </Link>
        </Menu.Item>
        <Menu.Item key="2">
            <Link to={`userInput/${assistant.ID}`}>
                <Icon type="code"/>User Input
            </Link>
        </Menu.Item>
        <Menu.Item key="3">
            <Link to={`analytics/${assistant.ID}`}>
                <Icon type="line-chart"/>Analytics
            </Link>
        </Menu.Item>
        <Menu.Divider/>
        <Menu.Item key="4">
            <Link to={`integration/${assistant.ID}`}>
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

    handleOk = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    handleCancel = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    editAssistantCallback = (editedAssistant) => {
        console.log(editedAssistant)
    };


    render() {
        const {assistant} = this.props;
        return (
            <>
                <Card loading={this.props.isLoading} style={{width: 300, margin: 15, float: 'left', height: 374}}
                      cover={
                          <img alt="example"
                               height={200}
                               width="100%"
                               src={covers[Math.floor(Math.random() * covers.length)]}/>
                      }
                      title={assistant.Name}
                      extra={
                          <div className="cardButtons">
                              <Switch defaultChecked={assistant.Active} onChange={this.onChange}/>
                              <div className='Edit'>
                                  <Button shape={"circle-outline"} icon={'edit'} size={"small"}
                                          onClick={this.showModal}/>
                              </div>
                          </div>
                      }
                      actions={[
                          <div>

                              <Link to={{
                                  pathname: `settings/${assistant.ID}`,
                                  state: {assistant: assistant}
                              }}>
                                  <Icon type="setting"/>
                                  <span> Settings</span>
                              </Link>
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
                    <Meta
                        description={assistant.TopBarText}
                    />
                </Card>
                <div>
                    <Modal
                        title="Edit Assistant"
                        visible={this.state.visible}
                        onOk={this.handleOk}
                        width={800}
                        onCancel={this.handleCancel}
                        destroyOnClose={true}
                        footer={[
                            <Button key="cancel" onClick={this.handleCancel}>Cancel</Button>,
                            <Button key="submit" type="primary" onClick={this.handleOk}>
                                Save
                            </Button>,
                        ]}>
                        <EditAssistant assistantCallback={this.editAssistantCallback} {...this.props} {...this.state} />
                    </Modal>
                </div>

            </>
        )
    }
}

export default Assistant;
