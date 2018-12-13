import React, {Component} from 'react';
import {Button, Modal, Form, Input} from "antd";

const FormItem = Form.Item;

class EditGroup extends Component {

    state = {};

    handleUpdate = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            this.props.group.name = values.name;
            this.props.group.description = values.description;
            this.props.handleUpdate(this.props.group)
        }
    });


    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;
        return (
            <Modal
                width={800}
                title="Edit Group"
                visible={this.props.visible}
                onOk={this.props.handleUpdate}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="delete" type="danger" onClick={() => this.props.handleDelete(this.props.group)}>
                        Delete
                    </Button>,
                    <Button key="Cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleUpdate}>
                        Update
                    </Button>
                ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Group Name"
                        extra="Enter a name for your group to easily identify it in the group list"
                        {...formItemLayout}>
                        {getFieldDecorator('name', {
                            initialValue: this.props.group.name,
                            rules: [{
                                required: true,
                                message: 'Please enter your group name',
                            }],
                        })(
                            <Input placeholder="Ex: Greetings group, Sales group"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Group Description"
                        extra="Just a description for you"
                        {...formItemLayout}>
                        {getFieldDecorator('description', {
                            initialValue: this.props.group.description,
                            rules: [{
                                required: true,
                                message: 'Please description to your group name',
                            }],
                        })(
                            <Input placeholder="Ex: this is first group, this group help get info from user"/>
                        )}
                    </FormItem>


                </Form>
            </Modal>
        );
    }
}

export default Form.create()(EditGroup)