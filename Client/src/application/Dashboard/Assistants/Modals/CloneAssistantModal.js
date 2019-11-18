import React, { Component } from 'react';

import { Button, Form, Input, Modal } from 'antd';


class CloneAssistantModal extends Component {


    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {

                console.log(values);
                // this.props.addAssistant(newAssistant);
                // return this.props.hideModal();
            }
        });
    };

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value)) {
            callback('Assistant name already exists');
        } else {
            callback();
        }
    };


    render() {
        const { getFieldDecorator } = this.props.form;
        const { hideModal, visible } = this.props;

        return (
            <Modal width={600}
                   title="Clone Assistant"
                   visible={visible}
                   onCancel={hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.handleAdd}>
                           Clone
                       </Button>
                   ]}>
                <Form layout='vertical'>

                    <Form.Item label="Assistant Name"
                               extra="Enter a name for your assistant">
                        {getFieldDecorator('assistantName', {
                            initialValue: '',
                            rules: [
                                { whitespace: true, required: true, message: 'Please input your assistant name' },
                                { validator: this.checkName }
                            ]
                        })(
                            <Input placeholder="Ex: My first assistant, Sales Assistant"/>
                        )}
                    </Form.Item>

                    <div style={{ display: 'flex' }}>
                        <div style={{ width: '50%', padding: '0 10px 0 0' }}>
                            <Form.Item label="Welcome Message"
                                       extra="This will be sent as first message">
                                {getFieldDecorator('welcomeMessage', {
                                    rules: [{
                                        whitespace: true, required: true, message: 'Please input your welcome message'
                                    }]
                                })(
                                    <Input placeholder="Ex: Hey there, Welcome visitor"/>
                                )}
                            </Form.Item>
                        </div>

                        <div style={{ width: '50%' }}>
                            <Form.Item label="Header Title"
                                       extra="This will appear on top of your chatbot">
                                {getFieldDecorator('topBarText', {
                                    rules: [{
                                        whitespace: true,
                                        required: true,
                                        message: 'Please input your header title'
                                    }]
                                })(
                                    <Input placeholder="Ex: Recruiter Bot"/>
                                )}
                            </Form.Item>
                        </div>
                    </div>

                </Form>
            </Modal>
        );
    }
}


export default Form.create()(CloneAssistantModal);
