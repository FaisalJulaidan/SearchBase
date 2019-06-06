import React, {Component} from 'react';
import {Button, Card, Col, Row, Switch, Tabs, Typography} from 'antd';
import './Assistant.less';
import styles from "./Assistant.module.less";
import {Link} from "react-router-dom";
import AssistantSettings from "./AssistantSettings/AssistantSettings";
import CRM from "./CRM/CRM";
import SelectAutoPilotModal from "./SelectAutoPilotModal/SelectAutoPilotModal";
import AuroraBlink from "components/AuroraBlink/AuroraBlink";
import {getLink, history} from "helpers";
import {store} from "store/store";
import {assistantActions, crmActions} from "store/actions";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'



const {Title, Paragraph, Text} = Typography;
const { TabPane } = Tabs;

class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false,
        selectAutoPilotModalVisible: false
    };

    componentWillMount() {
        store.dispatch(assistantActions.fetchAssistant(this.props.match.params.id)).then(()=> {

        }).catch(() => history.push(`/dashboard/assistants`))
    }

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
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            Assistants
                        </Title>
                        <Paragraph type="secondary">
                            Here you can see all assistants created by you
                        </Paragraph>

                    </div>


                    <div className={styles.Body}>
                        <Tabs>
                            <TabPane tab="Tab 1" key="1">
                                Content of tab 1
                            </TabPane>
                            <TabPane tab="Tab 2" key="2">
                                Content of tab 2
                            </TabPane>
                            <TabPane tab="Tab 3" key="3">
                                Content of tab 3
                            </TabPane>
                        </Tabs>
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

export default Assistant;
