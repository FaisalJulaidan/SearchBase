import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Prompt } from 'react-router-dom';
import { Breadcrumb, Col, Modal, Row, Spin, Switch, Tabs, Typography } from 'antd';
import './Assistant.less';
import styles from './Assistant.module.less';

import Conversations from './Conversations/Conversations';
import Settings from './Settings/Settings';
import Integration from './Integration/Integration';
import Analytics from './Analytics/Analytics';
import Flow from './Flow/Flow';
import Connections from './Connections/Connections';

import { history } from 'helpers';
import { assistantActions, conversationActions } from 'store/actions';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import queryString from 'query-string';


const { Title, Paragraph } = Typography;
const { TabPane } = Tabs;
const confirm = Modal.confirm;

class Assistant extends Component {

    state = {
        assistantSettingsVisible: false,
        CRMVisible: false,
        selectAutoPilotModalVisible: false,
        isFlowSaved: true,
        defaultTab: 'Conversations'
    };

    firstHead = null;

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistant(this.props.match.params.id))
            .then(() => {}).catch(() => history.push(`/dashboard/assistants`));

        // Set tab from url search params
        let params = queryString.parse(this.props.location.search);
        if (['Analytics', 'Conversations', 'Script', 'Connections', 'Settings'].includes(params['tab']))
            this.setState({ defaultTab: params['tab'] });

        window.onbeforeunload = () => {
            if (!this.state.isFlowSaved)
                return 'You are leaving the page';
            else
                return null;
        };
    }

    componentDidMount() {
        setTimeout(() => this.firstHead = [...document.head.children], 1000);
    }

    componentWillUnmount() {
        this.removeChatbot();
    }

    onScriptTabChanges = () => {
        if (!this.state.isFlowSaved)
            Modal.warning({
                title: `Your script is not saved`,
                content: 'Please go back and save it'
            });
    };

    isAssistantNameValid = name => !(this.props.assistantList.findIndex(assistant => assistant.Name.toLowerCase() === name.toLowerCase()) >= 0);

    onActivateHandler = (checked) => {
        if (!checked) {
            confirm({
                title: `Deactivate assistant`,
                content: <p>Are you sure you want to deactivate this assistant</p>,
                onOk: () => {
                    this.props.dispatch(assistantActions.changeAssistantStatus(this.props.assistant.ID, checked));
                }
            });
            return;
        }
        this.props.dispatch(assistantActions.changeAssistantStatus(this.props.assistant.ID, checked));
    };

    onTabClick = (key, e) => {
        // this.firstHead = [...document.head.children];
        if (key !== 'Script') {
            this.removeChatbot();
            this.onScriptTabChanges();
        }
        if (key === 'Conversations') {
            // Ensure moving to conversation tab refresh conversations list
            this.props.dispatch(conversationActions.fetchConversations(this.props.assistant.ID));
        }
    };

    setIsFlowSaved = (bool) => {
        this.setState({ isFlowSaved: !!bool });
    };

    removeChatbot = () => {
        let oldBot = document.getElementById('TheSearchBase_Chatbot');
        let oldBotScript = document.getElementById('oldBotScript');

        if (oldBot && oldBotScript) {
            console.log('removing the chatbot');

            oldBot.remove();
            oldBotScript.remove();
            let newHead = document.head.children;
            let elements = [];

            // find all new css
            for (const element of newHead)
                if (!isNodeExist(element, this.firstHead))
                    elements.push(element);

            // remove all new css
            for (let i = 0; i < elements.length; i++) {
                if (!elements[i].getAttributeNames()[1]?.includes('data-react-beautiful-dnd'))
                    elements[i].remove();
            }

        }
    };

    render() {
        const { assistant, location } = this.props;

        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>

                        <div style={{ marginBottom: 20 }}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={'javascript:void(0);'}
                                       onClick={() => history.push('/dashboard/assistants')}>
                                        Assistants
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{assistant?.Name}</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>

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
                                        style={{ marginTop: '17%', marginLeft: '70%' }}/>
                            </Col>
                        </Row>
                    </div>

                    <div className={[styles.Body, 'assistantTabs'].join(' ')}>
                        {!assistant ? <Spin/> :

                            <Tabs defaultActiveKey={this.state.defaultTab} size={'large'} animated={false}
                                  onTabClick={this.onTabClick}>
                                <TabPane tab="Analytics" key="Analytics">
                                    <Analytics assistant={assistant}
                                               location={location}/>
                                </TabPane>
                                <TabPane tab="Conversations" key="Conversations">
                                    <Conversations assistant={assistant}
                                                   location={location}/>
                                </TabPane>

                                <TabPane tab="Script" key="Script">
                                    <Flow setIsFlowSaved={this.setIsFlowSaved}
                                          isFlowSaved={this.state.isFlowSaved}
                                          assistant={assistant}
                                          location={location}/>
                                </TabPane>

                                <TabPane tab="Connections" key="Connections">
                                    <Connections assistant={assistant}
                                                 location={location}/>
                                </TabPane>

                                <TabPane tab="Integration" key="Integration">
                                    <Integration assistant={assistant}
                                                 removeChatbot={this.removeChatbot}
                                                 location={location}/>
                                </TabPane>

                                <TabPane tab="Settings" key="Settings">
                                    <Settings assistant={assistant}
                                              isAssistantNameValid={this.isAssistantNameValid}
                                              location={location}/>
                                </TabPane>
                            </Tabs>
                        }
                    </div>
                </NoHeaderPanel>

                <Prompt when={!this.state.isFlowSaved}
                        message={() => `Your script is not saved are you sure you want leave without saving it?`}/>
            </>
        );
    }
}

const isNodeExist = (element, inArray) => {
    let isExist = false;
    for (const inArray_element of inArray)
        if (element.isEqualNode(inArray_element)) {
            isExist = true;
            break;
        }
    return isExist;
};


(function(arr) {
    arr.forEach(function(item) {
        if (item.hasOwnProperty('remove')) {
            return;
        }
        Object.defineProperty(item, 'remove', {
            configurable: true,
            enumerable: true,
            writable: true,
            value: function remove() {
                this.parentNode.removeChild(this);
            }
        });
    });
})([Element.prototype, CharacterData.prototype, DocumentType.prototype]);


function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList,
        assistant: state.assistant.assistant,
        isAssistantLoading: state.assistant.isLoading,
        isLoading: state.assistant.isLoading,
        isStatusChanging: state.assistant.isStatusChanging
    };
}

export default connect(mapStateToProps)(Assistant);
