import React from 'react';
import {Button, Modal, Form, Input, Select, Icon} from "antd";
import {isEmpty} from "lodash";

const FormItem = Form.Item;
const Option = Select.Option;

class AddUserModal extends React.Component {

    onSubmit = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.handleSave(values);
            }
        });
    };


    render() {
        const {roles, form, visible, hideModal} = this.props;
        const {getFieldDecorator} = form;

        return (
            <Modal
                width={500}
                title="Add New User"
                onCancel={hideModal}
                destroyOnClose={true}
                visible={visible}
                footer={[
                    <Button key="Cancel" onClick={hideModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.onSubmit}>{"Add"}</Button>
                ]}>
                <Form layout='vertical'>
                    <FormItem
                        label="First Name">
                        {getFieldDecorator('firstname', {
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please enter your the new user\'s first name',
                            }],
                        })(
                            <Input placeholder="Ex: Wesley"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Surname">
                        {getFieldDecorator('surname', {
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please enter the User\'s surname',
                            }],
                        })(
                            <Input placeholder="Ex: Snipes"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Email"
                        help={"A temporary password will to the user to login and change his password to whatever he likes"}>
                        {getFieldDecorator('email', {
                            rules: [
                                {required: true, message: 'Please enter your the new user\'s email'},
                                {pattern: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
                                    message: 'Sorry, enter a valid email'}
                            ],
                        })(
                            <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                   placeholder="Wesley.Snipes@gmail.com"/>
                        )}
                    </FormItem>

                    <FormItem
                        label={"Phone Number:"}>
                        {getFieldDecorator("phoneNumber", {
                            rules: [{whitespace: true,
                                required: false,
                                message: "Please enter a valid email"},
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
                        extra="The role defines what permissions the User will have">
                        {getFieldDecorator('roleID', {
                            rules: [{
                                required: true,
                                message: 'Please select a user role',
                            }],
                        })(
                            <Select>
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

export default Form.create()(AddUserModal)
