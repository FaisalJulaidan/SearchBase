import React, {Component} from 'react';
import {Form, Input, Modal} from "antd";
import {autoPilotActions} from "store/actions";
import {store} from "store/store";
import PropTypes from 'prop-types';

const FormItem = Form.Item;

class EditAutoPilotModal extends Component {


    onSubmit = () => this.props.form.validateFields((err, values) => {
        console.log(err)
        if (!err) {
            this.props.updateAutoPilot(this.props.autoPilot.ID, values)
        }
    });


    render() {
        const {autoPilot, form} = this.props;
        const {getFieldDecorator} = form;

        return (
            <Modal title="Edit CRM Auto Pilot" visible={this.props.visible}
                   onOk={this.onSubmit}
                   onCancel={this.props.closeModal}>
                <Form layout='horizontal'>
                    <FormItem label="Name">
                        {getFieldDecorator('name', {
                            initialValue: autoPilot?.Name || '',
                            rules: [{
                                required: true
                            }],
                        })(
                            <Input type="text" placeholder="Name of the auto pilot"/>
                        )}
                    </FormItem>

                    <FormItem label="Description">
                        {getFieldDecorator('description', {
                            initialValue: autoPilot?.Description,
                            rules: [{
                                message: "Please add description",
                            }],
                        })(
                            <Input type="text" placeholder="Name of the auto pilot"/>
                        )}
                    </FormItem>
                </Form>
            </Modal>
        );
    }
}

EditAutoPilotModal.propTypes = {
    autoPilotsList: PropTypes.array,
};

export default Form.create()(EditAutoPilotModal);


