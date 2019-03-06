import {Button, Divider, Modal, Steps, Spin, message, Form, Input, Switch, InputNumber, Slider} from 'antd';

import React, {Component} from 'react';

const FormItem = Form.Item;


class DatabaseDetailsModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };


        const {getFieldDecorator} = this.props.form;

        const {databaseInfo} = this.props;

        return (
            <Modal width={"60%"}
                   title="Upload New Database"
                   visible={this.props.visible}
                   onCancel={this.props.hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="delete" type="danger" onClick={this.props.handleDelete}>
                           Delete
                       </Button>,
                       <Button key="cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.handleSave}>
                           Save
                       </Button>,
                   ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...formItemLayout}>
                        {
                            getFieldDecorator('assistantName', {
                                rules: [{
                                    required: true,
                                    message: 'Please input your assistant name',
                                }],
                            })
                            (<Input placeholder="Ex: My first assistant, Sales Assistant"/>)
                        }
                    </FormItem>


                </Form>
            </Modal>
        );
    }
}

export default Form.create()(DatabaseDetailsModal);