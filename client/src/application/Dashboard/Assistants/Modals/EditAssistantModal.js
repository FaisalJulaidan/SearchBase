import React, {Component} from 'react';
import {Button, Modal, Form, Input} from 'antd';


const FormItem = Form.Item;

class EditAssistantModal extends Component {

    constructor(props) {
        super(props);
    }

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value) && this.props.assistant.Name !== value) {
            callback('Assistant name already exists. Choose another one, please.');
        } else {
            callback();
        }
    };

    handleSave = () => this.props.form.validateFields((errors, values) => {
        const {assistant, updateAssistant} = this.props;
        if (!errors){
            return updateAssistant(assistant.ID, values)
        }

    });

    render() {
        const {getFieldDecorator} = this.props.form;
        const {assistant, hideModal, visible} = this.props;

        return (

            <Modal width={500}
                   title="Update Assistant"
                   visible={visible}
                   onCancel={hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.handleSave}>Save</Button>,
                   ]}>
                <Form layout='vertical'>

                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant">
                        {
                            getFieldDecorator('assistantName', {
                                initialValue: assistant?.Name || '',
                                rules: [
                                    {whitespace: true, required: true, message: 'Please input your assistant name'},
                                    {validator: this.checkName}
                                ]
                            })
                            (<Input placeholder="Recruitment Chatbot"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Description"
                        extra="Enter a description for your assistant to easily identify it in the dashboard">
                        {
                            getFieldDecorator('assistantDesc', {
                                initialValue: assistant?.Description,
                                rules: [{
                                    required: false,
                                    message: 'Please input your assistant description'
                                }]
                            })
                            (<Input placeholder="Ex: Qualify candidates for sales job"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Introduction Message"
                        extra="This will be sent as first message">
                        {
                            getFieldDecorator('welcomeMessage', {
                                initialValue: assistant?.Message,
                                rules: [{
                                    whitespace: true,
                                    required: true,
                                    message: 'Please input your welcome message',
                                }],
                            })(
                                <Input placeholder="Ex: Hey there, Welcome visitor"/>
                            )
                        }
                    </FormItem>

                    <FormItem
                        label="Header Title"
                        extra="This will appear on top of your Chatbot">
                        {
                            getFieldDecorator('topBarText', {
                                initialValue: assistant?.TopBarText,
                                rules: [{
                                    whitespace: true,
                                    required: true,
                                    message: 'Please input your header title',
                                }],
                            })(
                                <Input placeholder="Ex: Recruiter Bot"/>
                            )
                        }
                    </FormItem>


                </Form>
            </Modal>
        );
    }
}

export default Form.create()(EditAssistantModal);
