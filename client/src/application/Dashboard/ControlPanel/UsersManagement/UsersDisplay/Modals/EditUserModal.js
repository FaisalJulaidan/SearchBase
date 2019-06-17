import React from 'react';
import {Button, Modal, Form, Input, Select, Icon} from "antd";
import {isEmpty} from "lodash";

const FormItem = Form.Item;
const Option = Select.Option;

class EditUserModal extends React.Component {

    state = {};

    handleSave = () => this.props.form.validateFields((err, values) => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.handleSave(values);
            }
        });
    });

    closeModal = () => {
        this.props.handleCancel();
    };

    render() {
        const {userData, roles, form} = this.props;
        const {getFieldDecorator} = form;

        return (
            <Modal
                width={500}
                title="Add New User"
                destroyOnClose={true}
                visible={this.props.visible}
                onOk={this.props.handleSave}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="Cancel" onClick={this.closeModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleSave}>{"Add"}</Button>
                ]}>

                <Form layout='vertical'>
                    <FormItem
                        label="First name"
                        extra="Enter the name of the user">
                        {getFieldDecorator('name', {
                            initialValue: userData?.user.Firstname,
                            rules: [{
                                required: true,
                                message: 'Please enter your the new user\'s name',
                            }],
                        })(
                            <Input placeholder="Ex: Wesley"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Surname">
                        {getFieldDecorator('surname', {
                            initialValue: userData?.user.Surname,
                            rules: [{
                                required: true,
                                message: 'Please enter the User\'s surname',
                            }],
                        })(
                            <Input placeholder="Ex: Snipes"/>
                        )}
                    </FormItem>

                    <FormItem
                        label={"Phone Number:"}>
                        {getFieldDecorator("phoneNumber", {
                            initialValue: userData?.user.PhoneNumber,
                            rules: [{required: false, message: "Please enter a valid email"},
                                {pattern: /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/,
                                    message: 'Invalid phone number'}
                            ],
                        })(
                            <Input prefix={<Icon type="phone" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                   placeholder="+44 7502719493"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Role"
                        extra="The type defines what permissions the User will have">
                        {getFieldDecorator('role', {
                            initialValue: userData?.role.ID,
                            rules: [{
                                required: true,
                                message: 'Please select a user role',
                            }],
                        })(
                            <Select onChange={this.changeTypeHandler}>
                                {
                                    roles.map((role, i) => (
                                            <Option key={i} value={role.ID}>{role.Name}</Option>
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

export default Form.create()(EditUserModal)
