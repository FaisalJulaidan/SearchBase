import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './ForgetPassword.module.less';

import {Button, Col, Form, Icon, Input, Row} from 'antd';
import {Link} from "react-router-dom";

const FormItem = Form.Item;

class ForgetPassword extends React.Component {

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.dispatch(authActions.resetPassword({"email": values.email}));
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <div className={styles.ResetPasswordBackground}>
                <div className={[styles.ResetPasswordPanel, styles.fadeIn].join(' ')}>
                    <Row type="flex" justify="center">
                        <Col>
                            <h1>Reset Your Password</h1>
                        </Col>
                    </Row>

                    <br/>

                    <Row type="flex" justify="center">
                        <Col>
                            <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                                <FormItem className={styles.ResetPasswordFormItem}>
                                    {getFieldDecorator('email', {
                                        rules: [{required: true, message: 'Please input your email!'}],
                                    })(
                                        <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                               placeholder="Email"/>
                                    )}
                                </FormItem>
                            </Form>
                        </Col>
                    </Row>

                    <Row type="flex" justify="center" className={styles.ResetPasswordButton}>
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

export default connect(mapStateToProps)(Form.create()(ForgetPassword));
