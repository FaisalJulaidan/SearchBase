import React, {Component} from 'react';

import {Button, Form, Input, Modal, Select, Divider} from 'antd';
import countries from 'helpers/static_data/countries'

const FormItem = Form.Item;
const { Option, OptGroup } = Select;



class NewAssistantModal extends Component {

    state = {
        isPopupDisabled: true,
        isAlertsEnabled: false,
        // alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
        alertOptions: {0: "Immediately"}
    };

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value)) {
            callback('Assistant name already exists');
        } else {
            callback();
        }
    };


    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.addAssistant(values)
            }
        });
    };


    render() {

        const {getFieldDecorator} = this.props.form;
        const {hideModal, visible} = this.props;

        return (
            <Modal
                width={500}
                title="Create New Assistant"
                visible={visible}
                onCancel={hideModal}
                destroyOnClose={true}
                footer={[
                    <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleAdd}>
                        Add
                    </Button>,
                ]}>
                <Form layout='vertical'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant">
                        {getFieldDecorator('assistantName', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input your assistant name'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder="Ex: My first assistant, Sales Assistant"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Description"
                        extra="Enter a description for your assistant to easily identify it in the dashboard"
                    >
                        {
                            getFieldDecorator('assistantDesc', {
                                rules: [{
                                    required: false,
                                    message: 'Please input your assistant description'
                                }]
                            })
                            (<Input placeholder="Ex: Qualify candidates for sales job"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Welcome Message"
                        extra="This will be sent as first message"
                    >
                        {getFieldDecorator('welcomeMessage', {
                            rules: [{
                                whitespace: true, required: true, message: 'Please input your welcome message',
                            }],
                        })(
                            <Input placeholder="Ex: Hey there, Welcome visitor"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Header Title"
                        extra="This will appear on top of your chatbot"
                    >
                        {getFieldDecorator('topBarText', {
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please input your header title',
                            }],
                        })(
                            <Input placeholder="Ex: Recruiter Bot"/>
                        )}
                    </FormItem>

                    <Divider/>
                    <FormItem
                        label="Template"
                        extra="Use ready script template built by us">
                        {getFieldDecorator('template', {
                            initialValue: 'none',
                            rules: [{
                                required: true,
                                message: 'Please select a template name or None',
                            }],
                        })(
                            <Select>
                                <Option key={1} value={'none'}>None</Option>
                                <Option key={2} value={'main'}>Main</Option>
                                <Option key={3} value={'appointment'}>Appointment</Option>
                                <Option key={4} value={'join-us'}>Join Us</Option>
                                <Option key={5} value={'referral'}>Referral</Option>
                                <Option key={6} value={'apply'}>Apply Chatbot</Option>
                                <Option key={7} value={'update-candidates'}>Update Candidates</Option>
                                <Option key={8} value={'client-chatbot'}>Client Chatbot</Option>
                                <Option key={9} value={'pre-screen'}>Pre-Screen</Option>
                                <Option key={10} value={'template-1'}>Template 1</Option>
                            </Select>
                        )}
                    </FormItem>

                </Form>
            </Modal>
        );
    }
}


export default Form.create()(NewAssistantModal)
