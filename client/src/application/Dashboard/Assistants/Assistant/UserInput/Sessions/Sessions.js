import React from 'react';
import "./Sessions.less"
import styles from "./Sessions.module.less"
import {chatbotSessionsActions} from "../../../../../../store/actions";
import ViewsSessionModal from "./ViewSessionModal/ViewsSessionModal";
import { Table, Button, Modal } from 'antd';
import moment from 'moment';

const confirm = Modal.confirm;


class Sessions extends React.Component {

    state = {
        viewModal: false,
        selectedRecord: null
    };

    columns = [{
        title: '#',
        dataIndex: '#',
        key: '#',
        render: (text, record, index) => (<p>{index+1}</p>),
    }, {
        title: 'Date & Time',
        dataIndex: 'DateTime',
        key: 'DateTime',
        render: (text, record) => (<p>{moment(record.DateTime).format("llll")}</p>),
    }, {
        title: 'Questions Answered',
        dataIndex: 'QuestionsAnswered',
        key: 'QuestionsAnswered',
    }, {
        title: 'Solutions Returned',
        dataIndex: 'SolutionsReturned',
    }, {
        title: 'Time Spent',
        dataIndex: 'TimeSpent',
        key: 'TimeSpent',
        render: (text, record) => (<p>{
            moment.duration(parseInt(text), 'seconds').asMinutes().toFixed(2) + " minute(s)"
        }
        </p>),

    }, {
        title: 'Action',
        key: 'action',
        render: (text, record, index) => (
            <span>
              <a onClick={()=> {
                  this.setState({viewModal: true, selectedRecord: record})
                }
              }> View</a>
              {/*<Divider type="vertical" />*/}
              {/*<a>Delete</a>*/}
            </span>
        ),
    }];


    closeViewModal = () => {
        this.setState({viewModal: false, selectedRecord: null})
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


    render() {
        console.log(this.props.sessions);
        return (

            <div style={{height: '100%'}}>


                <Button className={styles.ClearAllBtn} type="primary" icon="delete"
                        onClick={this.showConfirmForClearing} loading={this.props.isClearingAll}>
                    Clear All
                </Button>

                <Table columns={this.columns}
                       dataSource={this.props.sessions.data}
                       loading={this.props.isLoading}
                       size='middle'
                />


                <ViewsSessionModal visible={this.state.viewModal}
                                   closeViewModal={this.closeViewModal}
                                   filesPath={this.props.sessions.filesPath}
                                   record={this.state.selectedRecord}
                                   assistant={this.props.assistant}
                />
            </div>
        );
    }
}

export default Sessions;