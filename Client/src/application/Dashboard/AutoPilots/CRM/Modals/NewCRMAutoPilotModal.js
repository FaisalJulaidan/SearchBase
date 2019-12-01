import React, { Component } from 'react';
import { Form, Input, Modal, Select } from 'antd';
import { autoPilotActions } from 'store/actions';
import { store } from 'store/store';
import PropTypes from 'prop-types';
import 'types/TimeSlots_Types';

const FormItem = Form.Item;

class NewCRMAutoPilotModal extends Component {

    onSubmit = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.addAutoPilot(values);
            }
        });
    };


    render() {

        const { getFieldDecorator } = this.props.form;
        return (
            <Modal title="Add CRM Auto Pilot" visible={this.props.visible}
                   onOk={this.onSubmit}
                   onCancel={this.props.closeModal}>
                <Form layout='horizontal' key="NewCRMAutoPilot">
                    <FormItem label="Name">
                        {getFieldDecorator('name', {
                            initialValue: '',
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please input a name for your CRM Auto Pilot'
                            }, {
                                validator: (_, value, callback) => {
                                    const { /**@type AutoPilot[]*/ CRMAutoPilotsList } = this.props;
                                    if (CRMAutoPilotsList.some(autoPilot => autoPilot.Name === value))
                                        return callback('Auto Pilot name already exists');
                                    else
                                        return callback();
                                }
                            }]
                        })(
                            <Input type="text" placeholder="Name of the auto pilot"/>
                        )}
                    </FormItem>
                    <FormItem label="Description">
                        {getFieldDecorator('description', {
                            rules: [{
                                required: false,
                                message: 'Please add description'
                            }]
                        })(
                            <Input type="text" placeholder="Name of the CRM auto pilot"/>
                        )}
                    </FormItem>
                </Form>
            </Modal>
        );
    }
}

export default Form.create()(NewCRMAutoPilotModal);


