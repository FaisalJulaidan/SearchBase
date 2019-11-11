import React, {Component} from 'react';

import {Button, Form, Input, Modal} from 'antd';

const FormItem = Form.Item;



class NewAssistantModal extends Component {

    state = {
        isPopupDisabled: true,
        isAlertsEnabled: false,
        // alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
        alertOptions: {0: "Immediately"}
    };

    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                // this.props.addAssistant(values)
            }
        });
    };



    render() {

        const {getFieldDecorator} = this.props.form;
        const {hideModal, visible} = this.props;

        return (
            <Modal
                width={500}
                title="Quickly create a new assistant"
                visible={visible}
                onCancel={hideModal}
                destroyOnClose={true}
                footer={[
                    <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleAdd}>
                        Build
                    </Button>,
                ]}>
                <Form layout='vertical'>
                    <FormItem
                        label="Job salary"
                        extra="Enter job salary">
                        {getFieldDecorator('jobSalary', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input your assistant name'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder="Ex: 50,000£"/>
                        )}
                    </FormItem>
                    <FormItem
                        label="Job Description"
                        extra="Enter job description">
                        {getFieldDecorator('jobDescription', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input job description'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder=""/>
                        )}
                    </FormItem>
                    <FormItem
                        label="Benefits"
                        extra="Enter a benefits">
                        {getFieldDecorator('benefits', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input benefits'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder=""/>
                        )}
                    </FormItem>
                    <FormItem
                        label="ًRequirements"
                        extra="Enter requirements">
                        {getFieldDecorator('requirements', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input requirements'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder=""/>
                        )}
                    </FormItem>
                    <FormItem
                        label="Job Location"
                        extra="Enter job location">
                        {getFieldDecorator('jobLocation', {
                            initialValue: '',
                            rules: [
                                {whitespace: true, required: true, message: 'Please input job location'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder="Ex: London, Manchester, Cardiff"/>
                        )}
                    </FormItem>
                </Form>
            </Modal>
        );
    }
}


export default Form.create()(NewAssistantModal)
