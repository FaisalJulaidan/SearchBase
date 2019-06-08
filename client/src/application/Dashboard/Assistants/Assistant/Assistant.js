import React, {Component} from 'react';
import {connect} from 'react-redux';
import { Prompt } from "react-router-dom";
import {Button, Col, Row, Switch, Tabs, Typography, Spin, Modal} from 'antd';
import './Assistant.less';
import styles from "./Assistant.module.less";
import {Link} from "react-router-dom";
import CRM from "./CRM/CRM";
import SelectAutoPilotModal from "./SelectAutoPilotModal/SelectAutoPilotModal";
import AuroraBlink from "components/AuroraBlink/AuroraBlink";

import Conversations from "./Conversations/Conversations"
import Settings from "./Settings/Settings"
import Integration from "./Integration/Integration"
import Analytics from "./Analytics/Analytics"
import Flow from "./Flow/Flow"

import {getLink, history} from "helpers";
import {store} from "store/store";
import {assistantActions, crmActions} from "store/actions";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {optionsActions} from "store/actions";


const {Title, Paragraph, Text} = Typography;
const { TabPane } = Tabs;
const confirm = Modal.confirm;

class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false,
        selectAutoPilotModalVisible: false,
        isFlowSaved: true
    };

    componentDidMount() {
        store.dispatch(assistantActions.fetchAssistant(this.props.match.params.id))
            .then(()=> {}).catch(() => history.push(`/dashboard/assistants`));

        if (!this.props.options) store.dispatch(optionsActions.getOptions())
    }


    isAssistantNameValid = (name) => {
        return !(this.props.assistantList.findIndex(assistant => assistant.Name.toLowerCase() === name.toLowerCase()) >= 0)
    };

    onActivateHandler = (checked) => {
        if(!checked){
            confirm({
                title: `Deactivate assistant`,
                content: <p>Are you sure you want to deactivate this assistant</p>,
                onOk: () => {
                    this.props.dispatch(assistantActions.changeAssistantStatus(this.props.assistant.ID, checked))
                }
            });
            return;
        }
        this.props.dispatch(assistantActions.changeAssistantStatus(this.props.assistant.ID, checked))
    };

    onTabClick = (key, e) => {
        if (key !== 'Script'){
            if (!this.state.isFlowSaved) {
                console.log('reload?');
                window.onbeforeunload = () => true
            } else {
                window.onbeforeunload = undefined
            }
        }
    };

    setIsFlowSaved = (bool) => {
        this.setState({isFlowSaved: !!bool})
    };


    render() {
        const {assistant, isAssistantLoading} = this.props;

        return (

            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>

                        <Row>
                            <Col span={20}>
                                <Title className={styles.Title}>
                                    {assistant?.Name}
                                </Title>
                                <Paragraph type="secondary">
                                    {assistant?.Description || 'No description'}
                                </Paragraph>
                            </Col>
                            <Col span={4}>
                                <Switch checkedChildren="On" unCheckedChildren="Off"
                                        checked={assistant?.Active}
                                        loading={this.props.isStatusChanging}
                                        onChange={this.onActivateHandler}
                                        style={{marginTop: '17%', marginLeft: '70%'}}/>
                            </Col>

                        </Row>

                    </div>

                    <div className={[styles.Body, 'assistantTabs'].join(' ')}>
                        {!assistant ? <Spin/> :

                            <Tabs defaultActiveKey={'Script'} size={"large"} animated={false} onTabClick={this.onTabClick}>
                                <TabPane tab="Analytics" key="Analytics">
                                    <Analytics assistant={assistant}/>
                                </TabPane>
                                <TabPane tab="Conversations" key="Conversations">
                                    <Conversations assistant={assistant} />
                                </TabPane>

                                <TabPane tab="Script" key="Script">
                                    <Flow setIsFlowSaved={this.setIsFlowSaved}
                                          isFlowSaved={this.state.isFlowSaved}
                                          assistant={{assistant}} />
                                </TabPane>

                                <TabPane tab="Connections" key="Connections">
                                    Content of tab 3
                                </TabPane>

                                <TabPane tab="Integration" key="Integration">
                                    <Integration assistant={assistant}/>
                                </TabPane>

                                <TabPane tab="Settings" key="Settings">
                                    <Settings assistant={assistant}
                                              isAssistantNameValid={this.isAssistantNameValid} />
                                </TabPane>
                            </Tabs>
                        }
                    </div>
                </NoHeaderPanel>

                <Prompt when={!this.state.isFlowsaved}
                        message={() => `Your script is not saved are you sure you want leave without saving it?`}/>

                {/*<AssistantSettings assistant={assistant}*/}
                                   {/*isAssistantNameValid={this.props.isAssistantNameValid}*/}
                                   {/*hideModal={this.hideSettingsModal}*/}
                                   {/*visible={this.state.assistantSettingsVisible}/>*/}

                {/*<CRM assistant={assistant}*/}
                     {/*CRMsList={this.props.CRMsList}*/}
                     {/*hideModal={this.hideCRMModal}*/}
                     {/*visible={this.state.CRMVisible}/>*/}

                {/*<SelectAutoPilotModal*/}
                    {/*assistant={assistant}*/}
                    {/*hideModal={this.hideSelectAutoPilotModal}*/}
                    {/*selectAutoPilotModalVisible={this.state.selectAutoPilotModalVisible}/>*/}

            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList,
        assistant: state.assistant.assistant,
        isAssistantLoading: state.assistant.isLoading,
        options: state.options.options,
        isLoading: state.assistant.isLoading,
        isStatusChanging: state.assistant.isStatusChanging,
    };
}

export default connect(mapStateToProps)(Assistant);
