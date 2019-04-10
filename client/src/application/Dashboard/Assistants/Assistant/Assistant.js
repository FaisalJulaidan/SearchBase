import React, {Component} from 'react';
import {Card, Row, Col, Divider, Switch, Button} from 'antd';
import {Link} from "react-router-dom";
import AssistantSettings from "./AssistantSettings/AssistantSettings";
import CRM from "./CRM/CRM";
import './Assistant.less';
import AuroraBlink from "components/AuroraBlink/AuroraBlink";

const {Meta} = Card;


const covers = [
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg',
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/group_chat_v059.svg',
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/status_update_jjgk.svg',
    'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/messages1_9ah2.svg'
];


class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false
    };


    showSettingsModal = () => this.setState({assistantSettingsVisible: true});
    hideSettingsModal = () => this.setState({assistantSettingsVisible: false});

    showCRMModal = () => this.setState({CRMVisible: true});
    hideCRMModal = () => this.setState({CRMVisible: false});

    onActiveChanged = checked => this.props.activateHandler(checked, this.props.assistant.ID);

    render() {
        const {assistant, isStatusChanging} = this.props;
        return (
            <>
                <Card loading={this.props.isLoading}
                      style={{width: 500, margin: 15, float: 'left', height: 321}}
                      cover={
                          <img alt="example"
                               height={150}
                               width="100%"
                               src={covers[Math.floor(Math.random() * covers.length)]}/>
                      }
                      title={assistant.Name}
                      extra={<Switch loading={isStatusChanging} checked={assistant.Active} onChange={this.onActiveChanged}/>}
                      actions={[]}
                      className={'assistant'}>

                    <Row type={'flex'} justify={'center'} gutter={8}>
                        <Col span={8}>
                            {/*1*/}
                            <Button block icon={'setting'} onClick={this.showSettingsModal}>Settings</Button>
                        </Col>

                        <Col span={8}>
                            {/*2*/}
                            <Link to={{
                                pathname: `assistants/${assistant.ID}/script`,
                                state: {assistant: assistant}
                            }}>
                                <Button block icon={'build'}>Script</Button>
                            </Link>
                        </Col>

                        <Col span={8}>
                            {/*3*/}
                            <Button block onClick={this.showCRMModal} icon={'cluster'}>
                                CRM
                                {assistant.CRMConnected ? <AuroraBlink color={'#00c878'}/> : null}
                            </Button>
                        </Col>
                    </Row>

                    <Row type={'flex'} justify={'center'} gutter={8}>
                        <Col span={8}>
                            {/*4*/}
                            <Link to={{
                                pathname: `assistants/${assistant.ID}/sessions`,
                                state: {assistant: assistant}
                            }}>
                                <Button block icon={'code'}>Conversations</Button>
                            </Link>
                        </Col>

                        <Col span={8}>
                            {/*5*/}
                            <Link to={{
                                pathname: `assistants/${assistant.ID}/analytics`,
                                state: {assistant: assistant}
                            }}>
                                <Button block icon={'line-chart'}>Analytics</Button>
                            </Link>

                        </Col>

                        <Col span={8}>
                            {/*6*/}
                            <Link to={{
                                pathname: `assistants/${assistant.ID}/integration`,
                                state: {assistant: assistant}
                            }}>
                                <Button block icon={'sync'}>Integration</Button>
                            </Link>
                        </Col>
                    </Row>
                </Card>

                <AssistantSettings assistant={assistant}
                                   isAssistantNameValid={this.props.isAssistantNameValid}
                                   hideModal={this.hideSettingsModal}
                                   visible={this.state.assistantSettingsVisible}/>

                <CRM assistant={assistant}
                     hideModal={this.hideCRMModal}
                     visible={this.state.CRMVisible}/>

            </>
        )
    }
}

export default Assistant;
