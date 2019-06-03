import React, {Component} from 'react';
import {Button, Card, Col, Row, Switch} from 'antd';
import {Link} from "react-router-dom";
import AssistantSettings from "./AssistantSettings/AssistantSettings";
import CRM from "./CRM/CRM";
import SelectAutoPilotModal from "./SelectAutoPilotModal/SelectAutoPilotModal";
import './Assistant.less';
import AuroraBlink from "components/AuroraBlink/AuroraBlink";
import {getLink} from "helpers";

const covers = [
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg',
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/group_chat_v059.svg',
    // 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/status_update_jjgk.svg',
    getLink('/static/images/undraw/messages.svg'),
];


class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false,
        selectAutoPilotModalVisible: false
    };


    showSettingsModal = () => this.setState({assistantSettingsVisible: true});
    hideSettingsModal = () => this.setState({assistantSettingsVisible: false});

    showCRMModal = () => this.setState({CRMVisible: true});
    hideCRMModal = () => this.setState({CRMVisible: false});

    showSelectAutoPilotModal = () => this.setState({selectAutoPilotModalVisible: true});
    hideSelectAutoPilotModal = () => this.setState({selectAutoPilotModalVisible: false});

    onActiveChanged = checked => this.props.activateHandler(checked, this.props.assistant.ID);

    render() {
        const {assistant, isStatusChanging} = this.props;
        return (
            <>
                <Card loading={this.props.isLoading}
                      style={{width: 500, margin: 15, float: 'left', height: 369}}
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
                            {/*4*/}
                            <Link to={{
                                pathname: `assistants/${assistant.ID}/conversations`,
                                state: {assistant: assistant}
                            }}>
                                <Button block icon={'code'}>Conversations</Button>
                            </Link>
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
                                {assistant.CRMConnected ?
                                    <AuroraBlink color={'#00c878'} style={{top: 7, right: 28}}/> : null}
                            </Button>
                        </Col>
                    </Row>

                    <Row type={'flex'} justify={'center'} gutter={8}>
                        <Col span={8}>
                            {/*1*/}
                            <Button block icon={'setting'} onClick={this.showSettingsModal}>Settings</Button>
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

                    <Row type={'flex'} justify={'center'} gutter={8}>
                        <Col span={24}>
                            <Button block icon={'api'}
                                    onClick={this.showSelectAutoPilotModal}
                            >Connect Auto Pilot</Button>
                        </Col>

                    </Row>
                </Card>

                <AssistantSettings assistant={assistant}
                                   isAssistantNameValid={this.props.isAssistantNameValid}
                                   hideModal={this.hideSettingsModal}
                                   visible={this.state.assistantSettingsVisible}/>

                <CRM assistant={assistant}
                     CRMsList={this.props.CRMsList}
                     hideModal={this.hideCRMModal}
                     visible={this.state.CRMVisible}/>

                <SelectAutoPilotModal
                    assistant={assistant}
                    hideModal={this.hideSelectAutoPilotModal}
                    selectAutoPilotModalVisible={this.state.selectAutoPilotModalVisible}/>

            </>
        )
    }
}

export default Assistant;
