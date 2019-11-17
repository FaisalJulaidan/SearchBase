import React, { Component } from 'react';

import { Button, Form, Input, Modal } from 'antd';
import job_template from 'helpers/static_data/job-template';


class NewAssistantModal extends Component {

    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                const { blocks } = job_template.flow.groups[0];

                delete values.keys;
                console.log(values);

                blocks.forEach(block => {
                    values.forEach(value => {
                        if (block.Type !== 'Question')
                            block.Content.text.replace(`$\{${value}\}$`, value);
                    });

                    if (block.Type === 'Question') {
                        let form = block.Content.text.match(/\$\{.*?}\$/g);
                        if (form)
                            forms.push(...form);

                        const answers = block.Content.answers;
                        answers.forEach(answer => {
                            form = answer.text.match(/\$\{.*?}\$/g);
                            if (form)
                                forms.push(...form);
                        });
                    }
                });
            }
        });
    };

    componentDidMount() {
        let forms = [];
        const { blocks } = job_template.flow.groups[0];
        blocks.forEach(block => {
            if (block.Type !== 'Question') {
                const form = block.Content.text.match(/\$\{.*?}\$/g);
                if (form)
                    forms.push(...form);
            }

            if (block.Type === 'Question') {
                let form = block.Content.text.match(/\$\{.*?}\$/g);
                if (form)
                    forms.push(...form);

                const answers = block.Content.answers;
                answers.forEach(answer => {
                    form = answer.text.match(/\$\{.*?}\$/g);
                    if (form)
                        forms.push(...form);
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
            <Modal width={500}
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
                    {formItems}
                </Form>
            </Modal>
        );
    }
}


export default Form.create()(NewAssistantModal);
