import React from 'react';
import styles from "./Conversations.module.less"
import ViewsModal from "./ViewModal/ViewsModal";
import {Button, Modal, Table, Tag, Divider} from 'antd';
import {conversationActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import Header from "../../../../../components/Header/Header";
import {CSVLink, CSVDownload} from "react-csv";

const confirm = Modal.confirm;


class Conversations extends React.Component {

    state = {
        filteredInfo: null,
        sortedInfo: null,
        selectedConversation: null,
        viewModal: false,
        destroyModal: false,
        downloadData: [],
        ConversationsRefreshed: true
    };


    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(conversationActions.fetchConversations(assistant.ID))
    }

    refreshConversations = () => {
        const {assistant} = this.props.location.state;
        this.setState({ConversationsRefreshed:true});
        this.props.dispatch(conversationActions.fetchConversations(assistant.ID))
    };


    handleFilter = (pagination, filters, sorter) => {
        console.log('Various parameters', pagination, filters, sorter);
        this.setState({
            filteredInfo: filters,
            sortedInfo: sorter,
        });
    };


    closeViewModal = () => {
        this.setState({viewModal: false, selectedConversation: null}, () => {
            setTimeout(function () { //Start the timer
                this.setState({destroyModal: false}) //After 0.5 second, set render to true
            }.bind(this), 170)
        })
    };


    clearAllConversations = (assistantID) => {
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk: ()=> {
                this.props.dispatch(conversationActions.clearAllConversations(assistantID))
            },
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
                        this.getNextConversation(deletedConversation);
                    this.props.dispatch(conversationActions.deleteConversation(ID, AssistantID))
                },
                maskClosable: true
            });
    };
    
    getNextConversation = currentConversation => {
        const {conversationsList} = this.props.conversations;
        const index = conversationsList?.findIndex(Conversation => Conversation?.ID === currentConversation?.ID);
        if (index > -1)
            this.setState({selectedConversation: conversationsList[index + 1] ? conversationsList[index + 1] : conversationsList[index]})
    };

    getBackConversation = currentConversation => {
        const {conversationsList} = this.props.conversations;
        const index = conversationsList?.findIndex(Conversation => Conversation?.ID === currentConversation?.ID);
        if (index > -1)
            this.setState({selectedConversation: conversationsList[index - 1] ? conversationsList[index - 1] : conversationsList[index]})
    };

    // get the conversation to be rendered and save them in the state in format which can be downloaded by the CSV
    populateDownloadData(Conversations){
        const conversationsList = Conversations.conversationsList;

        let data = [["ID", "User Type", "Name", "Questions Answered", "Solutions Returned", "Time Spent", "Date & Time",
            "Conversation", "User Profile", "Selected Results"]]; // Conversations Page Headers
        let dataRecord = undefined; // CSV line to push into data
        let recordData = undefined; // the questions and answers of the record
        let conversation = ""; // the questions and answers of the record in format to be pushed into dataRecord
        let profile = ""; // profile in format to be put in the CSV
        let keywordsByDataType = undefined;
        let selectedSolutions = undefined; // the selected solutions of the record
        let selectedSolutionsData = undefined; // the selected solutions of the record in the format to be put in the CSV
        console.log(Conversations);
        // go through the to-be-rendered conversation
        if(conversationsList){conversationsList.forEach(record => {
            conversation = "";

            // Conversations Page Base Table
            dataRecord = [record["ID"], record["UserType"], this.findUserName(record["Data"]["keywordsByDataType"],
                record["UserType"] ), record["QuestionsAnswered"], record["SolutionsReturned"],
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
        console.log(data);

        // put the data in the state and set refresh to false
        this.setState({downloadData:data, ConversationsRefreshed:false});
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
        const {conversations, options} = this.props;

        if(this.state.ConversationsRefreshed){this.populateDownloadData(conversations)}

        const columns = [{
            title: '#',
            dataIndex: '#',
            key: '#',
            render: (text, record, index) => (<p>{index + 1}</p>),

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
                  this.setState({viewModal: true, selectedConversation: record, destroyModal: true})
              }}>
                  View
              </a>
                    <Divider type="vertical" />
              <a onClick={() => {
                  this.deleteConversation(record)
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
                                    onClick={this.refreshConversations} loading={this.props.isLoading}>
                                Refresh
                            </Button>

                            <Button className={styles.Panel_Header_Button} type="primary" icon="download"
                                    loading={this.props.isLoading}>
                                <CSVLink filename={"Conversations_Export.csv"} data={this.state.downloadData}
                                         style={{color:"white"}}> Export CSV</CSVLink>
                            </Button>


                            <Button hidden className={styles.Panel_Header_Button} type="primary" icon="delete"
                                    disabled={!!(!conversations?.conversationsList?.length)}
                                    onClick={() => {
                                        this.clearAllConversations(assistant.ID)
                                    }} loading={this.props.isClearingAll}>
                                Clear All
                            </Button>
                        </div>
                    </div>

                    <div className={styles.Panel_Body}>
                        <Table columns={columns}
                               dataSource={conversations.conversationsList}
                               onChange={this.handleFilter}
                               loading={this.props.isLoading}
                               size='middle'
                        />

                        {
                            this.state.destroyModal && <ViewsModal visible={this.state.viewModal}
                                                                   closeViewModal={this.closeViewModal}
                                                                   filesPath={conversations.filesPath}
                                                                   flowOptions={options?.flow}
                                                                   conversation={this.state.selectedConversation}
                                                                   assistant={assistant}
                                                                   getNextConversation={this.getNextConversation}
                                                                   getBackConversation={this.getBackConversation}
                                                                   deleteConversation={this.deleteConversation}/>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state =>  {
    const {conversation} = state;
    return {
        options: state.options.options,
        conversations: conversation.conversations,
        isLoading: conversation.isLoading,
        errorMsg: conversation.errorMsg,

        isClearingAll: conversation.isClearingAll
    };
};
export default connect(mapStateToProps)(Conversations);
