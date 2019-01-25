import React from 'react';
import "./Categorised.less"
import styles from "./Categorised.module.less"
import { Table, Button, Modal } from 'antd';
import moment from 'moment';

const confirm = Modal.confirm;


class Categorised extends React.Component {

    state = {
        viewModal: false,
        selectedRecord: null
    };

    columns = [{
        title: '#',
        dataIndex: '#',
        key: '#',
        render: (text, record, index) => (<p>{index+1}</p>),
    },{
        title: ' Session ID',
        dataIndex: 'ID',
        key: 'ID',
        sorter: (a, b) => a.ID - b.ID,
        render: (text, record) => (<p>{record.ID}</p>),
    }];


    closeViewModal = () => {
        this.setState({viewModal: false, selectedRecord: null})
    };


    render() {
        const {sessions} = this.props;
        return (

            <div style={{height: '100%'}}>
                <Table columns={this.columns}
                       dataSource={sessions.sessionsList ? sessions.sessionsList : null}
                       loading={this.props.isLoading}
                       size='middle'
                />


            </div>
        );
    }
}



export default Categorised;