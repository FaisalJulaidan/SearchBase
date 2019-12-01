import React from 'react';
import styles from './Conversations.module.less';
import './Conversations.less';
import ViewsModal from './ViewModal/ViewsModal';
import { Badge, Button, Divider, Icon, Modal, Popover, Progress, Table, Tag } from 'antd';
import { conversationActions } from 'store/actions';
import connect from 'react-redux/es/connect/connect';
import { CSVLink } from 'react-csv';
import queryString from 'query-string';
import { convertTimezone } from 'helpers';

const confirm = Modal.confirm;


class Conversations extends React.Component {

    hasModalOpenedFromURLOnMount = false;

    state = {
        filteredInfo: null,
        sortedInfo: null,
        selectedConversation: null,
        viewModal: false,
        destroyModal: false,
        downloadData: []
    };

    constructor(props) {
        super(props);
        this.columns = [
            {
                title: '#',
                key: '#',
                render: (text, record) => (<p>{record.ID}</p>)

            }, {
                title: 'User Type',
                key: 'UserType',
                filters: [
                    { text: 'Candidate', value: 'Candidate' },
                    { text: 'Client', value: 'Client' }
                ],
                onFilter: (value, record) => record.UserType.indexOf(value) === 0,
                render: (text, record) => (<Tag key={record.UserType}>{record.UserType}</Tag>)
            }, {
                title: 'Name',
                key: 'Name',
                render: (text, record) => (
                    <p style={{ textTransform: 'capitalize' }}>{record.Name}</p>)

            }, {
                title: 'Duration',
                key: 'TimeSpent',
                sorter: (a, b) => a.TimeSpent - b.TimeSpent,
                render: (_, record) => {
                    let date = new Date(null);
                    date.setSeconds(record.TimeSpent); // specify value for SECONDS here
                    let mm = date.getUTCMinutes();
                    let ss = date.getSeconds();
                    if (mm < 10) mm = '0' + mm;
                    if (ss < 10) ss = '0' + ss;

                    return <p>{`${mm}:${ss}`} mins</p>;
                }
            }, {
                title: 'Date & Time',
                key: 'DateTime',
                sorter: (a, b) => new Date(a.DateTime).valueOf() - new Date(b.DateTime).valueOf(),
                render: (text, record) => (<p>{convertTimezone(record.DateTime, 'ddd, DD MMM YYYY HH:mm A')}</p>)

            }, {
                title: 'Score',
                key: 'Score',
                sorter: (a, b) => a.Score - b.Score,
                render: (text, record) => {
                    return (
                        <div style={{ width: 120, margin:'auto'}}>
                            <Progress percent={Math.round(record.Score * 100)} size="small"
                                      status={record.Score < 0.1 ? 'exception' : 'active'}/>
                        </div>
                    );
                }

            }, {
                title: 'Status',
                key: 'ApplicationStatus',
                align: 'center',
                filters: [
                    { text: 'Accepted', value: 'Accepted' },
                    { text: 'Pending', value: 'Pending' },
                    { text: 'Rejected', value: 'Rejected' }
                ],
                onFilter: (value, record) => record.ApplicationStatus.indexOf(value) === 0,
                render: (text, record) => {
                    const { isUpdatingStatus } = this.props;
                    const content = (
                        <div>
                            <Button className={styles.StatusChangeBtn} type="link"
                                    disabled={isUpdatingStatus}
                                    onClick={() => this.updateStatus('Rejected', record)}>
                                <Icon type="close-circle" theme="filled"
                                      style={{ color: 'red', fontSize: '18px' }}/>
                            </Button>

                            <Button className={styles.StatusChangeBtn} type="link"
                                    style={{ color: '#faad14', fontSize: '18px' }}
                                    disabled={isUpdatingStatus}
                                    onClick={() => this.updateStatus('Pending', record)}>
                                <Icon type="clock-circle"/>
                            </Button>

                            <Button className={styles.StatusChangeBtn} type="link"
                                    disabled={isUpdatingStatus}
                                    onClick={() => this.updateStatus('Accepted', record)}>
                                <Icon type="check-circle" theme="filled"
                                      style={{ color: '#52c41a', fontSize: '18px' }}/>
                            </Button>
                        </div>
                    );

                    return (
                        <Popover placement="top" title="Change status?" content={content} trigger="hover">
                            {this.buildStatusBadge(record.ApplicationStatus)}
                        </Popover>
                    );
                }

            },
            {
                title: 'Conversation',
                key: 'Completed',
                align: 'center',
                filters: [
                    { text: 'Completed', value: 'Completed' },
                    { text: 'Incomplete', value: 'Incomplete' }
                ],
                onFilter: (value, record) => {
                    return (record.Completed ? 'Completed' : 'Incomplete').indexOf(value) === 0;
                },
                render: (text, record) => (
                    <div>
                        {record.Completed ?
                            <Tag color="#87d068">Completed</Tag> :
                            <Tag color="red">Incomplete</Tag>
                        }
                    </div>)

            }, {
                title: 'Actions',
                key: 'actions',
                align: 'center',
                render: (text, record, index) => (
                    <div align="center">

                         <Icon
                             onClick={() => this.showViewModal(record)}
                             type="message"
                             theme="twoTone"
                             twoToneColor="#9254de"/>

                        <Divider type="vertical"/>

                        <Icon
                            onClick={() => {
                                this.deleteConversation(record);
                            }}
                            type="delete"
                            theme="twoTone"
                            twoToneColor="#f5222d"/>
                </div>
                )
            }
        ];
    }


    componentDidMount() {
        const { assistant, dispatch } = this.props;
        dispatch(conversationActions.fetchConversations(assistant.ID));
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        const { conversations, location } = this.props;

        // Open conversation modal using passed id from the URL's search params (conversation_id)
        if (this.props !== prevProps && !this.hasModalOpenedFromURLOnMount) {
            let params = queryString.parse(location.search, { parseNumbers: true });
            if (params['conversation_id']) {
                let c = conversations.conversationsList?.find(c => c.ID === params['conversation_id']);
                if (c) {
                    this.showViewModal(c);
                    this.hasModalOpenedFromURLOnMount = true;
                }
            }
        }
    }


    componentWillReceiveProps(nextProps) {
        if (nextProps.conversations !== this.props.conversations)
            this.populateDownloadData(this.props.conversations);

        if (nextProps.conversations?.conversationsList && this.state.selectedConversation) {
            const updatedConversation = nextProps.conversations.conversationsList
                .find(c => this.state.selectedConversation.ID === c.ID);

            if (updatedConversation)
                this.setState({ selectedConversation: updatedConversation });
        }
    }

    refreshConversations = () => {
        const { assistant } = this.props;
        this.props.dispatch(conversationActions.fetchConversations(assistant.ID));
    };


    handleFilter = (pagination, filters, sorter) => {
        this.setState({
            filteredInfo: filters,
            sortedInfo: sorter
        });
    };

    showViewModal = (selectedConversation) => {
        this.setState({ viewModal: true, selectedConversation: selectedConversation, destroyModal: true });
    };

    closeViewModal = () => {
        this.setState({ viewModal: false, selectedConversation: null }, () => {
            setTimeout(function() { //Start the timer
                this.setState({ destroyModal: false }); //After 0.5 second, set render to true
            }.bind(this), 170);
        });
    };


    clearAllConversations = (assistantID) => {
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk: () => {
                this.props.dispatch(conversationActions.clearAllConversations(assistantID));
            }
        });
    };


    deleteConversation = (deletedConversation) => {
        const ID = deletedConversation?.ID;
        const AssistantID = deletedConversation?.AssistantID;

        if (ID && AssistantID)
            confirm({
                title: `Delete Conversation confirmation`,
                content: `If you click OK, this conversation will be deleted with its associated data forever`,
                okType: 'danger',
                onOk: () => {
                    if (this.state.viewModal)
                        this.getNextConversation(deletedConversation)
                            .then(() => this.props.dispatch(conversationActions.deleteConversation(ID, AssistantID)));
                    else
                        this.props.dispatch(conversationActions.deleteConversation(ID, AssistantID));
                },
                maskClosable: true
            });
    };


    // The promise is for getNext before deletion conversations
    getNextConversation = currentConversation => new Promise(resolve => {
        const { conversationsList } = this.props.conversations;
        const index = conversationsList?.findIndex(Conversation => Conversation?.ID === currentConversation?.ID);
        if (index > -1)
            this.setState({
                    selectedConversation: conversationsList[index + 1] ?
                        conversationsList[index + 1] :
                        conversationsList[index]
                }
                , () => resolve());
    });

    getBackConversation = currentConversation => {
        const { conversationsList } = this.props.conversations;
        const index = conversationsList?.findIndex(Conversation => Conversation?.ID === currentConversation?.ID);
        if (index > -1)
            this.setState({ selectedConversation: conversationsList[index - 1] ? conversationsList[index - 1] : conversationsList[index] });
    };

    // get the conversation to be rendered and save them in the state in format which can be downloaded by the CSV
    populateDownloadData = Conversations => {
        const conversationsList = Conversations.conversationsList;

        let data = [['ID', 'User Type', 'Name', 'Questions Answered', 'Solutions Returned', 'Time Spent', 'Date & Time',
            'Score', 'Statue', 'Conversation', 'User Profile', 'Selected Results']]; // Conversations Page Headers
        let dataRecord = undefined; // CSV line to push into data
        let recordData = undefined; // the questions and answers of the record
        let conversation = ''; // the questions and answers of the record in format to be pushed into dataRecord
        let profile = ''; // profile in format to be put in the CSV
        let keywordsByDataType = undefined;
        let selectedSolutions = undefined; // the selected solutions of the record
        let selectedSolutionsData = undefined; // the selected solutions of the record in the format to be put in the CSV

        // go through the to-be-rendered conversation
        if (conversationsList) {
            conversationsList.forEach(record => {
                conversation = '';

                // Conversations Page Base Table
                dataRecord = [record['ID'], record['UserType'], record['Name'], record['QuestionsAnswered'], record['SolutionsReturned'],
                    record['TimeSpent'], record['DateTime'], record['Score'] * 100 + '%', record['ApplicationStatus']];

                // Conversation Questions and Answers   ex. "What is your name? : Bob House (Name)"
                recordData = record['Data']['collectedData'];
                recordData.forEach(conversationData => {
                    conversation += conversationData['questionText'] + ' : ' + conversationData['input'] +
                        (conversationData['dataType'] !== 'No Type' ? ' (' + conversationData['dataType'] + ')' : '') + '\r\n\r\n';
                });
                dataRecord.push(conversation);

                // User Profile
                profile = '';
                keywordsByDataType = record['Data']['keywordsByDataType'];
                for (let key in keywordsByDataType) {
                    if (keywordsByDataType.hasOwnProperty(key) && key.includes(record['UserType'])) {
                        profile += key + ' : ';
                        keywordsByDataType[key].forEach(word => {
                            profile += word + ' ';
                        });
                        profile += '\r\n';
                    }
                }
                dataRecord.push(profile);

                // Selected Solutions
                selectedSolutions = record['Data']['selectedSolutions'] ? record['Data']['selectedSolutions'] : [];
                selectedSolutionsData = '';
                selectedSolutions.forEach((solutionsRecord, index) => {
                    selectedSolutionsData += 'Selected Result ' + (index + 1) + '\r\n';
                    for (let key in solutionsRecord['data']) {
                        if (solutionsRecord['data'].hasOwnProperty(key)) {
                            selectedSolutionsData += solutionsRecord['data'][key] ? key + ' : ' +
                                solutionsRecord['data'][key] + '\r\n' : '';
                        }
                    }
                    selectedSolutionsData += '\r\n';
                });
                dataRecord.push(selectedSolutionsData);

                data.push(dataRecord);
                this.setState({downloadData: data})
            });
        }
    };

    updateStatus = (newStatus, conversation) => {
        const id = conversation?.ID;
        const AssistantID = conversation?.AssistantID;
        this.props.dispatch(conversationActions.updateConversationStatus(newStatus, id, AssistantID));
    };

    buildStatusBadge = (status, withText = true) => {
        let text = '';
        if (withText) text = status;

        if (status === 'Accepted')
            return <Badge status="success" text={text}/>;
        else if (status === 'Rejected')
            return <Badge status="error" text={text}/>;
        return <Badge status="processing" text={text}/>;
    };


    render() {
        const { assistant, conversations, options } = this.props;

        return (
            <>
                <div className={styles.Header}>
                    <Button type="primary" icon="sync"
                            onClick={this.refreshConversations} loading={this.props.isLoading}>
                        Refresh
                    </Button>

                    <Button type="primary" icon="download"
                            loading={this.props.isLoading}>
                        <CSVLink filename={'Conversations_Export.csv'} data={this.state.downloadData}
                                 style={{ color: 'white' }}> Export CSV</CSVLink>
                    </Button>

                    {/*<Button hidden type="primary" icon="delete"*/}
                    {/*disabled={!!(!conversations?.conversationsList?.length)}*/}
                    {/*onClick={() => {*/}
                    {/*this.clearAllConversations(assistant.ID)*/}
                    {/*}} loading={this.props.isClearingAll}>*/}
                    {/*Clear All*/}
                    {/*</Button>*/}
                </div>

                <Table columns={this.columns}
                       rowKey={record => record.ID}
                       dataSource={conversations.conversationsList}
                       onChange={this.handleFilter}
                       loading={this.props.isLoading}
                       bordered={true}
                       pagination={{ position: 'both', pageSize: 20 }}
                       size='default'
                       scroll={{ x: 'max-content' }}
                />

                {
                    this.state.destroyModal && <ViewsModal visible={this.state.viewModal}
                                                           closeViewModal={this.closeViewModal}
                                                           filesPath={conversations.Files}
                                                           flowOptions={options?.flow}
                                                           conversation={this.state.selectedConversation}
                                                           assistant={assistant}
                                                           getNextConversation={this.getNextConversation}
                                                           getBackConversation={this.getBackConversation}
                                                           deleteConversation={this.deleteConversation}
                                                           updateStatus={this.updateStatus}
                                                           isUpdatingStatus={this.props.isUpdatingStatus}
                                                           buildStatusBadge={this.buildStatusBadge}/>
                }
            </>
        );
    }
}

const mapStateToProps = state => {
    const { conversation, options } = state;
    return {
        conversations: conversation.conversations,
        options: options.options,
        isLoading: conversation.isLoading,
        errorMsg: conversation.errorMsg,
        isClearingAll: conversation.isClearingAll,
        isUpdatingStatus: conversation.isUpdatingStatus
    };
};
export default connect(mapStateToProps)(Conversations);
