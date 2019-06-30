import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../../store/actions/index';
import styles from './NewResetPassword.module.less';

import {Button, Col, Form, Icon, Input, Row} from 'antd';
import {Link} from "react-router-dom";

const FormItem = Form.Item;

class NewNewResetPassword extends React.Component {

    state = {
        confirmDirty: false,
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.dispatch(authActions.newResetPassword(
                    {
                        "password": values.password,
                        "payload": window.location.href.split("/").pop()
                    }));
            }
        });
    };

    handleConfirmBlur = (e) => {
        const value = e.target.value;
        this.setState({ confirmDirty: this.state.confirmDirty || !!value });
    };

    compareToFirstPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && value !== form.getFieldValue('password')) {
            callback('Passwords must match!');
        } else {
            callback();
        }
    };

    validateToNextPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && this.state.confirmDirty) {
            form.validateFields(['confirm'], { force: true });
        }
        callback();
    };

    render() {
        const {getFieldDecorator} = this.props.form;

        return (
            <div className={styles.NewResetPasswordBackground}>
                <div className={[styles.NewResetPasswordPanel, styles.fadeIn].join(' ')}>
                    <Row type="flex" justify="center">
                        <Col>
                            <h1>Reset your password</h1>
                        </Col>
                    </Row>

                    <br/>

                    <Row type="flex" justify="center">
                        <Col>
                            <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                                <FormItem className={styles.NewResetPasswordFormItem}>
                                    {getFieldDecorator('password', {
                                        rules: [
                                            {required: true, message: 'Please input your Password!'},
                                            {validator: this.validateToNextPassword},
                                            {pattern: /^.{6,}$/, message: 'Minimum is 6 characters'}
                                        ],
                                    })(
                                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                               type="password"
                                               placeholder="New Password"/>
                                    )}
                                </FormItem>

                                <FormItem className={styles.NewResetPasswordFormItem}>
                                    {getFieldDecorator('confirm', {
                                        rules: [
                                            {required: true, message: 'Please confirm your Password!'},
                                            {validator: this.compareToFirstPassword}
                                        ],
                                    })(
                                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                               type="password"
                                               placeholder="Confirm Password"
                                               onBlur={this.handleConfirmBlur}/>
                                    )}
                                </FormItem>

                            </Form>
                        </Col>
                    </Row>

                    <Row type="flex" justify="center" className={styles.NewResetPasswordButton}>
                        <Col span={12}>
                            <Button type="primary" htmlType="submit"
                                    style={{width: '100%'}}
                                    onClick={this.handleSubmit}>
                                Submit
                            </Button>
                        </Col>
                    </Row>
                    <br/>

                    <Row type="flex" justify="center">
                        <Col>
                            <Link style={{color: "#9254de"}} to="/login">Back to login?</Link>
                        </Col>
                    </Row>

                    <br/>
                </div>
            </div>
        );


    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(Form.create()(NewNewResetPassword));
