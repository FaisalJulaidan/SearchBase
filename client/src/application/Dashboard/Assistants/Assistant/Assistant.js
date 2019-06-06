import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Button, Card, Col, Row, Switch, Tabs, Typography, Spin} from 'antd';
import './Assistant.less';
import styles from "./Assistant.module.less";
import {Link} from "react-router-dom";
import CRM from "./CRM/CRM";
import SelectAutoPilotModal from "./SelectAutoPilotModal/SelectAutoPilotModal";
import AuroraBlink from "components/AuroraBlink/AuroraBlink";
import Conversations from "./Conversations/Conversations"
import Settings from "./Settings/Settings"
import {getLink, history} from "helpers";
import {store} from "store/store";
import {assistantActions, crmActions} from "store/actions";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {optionsActions} from "../../../../store/actions";



const {Title, Paragraph, Text} = Typography;
const { TabPane } = Tabs;

class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false,
        selectAutoPilotModalVisible: false
    };

    componentDidMount() {
        console.log("1111111111")
        store.dispatch(assistantActions.fetchAssistant(this.props.match.params.id))
            .then(()=> {}).catch(() => history.push(`/dashboard/assistants`));

        if (!this.props.options) store.dispatch(optionsActions.getOptions())
    }

    isAssistantNameValid = (name) => {
        return !(this.props.assistantList.findIndex(assistant => assistant.Name.toLowerCase() === name.toLowerCase()) >= 0)
    };


    showSettingsModal = () => this.setState({assistantSettingsVisible: true});
    hideSettingsModal = () => this.setState({assistantSettingsVisible: false});

    showCRMModal = () => this.setState({CRMVisible: true});
    hideCRMModal = () => this.setState({CRMVisible: false});

    showSelectAutoPilotModal = () => this.setState({selectAutoPilotModalVisible: true});
    hideSelectAutoPilotModal = () => this.setState({selectAutoPilotModalVisible: false});

    onActiveChanged = checked => this.props.activateHandler(checked, this.props.assistant.ID);

    render() {
        const {assistant, isAssistantLoading} = this.props;

        return (

            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            {assistant?.Name}
                        </Title>
                        <Paragraph type="secondary">
                            {assistant?.Description || 'No description'}
                        </Paragraph>
                        {console.log(assistant)}

                    </div>

                    <div className={[styles.Body, 'assistantTabs'].join(' ')}>
                        {!assistant ? <Spin/> :

                            <Tabs defaultActiveKey={'2'} size={"large"}>
                                <TabPane tab="Analytics" key="1">
                                    Content of tab 1
                                </TabPane>
                                <TabPane tab="Conversations" key="2">
                                    <Conversations assistant={assistant} />
                                </TabPane>

                                <TabPane tab="Script" key="3">
                                    Content of tab 3
                                </TabPane>

                                <TabPane tab="Connections" key="4">
                                    Content of tab 3
                                </TabPane>

                                <TabPane tab="Integration" key="5">
                                    Content of tab 3
                                </TabPane>

                                <TabPane tab="Settings" key="6">
                                    <Settings assistant={assistant}
                                              isAssistantNameValid={this.isAssistantNameValid} />
                                </TabPane>
                            </Tabs>
                        }
                    </div>
                </NoHeaderPanel>

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
