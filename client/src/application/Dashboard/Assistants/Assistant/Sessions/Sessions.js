import React from 'react';
import styles from "./Sessions.module.less"
import ViewsModal from "./ViewModal/ViewsModal";
import {Button, Modal, Table, Tag} from 'antd';
import moment from 'moment';
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
        viewModal: false
    };


    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    }

    refreshSessions = () => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    };

    clearAllChatbotSessions = () => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.clearAllChatbotSessions(assistant.ID))
    };


    handleFilter = (pagination, filters, sorter) => {
        console.log('Various parameters', pagination, filters, sorter);
        this.setState({
            filteredInfo: filters,
            sortedInfo: sorter,
        });
    };


    closeViewModal = () => {
        this.setState({viewModal: false, selectedSession: null})
    };


    showConfirmForClearing = () => {
        const clear = this.clearAllChatbotSessions;
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk() {clear()},
            onCancel() {},
        });
    };



    // Nested table that has all the answered questions per session (Not being used)
    expandedRowRender = (record, index, indent, expanded) => {
        const columns = [
            {
                title: 'Question',
                key: 'questionText',
                render: (text, record, index) => (<p>{record.questionText}</p>),
            },
            {
                title: 'Input',
                key: 'input',
                render: (text, record, index) => {

                    if (record.input === '&FILE_UPLOAD&') {
                        this.filesCounter+=1;
                        return (<Button hreftype="primary" data-index={this.filesCounter} icon="download" size="small"
                                        onClick={(e) => {this.downloadFile(e)}}>
                            Download File
                        </Button>);
                    }

                    else {
                        return (<p>
                            {record.input}
                        </p>);
                    }
                },
            }
        ];


        return (
            <Table
                columns={columns}
                dataSource={record.Data.collectedData}
                pagination={false}
                scroll={{ y: 500 }}
            />
        );
    };


    render() {
        const {assistant} = this.props.location.state;
        const {sessions} = this.props;
        let { sortedInfo, filteredInfo } = this.state;
        sortedInfo = sortedInfo || {};
        filteredInfo = filteredInfo || {};

        const columns = [{
            title: '#',
            dataIndex: '#',
            key: '#',
            render: (text, record, index) => (<p>{index+1}</p>),

        },{
            title: 'ID',
            dataIndex: 'ID',
            key: 'ID',
            sorter: (a, b) => a.ID - b.ID,
            render: (text, record) => (<p>{record.ID}</p>),

        },{
            title: 'User Type',
            dataIndex: 'UserType',
            key: 'UserType',
            filters: [
                { text: 'Candidate', value: 'Candidate' },
                { text: 'Client', value: 'Client' },
            ],
            onFilter: (value, record) => {
                console.log(value);
                record.UserType.includes(value)},
            render: (text, record) => (<Tag key={record.UserType}>{record.UserType}</Tag>),

        },{
            title: 'Questions Answered',
            dataIndex: 'QuestionsAnswered',
            key: 'QuestionsAnswered',
            sorter: (a, b) => a.QuestionsAnswered - b.QuestionsAnswered,
            render: (text, record) => (
                <p style={{textAlign:''}}>{text}</p>),

        }, {
            title: 'Solutions Returned',
            dataIndex: 'SolutionsReturned',
            sorter: (a, b) => a.SolutionsReturned - b.SolutionsReturned,
            render: (text, record) => (
                <p style={{textAlign:''}}>{text}</p>),

        }, {
            title: 'Time Spent',
            dataIndex: 'TimeSpent',
            key: 'TimeSpent',
            sorter: (a, b) => a.TimeSpent - b.TimeSpent,
            render: (text, record) => (<p style={{textAlign:'center'}}>{
                moment.duration(parseInt(record.TimeSpent), 'seconds').asMinutes().toFixed(2) + " minute(s)"
            }
            </p>),

        },{
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
              <a onClick={()=> {
                  this.setState({viewModal: true, selectedSession: record})
              }
              }> View</a>
                    {/*<Divider type="vertical" />*/}
                    {/*<a>Delete</a>*/}
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
                                    onClick={this.showConfirmForClearing} loading={this.props.isClearingAll}>
                                Clear All
                            </Button>
                        </div>
                    </div>

                    <div className={styles.Panel_Body}>

                        <Table columns={columns}
                               dataSource={sessions.sessionsList ? sessions.sessionsList : null}
                               onChange={this.handleFilter}
                               loading={this.props.isLoading}
                            // expandedRowRender={this.expandedRowRender}
                               size='middle'
                        />

                        <ViewsModal visible={this.state.viewModal}
                                    closeViewModal={this.closeViewModal}
                                    filesPath={sessions.filesPath}
                                    dataTypes={sessions.dataTypes}
                                    session={this.state.selectedSession}
                                    assistant={assistant}
                        />
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state =>  {
    const {chatbotSessions} = state;
    return {
        sessions: chatbotSessions.chatbotSessions,
        isLoading: chatbotSessions.isLoading,
        errorMsg: chatbotSessions.errorMsg,

        isClearingAll: chatbotSessions.isClearingAll
    };
};
export default connect(mapStateToProps)(Sessions);