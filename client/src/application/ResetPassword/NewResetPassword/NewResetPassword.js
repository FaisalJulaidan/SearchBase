import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './NewResetPassword.module.less';

import {Button, Col, Form, Icon, Input, Row} from 'antd';

const FormItem = Form.Item;

class NewNewResetPassword extends React.Component {

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.dispatch(authActions.newResetPassword({"email": values.email}));
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <div className={styles.NewResetPasswordBackground}>
                <div className={[styles.NewResetPasswordPanel, styles.fadeIn].join(' ')}>
                    <Row type="flex" justify="center">
                        <Col>
                            <h1>Reset Your Password</h1>
                        </Col>
                    </Row>

                    <br/>

                    <Row type="flex" justify="center">
                        <Col>
                            <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                                <FormItem className={styles.NewResetPasswordFormItem}>
                                    {getFieldDecorator('password', {
                                        rules: [{required: true, message: 'Please input your new Password!'}],
                                    })(
                                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                               type="password"
                                               placeholder="Password"/>
                                    )}
                                </FormItem>

                                <FormItem className={styles.NewResetPasswordFormItem}>
                                    {getFieldDecorator('confirm_password', {
                                        rules: [{required: true, message: 'Please confirm your Password!'}],
                                    })(
                                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                               type="password"
                                               placeholder="Password"/>
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
                            <a href="/login">Back to login?</a>
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
