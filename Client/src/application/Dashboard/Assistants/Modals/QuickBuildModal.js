import React, { Component } from 'react';

import { Button, Divider, Form, Input, Modal } from 'antd';
import { deepClone } from 'helpers/deepClone';


class NewAssistantModal extends Component {


    refrences = [];
    jobTemplate = {};

    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.refrences.forEach(ref => {
                    if (ref.Content?.text) // check if any of values is in the text, then replace it
                        values.keys.forEach(key => {
                            const tester = `\$\{${key}\}\$`;
                            if (ref.Content.text.includes(tester))
                                ref.Content.text = ref.Content.text.replace(tester, values[key]);
                        });

                    if (ref.text)
                        values.keys.forEach(key => {
                            const tester = `\$\{${key}\}\$`;

                            if (ref.text.includes(tester))
                                ref.text = ref.text.replace(tester, values[key]);
                        });
                });

                const newAssistant = {
                    assistantDesc: '',
                    assistantName: values.assistantName,
                    flow: this.jobTemplate.flow,
                    template: 'none',
                    topBarText: values.topBarText,
                    welcomeMessage: values.welcomeMessage
                };
                this.props.addAssistant(newAssistant);
                return this.props.hideModal();
            }
        });
    };

    async componentDidMount() {
        this.jobTemplate = deepClone(await import('helpers/quick_build_templates/job-template'));

        let forms = [];
        const { blocks } = this.jobTemplate.flow.groups[0];
        blocks.forEach(block => {
            if (block.Type !== 'Question') {
                const form = block.Content.text.match(/\$\{.*?}\$/g);
                if (form) {
                    this.refrences.push(block);
                    forms.push(...form);
                }
            }

            if (block.Type === 'Question') {
                let form = block.Content.text.match(/\$\{.*?}\$/g);
                if (form) {
                    this.refrences.push(block);
                    forms.push(...form);
                }

                const answers = block.Content.answers;
                answers.forEach(answer => {
                    form = answer.text.match(/\$\{.*?}\$/g);
                    if (form) {
                        this.refrences.push(answer);
                        forms.push(...form);
                    }
                });
            }
        });

        forms = forms.map(form => {
            form = form.replace('${', '');
            form = form.replace('}$', '');
            form = form.trim();
            return form;
        });

        forms = forms.filter((v, i, a) => a.indexOf(v) === i);


        const { form } = this.props;
        forms.forEach(from => {
            // can use data-binding to get
            const keys = form.getFieldValue('keys');
            const nextKeys = keys.concat(from);
            // can use data-binding to set
            // important! notify form to detect changes
            form.setFieldsValue({
                keys: nextKeys
            });
        });

    }

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value)) {
            callback('Assistant name already exists');
        } else {
            callback();
        }
    };


    render() {
        const { getFieldDecorator, getFieldValue } = this.props.form;
        const { hideModal, visible } = this.props;

        getFieldDecorator('keys', { initialValue: [] });

        const formItems = getFieldValue('keys').map(
            (key, index) => (
                <Form.Item key={index} label={key}>
                    {getFieldDecorator(`${key}`, {
                        rules: [{
                            required: true,
                            message: `Please input ${key}`
                        }]
                    })(
                        <Input placeholder={`${key} value`}/>
                    )}
                </Form.Item>
            )
        );

        return (
            <Modal width={600}
                   title="Quickly create a new assistant"
                   visible={visible}
                   onCancel={hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.handleAdd}>
                           Build
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


                    <Divider/>

                    <h3>Template Filling</h3>
                    <br/>

                    {formItems}
                </Form>
            </Modal>
        );
    }
}


export default Form.create()(NewAssistantModal);
