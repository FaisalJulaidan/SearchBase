import React from 'react';
import styles from "./Sessions.module.less"
import {chatbotSessionsActions} from "../../../../../../store/actions";
import ViewsModal from "./ViewModal/ViewsModal";
import { Table, Button, Modal, Tag } from 'antd';
import moment from 'moment';
import {alertError, http} from "../../../../../../helpers";
import saveAs from "file-saver";

const confirm = Modal.confirm;


class Sessions extends React.Component {

    filesCounter=-1; // important for file uploads
    state = {
        filteredInfo: null,
        sortedInfo: null,
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
        const clear = this.props.clearAllChatbotSessions;
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk() {clear()},
            onCancel() {},
        });
    };

    downloadFile = (e) => {
        // Get file name by index. indexes stored in each button corresponds to filenames stored in the state
        const fileName = this.state.fileNames[e.target.getAttribute('data-index')];
        if (!fileName){
            alertError("File Error", "Sorry, but file doesn't exist!");
            return;
        }

        http({
            url: `/assistant/${this.props.assistant.ID}/userinput/${fileName}`,
            method: 'GET',
            responseType: 'blob', // important
        }).then((response) => {
            saveAs(new Blob([response.data]), fileName);
        }).catch(error => {
            alertError("File Error", "Sorry, cannot download this file!")
        });
    };

    // Nested table that has all the answered questions per session
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


                <Button className={styles.ClearAllBtn} type="primary" icon="delete"
                        onClick={this.showConfirmForClearing} loading={this.props.isClearingAll}>
                    Clear All
                </Button>

                <Table columns={columns}
                       dataSource={sessions.sessionsList ? sessions.sessionsList : null}
                       onChange={this.handleFilter}
                       loading={this.props.isLoading}
                       // expandedRowRender={this.expandedRowRender}
                       size='middle'
                />


                <ViewsModal visible={this.state.viewModal}
                            closeViewModal={this.closeViewModal}
                            filesPath={this.props.sessions.filesPath}
                            dataTypes={this.props.sessions.dataTypes}
                            session={this.state.selectedSession}
                            assistant={this.props.assistant}
                />
            </div>
        );
    }
}

export default Sessions;