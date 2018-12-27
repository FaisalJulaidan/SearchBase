import React, {Component} from 'react';
import "./NewGroup.less"
import {Button, Modal, Form, Input} from "antd";

const FormItem = Form.Item;

class NewGroup extends Component {

    state = {};

    handleSave = () => this.props.form.validateFields((err, values) => {
        if (!err)
            this.props.handleSave(values)
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
                title="Create New Group"
                destroyOnClose={true}
                visible={this.props.visible}
                onOk={this.props.handleSave}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="Cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleSave}>
                        Add
                    </Button>
                ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Group Name"
                        extra="Enter a name for your group to easily identify it in the group list"
                        {...formItemLayout}>
                        {getFieldDecorator('name', {
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
                            rules: [{
                                required: true,
                                message: 'Please add description to your group name',
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

export default Form.create()(NewGroup)