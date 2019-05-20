import React from 'react';
import styles from "./Sessions.module.less"
import ViewsModal from "./ViewModal/ViewsModal";
import {Button, Modal, Table, Tag, Divider} from 'antd';
import {chatbotSessionsActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import Header from "../../../../../components/Header/Header";
import {CSVLink, CSVDownload} from "react-csv";

const confirm = Modal.confirm;


class Sessions extends React.Component {

    filesCounter=-1; // important for file uploads
    state = {
        filteredInfo: null,
        sortedInfo: null,
        selectedSession: null,
        viewModal: false,
        destroyModal: false,
        downloadData: [],
        sessionsRefreshed: true
    };


    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    }

    refreshSessions = () => {
        const {assistant} = this.props.location.state;
        this.setState({sessionsRefreshed:true});
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
                content: `If you click OK, this conversation will be deleted with its associated data forever`,
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

    // get the sessions to be rendered and save them in the state in format which can be downloaded by the CSV
    populateDownloadData(sessions){
        const sessionsList = sessions.sessionsList;

        let data = [["ID", "User Type", "Questions Answered", "Solutions Returned", "Time Spent", "Date & Time",
            "Conversation", "User Profile", "Selected Results"]]; // Sessions Page Headers
        let dataRecord = undefined; // CSV line to push into data
        let recordData = undefined; // the questions and answers of the record
        let conversation = ""; // the questions and answers of the record in format to be pushed into dataRecord
        let profile = ""; // profile in format to be put in the CSV
        let keywordsByDataType = undefined;
        let selectedSolutions = undefined; // the selected solutions of the record
        let selectedSolutionsData = undefined; // the selected solutions of the record in the format to be put in the CSV
        console.log(sessions)
        // go through the to-be-rendered sessions
        if(sessionsList){sessionsList.forEach(record => {
            conversation = "";

            // Sessions Page Base Table
            dataRecord = [record["ID"], record["UserType"], record["QuestionsAnswered"], record["SolutionsReturned"],
                record["TimeSpent"], record["DateTime"]];

            // Conversation Questions and Answers   ex. "What is your name? : Bob House (Name)"
            recordData = record["Data"]["collectedData"];
            recordData.forEach(conversationData => {
                conversation += conversationData["questionText"] + " : " + conversationData["input"] +
                    (conversationData["dataType"] !== "No Type" ? " (" + conversationData["dataType"] + ")" : "") + "\r\n\r\n";
            });
            dataRecord.push(conversation);

            // User Profile
            profile = "";
            keywordsByDataType = record["Data"]["keywordsByDataType"];
            for (let key in keywordsByDataType){
                if (keywordsByDataType.hasOwnProperty(key) && key.includes(record["UserType"])){
                    profile += key + " : ";
                    keywordsByDataType[key].forEach(word => { profile += word + " " });
                    profile += "\r\n"
                }
            }
            dataRecord.push(profile);

            // Selected Solutions
            selectedSolutions = record["Data"]["selectedSolutions"] ? record["Data"]["selectedSolutions"] : [];
            selectedSolutionsData = "";
            selectedSolutions.forEach((solutionsRecord, index) => {
                selectedSolutionsData += "Selected Result " + (index+1) + "\r\n";
                for (let key in solutionsRecord["data"]){
                    if (solutionsRecord["data"].hasOwnProperty(key)){
                        selectedSolutionsData += solutionsRecord["data"][key] ? key + " : " +
                            solutionsRecord["data"][key] + "\r\n" : "";
                    }
                }
                selectedSolutionsData += "\r\n";
            });
            dataRecord.push(selectedSolutionsData);

            data.push(dataRecord);
        });}
        console.log(data)

        // put the data in the state and set refresh to false
        this.setState({downloadData:data, sessionsRefreshed:false});
    }

    findUserName = (keywords, userType) => {
        if ('Client Name' in keywords && userType === 'Client')
            return keywords['Client Name'].join(' ');
        else if ('Candidate Name' in keywords && userType === 'Candidate')
            return keywords['Candidate Name'].join(' ');
        return 'Unavailable';
    };

    render() {
        const {assistant} = this.props.location.state;
        const {sessions, options} = this.props;

        if(this.state.sessionsRefreshed){this.populateDownloadData(sessions)}

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
            title: 'Name',
            dataIndex: 'Name',
            key: 'Name',
            render: (text, record) => (
                <p style={{textTransform: 'capitalize'}}>{this.findUserName(record.Data.keywordsByDataType, record.UserType)}</p>),

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

        },{
            title: 'Status',
            dataIndex: 'Completed',
            key: 'Completed',
            // filters: [
            //     {text: 'Completed', value: 'Completed'},
            //     {text: 'Incomplete', value: 'Incomplete'},
            // ],
            // onFilter: (value, record) => record.Completed ? record.UserType.indexOf(value) === 0 : false,
            render: (text, record) => (
                record.Completed ?
                    <Tag color="#87d068">Completed</Tag> :
                    <Tag color="red">Incomplete</Tag>),

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

                            <Button className={styles.Panel_Header_Button} type="primary" icon="download"
                                    loading={this.props.isLoading}>
                                <CSVLink filename={"Conversations_Export.csv"} data={this.state.downloadData}
                                         style={{color:"white"}}> Export CSV</CSVLink>
                            </Button>


                            <Button hidden className={styles.Panel_Header_Button} type="primary" icon="delete"
                                    disabled={!!(!sessions?.sessionsList?.length)}
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
