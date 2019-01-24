import React from 'react';
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
        // title: '#',
        // dataIndex: '#',
        // key: '#',
        // render: (text, record, index) => (<p>{index+1}</p>),
    }];


    closeViewModal = () => {
        this.setState({viewModal: false, selectedRecord: null})
    };


    render() {
        console.log(this.props.sessions);
        return (

            <div style={{height: '100%'}}>
                Table
                {/*<Table columns={this.columns}*/}
                       {/*dataSource={this.props.sessions.data}*/}
                       {/*loading={this.props.isLoading}*/}
                       {/*size='middle'*/}
                {/*/>*/}


            </div>
        );
    }
}



export default Categorised;