import React from 'react';
import {Button, Modal, Form, Input, Select, Tabs, Icon, Upload} from "antd";
import {isEmpty} from "lodash";

const FormItem = Form.Item;
const TabPane = Tabs.TabPane;
const OptGroup = Select.OptGroup;
const Option = Select.Option;

class UserModal extends React.Component {

    state = {
        roles: ["Admin", "User"]
    };

    handleSave = () => this.props.form.validateFields((err, values) => {
        const formData = new FormData();
        for (let key in values) {
            // skip loop if the property is from prototype
            if (!values.hasOwnProperty(key)) continue;

            formData.append(key, values[key]);
        }
        this.props.handleSave(formData);
    });

    closeModal = () => {
        this.props.handleCancel();
    };

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;

        return (
            <Modal
                width={800}
                title="Add New User"
                destroyOnClose={true}
                visible={this.props.newAutoPilotModalVisible}
                onOk={this.props.handleSave}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="Cancel" onClick={this.closeModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleSave}>{"Add"}</Button>
                ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="User Name"
                        extra="Enter the name of the user"
                        {...formItemLayout}>
                        {getFieldDecorator('name', {
                            rules: [{
                                required: true,
                                message: 'Please enter your the new user\'s name',
                            }],
                        })(
                            <Input placeholder="Ex: John Smith, Wesley Snipes"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="User Email"
                        extra="The email of the User. When added they will receive a random generated password which they can change later"
                        {...formItemLayout}>
                        {getFieldDecorator('email', {
                            rules: [{
                                required: true,
                                message: 'Please enter the User\'s email',
                            }],
                        })(
                            <Input placeholder="Ex: john_smith@mycompany.com"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="User Type"
                        extra="The type defines what permissions the User will have"
                        {...formItemLayout}>
                        {getFieldDecorator('type', {
                            initialValue: "User",
                            rules: [{
                                required: true,
                                message: 'Please select what User you are adding',
                            }],
                        })(
                            <Select onChange={this.changeTypeHandler}>
                                {
                                    this.state.roles.map(role => (
                                            <Option key={role} value={role}>{role}</Option>
                                        )
                                    )
                                }
                            </Select>
                        )}
                    </FormItem>
                </Form>
            </Modal>
        );
    }
}

export default Form.create()(UserModal)
