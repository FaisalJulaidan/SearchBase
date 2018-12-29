import React from 'react';
import "./UserInput.less"
import styles from "./UserInput.module.less"
import Header from "./Header/Header"

import {userInputActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import ViewModal from "./ViewModal/ViewModal";
import { Table, Button, Modal } from 'antd';
import moment from 'moment';

const confirm = Modal.confirm;


class UserInput extends React.Component {

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

    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(userInputActions.fetchUserInputs(assistant.ID))
    }

    closeViewModal = () => {
        this.setState({viewModal: false, selectedRecord: null})
    };

    clearAllUserInputs = () => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(userInputActions.clearAllUserInputs(assistant.ID))
    };

    showConfirmForClearing = () => {
        const clear = this.clearAllUserInputs;
        confirm({
            title: 'Do you want to delete all records?',
            content: 'By clicking OK, there will be no way to get these records back!',
            okType: 'danger',
            onOk() {clear()},
            onCancel() {},
        });
    };


    render() {
        const {assistant} = this.props.location.state;
        console.log(this.props.userInputs);
        return (

            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>{assistant.Name}: User Inputs</h3>
                            <p>Here you can find all the responses to your assistant's chatbot</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <Button className={styles.ClearAllBtn} type="primary" icon="delete"
                                onClick={this.showConfirmForClearing} loading={this.props.isClearingAll}>
                            Clear All
                        </Button>
                        <Table columns={this.columns}
                               dataSource={this.props.userInputs.data}
                               loading={this.props.isLoading}
                               size='middle'
                        />

                    </div>
                </div>

                <ViewModal visible={this.state.viewModal}
                           closeViewModal={this.closeViewModal}
                           filesPath={this.props.userInputs.filesPath}
                           record={this.state.selectedRecord}
                           assistant={this.props.location.state.assistant}
                />
            </div>




        );
    }
}

const mapStateToProps = state =>  {
    const {userInput} = state;
    return {
        userInputs: userInput.userInputs,
        isLoading: userInput.isLoading,
        errorMsg: userInput.errorMsg,

        isClearingAll: userInput.isClearingAll
    };
};


export default connect(mapStateToProps)(UserInput);