import React from "react";
import {Button, Form, Icon, Input} from "antd";

const FormItem = Form.Item;

class ChangePassword extends React.Component {

    state = {
        confirmDirty: false,
    };


    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.savePassword(values);
                this.props.form.resetFields()
            }
        });
    };

    handleConfirmBlur = (e) => {
        const value = e.target.value;
        this.setState({ confirmDirty: this.state.confirmDirty || !!value });
    };

    compareToFirstPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && value !== form.getFieldValue('newPassword')) {
            callback('The two new passwords that you entered are inconsistent!');
        } else {
            callback();
        }
    };

    validateToNextPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && this.state.confirmDirty) {
            form.validateFields(['confirmNewPassword'], { force: true });
        }
        callback();
    };

    render() {
        const {getFieldDecorator} = this.props.form;

        return (
            <Form layout='vertical' wrapperCol={{span: 6}} onSubmit={this.handleSubmit}>

                <FormItem
                    label={"Old Password:"}>
                    {getFieldDecorator('oldPassword', {
                        rules: [{whitespace: true, required: true, message: 'Please input your old password!'},],
                    })(
                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder=""/>
                    )}
                </FormItem>

                <FormItem
                    label={"New Password:"}>
                    {getFieldDecorator('newPassword', {
                        rules: [
                            {whitespace: true, required: true, message: 'Please input your new password!'},
                            {validator: this.validateToNextPassword},
                            {pattern: /^.{6,}$/, message: 'Minimum is 6 characters'}
                        ],
                    })(
                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder=""/>
                    )}
                </FormItem>

                <FormItem
                    label={"Confirm Password:"}>
                    {getFieldDecorator('confirmNewPassword', {
                        rules: [
                            {whitespace: true, required: true, message: 'Please confirm your new password!'},
                            {validator: this.compareToFirstPassword}
                        ],
                    })(
                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder=""
                               onBlur={this.handleConfirmBlur}/>
                    )}
                </FormItem>
                <br/>

                <Button htmlType={"submit"} type={'primary'} size={'large'}>Update Password</Button>
            </Form>
        )
    }
}

export default Form.create()(ChangePassword)