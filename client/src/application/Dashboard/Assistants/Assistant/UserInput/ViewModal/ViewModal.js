import React, {Component} from 'react';
import "./ViewModal.less"
import {Button, Modal, Table} from "antd";
import moment from "moment";


class ViewModal extends Component {

    state = {};

    columns = [{
        title: 'Question',
        key: 'questionText',
        render: (text, record, index) => (<p>{record.questionText}</p>),
    }, {
        title: 'Input',
        key: 'input',
        render: (text, record, index) => (
            <p>
                {record.input}
            </p>
        ),
    }];

    render() {
        return (
            <Modal
                width={800}
                title="User Inputs"
                destroyOnClose={true}
                visible={this.props.visible}
                onCancel={this.props.closeViewModal}
                onOk={this.props.closeViewModal}
                footer={[
                    <Button key="Cancel" onClick={this.props.closeViewModal}>OK</Button>
                ]}>
                {this.props.record ? (
                    <Table columns={this.columns}
                           dataSource={this.props.record.Data.collectedInformation}
                           size='middle'
                           pagination={false}
                    />
                ) : (<p>No Data</p>)}

            </Modal>
        );
    }
}

export default ViewModal;