import React, {Component} from 'react';
import {Form, Input, Modal} from "antd";
import {autoPilotActions} from "store/actions";
import {store} from "store/store";

const FormItem = Form.Item;

class NewAutoPilotModal extends Component {


    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            store.dispatch(
                autoPilotActions.addAutoPilot({
                        name: values.name,
                        description: values.description || ''
                    }
                )
            );
        }
        this.props.closeModal()
    });


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
                                message: "Please add name",
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

export default Form.create()(NewAutoPilotModal);

