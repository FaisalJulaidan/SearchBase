import React from 'react';
import styles from "./Sessions.module.less"
import ViewsModal from "./ViewModal/ViewsModal";
import {Button, Modal, Table, Tag, Divider} from 'antd';
import {chatbotSessionsActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import Header from "../../../../../components/Header/Header";

const confirm = Modal.confirm;


class Sessions extends React.Component {

    filesCounter=-1; // important for file uploads
    state = {
        filteredInfo: null,
        sortedInfo: null,
        selectedSession: null,
        viewModal: false,
        destroyModal: false
    };


    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    }

    refreshSessions = () => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    };


    handleFilter = (pagination, filters, sorter) => {
        console.log('Various parameters', pagination, filters, sorter);
        this.setState({
            filteredInfo: filters,
            sortedInfo: sorter,
        });
    };


    closeViewModal = () => {
        this.setState({viewModal: false, selectedSession: null}, () => {
            setTimeout(function () { //Start the timer
                this.setState({destroyModal: false}) //After 0.5 second, set render to true
            }.bind(this), 170)
        })
    };


    clearAllChatbotSessions = (assistantID) => {
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk: ()=> {
                this.props.dispatch(chatbotSessionsActions.clearAllChatbotSessions(assistantID))
            },
        });
    };


    deleteSession = (deletedSession) => {
        const ID = deletedSession?.ID;
        const AssistantID = deletedSession?.AssistantID;


        if (ID && AssistantID)
            confirm({
                title: `Delete session confirmation`,
                content: `If you click OK, this session will be deleted with its associated data forever`,
                okType: 'danger',
                onOk: () => {
                    if (this.state.viewModal)
                        this.getNextSession(deletedSession);
                    this.props.dispatch(chatbotSessionsActions.deleteChatbotSession(ID, AssistantID))
                },
                maskClosable: true
            });
    };


    getNextSession = currentSession => {
        const {sessionsList} = this.props.sessions;
        const index = sessionsList?.findIndex(session => session?.ID === currentSession?.ID);
        if (index > -1)
            this.setState({selectedSession: sessionsList[index + 1] ? sessionsList[index + 1] : sessionsList[index]})
    };

    getBackSession = currentSession => {
        const {sessionsList} = this.props.sessions;
        const index = sessionsList?.findIndex(session => session?.ID === currentSession?.ID);
        if (index > -1)
            this.setState({selectedSession: sessionsList[index - 1] ? sessionsList[index - 1] : sessionsList[index]})
    };


    render() {
        const {assistant} = this.props.location.state;
        const {sessions, options} = this.props;

        const columns = [{
            title: '#',
            dataIndex: '#',
            key: '#',
            render: (text, record, index) => (<p>{index + 1}</p>),

        }, {
            title: 'ID',
            dataIndex: 'ID',
            key: 'ID',
            sorter: (a, b) => a.ID - b.ID,
            render: (text, record) => (<p>{record.ID}</p>),

        }, {
            title: 'User Type',
            dataIndex: 'UserType',
            key: 'UserType',
            filters: [
                {text: 'Candidate', value: 'Candidate'},
                {text: 'Client', value: 'Client'},
            ],
            onFilter: (value, record) => record.UserType ? record.UserType.indexOf(value) === 0 : false,
            render: (text, record) => (<Tag key={record.UserType}>{record.UserType}</Tag>),

        }, {
            title: 'Questions Answered',
            dataIndex: 'QuestionsAnswered',
            key: 'QuestionsAnswered',
            sorter: (a, b) => a.QuestionsAnswered - b.QuestionsAnswered,
            render: (text, record) => (
                <p style={{textAlign: ''}}>{text}</p>),

        }, {
            title: 'Solutions Returned',
            dataIndex: 'SolutionsReturned',
            sorter: (a, b) => a.SolutionsReturned - b.SolutionsReturned,
            render: (text, record) => (
                <p style={{textAlign: ''}}>{text}</p>),

        }, {
            title: 'Time Spent',
            dataIndex: 'TimeSpent',
            key: 'TimeSpent',
            sorter: (a, b) => a.TimeSpent - b.TimeSpent,
            render: (_, record) => {
                let date = new Date(null);
                date.setSeconds(record.TimeSpent); // specify value for SECONDS here
                let mm = date.getUTCMinutes();
                let ss = date.getSeconds();
                if (mm < 10) mm = "0" + mm;
                if (ss < 10) ss = "0" + ss;

                return <p>{`${mm}:${ss}`} mins</p>
            }
        }, {
            title: 'Date & Time',
            dataIndex: 'DateTime',
            key: 'DateTime',
            sorter: (a, b) => new Date(a.DateTime).valueOf() - new Date(b.DateTime).valueOf(),
            render: (text, record) => (<p>{record.DateTime}</p>),

        }, {
            title: 'Action',
            key: 'action',
            render: (text, record, index) => (
                <span>
              <a onClick={() => {
                  this.setState({viewModal: true, selectedSession: record, destroyModal: true})
              }}>
                  View
              </a>
                    <Divider type="vertical" />
              <a onClick={() => {
                  this.deleteSession(record)
              }}>
                  Delete
              </a>
            </span>
            ),
        }];


        return (
            <div style={{height: '100%'}}>
                <Header display={assistant.Name}/>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>{assistant.Name}: conversations</h3>
                            <p>Here you can find all the responses to your chatbot</p>
                        </div>

                        <div>
                            <Button className={styles.Panel_Header_Button} type="primary" icon="sync"
                                    onClick={this.refreshSessions} loading={this.props.isLoading}>
                                Refresh
                            </Button>


                            <Button className={styles.Panel_Header_Button} type="primary" icon="delete"
                                    disabled={!!(!sessions.sessionsList.length)}
                                    onClick={() => {
                                        this.clearAllChatbotSessions(assistant.ID)
                                    }} loading={this.props.isClearingAll}>
                                Clear All
                            </Button>
                        </div>
                    </div>

                    <div className={styles.Panel_Body}>
                        <Table columns={columns}
                               dataSource={sessions.sessionsList}
                               onChange={this.handleFilter}
                               loading={this.props.isLoading}
                               size='middle'
                        />

                        {
                            this.state.destroyModal && <ViewsModal visible={this.state.viewModal}
                                                                   closeViewModal={this.closeViewModal}
                                                                   filesPath={sessions.filesPath}
                                                                   flowOptions={options?.flow}
                                                                   session={this.state.selectedSession}
                                                                   assistant={assistant}
                                                                   getNextSession={this.getNextSession}
                                                                   getBackSession={this.getBackSession}
                                                                   deleteSession={this.deleteSession}/>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state =>  {
    const {chatbotSessions} = state;
    return {
        options: state.options.options,
        sessions: chatbotSessions.chatbotSessions,
        isLoading: chatbotSessions.isLoading,
        errorMsg: chatbotSessions.errorMsg,

        isClearingAll: chatbotSessions.isClearingAll
    };
};
export default connect(mapStateToProps)(Sessions);
