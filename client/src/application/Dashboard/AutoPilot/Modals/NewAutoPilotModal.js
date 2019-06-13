import React, {Component} from 'react';
import {Form, Input, Modal} from "antd";
import {autoPilotActions} from "store/actions";
import {store} from "store/store";
import PropTypes from 'prop-types';
import 'types/TimeSlots_Types'

const FormItem = Form.Item;

class NewAutoPilotModal extends Component {

    onSubmit = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.addAutoPilot(values)
            }
        });
    };


    render() {
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;
        return (
            <Modal title="Add Auto Pilot" visible={this.props.visible}
                   onOk={this.onSubmit}
                   onCancel={this.props.closeModal}>
                <Form layout='horizontal'>
                    <FormItem label="Name"
                              {...layout}>
                        {getFieldDecorator('name', {
                            rules: [{
                                required: true,
                                message: "Please add name or the name you entered is duplicated",
                                validator: (_, value, callback) => {
                                    const { /**@type AutoPilot[]*/ autoPilotsList} = this.props;
                                    if (autoPilotsList.some(autoPilot => autoPilot.Name === value
                                        && this.props.autoPilot.Name !== value))
                                        return callback(value + ' is duplicated');
                                    else
                                        return callback()
                                }
                            }],
                        })(
                            <Input type="text" placeholder="Name of the auto pilot"/>
                        )}
                    </FormItem>

                    <FormItem label="Description"
                              {...layout}>
                        {getFieldDecorator('description', {
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

NewAutoPilotModal.propTypes = {
    autoPilotsList: PropTypes.array,
};
export default Form.create()(NewAutoPilotModal);


