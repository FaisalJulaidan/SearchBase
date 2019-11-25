import React, { Component } from 'react';
import { connect } from 'react-redux';

import { Button, Form, Input, Modal, Spin } from 'antd';
import { assistantActions } from 'store/actions';
import { deepClone } from 'helpers/deepClone';


class CloneAssistantModal extends Component {


    state = {
        assistant: {}
    };


    componentDidMount() {
        this.props.dispatch(assistantActions.fetchAssistant(this.props.assistant.ID))
            .then(() => {
                this.setState({
                    assistant: {
                        ...deepClone(this.props.assistant_full),
                        Name: this.generateAssistantName(this.props.assistant_full.Name)
                    }
                });
            });
    }


    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {

                console.log(this.assistant);
                console.log(values);

                const newAssistant = {
                    assistantDesc: values.assistantDesc,
                    assistantName: values.assistantName,
                    flow: this.state.assistant.Flow,
                    template: 'none',
                    topBarText: values.topBarText,
                    welcomeMessage: values.welcomeMessage
                };

                this.props.addAssistant(newAssistant);
                return this.props.hideModal();
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

    generateAssistantName = (initialName) => {
        let i = 1;

        while (true) {
            let newName = initialName + ' Clone ' + i;

            if (this.props.isAssistantNameValid(newName))
                return newName;
            else
                i++;
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
                <Spin spinning={!this.state.assistant.Name}>
                    <Form layout='vertical'>


                        <Form.Item label="Assistant Name"
                                   extra="Enter a name for your assistant">
                            {getFieldDecorator('assistantName', {
                                initialValue: this.state.assistant.Name,
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
                                        initialValue: this.state.assistant.Message,
                                        rules: [{
                                            whitespace: true,
                                            required: true,
                                            message: 'Please input your welcome message'
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
                                        initialValue: this.state.assistant.TopBarText,
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

                        <Form.Item label="Description"
                                   extra="Enter a description for your assistant to easily identify it in the dashboard">
                            {
                                getFieldDecorator('assistantDesc', {
                                    initialValue: this.state.assistant.Description,
                                    rules: [{
                                        required: false,
                                        message: 'Please input your assistant description'
                                    }]
                                })
                                (<Input placeholder="Ex: Qualify candidates for sales job"/>)
                            }
                        </Form.Item>

                        <br/>

                        <h4>*Note: Script will be cloned as is</h4>
                    </Form>
                </Spin>
            </Modal>
        );
    }
}

function mapStateToProps(state) {
    return {
        assistant_full: state.assistant.assistant
    };
}

export default connect(mapStateToProps)(Form.create()(CloneAssistantModal));

